"""Start Uvicorn briefly and verify the real local HTTP boundary."""

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
PORT = 8010


def read_json(path: str) -> dict[str, object]:
    with urlopen(f"http://{HOST}:{PORT}{path}", timeout=2) as response:
        if response.status != 200:
            raise RuntimeError(f"Unexpected HTTP status for {path}: {response.status}")
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.api.app.main:app",
            "--host",
            HOST,
            "--port",
            str(PORT),
        ],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
    )
    try:
        health = None
        for _ in range(40):
            if process.poll() is not None:
                break
            try:
                health = read_json("/health")
                break
            except (URLError, TimeoutError, ConnectionError):
                time.sleep(0.25)
        if health is None:
            output = process.stdout.read() if process.stdout else ""
            raise RuntimeError(f"Uvicorn did not become ready.\n{output}")

        summary = read_json("/api/v1/demand-insights/summary")
        if health != {"status": "ok", "service": "retail-intelligence-api"}:
            raise AssertionError(f"Unexpected live health response: {health}")
        if summary["schema_version"] != "1.0":
            raise AssertionError("Unexpected live Demand Summary schema version.")
        sales = summary["sales_summary"]
        if sales["total_units_sold"] != 293 or sales["total_revenue"] != 747.65:
            raise AssertionError(f"Unexpected live Demand Summary totals: {sales}")

        print("OK - Day 24 live Uvicorn smoke check passed")
        print(f"URL: http://{HOST}:{PORT}")
        print("Health: ok")
        print("Schema version: 1.0")
        print("Totals: 293 units | 747.65 revenue")
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


if __name__ == "__main__":
    main()
