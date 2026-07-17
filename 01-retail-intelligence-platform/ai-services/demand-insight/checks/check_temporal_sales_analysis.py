"""Manual end-to-end check for the Day 18 temporal sales artifact."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.analysis.temporal_sales_analysis import (  # noqa: E402
    INPUT_PATH,
    OUTPUT_PATH,
    build_temporal_results,
    load_sales_data,
)


def main() -> None:
    if not OUTPUT_PATH.exists():
        raise AssertionError(
            f"Output file does not exist: {OUTPUT_PATH}. "
            "Run temporal_sales_analysis.py first."
        )

    sales_df = load_sales_data(INPUT_PATH)
    daily_summary = pd.read_csv(OUTPUT_PATH, parse_dates=["date"])

    if len(daily_summary) != sales_df["date"].nunique():
        raise AssertionError("Daily summary must contain one row per date.")
    if daily_summary["date"].duplicated().any():
        raise AssertionError("Daily summary contains duplicated dates.")
    if not daily_summary["date"].is_monotonic_increasing:
        raise AssertionError("Daily summary is not ordered chronologically.")

    total_units = int(daily_summary["total_units_sold"].sum())
    total_revenue = round(float(daily_summary["total_revenue"].sum()), 2)
    if total_units != 293:
        raise AssertionError(f"Expected 293 units, found {total_units}.")
    if total_revenue != 747.65:
        raise AssertionError(f"Expected 747.65 revenue, found {total_revenue:.2f}.")

    results = build_temporal_results(daily_summary)
    if (results["top_units_date"], results["top_units_sold"]) != (
        "2026-01-06",
        45,
    ):
        raise AssertionError("Unexpected leading date or value by units sold.")
    if (results["top_revenue_date"], results["top_revenue"]) != (
        "2026-01-08",
        99.30,
    ):
        raise AssertionError("Unexpected leading date or value by revenue.")

    print("OK - Day 18 temporal sales analysis check passed")
    print(f"Artifact: {OUTPUT_PATH}")
    print(f"Rows / unique dates: {len(daily_summary)} / {sales_df['date'].nunique()}")
    print("Duplicated dates: 0")
    print("Chronological order: confirmed")
    print(f"Total units preserved: {total_units}")
    print(f"Total revenue preserved: {total_revenue:.2f}")
    print(
        "Leader by units: "
        f"{results['top_units_date']} ({results['top_units_sold']} units, "
        f"{results['top_units_share']:.2f}%)"
    )
    print(
        "Leader by revenue: "
        f"{results['top_revenue_date']} ({results['top_revenue']:.2f}, "
        f"{results['top_revenue_share']:.2f}%)"
    )


if __name__ == "__main__":
    main()
