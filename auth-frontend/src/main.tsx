import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { StytchProvider } from '@stytch/react';
import { createStytchUIClient } from '@stytch/react/ui';

const stytch = createStytchUIClient("public-token-test-4b505965-c303-4e46-b006-0ff180f62ef5");

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <StytchProvider stytch={stytch}>
      <App />
    </StytchProvider>
  </StrictMode>,
)
