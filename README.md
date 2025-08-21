# MCP Server with Authentication (WIP)

This project provides a **Streamable HTTP MCP server with authentication and a db** layer **(work in progress)**.

---

## 📂 Project Structure

- auth-frontend/   → React + Vite frontend for authentication (Stytch)
- server/          → MCP server implementation (FastMCP + SQLAlchemy)

⚙️ Frameworks & Tools

---

## 🔧 Setup
### 1. Install dependencies

#### Server dependencies:
Using uv: `uv add python-dotenv fastmcp stytch sqlalchemy`


Or with pip: `pip install python-dotenv fastmcp stytch sqlalchemy`


#### Auth Frontend dependencies:

```
npm create vite@latest
npm install
npm i @stytch/react
npm i @stytch/vanilla-js
```

### 2. Configure Stytch

- Log in to your Stytch Dashboard: [stytch.com](https://stytch.com/dashboard)
- Navigate to Connected Apps → Settings
- Toggle Allow dynamic client registration
- Set a valid Authorization URL, e.g.: `http://localhost:5173/auth/callback`

> [!NOTE]
> This URL is where users are redirected after logging in.

### 3. Install MCP Inspector

For debugging your server:
`npm install -g @modelcontextprotocol/inspector`

Or run directly with npx:
`npx @modelcontextprotocol/inspector`

**This will launch a browser-based UI to interact with your MCP server.**

--- 

## ▶️ Running the Project

### 1. Start the Auth Frontend:
From the **auth-frontend** directory:
```
npm run dev
```

This starts the Stytch login UI on:
http://localhost:5173

### 2. Start the MCP Server

From the **server/** directory:
```
uv run main.py
```

### 3. (Optional) Expose MCP Server with ngrok

Install ngrok: [Download here](https://ngrok.com/downloads/mac-os)

Authenticate:
`ngrok config add-authtoken <your-ngrok-token>`

Run tunnel:
`ngrok http 8000`


Example output:
```
Web Interface: http://127.0.0.1:4040
Forwarding:   https://<random-hash>.ngrok-free.app -> http://localhost:8000
```

👉 Use the forwarding URL for MCP Inspector:
https://<random-hash>.ngrok-free.app/mcp/


> [!WARNING]
> The trailing '/mcp/' is required, even the slaashes.

### 4. Connect via MCP Inspector

Transport Type:
Choose **Streamable HTTP** (if using ngrok) or **STDIO** (if running locally).

We are going to test via Streamable HTTP channel.

### 5. Authentication Flow

- Go to the auth-frontend
- Log in with Stytch → copy the generated Session JWT
- In MCP Inspector panel, under Authentication → paste the raw JWT

> [!WARNING]
> Do NOT prepend 'Bearer', just paste the token itself

- Click Connect

✅ Now MCP Inspector is authorized and connected to your MCP server.


## 📌 TODO

 - Finish ngrok setup docs (auto-launch + env injection)
 - Implement SQLAlchemy persistence layer
 - Expand FastMCP routes with more tools
 - Add OAuth2.0 automatic flow (currently manual JWT copy-paste)