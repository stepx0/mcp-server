import type { StytchLoginConfig } from '@stytch/vanilla-js'
import './App.css'
import { useState, useMemo } from 'react';
import { StytchLogin, IdentityProvider, useStytchUser, useStytch, useStytchSession } from "@stytch/react"

function Callback() {
  const { session } = useStytchSession();
  const stytch = useStytch();
  const [jwt, setJwt] = useState("");

  const grabTokens = () => {
    const tokens = stytch.session.getTokens(); // { session_token, session_jwt } | null
    setJwt(tokens?.session_jwt ?? "");
    console.log("tokens:", tokens);
  };

  return (
    <div style={{ padding: 24 }}>
      <h2>Auth complete</h2>
      <button onClick={grabTokens} disabled={!session}>Get session JWT</button>
      {jwt ? (
        <>
          <p>Copy this and use it as: <code>Authorization: Bearer &lt;JWT&gt;</code></p>
          <textarea style={{ width: "100%", height: 120 }} readOnly value={jwt} />
          <br />
          <button onClick={() => navigator.clipboard.writeText(jwt)}>Copy JWT</button>
        </>
      ) : (
        <p style={{ color: "tomato" }}>No JWT yet—click the button after login finishes.</p>
      )}
    </div>
  );
}


export default function App() {
  const { user } = useStytchUser();
  const { session } = useStytchSession();
  const stytch = useStytch();
  const [jwt, setJwt] = useState("");

  const origin = window.location.origin;
  const config: StytchLoginConfig = {
    products: ["passwords"],
    passwordOptions: {
      loginRedirectURL: `${origin}/auth/callback`,
      resetPasswordRedirectURL: `${origin}/auth/reset`,
    },
  };

const copyJwt = () => {
  const t = stytch.session.getTokens()?.session_jwt ?? "";
  if (!t) { alert("No JWT yet"); return; }
  navigator.clipboard.writeText(t);
  setJwt(t);
  console.log("JWT head/tail:", t.slice(0,20), "...", t.slice(-20));
};

  if (!user) {
    return (
      <div style={{ padding: 24 }}>
        <h2>Sign in (Passwords)</h2>
        <StytchLogin config={config} />
      </div>
    );
  }

  return (
    <div style={{ padding: 24 }}>
      <h2>Logged in ✅</h2>
      <button onClick={copyJwt} disabled={!session}>
        Copy JWT to clipboard
      </button>
      {jwt && (
        <>
          <p style={{ marginTop: 8 }}>Token copied! Paste it into MCP Inspector’s Authorization field:</p>
          <textarea style={{ width: "100%", height: 120 }} readOnly value={jwt} />
        </>
      )}
    </div>
  );
}
