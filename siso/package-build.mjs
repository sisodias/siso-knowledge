import { readFileSync, renameSync, readdirSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
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
// The package is the final consumer of the generated dist. Move it instead
// of duplicating ~200 MiB of assets, which also keeps low-space build hosts
// from producing a partially copied package.
rmSync(output, { recursive: true, force: true });
renameSync(sourceDist, output);

const html = readFileSync(resolve(output, 'index.html'), 'utf8');
const scripts = [...html.matchAll(/<script[^>]+src="([^"]+)"/g)].map(match => match[1]);
const styles = [...html.matchAll(/<link[^>]+href="([^"]+\.css)"/g)].map(match => match[1]);
const mainScript = scripts.at(-1);
if (!mainScript) throw new Error('Rspack output has no browser entry script');

// The upstream app is root-hosted. Rewrite all root-relative URLs so a copied
// package remains self-contained under any nested host path.
const textFiles = readdirSync(output, { recursive: true })
  .map(file => resolve(output, String(file)))
  .filter(file => /\.(?:css|js|html)$/.test(file));
for (const file of textFiles) {
  let source = readFileSync(file, 'utf8');
  if (file.includes('/js/runtime.') && file.endsWith('.js')) {
    source = source.replace(/h\.p="?\/?"?/, 'h.p=globalThis.__SISO_KNOWLEDGE_ASSET_BASE__||new URL("./",document.currentScript?.src||location.href).href');
    source = source.replace('var t=h.p+h.u(e),c=Error();', 'var t=new URL(h.u(e),globalThis.__SISO_KNOWLEDGE_ASSET_BASE__||new URL("./",document.currentScript?.src||location.href).href).href,c=Error();');
    source = source.replace('var t=h.miniCssF(e),c=h.p+t;', 'var t=h.miniCssF(e),c=new URL(t,globalThis.__SISO_KNOWLEDGE_ASSET_BASE__||new URL("./",document.currentScript?.src||location.href).href).href;');
  }
  if (file.includes('/js/index.') && file.endsWith('.js')) {
    source = source.replaceAll('i.p=environment.publicPath', 'i.p=globalThis.__SISO_KNOWLEDGE_ASSET_BASE__||new URL("./",document.currentScript?.src||location.href).href');
    source = source.replaceAll('return(environment.subPath||"/")+"js/"+', 'return (globalThis.__SISO_KNOWLEDGE_ASSET_BASE__||new URL("./",document.currentScript?.src||location.href).href)+"js/"+');
    source = source.replace(/:\"\/imgs\//g, ':globalThis.__SISO_KNOWLEDGE_ASSET_BASE__+"imgs/');
  }
  if (file.includes('/js/nbstore-') && file.endsWith('.worker.js')) {
    // The nbstore worker owns its HTTP fetches and cannot see the page fetch
    // bridge. Keep its GraphQL/API requests on the cookie-bearing host path.
    source = `globalThis.__SISO_KNOWLEDGE_COMPILED_PACKAGE__=true;globalThis.__SISO_KNOWLEDGE_BACKEND_BASE__=new URL("/admin/api/cms/affine",globalThis.location.origin).href;\n${source}`;
    const workerBackend = 'globalThis.__SISO_KNOWLEDGE_BACKEND_BASE__||new URL("/admin/api/cms/affine",globalThis.location.origin).href';
    source = source.replaceAll('new URL(e,this.serverBaseUrl)', `new URL(e,${workerBackend})`);
    source = source.replaceAll('new URL("/graphql",this.serverBaseUrl)', `new URL("/graphql",${workerBackend})`);
  }
  if (/\.(?:css|html)$/.test(file)) {
    source = source.replace(/(["'(])\/(?!\/)/g, '$1');
  }
  writeFileSync(file, source);
}

writeFileSync(resolve(output, 'siso-knowledge-module.js'), `
const assets = ${JSON.stringify({ scripts, styles })};
const assetBase = new URL('./', import.meta.url);
globalThis.__SISO_KNOWLEDGE_COMPILED_PACKAGE__ = true;
globalThis.__SISO_KNOWLEDGE_ASSET_BASE__ = assetBase.href;
let ready;
let activeUnmount;
function installRequestBridge(host, backendBase) {
  const target = (backendBase || new URL('/admin/api/cms/affine', location.origin).href).replace(/\\/$/, '');
  const bridgeState = globalThis.__SISO_KNOWLEDGE_FETCH_BRIDGE_STATE || { target, context: '' };
  bridgeState.target = target;
  bridgeState.context = host?.tokens?.sisoRequestContext ?? '';
  globalThis.__SISO_KNOWLEDGE_FETCH_BRIDGE_STATE = bridgeState;
  if (globalThis.__SISO_KNOWLEDGE_FETCH_BRIDGE) return;
  const nativeFetch = window.fetch.bind(window);
  // The host may pass an explicit backend base; compiled package mounts that
  // omit it still need the cookie-bearing same-origin CMS prefix.
  window.fetch = (input, init = {}) => {
    const request = new Request(input, init);
    const url = new URL(request.url, location.href);
    const rootRequest = url.origin === location.origin &&
      (url.pathname === '/api' || url.pathname.startsWith('/api/') ||
       url.pathname === '/graphql' || url.pathname.startsWith('/graphql/'));
    const state = globalThis.__SISO_KNOWLEDGE_FETCH_BRIDGE_STATE;
    if (!rootRequest && !request.url.startsWith(state.target)) return nativeFetch(input, init);
    const backendRequest = rootRequest
      ? new Request(state.target + url.pathname + url.search, request)
      : request;
    backendRequest.headers.set('x-siso-request-context', state.context);
    return nativeFetch(backendRequest, { ...init, credentials: 'include' });
  };
  globalThis.__SISO_KNOWLEDGE_FETCH_BRIDGE = true;
}
function loadAssets() {
  if (ready) return ready;
  ready = Promise.all([
    ...assets.styles.map(href => new Promise((resolve, reject) => {
      const link = document.createElement('link'); link.rel = 'stylesheet'; link.href = new URL(href.replace(/^\\//, ''), assetBase); link.onload = resolve; link.onerror = () => reject(new Error('SISO Knowledge stylesheet failed: ' + link.href)); document.head.append(link);
    })),
    ...assets.scripts.map(src => new Promise((resolve, reject) => {
      const script = document.createElement('script'); script.async = false; script.src = new URL(src.replace(/^\\//, ''), assetBase); script.onload = resolve; script.onerror = () => reject(new Error('SISO Knowledge script failed: ' + script.src)); document.head.append(script);
    })),
  ]);
  return ready;
}
function setInitialPath(options) {
  const workspaceId = options.host?.identity?.workspaceId;
  globalThis.__SISO_KNOWLEDGE_INITIAL_PATH__ = options.initialPath ??
    (workspaceId ? '/workspace/' + workspaceId + '/all' : '/workspace/DsUQAzkXhV7Ex0wbymoab/all');
}
let prefetchReady;
function prefetchAssets() {
  if (prefetchReady) return prefetchReady;
  const preload = (href, as) => new Promise(resolve => {
    const link = document.createElement('link');
    link.rel = 'preload'; link.as = as; link.href = new URL(href.replace(/^\\//, ''), assetBase);
    // A preload is an optimization only. If an edge refuses it, mount() will
    // still load the real stylesheet/script after installing the request bridge.
    link.onload = resolve; link.onerror = resolve; document.head.append(link);
  });
  prefetchReady = Promise.all([
    ...assets.styles.map(href => preload(href, 'style')),
    ...assets.scripts.map(src => preload(src, 'script')),
  ]).then(() => undefined);
  return prefetchReady;
}
export async function mount(target, host) {
  const options = host?.host ? host : { host };
  setInitialPath(options);
  // Install before evaluating donor scripts: AFFiNE captures fetch during
  // module initialization, before its React mount callback runs.
  installRequestBridge(options.host, options.backendBase);
  await loadAssets();
  if (!globalThis.SisoKnowledgeModule?.mount) throw new Error('SISO Knowledge compiled entry did not initialize');
  activeUnmount = globalThis.SisoKnowledgeModule.mount(target, options);
  return activeUnmount;
}
export async function preload(host) {
  if (host) {
    const options = host.host ? host : { host };
    setInitialPath(options);
    installRequestBridge(options.host, options.backendBase);
    await loadAssets();
    return;
  }
  await prefetchAssets();
}
export function unmount() { activeUnmount?.(); activeUnmount = undefined; }
export const entry = ${JSON.stringify(mainScript)};
`.trimStart());

const files = readdirSync(output, { recursive: true })
  .map(file => String(file).replaceAll('\\', '/'))
  .filter(file => statSync(resolve(output, file)).isFile())
  .filter(file => file !== 'package-manifest.json')
  .sort()
  .map(file => {
    const bytes = readFileSync(resolve(output, file));
    return { path: file, bytes: bytes.byteLength, sha256: createHash('sha256').update(bytes).digest('hex') };
  });

writeFileSync(resolve(output, 'package-manifest.json'), JSON.stringify({
  package: '@siso/knowledge-module',
  entry: 'siso-knowledge-module.js',
  html: 'index.html',
  compiled: true,
  sourceBoundary: 'Rspack output only; no AFFiNE source files are shipped',
  assetBase: 'relative-to-entry-directory',
  assets: { scripts, styles },
  files,
  preload: { host: 'SisoKnowledgeHostContext', returns: 'Promise<void>' },
  mount: { target: 'HTMLElement', host: 'SisoKnowledgeHostContext', returns: '() => void' },
}, null, 2));
console.log(JSON.stringify({ output, entry: resolve(output, 'siso-knowledge-module.js'), assets: scripts.length + styles.length, files: files.length }));
