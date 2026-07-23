"""Tests for the backend Cloud Run process entry point."""

from __future__ import annotations

import importlib.util
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = PROJECT_ROOT / "deployment" / "docker" / "start-backend.py"
SPEC = importlib.util.spec_from_file_location("cloud_run_backend", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_runtime_port_defaults_to_cloud_run_port(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PORT", raising=False)

    assert MODULE.runtime_port() == 8080


def test_runtime_port_accepts_cloud_run_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PORT", "9090")

    assert MODULE.runtime_port() == 9090


@pytest.mark.parametrize("value", ["invalid", "0", "65536"])
def test_runtime_port_rejects_invalid_values(
    monkeypatch: pytest.MonkeyPatch,
    value: str,
) -> None:
    monkeypatch.setenv("PORT", value)

    with pytest.raises(RuntimeError, match="PORT"):
        MODULE.runtime_port()


def test_container_entry_point_serves_health_from_repository_root() -> None:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]

    environment = os.environ.copy()
    environment.update(
        {
            "PORT": str(port),
            "CORS_ALLOWED_ORIGINS": "https://placeholder.invalid",
        }
    )
    process = subprocess.Popen(
        [sys.executable, str(MODULE_PATH)],
        cwd=PROJECT_ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
    )
    try:
        health: dict[str, str] | None = None
        for _ in range(40):
            if process.poll() is not None:
                break
            try:
                with urlopen(f"http://127.0.0.1:{port}/health", timeout=1) as response:
                    health = json.loads(response.read().decode("utf-8"))
                break
            except (URLError, TimeoutError, ConnectionError):
                time.sleep(0.1)

        if health is None:
            output = process.stdout.read() if process.stdout else ""
            pytest.fail(f"Cloud Run entry point did not become ready.\n{output}")

        assert health == {"status": "ok", "service": "retail-intelligence-api"}
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
