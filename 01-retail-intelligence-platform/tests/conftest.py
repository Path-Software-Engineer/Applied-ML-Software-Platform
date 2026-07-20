"""Shared pytest configuration for isolated workspace-safe tests."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from uuid import uuid4

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
AI_MODULE_ROOT = PROJECT_ROOT / "ai-services" / "demand-insight"
MODEL_COMPARISON_SRC = (
    PROJECT_ROOT / "ai-services" / "model-comparison" / "src"
)
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(AI_MODULE_ROOT))
sys.path.insert(0, str(MODEL_COMPARISON_SRC))


@pytest.fixture
def tmp_path() -> Path:
    """Provide an isolated writable path inside the ignored runtime directory."""
    root = PROJECT_ROOT / ".runtime" / "pytest"
    path = root / uuid4().hex
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path)
        if root.exists() and not any(root.iterdir()):
            root.rmdir()
