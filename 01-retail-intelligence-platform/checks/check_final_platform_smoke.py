"""Exercise the compiled three-stage platform through real local HTTP processes."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HOST = "127.0.0.1"
API_PORT = 8012
WEB_PORT = 5175
SMOKE_ROOT = PROJECT_ROOT / ".runtime" / "smoke-dashboard"


def read(path: str, port: int) -> tuple[int, bytes, str]:
    with urlopen(f"http://{HOST}:{port}{path}", timeout=3) as response:
        return response.status, response.read(), response.headers.get("Content-Type", "")


def wait_for(path: str, port: int) -> tuple[int, bytes, str]:
    for _ in range(40):
        try:
            return read(path, port)
        except (URLError, TimeoutError, ConnectionError):
            time.sleep(0.25)
    raise RuntimeError(f"Local service did not become ready on port {port}.")


def stop(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def main() -> None:
    if not (SMOKE_ROOT / "index.html").is_file():
        raise AssertionError(
            "Compiled smoke dashboard is missing; run build-smoke-dashboard.ps1."
        )

    api = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.api.app.main:app",
            "--host",
            HOST,
            "--port",
            str(API_PORT),
        ],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
    )
    web = subprocess.Popen(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "serve-smoke-dashboard.py"),
            "--host",
            HOST,
            "--port",
            str(WEB_PORT),
            "--directory",
            str(SMOKE_ROOT),
            "--api-base-url",
            f"http://{HOST}:{API_PORT}",
        ],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
    )
    try:
        health_status, health_body, _ = wait_for("/health", API_PORT)
        page_status, page_body, page_type = wait_for("/", WEB_PORT)
        script_status, script_body, script_type = read("/main.js", WEB_PORT)
        routes = {
            "demand": "/api/v1/demand-insights/summary",
            "comparison": "/api/v1/model-comparisons/summary",
            "inventory": "/api/v1/inventory-decisions/summary",
        }
        responses = {name: read(path, WEB_PORT) for name, path in routes.items()}
        resources = {name: json.loads(body) for name, (_, body, _) in responses.items()}

        assert health_status == page_status == script_status == 200
        assert all(status == 200 for status, _, _ in responses.values())
        assert json.loads(health_body) == {
            "status": "ok",
            "service": "retail-intelligence-api",
        }
        assert b'<div id="root"></div>' in page_body
        for label in (b"Demand Insight", b"Model Comparison", b"Inventory Decision"):
            assert label in script_body
        assert "text/html" in page_type
        assert "javascript" in script_type
        assert all("application/json" in content_type for _, _, content_type in responses.values())
        assert resources["demand"]["sales_summary"]["total_units_sold"] == 293
        assert resources["comparison"]["decision"]["selected_candidate"]["model_id"] == "random_forest"
        assert resources["inventory"]["summary"]["suggested_review_quantity_units"] == 97

        print("OK - Sprint 3 Day 145 final platform HTTP smoke check passed")
        print("Compiled React shell and API health: 200")
        print("Demand Insight: 293 observed units")
        print("Model Comparison: Random Forest selected candidate")
        print("Inventory Decision: 97 suggested review units")
    finally:
        stop(web)
        stop(api)


if __name__ == "__main__":
    main()
