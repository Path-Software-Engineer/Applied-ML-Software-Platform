"""Readable Day 128 validation for the Inventory Decision read service."""

from __future__ import annotations

from datetime import date
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.api.app.services.inventory_decision_service import (  # noqa: E402
    InventoryDecisionService,
)


def main() -> None:
    resource = InventoryDecisionService(PROJECT_ROOT).get_summary(
        today=date(2026, 7, 22)
    )

    assert resource["schema_version"] == "1.0"
    assert resource["summary"]["products"] == 6
    assert resource["summary"]["products_requiring_replenishment_review"] == 2
    assert resource["freshness"]["status"] == "stale"
    assert len(resource["ranking"]) == len(resource["recommendation_cards"]) == 6

    print("OK - Sprint 3 Day 128 Inventory Decision service check passed")
    print("Schema / products / cards: 1.0 / 6 / 6")
    print(f"Freshness: stale at {resource['freshness']['age_days']} days")
    print("HTTP route: not implemented on Day 128")


if __name__ == "__main__":
    main()
