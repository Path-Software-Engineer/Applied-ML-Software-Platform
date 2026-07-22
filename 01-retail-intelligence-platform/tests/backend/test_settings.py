"""Tests for deployment-safe runtime settings."""

from __future__ import annotations

import pytest

from backend.api.app.settings import (
    DEFAULT_CORS_ALLOWED_ORIGINS,
    cors_allowed_origins,
)


def test_cors_defaults_to_local_frontend(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CORS_ALLOWED_ORIGINS", raising=False)

    assert cors_allowed_origins() == list(DEFAULT_CORS_ALLOWED_ORIGINS)


def test_cors_accepts_exact_https_origins_and_removes_duplicates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "CORS_ALLOWED_ORIGINS",
        "https://retail-web.example.run.app/, https://retail-web.example.run.app",
    )

    assert cors_allowed_origins() == ["https://retail-web.example.run.app"]


@pytest.mark.parametrize(
    "value",
    [
        "",
        "*",
        "retail-web.example.run.app",
        "ftp://retail-web.example.run.app",
        "https://user:secret@retail-web.example.run.app",
        "https://retail-web.example.run.app/path",
        "https://retail-web.example.run.app?debug=true",
    ],
)
def test_cors_rejects_unsafe_or_non_origin_values(
    monkeypatch: pytest.MonkeyPatch,
    value: str,
) -> None:
    monkeypatch.setenv("CORS_ALLOWED_ORIGINS", value)

    with pytest.raises(RuntimeError, match="CORS_ALLOWED_ORIGINS"):
        cors_allowed_origins()
