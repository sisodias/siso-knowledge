import { createHmac } from 'node:crypto';
import { createServer } from 'node:http';

const port = Number(process.env.SISO_KNOWLEDGE_ISSUER_PORT ?? 4320);
const secret = process.env.SISO_KNOWLEDGE_CONTEXT_SECRET ?? 'knowledge-local-disposable-secret';
const hostSessionTokens = new Set(
  (process.env.SISO_KNOWLEDGE_HOST_SESSION_TOKENS ?? 'knowledge-local-disposable-session')
    .split(',')
    .map(value => value.trim())
    .filter(Boolean),
);
const revokedHostSessionTokens = new Set();
const hostCookieNames = ['__Host-siso_session', 'siso_host_session'];

function parseCookies(header) {
  return new Map((header ?? '').split(';').filter(Boolean).map(part => {
    const [name, ...value] = part.trim().split('=');
    return [name, value.join('=')];
  }));
}

function getHostSessionToken(req) {
  const cookies = parseCookies(req.headers.cookie);
  for (const name of hostCookieNames) {
    const raw = cookies.get(name);
    if (!raw) continue;
    try {
      return { name, token: decodeURIComponent(raw) };
    } catch {
      return { name, token: raw };
    }
  }
  return null;
}

function getActiveHostSession(req) {
  const cookie = getHostSessionToken(req);
  if (!cookie || !hostSessionTokens.has(cookie.token) || revokedHostSessionTokens.has(cookie.token)) return null;
  return cookie;
}

function createContext() {
  const now = Math.floor(Date.now() / 1000);
  return {
    clientId: 'bykonz-yard',
    userId: 'knowledge-local-user',
    email: 'knowledge.local@siso.local',
    displayName: 'Knowledge Local QA',
    workspaceId: 'knowledge-local-workspace',
    capabilities: ['view', 'edit', 'share', 'admin'],
    iat: now,
    exp: now + 120,
  };
}

function signContext(claims) {
  const payload = Buffer.from(JSON.stringify(claims)).toString('base64url');
  const signature = createHmac('sha256', secret).update(payload).digest('base64url');
  return `${payload}.${signature}`;
}

function sendJson(res, status, value) {
  res.setHeader('content-type', 'application/json');
  res.setHeader('cache-control', 'no-store');
  res.writeHead(status);
  res.end(JSON.stringify(value));
}

const server = createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', req.headers.origin ?? 'http://127.0.0.1:4179');
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Headers', 'content-type');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }
  if (req.url === '/api/auth/session') {
    if (!getActiveHostSession(req)) return sendJson(res, 401, { error: 'host_session_required' });
    const now = Math.floor(Date.now() / 1000);
    return sendJson(res, 200, { user: { id: 'knowledge-local-user', email: 'knowledge.local@siso.local', name: 'Knowledge Local QA', workspaceId: 'knowledge-local-workspace' }, expiresAt: new Date((now + 3600) * 1000).toISOString() });
  }
  if (req.url === '/api/siso/knowledge-context') {
    if (!getActiveHostSession(req)) return sendJson(res, 401, { error: 'host_session_required' });
    const claims = createContext();
    return sendJson(res, 200, { ...claims, token: signContext(claims), issuedAt: new Date(claims.iat * 1000).toISOString(), expiresAt: new Date(claims.exp * 1000).toISOString() });
  }
  if (req.method === 'POST' && req.url === '/api/siso/revoke') {
    const session = getActiveHostSession(req);
    if (!session) return sendJson(res, 401, { error: 'host_session_required' });
    revokedHostSessionTokens.add(session.token);
    res.writeHead(204);
    return res.end();
  }
  res.writeHead(404); res.end('not found');
});
server.listen(port, '127.0.0.1');
process.once('SIGTERM', () => server.close(() => process.exit(0)));
process.once('SIGINT', () => server.close(() => process.exit(0)));
