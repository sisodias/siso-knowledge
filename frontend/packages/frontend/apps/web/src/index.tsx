import './setup';

import { Telemetry } from '@affine/core/components/telemetry';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import { App } from './app';
import { SisoKnowledgeModuleRoot } from './siso-module-contract';

async function loadLocalHostContext() {
  if (location.hostname !== '127.0.0.1' || location.port !== '3022') return null;
  // The host cookie is opaque to the browser and is only forwarded to the
  // issuer by the server. The signing secret never leaves the issuer.
  document.cookie = 'siso_host_session=knowledge-local-disposable-session; Path=/; SameSite=Lax';
  const response = await fetch('http://127.0.0.1:4320/api/siso/knowledge-context');
  if (!response.ok) throw new Error(`SISO local issuer unavailable (${response.status})`);
  const session = await response.json() as {
    userId: string; email: string; displayName?: string; clientId: string;
    workspaceId: string; expiresAt: string; capabilities: Array<'view' | 'edit' | 'share' | 'admin'>;
    token: string;
  };
  return {
    host: {
      identity: session,
      database: { config: { schema: 'knowledge' as const, redisNamespace: 'knowledge' as const, yjsNamespace: 'knowledge' as const, blobNamespace: 'knowledge' as const } },
      tokens: { sisoRequestContext: session.token },
    },
  };
}

async function mountApp() {
  // oxlint-disable-next-line @typescript-eslint/no-non-null-assertion
  const root = document.getElementById('app')!;
  const localHost = await loadLocalHostContext();
  createRoot(root).render(
    <StrictMode>
      <Telemetry />
      {localHost ? <SisoKnowledgeModuleRoot {...localHost} donorApp={App} /> : <App />}
    </StrictMode>
  );
}

try {
  await mountApp();
} catch (err) {
  console.error('Failed to bootstrap app', err);
}
