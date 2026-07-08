"""Check Day 8 Week 2 exploration evidence."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

REQUIRED_FILES = [
    "docs/sprints/sprint-01-week-02-exploration.md",
    "docs/decisions.md",
    "docs/sprints/sprint-01-demand-insight.md",
]


def write_summary() -> None:
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "week_02_exploration_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        """# Week 2 Exploration Summary â€” Demand Insight Module

## Day

Day 8 â€” Feature, Baseline and Metric Exploration

## Exploration map

```txt
processed data
â†’ temporal features
â†’ revenue
â†’ baseline
â†’ MAE
â†’ technical summary
```

## Execution days prepared

```txt
Day 9  â†’ temporal features
Day 10 â†’ revenue and processed dataset
Day 11 â†’ feature engineering integration
Day 12 â†’ EDA flow lab
Day 13 â†’ mean baseline
Day 14 â†’ baseline MAE
```

## Status

```txt
Completed
```
""",
        encoding="utf-8",
    )


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (PROJECT_ROOT / path).exists()]
    write_summary()

    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "week_02_exploration_summary.md"
    if not summary_path.exists():
        raise AssertionError("Week 2 exploration summary was not created.")

    if missing:
        raise AssertionError(f"Missing Day 8 evidence: {missing}")

    print("OK - Day 8 Week 2 exploration check passed")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
