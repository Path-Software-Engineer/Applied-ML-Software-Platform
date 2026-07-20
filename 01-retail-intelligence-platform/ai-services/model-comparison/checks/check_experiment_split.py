"""Readable Day 58 validation for the official experiment split."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "model-comparison" / "src"
sys.path.insert(0, str(MODULE_SRC))

from model_comparison.data import run_experiment_preparation  # noqa: E402


def main() -> None:
    """Generate and validate official split evidence."""
    split = run_experiment_preparation(PROJECT_ROOT)
    manifest_path = (
        PROJECT_ROOT
        / "reports"
        / "outputs"
        / "model-comparison"
        / "split_manifest.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    train = pd.read_csv(
        PROJECT_ROOT / "data" / "processed" / "model-comparison" / "train.csv"
    )
    test = pd.read_csv(
        PROJECT_ROOT / "data" / "processed" / "model-comparison" / "test.csv"
    )

    assert len(split.train) == len(train) == 12
    assert len(split.test) == len(test) == 6
    assert manifest["split"]["train_end"] == "2026-01-06"
    assert manifest["split"]["test_start"] == "2026-01-07"
    assert not set(train["sale_id"]) & set(test["sale_id"])
    assert manifest["dataset_sha256"]
    assert manifest["production_status"] == "learning_evidence_only"

    print("OK - Sprint 2 Day 58 experiment split check passed")
    print(f"Train / test rows: {len(train)} / {len(test)}")
    print("Boundary: 2026-01-06 -> 2026-01-07")
    print(f"Dataset SHA-256: {manifest['dataset_sha256']}")
    print("Target / unit: units_sold / units_per_sale_record")


if __name__ == "__main__":
    main()
