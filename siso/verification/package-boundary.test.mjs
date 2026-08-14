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
