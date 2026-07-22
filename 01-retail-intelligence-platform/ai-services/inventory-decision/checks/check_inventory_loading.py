"""Readable Day 115 validation for inventory loading."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "inventory-decision" / "src"
sys.path.insert(0, str(MODULE_SRC))

from inventory_decision.data.loader import load_inventory_snapshot  # noqa: E402


def main() -> None:
    source = PROJECT_ROOT / "data" / "raw" / "inventory" / "inventory_snapshot.csv"
    snapshot = load_inventory_snapshot(source)

    assert snapshot["product_id"].tolist() == [f"P{index:03d}" for index in range(1, 7)]
    assert snapshot["snapshot_id"].nunique() == 1
    assert snapshot["stock_on_hand"].min() == 0
    assert snapshot["stock_on_hand"].sum() == 99

    print("OK - Sprint 3 Day 115 inventory loading check passed")
    print(f"Rows / unique products: {len(snapshot)} / {snapshot['product_id'].nunique()}")
    print(f"Observed stock total: {snapshot['stock_on_hand'].sum()} units")
    print("Decision policy applied: no")


if __name__ == "__main__":
    main()
