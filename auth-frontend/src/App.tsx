// App.tsx
import "./App.css";
import { useState, useMemo } from "react";
import {
  StytchLogin,
  useStytchUser,
  useStytch,
  useStytchSession,
} from "@stytch/react";
import type { StytchLoginConfig } from "@stytch/vanilla-js";

export default function App() {
  const { user } = useStytchUser();
  const { session } = useStytchSession();
  const stytch = useStytch();
  const [jwt, setJwt] = useState("");

  const origin = typeof window !== "undefined" ? window.location.origin : "";
  const config: StytchLoginConfig = useMemo(
    () => ({
      products: ["passwords"],
      passwordOptions: {
        loginRedirectURL: `${origin}/auth/callback`,
        resetPasswordRedirectURL: `${origin}/auth/reset`,
      },
    }),
    [origin]
  );

  const copyJwt = async () => {
    const t = stytch.session.getTokens()?.session_jwt ?? "";
    if (!t) {
      alert("No JWT yet — complete login first.");
      return;
    }
    await navigator.clipboard.writeText(t);
    setJwt(t);
    console.log("JWT head/tail:", t.slice(0, 20), "...", t.slice(-20));
  };

  const logout = async () => {
    try {
      await stytch.session.revoke(); // end current session
    } finally {
      setJwt("");
      window.location.reload(); // return to login state
    }
  };

  // basic callback/reset routes (optional)
  const path = typeof window !== "undefined" ? window.location.pathname : "/";
  if (path.startsWith("/auth/callback")) {
    return (
      <div style={{ padding: 24 }}>
        <h2>Auth complete</h2>
        <a href="/">Go back</a>
      </div>
    );
  }
  if (path.startsWith("/auth/reset")) {
    return (
      <div style={{ padding: 24 }}>
        <h2>Password reset</h2>
        <a href="/">Go back</a>
      </div>
    );
  }

  if (!user) {
    return (
      <div style={{ padding: 24 }}>
        <h2>Sign in (Passwords)</h2>
        <StytchLogin config={config} />
      </div>
    );
  }

  return (
    <div style={{ padding: 24, display: "grid", gap: 12 }}>
      <h2>Logged in ✅</h2>
      <div style={{ display: "flex", gap: 8 }}>
        <button onClick={copyJwt} disabled={!session}>
          Copy JWT to clipboard
        </button>
        <button onClick={logout}>Log out</button>
      </div>
      {jwt && (
        <>
          <p>Paste this into MCP Inspector’s Authorization field as:</p>
          <textarea style={{ width: "100%", height: 140 }} readOnly value={jwt} />
        </>
      )}
    </div>
  );
}
