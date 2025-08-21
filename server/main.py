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
