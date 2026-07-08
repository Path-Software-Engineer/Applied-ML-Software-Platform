"""Check Day 14 baseline MAE."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.baselines.baseline import (  # noqa: E402
    calculate_mae,
    calculate_mean_baseline,
    create_mean_baseline_predictions,
)

DATASET = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_features.csv"
TARGET_COLUMN = "units_sold"


def write_summary(baseline_value: float, baseline_mae: float, rows: int) -> None:
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "baseline_mae_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        f"""# Baseline MAE Summary

## Day

Day 14 â€” Baseline MAE

## Target

```txt
{TARGET_COLUMN}
```

## Results

| Metric | Value |
| ------ | ----: |
| Rows | {rows} |
| Baseline | {baseline_value:.2f} |
| Baseline MAE | {baseline_mae:.2f} |

## Interpretation

The baseline gives the base prediction.

MAE says how wrong that prediction is on average.

## Status

```txt
Completed
```
""",
        encoding="utf-8",
    )


def main() -> None:
    if not DATASET.exists():
        raise FileNotFoundError(f"Missing feature dataset: {DATASET}")

    data = pd.read_csv(DATASET)
    if TARGET_COLUMN not in data.columns:
        raise AssertionError(f"Missing target column: {TARGET_COLUMN}")

    target = data[TARGET_COLUMN]
    predictions = create_mean_baseline_predictions(target)
    baseline_value = calculate_mean_baseline(target)
    baseline_mae = calculate_mae(target, predictions)

    if baseline_mae < 0:
        raise AssertionError("MAE cannot be negative.")

    write_summary(baseline_value=baseline_value, baseline_mae=baseline_mae, rows=len(data))

    print("OK - Day 14 baseline MAE check passed")
    print(f"Baseline: {baseline_value:.2f}")
    print(f"Baseline MAE: {baseline_mae:.2f}")
    print("Summary: reports/summaries/demand-insight/baseline_mae_summary.md")


if __name__ == "__main__":
    main()
