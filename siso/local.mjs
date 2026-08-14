import { existsSync, mkdirSync, readFileSync, writeFileSync, unlinkSync, openSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const infraRoot = resolve(root, '../siso-client-platform/infra');
const manifestPath = resolve(infraRoot, 'local/module-infra.json');
const runtimeDir = resolve(root, '.siso-local');
const statePath = resolve(runtimeDir, 'state.json');
const readEnv = () => Object.fromEntries(readFileSync(resolve(infraRoot, '.runtime/credentials.env'), 'utf8').split('\n').filter(Boolean).map(line => line.split(/=(.*)/s).slice(0, 2)));
const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
const envSecrets = readEnv();
const backendPort = 3012;
const frontendPort = 3022;
const issuerPort = 4320;
const backendConfigPath = resolve(root, 'backend/backend/server/config.json');
const state = existsSync(statePath) ? JSON.parse(readFileSync(statePath, 'utf8')) : {};
async function serviceAlive(value) {
  if (!value || typeof value !== 'object') return false;
  try { process.kill(value.pid, 0); return true; } catch {}
  try { return (await fetch(value.url, { signal: AbortSignal.timeout(750) })).ok; } catch { return false; }
}

function sharedEnv() {
  const pg = manifest.postgres;
  const redis = manifest.redis;
  return {
    ...process.env,
    NODE_ENV: 'development',
    SISO_NOTES_ENV: 'dev',
    DATABASE_URL: `postgresql://${pg.modules.knowledge.user}:${encodeURIComponent(envSecrets.knowledge_PASSWORD)}@${pg.host}:${pg.port}/${pg.database}?schema=${pg.modules.knowledge.schema}&options=-c%20search_path%3D${pg.modules.knowledge.schema}`,
    REDIS_SERVER_HOST: redis.host,
    REDIS_SERVER_PORT: String(redis.port),
    REDIS_SERVER_USERNAME: redis.modules.knowledge.user,
    REDIS_SERVER_PASSWORD: envSecrets.REDIS_knowledge_PASSWORD,
    REDIS_SERVER_DATABASE: '0',
    SISO_KNOWLEDGE_REDIS_NAMESPACE: 'true',
    // Shared infra grants the module-scoped PSUBSCRIBE pattern required by
    // Socket.IO; realtime must remain enabled in the acceptance runtime.
    SISO_DISABLE_SOCKET_REDIS: 'false',
    SISO_NOTES_SERVER_PORT: String(backendPort),
    SISO_NOTES_SERVER_EXTERNAL_URL: `http://127.0.0.1:${backendPort}`,
    SISO_HOST_SESSION_URL: 'http://127.0.0.1:4320/api/auth/session',
    SISO_KNOWLEDGE_CONTEXT_SECRET: 'knowledge-local-disposable-secret',
    SISO_ENABLE_NATIVE_RUNTIME: 'true',
    TS_NODE_TRANSPILE_ONLY: 'true',
  };
}

function writeRuntimeConfig() {
  const objectStore = manifest.object_store;
  const knowledgeStore = objectStore.modules.knowledge;
  writeFileSync(backendConfigPath, JSON.stringify({
    storages: {
      blob: { storage: {
        provider: 'aws-s3', bucket: knowledgeStore.bucket,
        config: { endpoint: objectStore.endpoint, region: 'local', forcePathStyle: true,
          credentials: { accessKeyId: envSecrets[knowledgeStore.access_key_env], secretAccessKey: envSecrets[knowledgeStore.secret_key_env] } }
      } },
      avatar: { storage: {
        provider: 'aws-s3', bucket: knowledgeStore.bucket,
        config: { endpoint: objectStore.endpoint, region: 'local', forcePathStyle: true,
          credentials: { accessKeyId: envSecrets[knowledgeStore.access_key_env], secretAccessKey: envSecrets[knowledgeStore.secret_key_env] } }
      } }
    }
  }, null, 2));
}

function start(name, cwd, command, args, env) {
  const log = openSync(resolve(runtimeDir, `${name}.log`), 'a');
  const child = spawn(command, args, { cwd, env, detached: true, stdio: ['ignore', log, log] });
  child.unref();
  state[name] = { pid: child.pid, url: name === 'backend' ? `http://127.0.0.1:${backendPort}` : `http://127.0.0.1:${frontendPort}` };
}

const action = process.argv[2] ?? 'status';
if (action === 'start') {
  mkdirSync(runtimeDir, { recursive: true });
  writeRuntimeConfig();
  start('backend', resolve(root, 'backend'), 'corepack', ['yarn', 'workspace', '@siso/server', 'start'], sharedEnv());
  start('issuer', root, process.execPath, ['siso/issuer.mjs'], { ...process.env, SISO_KNOWLEDGE_ISSUER_PORT: String(issuerPort), SISO_KNOWLEDGE_CONTEXT_SECRET: 'knowledge-local-disposable-secret' });
  start('frontend', resolve(root, 'frontend'), 'corepack', ['yarn', 'affine', '@affine/web', 'dev'], { ...process.env, GITHUB_SHA: process.env.GITHUB_SHA ?? 'siso-knowledge-local', SISO_DOCS_PORT: String(frontendPort), SISO_KNOWLEDGE_HOST_BASE_PATH: '/knowledge' });
  writeFileSync(statePath, JSON.stringify({ ...state, moduleUrl: `http://127.0.0.1:${frontendPort}/`, issuerUrl: `http://127.0.0.1:${issuerPort}` }, null, 2));
  console.log(`knowledge backend=http://127.0.0.1:${backendPort}`);
  console.log(`knowledge desktop=http://127.0.0.1:${frontendPort}/`);
} else if (action === 'status') {
  const liveState = Object.fromEntries(await Promise.all(Object.entries(state).map(async ([name, value]) => {
    if (!value || typeof value !== 'object') return [name, value];
    return [name, { ...value, alive: await serviceAlive(value) }];
  })));
  console.log(JSON.stringify({ manifest: manifestPath, sharedPostgres: `${manifest.postgres.host}:${manifest.postgres.port}/${manifest.postgres.database}`, sharedRedis: `${manifest.redis.host}:${manifest.redis.port}`, state: liveState }, null, 2));
} else if (action === 'stop') {
  for (const entry of Object.values(state)) if (entry?.pid) { try { process.kill(entry.pid, 'SIGTERM'); } catch {} }
  if (existsSync(statePath)) unlinkSync(statePath);
  if (existsSync(backendConfigPath)) unlinkSync(backendConfigPath);
  console.log('knowledge stopped');
} else {
  throw new Error(`Unknown action: ${action}`);
}
