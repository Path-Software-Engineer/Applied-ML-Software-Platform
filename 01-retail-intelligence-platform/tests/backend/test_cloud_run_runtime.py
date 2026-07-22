"""Tests for the backend Cloud Run process entry point."""

from __future__ import annotations

import importlib.util
from pathlib import Path

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
