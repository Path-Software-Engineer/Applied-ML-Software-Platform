from __future__ import annotations

import sys
import shutil
from pathlib import Path
from uuid import uuid4

import pytest

MODULE_ROOT = Path(__file__).resolve().parents[3] / "ai-services" / "demand-insight"
sys.path.insert(0, str(MODULE_ROOT))


@pytest.fixture
def tmp_path() -> Path:
    """Provide an isolated writable path inside the workspace on Windows."""
    root = Path(__file__).resolve().parent / ".tmp"
    path = root / uuid4().hex
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path)
        if root.exists() and not any(root.iterdir()):
            root.rmdir()
