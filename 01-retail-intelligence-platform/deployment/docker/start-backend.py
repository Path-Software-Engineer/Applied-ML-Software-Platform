"""Start the FastAPI process using the Cloud Run container contract."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import uvicorn


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def configure_import_path() -> None:
    """Make the copied repository root importable from the script entry point."""

    project_root = str(PROJECT_ROOT)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


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
    configure_import_path()
    uvicorn.run(
        "backend.api.app.main:app",
        host="0.0.0.0",
        port=runtime_port(),
        access_log=True,
    )
