import assert from 'node:assert/strict';
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import test from 'node:test';

const root = new URL('../', import.meta.url).pathname;
const read = file => fs.readFileSync(`${root}${file}`, 'utf8');

test('pins and module-root contract are present', () => {
  const manifest = JSON.parse(read('upstream-manifest.json'));
  assert.equal(manifest.sources.frontend.commit, '837a5c285caf2078e340a6220de38bdd8ab1da9a');
  assert.equal(manifest.sources.backend.commit, '4b5d79282be91fd529dcff84b066f00b3784496a');
  assert.match(read('siso/module-root.tsx'), /SisoKnowledgeModuleRoot/);
  assert.match(read('frontend/packages/frontend/apps/web/src/siso-knowledge-module.tsx'), /donorApp=\{App\}/);
});

test('forbidden federated topology is absent from the module seams', () => {
  const files = ['module-manifest.json', 'siso/module-root.tsx', 'frontend/packages/frontend/apps/web/src/siso-knowledge-module.tsx'];
  const source = files.map(read).join('\n');
  assert.doesNotMatch(source, /iframe|postMessage|redirect|remote frontend|login bootstrap/i);
});

test('source remotes cannot push', () => {
  for (const remote of ['frontend-upstream', 'backend-upstream']) {
    assert.equal(execFileSync('git', ['config', `remote.${remote}.pushurl`], { cwd: root, encoding: 'utf8' }).trim(), 'DISABLED');
  }
});
