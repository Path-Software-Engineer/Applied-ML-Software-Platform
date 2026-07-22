"""Start the FastAPI process using the Cloud Run container contract."""

from __future__ import annotations

import os

import uvicorn


def runtime_port() -> int:
    raw = os.getenv("PORT", "8080")
    try:
        port = int(raw)
    except ValueError as error:
        raise RuntimeError("PORT must be an integer.") from error
    if not 1 <= port <= 65535:
        raise RuntimeError("PORT must be between 1 and 65535.")
    return port


if __name__ == "__main__":
    uvicorn.run(
        "backend.api.app.main:app",
        host="0.0.0.0",
        port=runtime_port(),
        access_log=True,
    )
