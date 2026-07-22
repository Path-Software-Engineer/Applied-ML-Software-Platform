"""Runtime settings shared by local execution and managed deployments."""

from __future__ import annotations

import os
from urllib.parse import urlsplit


DEFAULT_CORS_ALLOWED_ORIGINS = (
    "http://localhost:5173",
    "http://127.0.0.1:5173",
)


def cors_allowed_origins() -> list[str]:
    """Return validated, exact browser origins without accepting wildcards."""

    raw = os.getenv("CORS_ALLOWED_ORIGINS")
    if raw is None:
        return list(DEFAULT_CORS_ALLOWED_ORIGINS)

    candidates = [item.strip().rstrip("/") for item in raw.split(",")]
    origins: list[str] = []
    for origin in candidates:
        parsed = urlsplit(origin)
        if (
            not origin
            or origin == "*"
            or parsed.scheme not in {"http", "https"}
            or not parsed.netloc
            or parsed.path not in {"", "/"}
            or parsed.query
            or parsed.fragment
            or parsed.username
            or parsed.password
        ):
            raise RuntimeError(
                "CORS_ALLOWED_ORIGINS must contain comma-separated exact HTTP(S) origins."
            )
        if origin not in origins:
            origins.append(origin)

    if not origins:
        raise RuntimeError("CORS_ALLOWED_ORIGINS must contain at least one origin.")
    return origins
