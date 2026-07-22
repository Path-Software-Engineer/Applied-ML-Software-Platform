"""Readable Day 118 validation for factual snapshot evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "inventory-decision" / "src"
sys.path.insert(0, str(MODULE_SRC))

from inventory_decision.reporting import run_snapshot_summary  # noqa: E402


def main() -> None:
    summary = run_snapshot_summary(PROJECT_ROOT)
    output_root = PROJECT_ROOT / "reports" / "summaries" / "inventory-decision"
    persisted = json.loads(
        (output_root / "inventory_snapshot_summary.json").read_text(encoding="utf-8")
    )
    markdown = (output_root / "inventory_snapshot_summary.md").read_text(
        encoding="utf-8"
    )

    assert persisted == summary
    assert summary["snapshot"]["products"] == 6
    assert summary["snapshot"]["stock_on_hand_units"] == 99
    assert summary["snapshot"]["zero_stock_products"] == 1
    assert summary["snapshot"]["products_missing_source_lead_time"] == 6
    assert summary["coverage"]["unmatched_products"] == 0
    assert summary["decision_status"] == "not_calculated"
    assert "Reorder points" in markdown

    print("OK - Sprint 3 Day 118 snapshot summary check passed")
    print("Products / stock: 6 / 99 units")
    print("Zero stock / missing source lead time: 1 / 6")
    print("Decision status: not calculated")


if __name__ == "__main__":
    main()
