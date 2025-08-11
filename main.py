from fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from dotenv import load_dotenv

load_dotenv()

# This is the server name visible to the clients
mcp = FastMCP(name="MCP Template")


@mcp.tool()
def demo_function() -> str:
    """This is a demo function: simulates a simple get string values"""
    return "no data at the moment"


@mcp.tool()
def add_function(content: str) -> str:
    """This is a demo function: simulates a simple add string value"""
    return f"added value: {content}"


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
                 allow_methods = ["*"],
                 allow_headers=["*"]
             )
        ]
    )
