from pathlib import Path

import sys

import pandas as pd


CURRENT_FILE = Path(__file__).resolve()
MODULE_ROOT = CURRENT_FILE.parents[1]
PROJECT_ROOT = CURRENT_FILE.parents[3]

sys.path.append(str(MODULE_ROOT))

from src.data.data_cleaner import (  # noqa: E402
    REQUIRED_COLUMNS,
    build_clean_sales_dataset,
    clean_sales_data,
    validate_required_columns,
)


RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "demand-insight"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed" / "demand-insight"
REPORTS_DIR = PROJECT_ROOT / "reports" / "summaries" / "demand-insight"

RAW_DATA_PATH = RAW_DATA_DIR / "sales.csv"
CLEAN_DATA_PATH = PROCESSED_DATA_DIR / "sales_clean.csv"
SUMMARY_PATH = REPORTS_DIR / "data_cleaning_summary.md"


def resolve_raw_data_path() -> Path:
    """Return sales.csv if it exists, otherwise return the first CSV found."""
    if RAW_DATA_PATH.exists():
        return RAW_DATA_PATH

    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV file found in {RAW_DATA_DIR}. Add a raw sales CSV before running this check."
        )

    return csv_files[0]


def write_summary(raw_data: pd.DataFrame, clean_data: pd.DataFrame, raw_path: Path) -> None:
    """Write a Markdown summary with data cleaning evidence."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    rows_removed = len(raw_data) - len(clean_data)
    duplicate_count_after_cleaning = clean_data.duplicated().sum()
    missing_values_after_cleaning = clean_data[REQUIRED_COLUMNS].isna().sum().sum()

    summary = f"""# Data Cleaning Summary

## Sprint

Sprint 1 — Demand Insight Module

## Day

Día 5 — Data Cleaning

## Input

Raw dataset:

```txt
{raw_path}
```

## Output

Clean dataset:

```txt
{CLEAN_DATA_PATH}
```

## Cleaning rules applied

- Validated required columns.
- Converted `date` to datetime.
- Converted `units_sold` to numeric.
- Converted `unit_price` to numeric.
- Trimmed text fields.
- Removed rows with missing required values.
- Removed rows with negative `units_sold`.
- Removed rows with negative `unit_price`.
- Removed duplicate rows.
- Sorted data by `date` and `product_id`.

## Evidence

| Metric | Value |
| ------ | ----: |
| Raw rows | {len(raw_data)} |
| Clean rows | {len(clean_data)} |
| Rows removed | {rows_removed} |
| Required columns | {len(REQUIRED_COLUMNS)} |
| Missing values after cleaning | {missing_values_after_cleaning} |
| Duplicate rows after cleaning | {duplicate_count_after_cleaning} |

## Required columns

```txt
{REQUIRED_COLUMNS}
```

## Interpretation

The dataset is now clean enough to move into the first pipeline stage.

This does not mean the dataset is feature-ready yet.

Feature engineering starts after cleaning is reliable.
"""

    SUMMARY_PATH.write_text(summary, encoding="utf-8")


def main() -> None:
    raw_path = resolve_raw_data_path()
    raw_data = pd.read_csv(raw_path)

    validate_required_columns(raw_data)

    clean_data = build_clean_sales_dataset(
        raw_path=raw_path,
        output_path=CLEAN_DATA_PATH,
    )

    assert not clean_data.empty, "Clean dataset should not be empty."
    assert CLEAN_DATA_PATH.exists(), "Clean dataset file was not created."
    assert all(column in clean_data.columns for column in REQUIRED_COLUMNS), (
        "Clean dataset is missing required columns."
    )
    assert clean_data[REQUIRED_COLUMNS].isna().sum().sum() == 0, (
        "Clean dataset still has missing values in required columns."
    )
    assert (clean_data["units_sold"] >= 0).all(), "units_sold should not contain negative values."
    assert (clean_data["unit_price"] >= 0).all(), "unit_price should not contain negative values."
    assert clean_data.duplicated().sum() == 0, "Clean dataset should not contain duplicate rows."

    write_summary(raw_data=raw_data, clean_data=clean_data, raw_path=raw_path)

    print("Data cleaning check passed.")
    print(f"Raw dataset: {raw_path}")
    print(f"Clean dataset: {CLEAN_DATA_PATH}")
    print(f"Summary: {SUMMARY_PATH}")
    print(f"Raw rows: {len(raw_data)}")
    print(f"Clean rows: {len(clean_data)}")


if __name__ == "__main__":
    main()