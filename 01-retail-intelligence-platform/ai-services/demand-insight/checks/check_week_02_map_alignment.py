"""Run the Week 2 production pipeline and validate its existing evidence."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.pipelines.feature_baseline_metric_pipeline import (  # noqa: E402
    ERROR_COLUMN,
    PREDICTION_COLUMN,
    run_feature_baseline_metric_pipeline,
)


def main() -> None:
    result = run_feature_baseline_metric_pipeline(PROJECT_ROOT)
    output = pd.read_csv(result["output_path"])
    required = {"day_of_week", "month", "year", "is_weekend", "revenue", PREDICTION_COLUMN, ERROR_COLUMN}
    missing = sorted(required.difference(output.columns))
    evidence = [
        PROJECT_ROOT / "docs/sprints/sprint-01-demand-insight/week-02/review.md",
        Path(result["summary_path"]),
        PROJECT_ROOT / "reports/summaries/demand-insight/week_02_technical_report.md",
    ]
    if missing or any(not path.exists() for path in evidence):
        raise AssertionError(f"Week 2 alignment failed: columns={missing}, evidence={evidence}")
    if result["baseline_mae"] < 0:
        raise AssertionError("Baseline MAE cannot be negative.")
    print(f"OK - Week 2 map alignment: {result['rows']} rows, MAE {result['baseline_mae']:.2f}")


if __name__ == "__main__":
    main()
