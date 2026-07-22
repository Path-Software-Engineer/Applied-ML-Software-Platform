"""Readable Day 121 validation for replenishment policy 1.0."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "inventory-decision" / "src"
sys.path.insert(0, str(MODULE_SRC))

from inventory_decision.policies import run_replenishment_policy  # noqa: E402


def main() -> None:
    decisions = run_replenishment_policy(PROJECT_ROOT)
    indexed = decisions.set_index("product_id")

    assert len(decisions) == 6
    assert set(decisions["policy_version"]) == {"inventory-review-policy/1.0"}
    assert set(decisions["lead_time_source"]) == {"policy_default"}
    assert indexed.loc["P003", "reorder_point_units"] == 35
    assert indexed.loc["P003", "target_stock_units"] == 70
    assert indexed.loc["P003", "suggested_quantity_units"] == 70
    assert indexed.loc["P002", "suggested_quantity_units"] == 27
    assert (decisions["suggested_quantity_units"] >= 0).all()
    assert decisions["reorder_required"].sum() == 2

    print("OK - Sprint 3 Day 121 replenishment policy check passed")
    print("Policy: inventory-review-policy/1.0")
    print("Products requiring review: 2 / 6")
    print("Bread reorder / target / suggested: 35 / 70 / 70 units")
    print("Negative suggested quantities: 0")


if __name__ == "__main__":
    main()
