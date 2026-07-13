"""Validate existing Week 2 exploration documentation."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
REQUIRED = [
    "docs/sprints/sprint-01-demand-insight/week-02/exploration.md",
    "docs/decisions.md",
    "docs/sprints/sprint-01-demand-insight/README.md",
    "reports/summaries/demand-insight/week_02_exploration_summary.md",
]


def main() -> None:
    missing = [path for path in REQUIRED if not (PROJECT_ROOT / path).exists()]
    if missing:
        raise AssertionError(f"Missing Week 2 exploration evidence: {missing}")
    print(f"OK - Week 2 exploration: {len(REQUIRED)} evidence files")


if __name__ == "__main__":
    main()
