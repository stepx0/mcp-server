This is a Streamable http server with auth (wip)

Requirements:
uv add dotenv fastmcp stytch sqlalchemy (or pip install ...)

MCP testing:
install: npm i -g @modelcontextprotocol/inspector
run: mcp-inspector (or npx modelcontextprotocol/inspector)
A browser interface will show.

If MCP server already running, select: Streamable HTTP.
If not, select: STDIO.

STDIO:
Command: uv (or python/pip etc., whatever python command you would use to launch the server)
Arguments: run Path-to-file/main.py (the second part of the command you would use)
Click connect.


Streamable HTTP:
In this case, it's usefult to use ngrok to simulate a public url to our localhost.

Download ngrok from here: https://ngrok.com/downloads/mac-os
Then run 'ngrok config add-authtoken <token>' (the token you get signing in)

Run your server then with:
'uv run main.py' (or equivalents)
in a new terminal tab, run ngrok http 8000

It will output something like:
'''
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://<random-hash-value>.ngrok-free.app -> http://localhost:8000
''' 

In the MCP Inspector panel add the url of the server: https://<random-hash-value>.ngrok-free.app/mcp/
Click connect

Claude test:
'claude mcp add --transport http mcp-server https://<random-hash-value>.ngrok-free.app/mcp/'
claude -> then test


Authentication:

We are using stytch to handle this part, bu whatever auth system can be used.

We need to go to Stytch.com project dashboard, then:
Click "Connected Apps" in the menu;
Click Setting "Edit" button;
Toggle the switch "Allow dynamic client registation"
Set a valid url in the Authorization URL textbox.

This las url will be the one that pops out with the frontend inw ich the user has to log in. 