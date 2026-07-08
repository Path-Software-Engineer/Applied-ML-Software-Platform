"""Check Day 9 temporal features."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.features.feature_engineering import add_date_features  # noqa: E402

INPUT_CANDIDATES = [
    "data/processed/demand-insight/sales_pipeline_ready.csv",
    "data/processed/demand-insight/sales_clean.csv",
]

REQUIRED_FEATURES = ["day_of_week", "month", "year", "is_weekend"]


def find_input_dataset() -> Path:
    for relative_path in INPUT_CANDIDATES:
        candidate = PROJECT_ROOT / relative_path
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No clean or pipeline-ready dataset found for temporal features.")


def write_summary(data: pd.DataFrame, input_path: Path, output_path: Path) -> None:
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "temporal_features_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        f"""# Temporal Features Summary

## Day

Day 9 â€” Temporal Features

## Input

```txt
{input_path.as_posix()}
```

## Output

```txt
{output_path.as_posix()}
```

## Features created

```txt
{', '.join(REQUIRED_FEATURES)}
```

## Result

| Metric | Value |
| ------ | ----: |
| Rows | {len(data)} |
| Columns | {len(data.columns)} |

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
    featured = add_date_features(data)

    missing = [column for column in REQUIRED_FEATURES if column not in featured.columns]
    if missing:
        raise AssertionError(f"Missing temporal features: {missing}")

    output_path = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_temporal_features.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    featured.to_csv(output_path, index=False)
    write_summary(featured, input_path, output_path)

    print("OK - Day 9 temporal features check passed")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Rows: {len(featured)}")
    print(f"Columns: {len(featured.columns)}")


if __name__ == "__main__":
    main()
