import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';

const root = new URL('../../', import.meta.url).pathname;
const manifest = JSON.parse(fs.readFileSync(`${root}dist/package-manifest.json`, 'utf8'));
const entry = fs.readFileSync(`${root}dist/${manifest.entry}`, 'utf8');

test('compiled package exposes stable mount/unmount entry', () => {
  assert.equal(manifest.compiled, true);
  assert.equal(manifest.entry, 'siso-knowledge-module.js');
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
  const runtime = manifest.files.find(file => file.path.startsWith('js/runtime.') && file.path.endsWith('.js'));
  assert.ok(runtime, 'runtime chunk is included in the manifest');
  const runtimeSource = fs.readFileSync(`${root}dist/${runtime.path}`, 'utf8');
  assert.match(runtimeSource, /\/\^\(3146\|4014\|8200\)\$\//, 'runtime regex literals remain syntactically intact');
  assert.match(runtimeSource, /h\.p=globalThis\.__SISO_KNOWLEDGE_ASSET_BASE__\|\|new URL\("\.\/",document\.currentScript\?\.src\|\|location\.href\)\.href/);
  assert.match(runtimeSource, /h\.u=e=>"js\/"/);
  assert.match(runtimeSource, /new URL\(h\.u\(e\),globalThis\.__SISO_KNOWLEDGE_ASSET_BASE__/);
  assert.match(runtimeSource, /new URL\(t,globalThis\.__SISO_KNOWLEDGE_ASSET_BASE__/);
  const index = manifest.files.find(file => file.path.startsWith('js/index.') && file.path.endsWith('.js'));
  assert.ok(index, 'index chunk is included in the manifest');
  const indexSource = fs.readFileSync(`${root}dist/${index.path}`, 'utf8');
  assert.match(indexSource, /i\.p=globalThis\.__SISO_KNOWLEDGE_ASSET_BASE__/);
  assert.match(indexSource, /globalThis\.__SISO_KNOWLEDGE_ASSET_BASE__\+"imgs\//);
  for (const name of ['npm-async-@lottiefiles', 'npm-async-@shikijs']) {
    assert.ok(manifest.files.some(file => file.path.startsWith(`js/${name}.`) && file.path.endsWith('.js')), `${name} async chunk is shipped`);
  }
});
