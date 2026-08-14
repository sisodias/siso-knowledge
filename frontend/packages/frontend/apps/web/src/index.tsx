import './setup';

import { Telemetry } from '@affine/core/components/telemetry';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import { App } from './app';
import { SisoKnowledgeModuleRoot } from './siso-module-contract';

type SisoMountHost = Parameters<typeof SisoKnowledgeModuleRoot>[0]['host'];

async function loadLocalHostContext(): Promise<{ host: SisoMountHost; backendBase: string } | null> {
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
  (window as any).__SISO_KNOWLEDGE_CONTEXT_TOKEN = session.token;
  const nativeFetch = window.fetch.bind(window);
  window.fetch = (input, init = {}) => {
    const request = new Request(input, init);
    if (request.url.startsWith(`${location.origin}/api`) || request.url.startsWith(`${location.origin}/graphql`)) {
      const backendUrl = new URL(request.url);
      backendUrl.port = '3012';
      const backendRequest = new Request(backendUrl, request);
      backendRequest.headers.set('x-siso-request-context', session.token);
      return nativeFetch(backendRequest, { ...init, credentials: 'include' });
    }
    if (request.url.startsWith('http://127.0.0.1:3012')) {
      request.headers.set('x-siso-request-context', session.token);
      return nativeFetch(request, { ...init, credentials: 'include' });
    }
    return nativeFetch(input, init);
  };
  return {
    host: {
      identity: session,
      database: { config: { schema: 'knowledge' as const, redisNamespace: 'knowledge' as const, yjsNamespace: 'knowledge' as const, blobNamespace: 'knowledge' as const } },
      tokens: { sisoRequestContext: session.token },
    },
    backendBase: 'http://127.0.0.1:3012',
  };
}

export interface SisoKnowledgeMountOptions {
  host: SisoMountHost;
  backendBase?: string;
}

function installRequestBridge(host: SisoMountHost, backendBase?: string) {
  if (!backendBase || (window as any).__SISO_KNOWLEDGE_FETCH_BRIDGE) return;
  const nativeFetch = window.fetch.bind(window);
  const target = backendBase.replace(/\/$/, '');
  window.fetch = (input, init = {}) => {
    const request = new Request(input, init);
    if (!request.url.startsWith(target) && !request.url.startsWith(`${location.origin}/api`) && !request.url.startsWith(`${location.origin}/graphql`)) {
      return nativeFetch(input, init);
    }
    const backendRequest = request.url.startsWith(target)
      ? request
      : new Request(`${target}${new URL(request.url).pathname}${new URL(request.url).search}`, request);
    backendRequest.headers.set('x-siso-request-context', host.tokens.sisoRequestContext ?? '');
    return nativeFetch(backendRequest, { ...init, credentials: 'include' });
  };
  (window as any).__SISO_KNOWLEDGE_FETCH_BRIDGE = true;
}

export function mountSisoKnowledge(target: HTMLElement, options: SisoKnowledgeMountOptions) {
  installRequestBridge(options.host, options.backendBase);
  const root = createRoot(target);
  root.render(
    <StrictMode>
      <Telemetry />
      <SisoKnowledgeModuleRoot host={options.host} donorApp={App} />
    </StrictMode>
  );
  return () => root.unmount();
}

(globalThis as typeof globalThis & {
  SisoKnowledgeModule?: { mount: typeof mountSisoKnowledge };
}).SisoKnowledgeModule = { mount: mountSisoKnowledge };

async function mountApp() {
  const root = document.getElementById('app');
  if (!root) return;
  const localHost = await loadLocalHostContext();
  if (localHost) {
    mountSisoKnowledge(root, localHost);
  } else {
    createRoot(root).render(
      <StrictMode>
        <Telemetry />
        <App />
      </StrictMode>
    );
  }
}

if (!(globalThis as typeof globalThis & { __SISO_KNOWLEDGE_COMPILED_PACKAGE__?: boolean }).__SISO_KNOWLEDGE_COMPILED_PACKAGE__) {
  try {
    await mountApp();
  } catch (err) {
    console.error('Failed to bootstrap app', err);
  }
}
