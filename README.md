This is a Streamable http server with auth (wip)

Requirements:
uv add dotenv fastmcp stytch sqlalchemy (or pip install ...)

MCP testing:
install: npm i -g @modelcontextprotocol/inspector
run: mcp-inspector (or npx modelcontextprotocol/inspector)
A browser interface will show.

If MCP server already running, select: Streamable HTTP.
If not, select: STDIO.

Streamable HTTP:
Add the url of the server: http://127.0.0.1:8000/mcp/
Click connect

STDIO:
Command: uv (or python/pip etc., whatever python command you would use to launch the server)
Arguments: run Path-to-file/main.py (the second part of the command you would use)
Click connect.