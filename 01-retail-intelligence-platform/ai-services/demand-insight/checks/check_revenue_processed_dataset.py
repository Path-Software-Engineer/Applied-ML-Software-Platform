"""Check Day 10 revenue and processed dataset."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.features.feature_engineering import add_revenue_column  # noqa: E402

INPUT_CANDIDATES = [
    "data/processed/demand-insight/sales_temporal_features.csv",
    "data/processed/demand-insight/sales_pipeline_ready.csv",
    "data/processed/demand-insight/sales_clean.csv",
]


def find_input_dataset() -> Path:
    for relative_path in INPUT_CANDIDATES:
        candidate = PROJECT_ROOT / relative_path
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No processed dataset found for revenue calculation.")


def write_summary(data: pd.DataFrame, input_path: Path, output_path: Path) -> None:
    total_revenue = float(data["revenue"].sum())
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "revenue_processed_dataset_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        f"""# Revenue and Processed Dataset Summary

## Day

Day 10 â€” Revenue and Processed Dataset

## Input

```txt
{input_path.as_posix()}
```

## Output

```txt
{output_path.as_posix()}
```

## Rule

```txt
revenue = units_sold * unit_price
```

## Result

| Metric | Value |
| ------ | ----: |
| Rows | {len(data)} |
| Columns | {len(data.columns)} |
| Total revenue | {total_revenue:.2f} |

## Status

```txt
Completed
```
""",
        encoding="utf-8",
    )


def main() -> None:
    input_path = find_input_dataset()
    data = pd.read_csv(input_path)
    with_revenue = add_revenue_column(data)

    expected_revenue = with_revenue["units_sold"] * with_revenue["unit_price"]
    if not expected_revenue.equals(with_revenue["revenue"]):
        raise AssertionError("Revenue column does not match units_sold * unit_price.")

    output_path = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_revenue.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with_revenue.to_csv(output_path, index=False)
    write_summary(with_revenue, input_path, output_path)

    print("OK - Day 10 revenue processed dataset check passed")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Rows: {len(with_revenue)}")
    print(f"Columns: {len(with_revenue.columns)}")
    print(f"Total revenue: {with_revenue['revenue'].sum():.2f}")


if __name__ == "__main__":
    main()
