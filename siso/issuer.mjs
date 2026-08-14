import { createHmac } from 'node:crypto';
import { createServer } from 'node:http';

const port = Number(process.env.SISO_KNOWLEDGE_ISSUER_PORT ?? 4320);
const secret = process.env.SISO_KNOWLEDGE_CONTEXT_SECRET ?? 'knowledge-local-disposable-secret';
const now = Math.floor(Date.now() / 1000);
const claims = {
  clientId: 'bykonz-yard',
  userId: 'knowledge-local-user',
  email: 'knowledge.local@siso.local',
  displayName: 'Knowledge Local QA',
  workspaceId: 'knowledge-local-workspace',
  capabilities: ['view', 'edit', 'share', 'admin'],
  iat: now,
  exp: now + 3600,
};
const payload = Buffer.from(JSON.stringify(claims)).toString('base64url');
const signature = createHmac('sha256', secret).update(payload).digest('base64url');
const token = `${payload}.${signature}`;

const server = createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', 'http://127.0.0.1:3022');
  res.setHeader('Access-Control-Allow-Headers', 'content-type');
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }
  if (req.url === '/api/auth/session' || req.url === '/api/siso/knowledge-context') {
    res.setHeader('content-type', 'application/json');
    res.writeHead(200);
    res.end(JSON.stringify({ ...claims, token, issuedAt: new Date(now * 1000).toISOString(), expiresAt: new Date(claims.exp * 1000).toISOString() }));
    return;
  }
  res.writeHead(404); res.end('not found');
});
server.listen(port, '127.0.0.1');
process.once('SIGTERM', () => server.close(() => process.exit(0)));
process.once('SIGINT', () => server.close(() => process.exit(0)));
