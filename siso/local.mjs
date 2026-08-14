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
const state = existsSync(statePath) ? JSON.parse(readFileSync(statePath, 'utf8')) : {};

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
    SISO_NOTES_SERVER_PORT: String(backendPort),
    SISO_NOTES_SERVER_EXTERNAL_URL: `http://127.0.0.1:${backendPort}`,
    SISO_HOST_SESSION_URL: 'http://127.0.0.1:4320/api/auth/session',
    SISO_DISABLE_SOCKET_REDIS: 'true',
    SISO_ENABLE_NATIVE_RUNTIME: 'false',
    TS_NODE_TRANSPILE_ONLY: 'true',
  };
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
  start('backend', resolve(root, 'backend'), 'corepack', ['yarn', 'workspace', '@siso/server', 'start'], sharedEnv());
  start('frontend', resolve(root, 'frontend'), 'corepack', ['yarn', 'affine', '@affine/web', 'dev'], { ...process.env, GITHUB_SHA: process.env.GITHUB_SHA ?? 'siso-knowledge-local', SISO_DOCS_PORT: String(frontendPort), SISO_KNOWLEDGE_HOST_BASE_PATH: '/knowledge' });
  writeFileSync(statePath, JSON.stringify({ ...state, moduleUrl: `http://127.0.0.1:${frontendPort}/` }, null, 2));
  console.log(`knowledge backend=http://127.0.0.1:${backendPort}`);
  console.log(`knowledge desktop=http://127.0.0.1:${frontendPort}/`);
} else if (action === 'status') {
  const liveState = Object.fromEntries(Object.entries(state).map(([name, value]) => {
    if (!value || typeof value !== 'object') return [name, value];
    let alive = false;
    try { process.kill(value.pid, 0); alive = true; } catch {}
    return [name, { ...value, alive }];
  }));
  console.log(JSON.stringify({ manifest: manifestPath, sharedPostgres: `${manifest.postgres.host}:${manifest.postgres.port}/${manifest.postgres.database}`, sharedRedis: `${manifest.redis.host}:${manifest.redis.port}`, state: liveState }, null, 2));
} else if (action === 'stop') {
  for (const entry of Object.values(state)) if (entry?.pid) { try { process.kill(entry.pid, 'SIGTERM'); } catch {} }
  if (existsSync(statePath)) unlinkSync(statePath);
  console.log('knowledge stopped');
} else {
  throw new Error(`Unknown action: ${action}`);
}
