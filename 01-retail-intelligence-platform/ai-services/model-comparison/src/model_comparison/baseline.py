"""Training-mean baseline evaluated on the official test partition."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .metrics import calculate_regression_metrics
from .results import (
    RESULT_SCHEMA_VERSION,
    CandidateResult,
    build_prediction_table,
)


def evaluate_training_mean_baseline(
    train: pd.DataFrame,
    test: pd.DataFrame,
    manifest: dict[str, object],
) -> tuple[CandidateResult, pd.DataFrame]:
    """Fit a mean on training targets only and evaluate the test rows."""
    if train.empty or test.empty:
        raise ValueError("Baseline evaluation requires train and test rows.")
    baseline_value = float(pd.to_numeric(train["units_sold"]).mean())
    predictions = [baseline_value] * len(test)
    metrics = calculate_regression_metrics(test["units_sold"], predictions)
    split = manifest["split"]
    if not isinstance(split, dict):
        raise ValueError("Split manifest has an invalid split section.")

    result = CandidateResult(
        schema_version=RESULT_SCHEMA_VERSION,
        model_id="training_mean",
        model_name="Training Mean Baseline",
        model_family="baseline",
        configuration={"strategy": "mean_of_training_target"},
        dataset_sha256=str(manifest["dataset_sha256"]),
        split_strategy=str(split["strategy"]),
        target=str(manifest["target"]),
        target_unit=str(manifest["target_unit"]),
        train_rows=len(train),
        test_rows=len(test),
        metrics=metrics,
    )
    return result, build_prediction_table(test, predictions)


def run_baseline_evaluation(
    project_root: Path,
) -> tuple[CandidateResult, pd.DataFrame]:
    """Evaluate and persist official Day 59 baseline evidence."""
    input_root = project_root / "data" / "processed" / "model-comparison"
    output_root = project_root / "reports" / "outputs" / "model-comparison"
    train = pd.read_csv(input_root / "train.csv")
    test = pd.read_csv(input_root / "test.csv")
    manifest = json.loads(
        (output_root / "split_manifest.json").read_text(encoding="utf-8")
    )
    result, predictions = evaluate_training_mean_baseline(train, test, manifest)

    prediction_path = output_root / "predictions" / "training_mean.csv"
    result_path = output_root / "results" / "training_mean.json"
    prediction_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(prediction_path, index=False)
    result_path.write_text(
        json.dumps(result.to_dict(), indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return result, predictions


def main() -> None:
    """Generate the official baseline artifacts."""
    project_root = Path(__file__).resolve().parents[4]
    result, _ = run_baseline_evaluation(project_root)
    print("Training Mean baseline generated")
    print(f"MAE: {result.metrics.mae:.4f} units")
    print(f"RMSE: {result.metrics.rmse:.4f} units")
    print(f"R²: {result.metrics.r2:.4f}")


if __name__ == "__main__":
    main()
