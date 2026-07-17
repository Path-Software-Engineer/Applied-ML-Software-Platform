"""Manual end-to-end check for the Day 23 Demand Summary service."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.api.app.services.demand_summary_service import (  # noqa: E402
    DemandSummaryService,
)


def main() -> None:
    service = DemandSummaryService(PROJECT_ROOT)
    summary = service.get_summary()
    output_path = service.save_summary(summary)

    expected = {
        "schema_version": "1.0",
        "total_units_sold": 293,
        "total_revenue": 747.65,
        "baseline": 16.28,
        "mae": 5.42,
        "product_units": ("Bread", 105),
        "product_revenue": ("Rice 1kg", 220.50),
        "date_units": ("2026-01-06", 45),
        "date_revenue": ("2026-01-08", 99.30),
    }
    actual = {
        "schema_version": summary["schema_version"],
        "total_units_sold": summary["sales_summary"]["total_units_sold"],
        "total_revenue": summary["sales_summary"]["total_revenue"],
        "baseline": summary["baseline"]["mean_units_prediction"],
        "mae": summary["baseline"]["mae"],
        "product_units": (
            summary["leaders"]["product_by_units"]["name"],
            summary["leaders"]["product_by_units"]["value"],
        ),
        "product_revenue": (
            summary["leaders"]["product_by_revenue"]["name"],
            summary["leaders"]["product_by_revenue"]["value"],
        ),
        "date_units": (
            summary["leaders"]["date_by_units"]["name"],
            summary["leaders"]["date_by_units"]["value"],
        ),
        "date_revenue": (
            summary["leaders"]["date_by_revenue"]["name"],
            summary["leaders"]["date_by_revenue"]["value"],
        ),
    }
    if actual != expected:
        raise AssertionError(f"Unexpected Demand Summary: {actual}")

    stored = json.loads(output_path.read_text(encoding="utf-8"))
    if stored != summary:
        raise AssertionError("Stored Demand Summary differs from service response.")
    if len(summary["insight_cards"]) != 5:
        raise AssertionError("Demand Summary must expose five Insight Cards.")

    print("OK - Day 23 Demand Summary service check passed")
    print(f"Schema version: {summary['schema_version']}")
    print(f"Observed period: {summary['period']['start_date']} to {summary['period']['end_date']}")
    print("Totals: 293 units | 747.65 revenue")
    print("Baseline / MAE: 16.28 / 5.42")
    print(f"Insight Cards: {len(summary['insight_cards'])}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
