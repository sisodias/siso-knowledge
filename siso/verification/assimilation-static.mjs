import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';

const baseline = 'a4a069626c9fd1fa0d2a88cd3fd12fb2b408ec1c';
const root = resolve(new URL('../../', import.meta.url).pathname);
const read = path => readFileSync(resolve(root, path), 'utf8');

const sourcePaths = [
  'siso/module-root.tsx',
  'siso/theme-adapter.ts',
  'siso/assimilation/brand-chrome-policy.ts',
];
const source = Object.fromEntries(sourcePaths.map(path => [path, read(path)]));

assert.doesNotMatch(
  source['siso/theme-adapter.ts'],
  /#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/i,
  'the production adapter must reference semantic tokens, not palette values'
);
assert.match(
  source['siso/module-root.tsx'],
  /data-siso-knowledge-chrome/
);
assert.match(
  source['siso/module-root.tsx'],
  /createSisoKnowledgeThemeStyle\(themeMode\)/
);

const tokenLinks = [
  ...source['siso/theme-adapter.ts'].matchAll(
    /'(\-\-affine-[^']+)'\s*:\s*'(\-\-actionist-[^']+)'/g
  ),
].map(([, donor, base]) => ({ donor, base }));
assert.ok(tokenLinks.length >= 60, 'visible donor token bridge is incomplete');
assert.equal(
  new Set(tokenLinks.map(link => link.donor)).size,
  tokenLinks.length,
  'donor token links must be unique'
);

const requiredBaseTokens = new Set(
  Object.values(source)
    .flatMap(text => [...text.matchAll(/--actionist-[a-z0-9-]+/g)])
    .map(match => match[0])
);
const fixturePaths = readdirSync(resolve(root, 'siso/verification/themes'))
  .filter(path => path.endsWith('.json'))
  .sort();
assert.deepEqual(fixturePaths, ['dark.json', 'light-neutral.json', 'stress.json']);

for (const path of fixturePaths) {
  const fixture = JSON.parse(read(`siso/verification/themes/${path}`));
  assert.equal(fixture.schemaVersion, 1);
  assert.equal(fixture.verificationOnly, true);
  assert.ok(['light', 'dark'].includes(fixture.mode));
  for (const token of requiredBaseTokens) {
    assert.equal(
      typeof fixture.tokens[token],
      'string',
      `${path} is missing ${token}`
    );
    assert.ok(fixture.tokens[token].trim(), `${path} has an empty ${token}`);
  }
}

const privatePathPattern = new RegExp(
  `/(?:${['Users', 'Volumes'].join('|')})/[A-Za-z0-9._-]+/`,
  'i'
);
for (const [path, text] of Object.entries(source)) {
  assert.doesNotMatch(text, privatePathPattern, path);
}

const changedPaths = execFileSync(
  'git',
  ['diff', '--name-only', baseline, '--'],
  { cwd: root, encoding: 'utf8' }
)
  .trim()
  .split('\n')
  .filter(Boolean);
const allowed = [
  /^siso\/module-root\.tsx$/,
  /^siso\/theme-adapter\.ts$/,
  /^siso\/assimilation\//,
  /^siso\/verification\/assimilation-[^/]+\.(?:mjs|json)$/,
  /^siso\/verification\/themes\//,
];
assert.ok(
  changedPaths.every(path => allowed.some(pattern => pattern.test(path))),
  `out-of-scope paths: ${changedPaths.filter(path => !allowed.some(pattern => pattern.test(path))).join(', ')}`
);

console.log(
  JSON.stringify({
    status: 'PASS',
    baseline,
    changedPaths,
    donorTokenLinks: tokenLinks.length,
    requiredBaseTokens: requiredBaseTokens.size,
    fixtures: fixturePaths,
  })
);
