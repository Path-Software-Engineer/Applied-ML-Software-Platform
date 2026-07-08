"""Check Day 13 mean baseline."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.baselines.baseline import (  # noqa: E402
    calculate_mean_baseline,
    create_mean_baseline_predictions,
)

DATASET = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_features.csv"
TARGET_COLUMN = "units_sold"


def write_summary(baseline_value: float, rows: int) -> None:
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "mean_baseline_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        f"""# Mean Baseline Summary

## Day

Day 13 â€” Mean Baseline

## Target

```txt
{TARGET_COLUMN}
```

## Baseline

```txt
{baseline_value:.2f} units
```

## Result

| Metric | Value |
| ------ | ----: |
| Rows | {rows} |
| Baseline | {baseline_value:.2f} |

## Interpretation

The mean baseline does not learn patterns.

It gives the minimum reference that future models should beat.

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
    baseline_value = calculate_mean_baseline(target)
    predictions = create_mean_baseline_predictions(target)

    if len(predictions) != len(target):
        raise AssertionError("Baseline predictions length does not match target length.")

    write_summary(baseline_value=baseline_value, rows=len(data))

    print("OK - Day 13 mean baseline check passed")
    print(f"Baseline: {baseline_value:.2f}")
    print("Summary: reports/summaries/demand-insight/mean_baseline_summary.md")


if __name__ == "__main__":
    main()
