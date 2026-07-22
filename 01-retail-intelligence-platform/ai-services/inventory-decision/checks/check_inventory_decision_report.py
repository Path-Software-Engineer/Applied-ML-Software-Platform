"""Readable Day 125 validation for the canonical decision report."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "inventory-decision" / "src"
sys.path.insert(0, str(MODULE_SRC))

from inventory_decision.reporting import run_inventory_decision_report  # noqa: E402


def main() -> None:
    report = run_inventory_decision_report(PROJECT_ROOT)
    output_root = PROJECT_ROOT / "reports" / "outputs" / "inventory-decision"
    persisted = json.loads(
        (output_root / "inventory_decision_report.json").read_text(encoding="utf-8")
    )
    first_bytes = (output_root / "inventory_decision_report.json").read_bytes()
    run_inventory_decision_report(PROJECT_ROOT)

    assert persisted == report
    assert (output_root / "inventory_decision_report.json").read_bytes() == first_bytes
    assert report["summary"] == {
        "products": 6,
        "stock_on_hand_units": 99,
        "products_requiring_replenishment_review": 2,
        "critical_products": 1,
        "high_risk_products": 1,
        "watch_products": 0,
        "healthy_products": 4,
        "suggested_review_quantity_units": 97,
    }
    assert len(report["ranking"]) == len(report["recommendation_cards"]) == 6
    assert report["limitations"]

    print("OK - Sprint 3 Day 125 inventory decision report check passed")
    print("Products / review queue: 6 / 2")
    print("Critical / high / healthy: 1 / 1 / 4")
    print("Suggested review quantity: 97 units")
    print("Canonical JSON: byte-reproducible")


if __name__ == "__main__":
    main()
