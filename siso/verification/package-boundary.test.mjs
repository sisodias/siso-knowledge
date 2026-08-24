import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';

const root = new URL('../../', import.meta.url).pathname;
const manifest = JSON.parse(fs.readFileSync(`${root}dist/package-manifest.json`, 'utf8'));
const entry = fs.readFileSync(`${root}dist/${manifest.entry}`, 'utf8');

test('compiled package exposes stable preload/mount/unmount entry', () => {
  assert.equal(manifest.compiled, true);
  assert.equal(manifest.entry, 'siso-knowledge-module.js');
  assert.equal(manifest.preload.returns, 'Promise<void>');
  assert.match(entry, /export async function preload/);
  assert.match(entry, /export async function preload\(\)\s*\{\s*await loadAssets\(\);/);
  assert.match(entry, /export async function mount/);
  assert.match(entry, /export function unmount/);
  assert.match(entry, /SisoKnowledgeModule/);
});

test('compiled package boundary contains no raw AFFiNE source', () => {
  const files = fs.readdirSync(`${root}dist`, { recursive: true });
  assert.ok(files.length > 100, 'complete compiled asset graph is present');
  assert.equal(files.some(file => /\.(?:tsx|jsx|ts)$/.test(String(file))), false);
  assert.equal(entry.includes('affineassets.com'), false);
});

test('compiled package has a nested-host asset contract', () => {
  assert.equal(manifest.assetBase, 'relative-to-entry-directory');
  assert.ok(manifest.files.length > 1000, 'manifest enumerates the complete copied asset graph');
  assert.ok(manifest.files.every(file => file.sha256.length === 64 && file.bytes > 0));
  assert.match(entry, /new URL\('\.\/', import\.meta\.url\)/);
  assert.match(entry, /__SISO_KNOWLEDGE_ASSET_BASE__/);
  assert.match(entry, /stylesheet failed/);
  assert.match(entry, /__SISO_KNOWLEDGE_INITIAL_PATH__/);
  assert.match(entry, /identity\?\.workspaceId/);
  assert.match(entry, /__SISO_KNOWLEDGE_FETCH_BRIDGE/);
  assert.match(entry, /backendBase/);
  assert.doesNotMatch(entry, /if \(!backendBase \|\| globalThis\.__SISO_KNOWLEDGE_FETCH_BRIDGE\)/);
  assert.match(entry, /new URL\('\/admin\/api\/cms\/affine', location\.origin\)/);
  assert.match(entry, /url\.pathname === '\/api'/);
  assert.match(entry, /url\.pathname === '\/graphql'/);
  assert.match(entry, /target \+ url\.pathname \+ url\.search/);
  const runtime = manifest.files.find(file => file.path.startsWith('js/runtime.') && file.path.endsWith('.js'));
  assert.ok(runtime, 'runtime chunk is included in the manifest');
  const runtimeSource = fs.readFileSync(`${root}dist/${runtime.path}`, 'utf8');
  assert.match(runtimeSource, /\/\^\(3146\|4014\|8200\)\$\//, 'runtime regex literals remain syntactically intact');
  assert.match(runtimeSource, /h\.p=globalThis\.__SISO_KNOWLEDGE_ASSET_BASE__\|\|new URL\("\.\/",document\.currentScript\?\.src\|\|location\.href\)\.href/);
  assert.match(runtimeSource, /h\.u=e=>"js\/"/);
  assert.match(runtimeSource, /new URL\(h\.u\(e\),globalThis\.__SISO_KNOWLEDGE_ASSET_BASE__/);
  assert.match(runtimeSource, /new URL\(t,globalThis\.__SISO_KNOWLEDGE_ASSET_BASE__/);
  const worker = manifest.files.find(file => file.path.startsWith('js/nbstore-') && file.path.endsWith('.worker.js'));
  assert.ok(worker, 'nbstore worker is included in the manifest');
  const workerSource = fs.readFileSync(`${root}dist/${worker.path}`, 'utf8');
  const workerFlag = workerSource.indexOf('__SISO_KNOWLEDGE_COMPILED_PACKAGE__=true');
  const workerSocketPath = workerSource.indexOf('admin/api/cms/affine/socket.io');
  assert.ok(workerFlag >= 0 && workerFlag < workerSocketPath, 'worker compiled flag is assigned before SocketManager code');
  assert.match(workerSource, /admin\/api\/cms\/affine/);
  assert.match(workerSource, /polling.*websocket/, 'compiled worker permits polling through the nested proxy');
  const index = manifest.files.find(file => file.path.startsWith('js/index.') && file.path.endsWith('.js'));
  assert.ok(index, 'index chunk is included in the manifest');
  const indexSource = fs.readFileSync(`${root}dist/${index.path}`, 'utf8');
  assert.match(indexSource, /i\.p=globalThis\.__SISO_KNOWLEDGE_ASSET_BASE__/);
  assert.match(indexSource, /globalThis\.__SISO_KNOWLEDGE_ASSET_BASE__\+"imgs\//);
  // SocketManager is bundled into a vendor/async chunk rather than index in
  // some AFFiNE builds. Scan every shipped JS chunk so this contract covers
  // the emitted code that actually constructs the Socket.IO manager.
  const javascript = manifest.files
    .filter(file => file.path.endsWith('.js'))
    .map(file => fs.readFileSync(`${root}dist/${file.path}`, 'utf8'))
    .join('\n');
  assert.match(javascript, /admin\/api\/cms\/affine\/socket\.io/);
  for (const name of ['npm-async-@lottiefiles', 'npm-async-@shikijs']) {
    assert.ok(manifest.files.some(file => file.path.startsWith(`js/${name}.`) && file.path.endsWith('.js')), `${name} async chunk is shipped`);
  }
});
