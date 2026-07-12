"""Validate existing Week 1 closure evidence without generating reports."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
REQUIRED_PATHS = [
    "docs/architecture.md",
    "docs/decisions.md",
    "ai-services/demand-insight/src/data/data_loader.py",
    "ai-services/demand-insight/src/data/data_cleaner.py",
    "ai-services/demand-insight/src/pipelines/first_data_pipeline.py",
    "data/processed/demand-insight/sales_pipeline_ready.csv",
    "reports/summaries/demand-insight/first_data_pipeline_summary.md",
    "reports/summaries/demand-insight/week_01_close_summary.md",
]


def main() -> None:
    missing = [path for path in REQUIRED_PATHS if not (PROJECT_ROOT / path).exists()]
    raw_count = len(list((PROJECT_ROOT / "data/raw/demand-insight").glob("*.csv")))
    if raw_count == 0 or missing:
        raise AssertionError(f"Incomplete Week 1 evidence: raw={raw_count}, missing={missing}")
    print(f"OK - Week 1 close: {raw_count} raw CSV, {len(REQUIRED_PATHS)} evidence files")


if __name__ == "__main__":
    main()
