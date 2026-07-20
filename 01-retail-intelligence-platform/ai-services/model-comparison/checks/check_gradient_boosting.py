"""Readable Day 62 check for the Gradient Boosting candidate."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "model-comparison" / "src"
sys.path.insert(0, str(MODULE_SRC))

from model_comparison.gradient_boosting import (  # noqa: E402
    run_gradient_boosting,
)


def main() -> None:
    """Regenerate and validate official Gradient Boosting evidence."""
    first = run_gradient_boosting(PROJECT_ROOT)
    output_root = PROJECT_ROOT / "reports" / "outputs" / "model-comparison"
    first_predictions = (
        output_root / "predictions" / "gradient_boosting.csv"
    ).read_bytes()
    second = run_gradient_boosting(PROJECT_ROOT)
    second_predictions = (
        output_root / "predictions" / "gradient_boosting.csv"
    ).read_bytes()
    stored = json.loads(
        (output_root / "results" / "gradient_boosting.json").read_text(
            encoding="utf-8"
        )
    )
    parameters = stored["configuration"]["estimator_parameters"]

    assert first_predictions == second_predictions
    assert first.metrics == second.metrics
    assert parameters["random_state"] == 42
    assert parameters["learning_rate"] == 0.05
    assert parameters["loss"] == "squared_error"
    assert stored["dataset_sha256"]
    assert stored["train_rows"] == 12
    assert stored["test_rows"] == 6
    assert stored["production_status"] == "learning_evidence_only"

    print("OK - Sprint 2 Day 62 Gradient Boosting check passed")
    print(f"MAE / RMSE: {first.metrics.mae:.4f} / {first.metrics.rmse:.4f}")
    print(f"R² diagnostic: {first.metrics.r2:.4f}")
    print("Repeated prediction artifact: byte-identical")


if __name__ == "__main__":
    main()
