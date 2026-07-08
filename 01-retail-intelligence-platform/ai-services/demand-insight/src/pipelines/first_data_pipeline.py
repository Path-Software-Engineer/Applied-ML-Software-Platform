"""First data pipeline for the Demand Insight Module.

This module connects the previous work from Day 4 and Day 5:
raw sales data -> validation -> cleaning -> pipeline-ready dataset -> summary.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["date", "product_id", "product_name", "units_sold", "unit_price"]
RAW_DATA_CANDIDATES = ["sales.csv", "sales_raw.csv", "retail_sales.csv"]


def find_raw_sales_file(project_root: Path) -> Path:
    """Find the raw sales CSV inside data/raw/demand-insight."""
    raw_dir = project_root / "data" / "raw" / "demand-insight"

    for filename in RAW_DATA_CANDIDATES:
        candidate = raw_dir / filename
        if candidate.exists():
            return candidate

    csv_files = sorted(raw_dir.glob("*.csv"))
    if csv_files:
        return csv_files[0]

    raise FileNotFoundError(f"No CSV file found in {raw_dir}")


def load_raw_sales_data(raw_data_path: str | Path) -> pd.DataFrame:
    """Load raw sales data from CSV."""
    path = Path(raw_data_path)

    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found: {path}")

    return pd.read_csv(path)


def validate_required_columns(data: pd.DataFrame) -> None:
    """Validate that the dataset contains the required sales columns."""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in data.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def prepare_pipeline_dataset(data: pd.DataFrame) -> pd.DataFrame:
    """Create a clean, pipeline-ready dataset from raw sales data."""
    validate_required_columns(data)

    prepared = data.copy()
    prepared = prepared.drop_duplicates()
    prepared = prepared.dropna(subset=REQUIRED_COLUMNS)

    prepared["date"] = pd.to_datetime(prepared["date"], errors="coerce")
    prepared["units_sold"] = pd.to_numeric(prepared["units_sold"], errors="coerce")
    prepared["unit_price"] = pd.to_numeric(prepared["unit_price"], errors="coerce")

    prepared = prepared.dropna(subset=["date", "units_sold", "unit_price"])
    prepared = prepared[prepared["units_sold"] >= 0]
    prepared = prepared[prepared["unit_price"] >= 0]

    prepared = prepared.sort_values(["date", "product_id"]).reset_index(drop=True)
    prepared["date"] = prepared["date"].dt.strftime("%Y-%m-%d")

    return prepared


def write_pipeline_summary(
    data: pd.DataFrame,
    raw_data_path: str | Path,
    output_path: str | Path,
    summary_path: str | Path,
) -> None:
    """Write a markdown summary for the first data pipeline."""
    raw_path = Path(raw_data_path)
    output = Path(output_path)
    summary = Path(summary_path)
    summary.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# First Data Pipeline Summary

## Sprint

Sprint 1 â€” Demand Insight Module

## Day

Day 6 â€” First Data Pipeline

## Pipeline flow

```txt
raw sales data
â†’ load dataset
â†’ validate required columns
â†’ clean rows
â†’ export pipeline-ready dataset
â†’ write summary
```

## Inputs

```txt
{raw_path.as_posix()}
```

## Outputs

```txt
{output.as_posix()}
```

## Result

| Metric | Value |
| ------ | ----: |
| Rows | {len(data)} |
| Columns | {len(data.columns)} |

## Required columns

```txt
{', '.join(REQUIRED_COLUMNS)}
```

## Interpretation

The Demand Insight Module now has a repeatable first data pipeline.

This pipeline connects raw data loading, column validation, cleaning rules and a processed output that can be reused by later feature engineering, baseline and insight steps.

## Status

```txt
Completed
```
"""

    summary.write_text(content, encoding="utf-8")


def build_pipeline_ready_dataset(
    raw_data_path: str | Path,
    output_path: str | Path,
    summary_path: str | Path | None = None,
) -> pd.DataFrame:
    """Run the first data pipeline and return the pipeline-ready dataset."""
    raw_data = load_raw_sales_data(raw_data_path)
    pipeline_ready = prepare_pipeline_dataset(raw_data)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    pipeline_ready.to_csv(output, index=False)

    if summary_path is not None:
        write_pipeline_summary(
            data=pipeline_ready,
            raw_data_path=raw_data_path,
            output_path=output_path,
            summary_path=summary_path,
        )

    return pipeline_ready
