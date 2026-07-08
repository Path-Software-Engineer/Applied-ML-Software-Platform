"""Check Sprint 1 Week 2 alignment with the current Software Engineer map."""

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

REQUIRED_COLUMNS = [
    "day_of_week",
    "month",
    "year",
    "is_weekend",
    "revenue",
    PREDICTION_COLUMN,
    ERROR_COLUMN,
]

REQUIRED_EVIDENCE = [
    "docs/sprints/sprint-01-week-02-review.md",
    "reports/summaries/demand-insight/feature_baseline_metric_pipeline_summary.md",
]


def write_week_02_technical_report(result: dict[str, object]) -> Path:
    report_path = (
        PROJECT_ROOT
        / "reports"
        / "summaries"
        / "demand-insight"
        / "week_02_technical_report.md"
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        f"""# Week 2 Technical Report â€” Demand Insight Module

## Purpose

Close the official Week 2 requirements from the current Software Engineer map.

## Official Week 2 closure

```txt
Day 6 â†’ Pipeline with features, baseline and metric
Day 7 â†’ Initial technical report and documentation
```

## Integrated flow

```txt
processed dataset
â†’ temporal features
â†’ revenue
â†’ mean baseline
â†’ baseline predictions
â†’ MAE
â†’ technical report
```

## Evidence

| Item | Value |
| ---- | ----- |
| Input dataset | `{result['input_path']}` |
| Pipeline output | `{result['output_path']}` |
| Pipeline summary | `{result['summary_path']}` |
| Rows | {result['rows']} |
| Columns | {result['columns']} |
| Baseline | {result['baseline_value']:.2f} |
| Baseline MAE | {result['baseline_mae']:.2f} |

## Interpretation

The module now has a repeatable technical path from processed data to baseline metric.

This closes Week 2 and prepares Week 3 for analysis, insight cards and user-facing language.

## Status

```txt
Completed
```
""",
        encoding="utf-8",
    )
    return report_path


def main() -> None:
    result = run_feature_baseline_metric_pipeline(PROJECT_ROOT)

    output_path = Path(result["output_path"])
    if not output_path.exists():
        raise AssertionError(f"Pipeline output was not created: {output_path}")

    output = pd.read_csv(output_path)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in output.columns]
    if missing_columns:
        raise AssertionError(f"Missing required pipeline columns: {missing_columns}")

    if result["baseline_mae"] < 0:
        raise AssertionError("Baseline MAE cannot be negative.")

    report_path = write_week_02_technical_report(result)

    missing_evidence = [path for path in REQUIRED_EVIDENCE if not (PROJECT_ROOT / path).exists()]
    if missing_evidence:
        raise AssertionError(f"Missing alignment evidence: {missing_evidence}")

    if not report_path.exists():
        raise AssertionError("Week 2 technical report was not created.")

    print("OK - Sprint 1 Week 2 map alignment check passed")
    print(f"Pipeline output: {output_path}")
    print(f"Technical report: {report_path}")
    print(f"Baseline: {result['baseline_value']:.2f}")
    print(f"Baseline MAE: {result['baseline_mae']:.2f}")


if __name__ == "__main__":
    main()
