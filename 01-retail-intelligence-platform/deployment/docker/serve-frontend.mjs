import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { createServer } from "node:http";
import { extname, resolve, sep } from "node:path";
import { pathToFileURL } from "node:url";


const contentTypes = new Map([
  [".css", "text/css; charset=utf-8"],
  [".html", "text/html; charset=utf-8"],
  [".ico", "image/x-icon"],
  [".js", "text/javascript; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".png", "image/png"],
  [".svg", "image/svg+xml"],
  [".webp", "image/webp"],
  [".woff2", "font/woff2"],
]);


function runtimePort(value) {
  const port = Number(value);
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw new Error("PORT must be an integer between 1 and 65535.");
  }
  return port;
}


function securityHeaders(response) {
  response.setHeader("Content-Security-Policy", "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self' https:; font-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'none'");
  response.setHeader("Referrer-Policy", "no-referrer");
  response.setHeader("X-Content-Type-Options", "nosniff");
  response.setHeader("X-Frame-Options", "DENY");
  response.setHeader("Permissions-Policy", "camera=(), microphone=(), geolocation=()");
}


function respond(response, status, body, contentType = "text/plain; charset=utf-8") {
  const payload = Buffer.from(body);
  response.writeHead(status, {
    "Content-Type": contentType,
    "Content-Length": payload.length,
  });
  response.end(payload);
}


async function fileFor(root, pathname) {
  let decoded;
  try {
    decoded = decodeURIComponent(pathname);
  } catch {
    return { status: 400 };
  }

  const requested = decoded === "/" ? "/index.html" : decoded;
  const candidate = resolve(root, `.${requested}`);
  if (candidate !== root && !candidate.startsWith(`${root}${sep}`)) {
    return { status: 403 };
  }

  try {
    const metadata = await stat(candidate);
    if (metadata.isFile()) return { path: candidate, metadata };
  } catch {
    // A client-side route falls through to the application shell.
  }

  if (extname(requested)) return { status: 404 };
  const fallback = resolve(root, "index.html");
  return { path: fallback, metadata: await stat(fallback) };
}


export function createFrontendServer({ staticRoot } = {}) {
  const root = resolve(staticRoot ?? process.env.STATIC_ROOT ?? "/app/dist");

  return createServer(async (request, response) => {
    securityHeaders(response);

    if (request.url === "/health") {
      respond(response, 200, JSON.stringify({ status: "ok", service: "retail-intelligence-web" }), "application/json; charset=utf-8");
      return;
    }

    if (!new Set(["GET", "HEAD"]).has(request.method ?? "")) {
      response.setHeader("Allow", "GET, HEAD");
      respond(response, 405, "Method Not Allowed");
      return;
    }

    const url = new URL(request.url ?? "/", "http://localhost");
    let selected;
    try {
      selected = await fileFor(root, url.pathname);
    } catch {
      respond(response, 500, "Static application is unavailable.");
      return;
    }

    if (!selected.path) {
      respond(response, selected.status, selected.status === 404 ? "Not Found" : "Invalid request");
      return;
    }

    const extension = extname(selected.path).toLowerCase();
    const cacheControl = selected.path.endsWith("index.html")
      ? "no-cache"
      : "public, max-age=31536000, immutable";
    response.writeHead(200, {
      "Content-Type": contentTypes.get(extension) ?? "application/octet-stream",
      "Content-Length": selected.metadata.size,
      "Cache-Control": cacheControl,
    });
    if (request.method === "HEAD") {
      response.end();
      return;
    }
    createReadStream(selected.path).pipe(response);
  });
}


export function startFrontendServer({ staticRoot, port: portValue } = {}) {
  const port = runtimePort(portValue ?? process.env.PORT ?? "8080");
  const server = createFrontendServer({ staticRoot });
  server.listen(port, "0.0.0.0", () => {
    console.log(JSON.stringify({ event: "frontend_started", port }));
  });

  function shutdown() {
    server.close(() => process.exit(0));
  }

  process.on("SIGTERM", shutdown);
  process.on("SIGINT", shutdown);
  return server;
}


if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  startFrontendServer();
}
