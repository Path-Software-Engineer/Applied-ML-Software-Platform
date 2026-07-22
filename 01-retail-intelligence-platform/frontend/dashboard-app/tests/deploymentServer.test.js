import assert from "node:assert/strict";
import { mkdtemp, mkdir, rm, writeFile } from "node:fs/promises";
import { once } from "node:events";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import test from "node:test";

import { createFrontendServer } from "../../../deployment/docker/serve-frontend.mjs";


test("serves the production shell with health and security boundaries", async () => {
  const staticRoot = await mkdtemp(join(tmpdir(), "retail-web-"));
  await mkdir(join(staticRoot, "assets"));
  await writeFile(join(staticRoot, "index.html"), "<main>Retail Intelligence</main>");
  await writeFile(join(staticRoot, "assets", "app.js"), "export default true;");
  const server = createFrontendServer({ staticRoot: resolve(staticRoot) });
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  const { port } = server.address();

  try {
    const origin = `http://127.0.0.1:${port}`;
    const health = await fetch(`${origin}/healthz`);
    assert.equal(health.status, 200);
    assert.deepEqual(await health.json(), {
      status: "ok",
      service: "retail-intelligence-web",
    });

    const shell = await fetch(`${origin}/inventory-decision`);
    assert.equal(shell.status, 200);
    assert.match(await shell.text(), /Retail Intelligence/);
    assert.equal(shell.headers.get("x-content-type-options"), "nosniff");
    assert.match(shell.headers.get("content-security-policy"), /frame-ancestors 'none'/);

    const asset = await fetch(`${origin}/assets/app.js`);
    assert.equal(asset.status, 200);
    assert.match(asset.headers.get("cache-control"), /immutable/);

    assert.equal((await fetch(`${origin}/missing.js`)).status, 404);
    assert.equal((await fetch(origin, { method: "POST" })).status, 405);
  } finally {
    const closed = once(server, "close");
    server.close();
    await closed;
    await rm(staticRoot, { recursive: true, force: true });
  }
});
