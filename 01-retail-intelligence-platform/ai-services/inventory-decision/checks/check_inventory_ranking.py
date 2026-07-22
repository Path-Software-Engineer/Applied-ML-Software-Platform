"""Readable Day 123 validation for labels and deterministic ranking."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "inventory-decision" / "src"
sys.path.insert(0, str(MODULE_SRC))

from inventory_decision.risk import run_risk_ranking  # noqa: E402


def main() -> None:
    ranking = run_risk_ranking(PROJECT_ROOT)

    assert ranking["product_id"].iloc[:2].tolist() == ["P003", "P002"]
    assert ranking["risk_label"].iloc[:2].tolist() == ["critical", "high"]
    assert ranking["recommended_action"].iloc[:2].tolist() == [
        "replenish_now",
        "replenish_soon",
    ]
    assert ranking["priority_rank"].tolist() == list(range(1, 7))
    assert ranking["reason"].str.len().gt(0).all()

    print("OK - Sprint 3 Day 123 inventory ranking check passed")
    print("Priority 1: Bread / critical / replenish now")
    print("Priority 2: Milk 1L / high / replenish soon")
    print("Tie-break: score desc, coverage asc, product_id asc")


if __name__ == "__main__":
    main()
