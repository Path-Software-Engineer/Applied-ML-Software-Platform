"""Feature + baseline + metric pipeline for Sprint 1 Week 2 alignment."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.baselines.baseline import (
    calculate_mae,
    calculate_mean_baseline,
    create_mean_baseline_predictions,
)
from src.features.feature_engineering import build_sales_features

INPUT_CANDIDATES = [
    "data/processed/demand-insight/sales_pipeline_ready.csv",
    "data/processed/demand-insight/sales_clean.csv",
    "data/processed/demand-insight/sales_features.csv",
]
TARGET_COLUMN = "units_sold"
PREDICTION_COLUMN = "mean_baseline_prediction"
ERROR_COLUMN = "baseline_absolute_error"


class DemandMetricPipelineError(Exception):
    """Raised when the Week 2 demand metric pipeline cannot run."""


def find_input_dataset(project_root: Path) -> Path:
    """Find the best available input dataset for the demand metric pipeline."""
    for relative_path in INPUT_CANDIDATES:
        candidate = project_root / relative_path
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No valid input dataset found for the demand metric pipeline.")


def build_feature_baseline_metric_table(data: pd.DataFrame) -> tuple[pd.DataFrame, float, float]:
    """Build features, baseline predictions and MAE in one integrated table."""
    featured = build_sales_features(data)

    if TARGET_COLUMN not in featured.columns:
        raise DemandMetricPipelineError(f"Missing target column: {TARGET_COLUMN}")

    target = featured[TARGET_COLUMN]
    predictions = create_mean_baseline_predictions(target)
    baseline_value = calculate_mean_baseline(target)
    baseline_mae = calculate_mae(target, predictions)

    output = featured.copy()
    output[PREDICTION_COLUMN] = predictions
    output[ERROR_COLUMN] = (output[TARGET_COLUMN] - output[PREDICTION_COLUMN]).abs()

    return output, baseline_value, baseline_mae


def write_pipeline_summary(
    project_root: Path,
    input_path: Path,
    output_path: Path,
    rows: int,
    columns: int,
    baseline_value: float,
    baseline_mae: float,
) -> Path:
    """Write the pipeline summary report."""
    summary_path = (
        project_root
        / "reports"
        / "summaries"
        / "demand-insight"
        / "feature_baseline_metric_pipeline_summary.md"
    )
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        f"""# Feature + Baseline + Metric Pipeline Summary

## Official map alignment

This output closes the official Week 2 Day 6 requirement:

```txt
Pipeline with features, baseline and metric.
```

## Input

```txt
{input_path.as_posix()}
```

## Output

```txt
{output_path.as_posix()}
```

## Pipeline flow

```txt
processed dataset
â†’ feature engineering
â†’ mean baseline
â†’ baseline predictions
â†’ MAE
â†’ technical summary
```

## Results

| Metric | Value |
| ------ | ----: |
| Rows | {rows} |
| Columns | {columns} |
| Baseline | {baseline_value:.2f} |
| Baseline MAE | {baseline_mae:.2f} |

## Interpretation

The baseline gives the reference prediction.

MAE shows the average error in units sold.

This pipeline makes the Week 2 technical flow repeatable before moving into analysis and insights.

## Status

```txt
Completed
```
""",
        encoding="utf-8",
    )
    return summary_path


def run_feature_baseline_metric_pipeline(project_root: Path) -> dict[str, object]:
    """Run the integrated Week 2 demand metric pipeline."""
    input_path = find_input_dataset(project_root)
    data = pd.read_csv(input_path)
    output, baseline_value, baseline_mae = build_feature_baseline_metric_table(data)

    output_path = (
        project_root
        / "data"
        / "processed"
        / "demand-insight"
        / "sales_feature_baseline_metric_pipeline.csv"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)

    summary_path = write_pipeline_summary(
        project_root=project_root,
        input_path=input_path,
        output_path=output_path,
        rows=len(output),
        columns=len(output.columns),
        baseline_value=baseline_value,
        baseline_mae=baseline_mae,
    )

    return {
        "input_path": input_path,
        "output_path": output_path,
        "summary_path": summary_path,
        "rows": len(output),
        "columns": len(output.columns),
        "baseline_value": baseline_value,
        "baseline_mae": baseline_mae,
    }
