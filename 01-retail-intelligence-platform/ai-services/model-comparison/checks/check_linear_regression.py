"""Readable Day 60 check for the Linear Regression candidate."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "model-comparison" / "src"
sys.path.insert(0, str(MODULE_SRC))

from model_comparison.linear_regression import run_linear_regression  # noqa: E402


def main() -> None:
    """Regenerate and validate official Linear Regression evidence."""
    result = run_linear_regression(PROJECT_ROOT)
    output_root = PROJECT_ROOT / "reports" / "outputs" / "model-comparison"
    stored = json.loads(
        (output_root / "results" / "linear_regression.json").read_text(
            encoding="utf-8"
        )
    )
    prediction_lines = (
        output_root / "predictions" / "linear_regression.csv"
    ).read_text(encoding="utf-8").strip().splitlines()

    assert result.model_id == "linear_regression"
    assert stored["configuration"]["preprocessing"]["fit_scope"] == (
        "training_partition_only"
    )
    assert stored["dataset_sha256"]
    assert stored["train_rows"] == 12
    assert stored["test_rows"] == 6
    assert len(prediction_lines) == 7
    assert stored["production_status"] == "learning_evidence_only"

    print("OK - Sprint 2 Day 60 Linear Regression check passed")
    print(f"MAE / RMSE: {result.metrics.mae:.4f} / {result.metrics.rmse:.4f}")
    print(f"R² diagnostic: {result.metrics.r2:.4f}")
    print("Preprocessing fit scope: training partition only")


if __name__ == "__main__":
    main()
