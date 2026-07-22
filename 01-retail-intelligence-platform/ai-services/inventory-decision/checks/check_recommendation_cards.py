"""Readable Day 124 validation for Inventory Recommendation Cards."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "inventory-decision" / "src"
sys.path.insert(0, str(MODULE_SRC))

from inventory_decision.recommendations import run_recommendation_cards  # noqa: E402


def main() -> None:
    payload = run_recommendation_cards(PROJECT_ROOT)
    output_root = (
        PROJECT_ROOT / "reports" / "recommendation-cards" / "inventory-decision"
    )
    persisted = json.loads(
        (output_root / "recommendation_cards.json").read_text(encoding="utf-8")
    )
    markdown = (output_root / "recommendation_cards.md").read_text(encoding="utf-8")

    assert payload == persisted
    assert len(payload["cards"]) == 6
    assert len({card["card_id"] for card in payload["cards"]}) == 6
    assert payload["cards"][0]["product"]["product_id"] == "P003"
    assert payload["cards"][0]["action"]["suggested_quantity_units"] == 70
    assert all(card["reason"] and card["limitation"] for card in payload["cards"])
    assert "suggested review quantity" in markdown

    print("OK - Sprint 3 Day 124 Recommendation Cards check passed")
    print("Cards / unique IDs: 6 / 6")
    print("Top action: Bread / replenish now / 70 suggested units")
    print("Reason and limitation: present on every card")


if __name__ == "__main__":
    main()
