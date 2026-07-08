"""Check Day 7 week 1 close evidence."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

REQUIRED_PATHS = [
    "README.md",
    "project-structure.txt",
    "docs/architecture.md",
    "docs/decisions.md",
    "docs/user-stories.md",
    "docs/technical-stories.md",
    "docs/sprints/sprint-01-demand-insight.md",
    "ai-services/demand-insight/src/data/data_loader.py",
    "ai-services/demand-insight/checks/check_data_loading.py",
    "ai-services/demand-insight/src/data/data_cleaner.py",
    "ai-services/demand-insight/checks/check_data_cleaning.py",
    "ai-services/demand-insight/src/pipelines/first_data_pipeline.py",
    "ai-services/demand-insight/checks/check_first_data_pipeline.py",
    "data/processed/demand-insight/sales_pipeline_ready.csv",
    "reports/summaries/demand-insight/first_data_pipeline_summary.md",
]


def write_week_close_summary(missing_paths: list[str], raw_csv_count: int) -> None:
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "week_01_close_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    status = "Completed" if not missing_paths and raw_csv_count > 0 else "Needs review"
    missing_text = "None" if not missing_paths else "\n".join(f"- {path}" for path in missing_paths)

    content = f"""# Week 1 Close Summary â€” Demand Insight Module

## Sprint

Sprint 1 â€” Demand Insight Module

## Day

Day 7 â€” Week 1 Close

## Week 1 focus

```txt
project base
â†’ dataset setup
â†’ data loading
â†’ data cleaning
â†’ first data pipeline
â†’ documentation close
```

## Evidence status

| Evidence | Status |
| -------- | ------ |
| Raw CSV files found | {raw_csv_count} |
| Missing required paths | {len(missing_paths)} |
| Week close status | {status} |

## Missing paths

{missing_text}

## Interpretation

Week 1 closes the foundation of the Demand Insight Module.

The project is ready to move toward feature engineering, baseline, metrics and insight generation only after the missing path count is zero.

## Status

```txt
{status}
```
"""

    summary_path.write_text(content, encoding="utf-8")


def main() -> None:
    raw_dir = PROJECT_ROOT / "data" / "raw" / "demand-insight"
    raw_csv_count = len(list(raw_dir.glob("*.csv"))) if raw_dir.exists() else 0

    missing_paths = [path for path in REQUIRED_PATHS if not (PROJECT_ROOT / path).exists()]
    write_week_close_summary(missing_paths=missing_paths, raw_csv_count=raw_csv_count)

    if raw_csv_count == 0:
        raise AssertionError("No raw CSV files found in data/raw/demand-insight.")

    if missing_paths:
        raise AssertionError(f"Missing required Week 1 evidence: {missing_paths}")

    print("OK - Day 7 week 1 close check passed")
    print("Summary: reports/summaries/demand-insight/week_01_close_summary.md")


if __name__ == "__main__":
    main()
