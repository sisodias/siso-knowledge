import { cpSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { resolve } from 'node:path';

const root = resolve(new URL('..', import.meta.url).pathname);
const frontend = resolve(root, 'frontend');
const sourceDist = resolve(frontend, 'packages/frontend/apps/web/dist');
const output = resolve(root, 'dist');

execFileSync('corepack', ['yarn', 'affine', '@affine/web', 'build'], {
  cwd: frontend,
  stdio: 'inherit',
  env: {
    ...process.env,
    PUBLIC_PATH: '/',
    GITHUB_SHA: process.env.GITHUB_SHA ?? 'siso-knowledge-package',
    SISO_LOCAL_BACKEND_URL: process.env.SISO_LOCAL_BACKEND_URL ?? 'http://127.0.0.1:3012',
  },
});

rmSync(output, { recursive: true, force: true });
mkdirSync(output, { recursive: true });
cpSync(sourceDist, output, { recursive: true });

const html = readFileSync(resolve(output, 'index.html'), 'utf8');
const scripts = [...html.matchAll(/<script[^>]+src="([^"]+)"/g)].map(match => match[1]);
const styles = [...html.matchAll(/<link[^>]+href="([^"]+\.css)"/g)].map(match => match[1]);
const mainScript = scripts.at(-1);
if (!mainScript) throw new Error('Rspack output has no browser entry script');

writeFileSync(resolve(output, 'siso-knowledge-module.js'), `
const assets = ${JSON.stringify({ scripts, styles })};
let ready;
let activeUnmount;
function loadAssets() {
  if (ready) return ready;
  ready = Promise.all([
    ...assets.styles.map(href => new Promise(resolve => {
      const link = document.createElement('link'); link.rel = 'stylesheet'; link.href = new URL(href.replace(/^\\//, ''), import.meta.url); link.onload = link.onerror = resolve; document.head.append(link);
    })),
    ...assets.scripts.map(src => new Promise(resolve => {
      const script = document.createElement('script'); script.src = new URL(src.replace(/^\\//, ''), import.meta.url); script.onload = script.onerror = resolve; document.head.append(script);
    })),
  ]);
  return ready;
}
export async function mount(target, host) {
  await loadAssets();
  if (!globalThis.SisoKnowledgeModule?.mount) throw new Error('SISO Knowledge compiled entry did not initialize');
  activeUnmount = globalThis.SisoKnowledgeModule.mount(target, host);
  return activeUnmount;
}
export function unmount() { activeUnmount?.(); activeUnmount = undefined; }
export const entry = ${JSON.stringify(mainScript)};
`.trimStart());

writeFileSync(resolve(output, 'package-manifest.json'), JSON.stringify({
  package: '@siso/knowledge-module',
  entry: 'siso-knowledge-module.js',
  html: 'index.html',
  compiled: true,
  sourceBoundary: 'Rspack output only; no AFFiNE source files are shipped',
  assets: { scripts, styles },
  mount: { target: 'HTMLElement', host: 'SisoKnowledgeHostContext', returns: '() => void' },
}, null, 2));
console.log(JSON.stringify({ output, entry: resolve(output, 'siso-knowledge-module.js'), assets: scripts.length + styles.length }));
