"""Compare raw, clean and processed EDA flows for Demand Insight."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[4]


def find_raw_csv() -> Path:
    raw_dir = PROJECT_ROOT / "data" / "raw" / "demand-insight"
    csv_files = sorted(raw_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No raw CSV files found in {raw_dir}")
    return csv_files[0]


def dataset_info(label: str, path: Path) -> dict[str, object]:
    if not path.exists():
        return {"label": label, "path": path.as_posix(), "exists": False, "rows": 0, "columns": 0, "column_names": []}

    data = pd.read_csv(path)
    return {
        "label": label,
        "path": path.as_posix(),
        "exists": True,
        "rows": len(data),
        "columns": len(data.columns),
        "column_names": list(data.columns),
    }


def write_report(infos: list[dict[str, object]]) -> Path:
    output_path = PROJECT_ROOT / "labs" / "tec-labs" / "tec-sales-eda-lab" / "outputs" / "eda_flow_comparison.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for info in infos:
        status = "yes" if info["exists"] else "no"
        rows.append(f"| {info['label']} | {status} | {info['rows']} | {info['columns']} | `{info['path']}` |")

    content = f"""# EDA Flow Comparison

## Lab

`tec-sales-eda-lab`

## Goal

Compare the raw, clean and processed data flows of the Demand Insight Module.

## Comparison

| Dataset | Exists | Rows | Columns | Path |
| ------- | ------ | ---: | ------: | ---- |
{chr(10).join(rows)}

## Interpretation

```txt
raw shows what arrived
clean shows what was validated
processed shows what was enriched
```

## Status

```txt
Completed
```
"""

    output_path.write_text(content, encoding="utf-8")
    return output_path


def main() -> None:
    raw_path = find_raw_csv()
    clean_path = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_clean.csv"
    processed_path = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_features.csv"

    infos = [
        dataset_info("raw", raw_path),
        dataset_info("clean", clean_path),
        dataset_info("processed", processed_path),
    ]

    output_path = write_report(infos)
    print("OK - EDA flow comparison generated")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
