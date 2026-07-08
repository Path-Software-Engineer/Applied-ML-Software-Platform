"""Check Day 6 first data pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.pipelines.first_data_pipeline import (  # noqa: E402
    REQUIRED_COLUMNS,
    build_pipeline_ready_dataset,
    find_raw_sales_file,
)


def main() -> None:
    raw_data_path = find_raw_sales_file(PROJECT_ROOT)
    output_path = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_pipeline_ready.csv"
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "first_data_pipeline_summary.md"

    pipeline_ready = build_pipeline_ready_dataset(
        raw_data_path=raw_data_path,
        output_path=output_path,
        summary_path=summary_path,
    )

    if pipeline_ready.empty:
        raise AssertionError("Pipeline-ready dataset is empty.")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in pipeline_ready.columns]
    if missing_columns:
        raise AssertionError(f"Missing required columns in pipeline output: {missing_columns}")

    if not output_path.exists():
        raise AssertionError(f"Expected output file was not created: {output_path}")

    if not summary_path.exists():
        raise AssertionError(f"Expected summary file was not created: {summary_path}")

    print("OK - Day 6 first data pipeline check passed")
    print(f"Raw data: {raw_data_path}")
    print(f"Output: {output_path}")
    print(f"Summary: {summary_path}")
    print(f"Rows: {len(pipeline_ready)}")
    print(f"Columns: {len(pipeline_ready.columns)}")


if __name__ == "__main__":
    main()
