import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { readFileSync, statSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(new URL('../../', import.meta.url).pathname);
const dist = resolve(root, 'dist');
const manifest = JSON.parse(readFileSync(resolve(dist, 'package-manifest.json'), 'utf8'));

/**
 * Serve the package at the same nested URL used by the host. This is also a
 * useful adapter for Playwright: navigate to /admin/docs/host.html and import
 * the entry from the host div without adding a parent Router.
 */
export function createNestedHostServer() {
  const server = createServer((request, response) => {
    const pathname = decodeURIComponent(new URL(request.url, 'http://nested-host.test').pathname);
    if (pathname === '/admin/docs/host.html') {
      response.setHeader('content-type', 'text/html');
      response.end('<!doctype html><div id="knowledge-host"></div><script>window.__errors=[];addEventListener("error",e=>window.__errors.push({message:e.message,filename:e.filename,lineno:e.lineno,colno:e.colno}));</script><script type="module">import { mount } from "./siso-knowledge-module.js"; window.__nestedHostImport = mount;</script>');
      return;
    }
    if (!pathname.startsWith('/admin/docs/')) return void response.writeHead(404).end();
    const file = resolve(dist, pathname.slice('/admin/docs/'.length));
    if (!file.startsWith(`${dist}/`) || !statSync(file, { throwIfNoEntry: false } )?.isFile()) return void response.writeHead(404).end();
    const contentTypes = { '.css': 'text/css', '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json' };
    response.setHeader('content-type', contentTypes[file.slice(file.lastIndexOf('.'))] ?? 'application/octet-stream');
    response.end(readFileSync(file));
  });
  return server;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const server = createNestedHostServer();
  await new Promise(resolveReady => server.listen(0, '127.0.0.1', resolveReady));
  const { port } = server.address();
  const entry = await fetch(`http://127.0.0.1:${port}/admin/docs/siso-knowledge-module.js`).then(response => response.text());
  assert.match(entry, /new URL\('\.\/', import\.meta\.url\)/);
  for (const file of manifest.files) {
    assert.equal((await fetch(`http://127.0.0.1:${port}/admin/docs/${encodeURI(file.path)}`)).status, 200, file.path);
  }
  for (const file of [
    'npm-async-@vanilla-extract.8be0bdd4.css',
    'imgs/app-icon-canary.ico',
    'assets/500.light.74fb0cf7.png',
  ]) {
    assert.equal((await fetch(`http://127.0.0.1:${port}/admin/docs/${file}`)).status, 200, file);
  }
  server.close();
  console.log(`nested host asset harness passed (${manifest.files.length} files)`);
}
