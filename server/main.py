from fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse
from fastmcp.server.auth import BearerAuthProvider
from fastmcp.server.dependencies import get_access_token, AccessToken
import jwt
import requests

import os, time, datetime as dt, jwt, requests
from dotenv import load_dotenv


load_dotenv()


# --- DEBUG VERIFY (outside MCP) ---
RAW = os.getenv("DEBUG_JWT", "") or """eyJhbGciOiJSUzI1NiIsImtpZCI6Imp3ay10ZXN0LWIxMTU3OTFjLWNmOWItNGQ3ZS1iYzAyLTc4Njc5YTI4ZGU3MCIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsicHJvamVjdC10ZXN0LTJmZDg2M2FkLWQxNDYtNGVkOC04NzUzLTY0ZWE1ZDBlY2I2YSJdLCJleHAiOjE3NTU2ODgxNjksImh0dHBzOi8vc3R5dGNoLmNvbS9zZXNzaW9uIjp7ImlkIjoic2Vzc2lvbi10ZXN0LTQ0MGM5MjQ1LWE4MTgtNGE0ZS04MjE1LTMyMzBmMzcwMjBlZiIsInN0YXJ0ZWRfYXQiOiIyMDI1LTA4LTIwVDEwOjU3OjExWiIsImxhc3RfYWNjZXNzZWRfYXQiOiIyMDI1LTA4LTIwVDExOjA0OjI5WiIsImV4cGlyZXNfYXQiOiIyMDI1LTA4LTIwVDExOjI3OjExWiIsImF0dHJpYnV0ZXMiOnsidXNlcl9hZ2VudCI6IiIsImlwX2FkZHJlc3MiOiIifSwiYXV0aGVudGljYXRpb25fZmFjdG9ycyI6W3sidHlwZSI6InBhc3N3b3JkIiwiZGVsaXZlcnlfbWV0aG9kIjoia25vd2xlZGdlIiwibGFzdF9hdXRoZW50aWNhdGVkX2F0IjoiMjAyNS0wOC0yMFQxMDo1NzoxMVoifV19LCJpYXQiOjE3NTU2ODc4NjksImlzcyI6InN0eXRjaC5jb20vcHJvamVjdC10ZXN0LTJmZDg2M2FkLWQxNDYtNGVkOC04NzUzLTY0ZWE1ZDBlY2I2YSIsIm5iZiI6MTc1NTY4Nzg2OSwic3ViIjoidXNlci10ZXN0LTI4ZWFlZTI1LWFlYjItNDNmNi1hNjlhLTA4ZjJmOTI1YjZjYyJ9.g1fixcXKpHAV16_mZfYbERrlSd8YxEo7SKWYZUSSfsbvztcR1LNvemFwUKkLJXbbz0tf3QHAGO22HLvp3QpwNaW3uNlqEaKL3TpA9OD6SOe0JmZ5rS4Mk10zeKTnmqfmrTfjpDGmAk_ijh49M4lSmOKvIlKEn177OKpQ0pUZOVUzolZHyx5I4B87DIeY1zWOljduIdI-ueSrauKXy-TbtQYorubyaVACt1kDEdEr61LKrTv56K-hIWZTlRh5mVoSHQqPjTJkeiB03jWRkFCUvZQyxPye3OMkCRdrumpdlNYCICglx-9l0Bs8ZVnMamYKO9cUUc82HzlYWPg7qP0xAw
"""
TOKEN = RAW.split()[1] if RAW.startswith("Bearer ") else RAW   # <-- strip 'Bearer '

def stamp(s): return dt.datetime.utcfromtimestamp(s).strftime("%Y-%m-%d %H:%M:%S UTC")

# 1) Decode WITHOUT verifying to inspect claims
pl = jwt.decode(TOKEN, options={"verify_signature": False})
now = int(time.time())

print("now (epoch):", now, stamp(now))
print("iat (epoch):", pl["iat"], stamp(pl["iat"]))
print("exp (epoch):", pl["exp"], stamp(pl["exp"]))
print("Δ(now - exp):", now - pl["exp"], "seconds (positive => your clock is ahead)")

# 2) Sanity print to ensure you’re using the token you think
print("token head/tail:", TOKEN[:20], "...", TOKEN[-20:])

print("TOKEN EXP: ", pl["exp"])

# Values from your token/debug output
PROJECT_ID = "project-test-2fd863ad-d146-4ed8-8753-64ea5d0ecb6a"
ISSUER = "stytch.com/project-test-2fd863ad-d146-4ed8-8753-64ea5d0ecb6a"
JWKS_URL = f"https://test.stytch.com/v1/sessions/jwks/{PROJECT_ID}"

jwks = requests.get(JWKS_URL).json()
print(f"Fetched {len(jwks['keys'])} keys from JWKS")

# Set up the JWKS key fetching
key = jwt.PyJWKClient(JWKS_URL).get_signing_key_from_jwt(TOKEN).key

# Verify token
decoded = jwt.decode(
    TOKEN,
    key,
    algorithms=["RS256"],
    audience=[PROJECT_ID],
    issuer=ISSUER,
)
print("✅ Token is valid!")
print(decoded)

# Choose the right JWKS base for sessions JWTs
STYTCH_BASE = "https://test.stytch.com" if os.getenv(
    "STYTCH_ENV", "test") == "test" else "https://api.stytch.com"
JWKS_URL = f"{STYTCH_BASE}/v1/sessions/jwks/{os.getenv('STYTCH_PROJECT_ID')}"

# Check to see if client has a valid access token to actually use the server
auth = BearerAuthProvider(
    jwks_uri=JWKS_URL,                         # <-- Stytch sessions JWKS endpoint
    # <-- EXACT match to JWT 'iss' (string equality)
    issuer=os.getenv("STYTCH_DOMAIN"),
    algorithm="RS256",
    # <-- pass as list (JWT 'aud' is an array)
    audience=[os.getenv("STYTCH_PROJECT_ID")],
)

# This is the server name visible to the clients
mcp = FastMCP(name="MCP Template", auth=auth)


# '_ctx' param is used by Stytch to check auths
@mcp.tool()
def demo_function(_ctx) -> str:
    """This is a demo function: simulates a simple get string values"""
    return "no data at the moment"


@mcp.tool()
def add_function(_ctx, content: str) -> str:
    """This is a demo function: simulates a simple add string value"""
    return f"added value: {content}"


@mcp.custom_route("/.well-known/oauth-protected-resource",
                  methods=["GET", "OPTIONS"])
def oauth_metadata(request: StarletteRequest) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/")

    return JSONResponse(
        {
            "resource": base_url,
            "authorization_servers": [os.getenv("STYTCH_DOMAIN")],
            "scopes_supported": ["read", "write"],
            "bearer_methods_supported": ["header", "body"]
        }
    )


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
        path="/mcp/",
        middleware=[
             Middleware(
                 CORSMiddleware,
                 allow_origins=["*"],
                 allow_credentials=True,
                 allow_methods=["*"],
                 allow_headers=["*"]
             )
        ]
    )
