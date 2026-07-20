"""Readable Day 59 check for baseline and metric registry evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "model-comparison" / "src"
sys.path.insert(0, str(MODULE_SRC))

from model_comparison.baseline import run_baseline_evaluation  # noqa: E402


def main() -> None:
    """Generate and validate official baseline evidence."""
    result, predictions = run_baseline_evaluation(PROJECT_ROOT)
    result_path = (
        PROJECT_ROOT
        / "reports"
        / "outputs"
        / "model-comparison"
        / "results"
        / "training_mean.json"
    )
    stored = json.loads(result_path.read_text(encoding="utf-8"))
    train = pd.read_csv(
        PROJECT_ROOT / "data" / "processed" / "model-comparison" / "train.csv"
    )

    expected_mean = float(train["units_sold"].mean())
    assert predictions["predicted_units"].nunique() == 1
    assert predictions["predicted_units"].iloc[0] == expected_mean
    assert len(predictions) == 6
    assert stored["schema_version"] == "1.0"
    assert stored["metrics"]["metadata"]["mae"]["unit"] == "units"
    assert stored["production_status"] == "learning_evidence_only"

    print("OK - Sprint 2 Day 59 baseline and metrics check passed")
    print(f"Training mean: {expected_mean:.4f} units")
    print(f"MAE / RMSE: {result.metrics.mae:.4f} / {result.metrics.rmse:.4f}")
    print(f"R² diagnostic: {result.metrics.r2:.4f}")
    print("Prediction rows: 6")


if __name__ == "__main__":
    main()
