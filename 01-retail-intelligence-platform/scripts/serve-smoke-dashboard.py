"""Serve the compiled React smoke bundle and proxy read-only API requests."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIRECTORY = PROJECT_ROOT / ".runtime" / "smoke-dashboard"
class SmokeRequestHandler(SimpleHTTPRequestHandler):
    """Static handler with a narrow GET-only proxy for local API smoke."""

    api_base_url = "http://127.0.0.1:8000"

    def do_GET(self) -> None:  # noqa: N802 - inherited HTTP method name
        if self.path.startswith("/api/"):
            self._proxy_api_get()
            return
        super().do_GET()

    def _proxy_api_get(self) -> None:
        request = Request(
            f"{self.api_base_url}{self.path}",
            headers={"Accept": self.headers.get("Accept", "application/json")},
            method="GET",
        )
        try:
            with urlopen(request, timeout=10) as response:
                body = response.read()
                self.send_response(response.status)
                self.send_header(
                    "Content-Type",
                    response.headers.get("Content-Type", "application/octet-stream"),
                )
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        except HTTPError as error:
            body = error.read()
            self.send_response(error.code)
            self.send_header(
                "Content-Type",
                error.headers.get("Content-Type", "application/json"),
            )
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except URLError:
            body = b'{"detail":"Local API is unavailable."}'
            self.send_response(503)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5173)
    parser.add_argument("--directory", type=Path, default=DEFAULT_DIRECTORY)
    parser.add_argument("--api-base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()

    directory = args.directory.resolve()
    if not (directory / "index.html").is_file():
        raise SystemExit(
            "Smoke dashboard is missing. Run scripts/build-smoke-dashboard.ps1."
        )
    SmokeRequestHandler.api_base_url = args.api_base_url.rstrip("/")
    handler = partial(SmokeRequestHandler, directory=str(directory))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Smoke dashboard: http://{args.host}:{args.port}")
    print(f"API proxy: {SmokeRequestHandler.api_base_url}")
    server.serve_forever()


if __name__ == "__main__":
    main()
