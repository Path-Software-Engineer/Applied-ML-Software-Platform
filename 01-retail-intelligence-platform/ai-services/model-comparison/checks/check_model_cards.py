"""Readable Day 68 check for candidate Model Cards."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "model-comparison" / "src"
sys.path.insert(0, str(MODULE_SRC))

from model_comparison.model_cards import run_model_cards  # noqa: E402


def main() -> None:
    """Regenerate and validate official Model Card evidence."""
    cards = run_model_cards(PROJECT_ROOT)
    card_root = PROJECT_ROOT / "reports" / "model-cards" / "model-comparison"
    payload = json.loads(
        (card_root / "model_cards.json").read_text(encoding="utf-8")
    )
    markdown_cards = [
        card_root / f"{card['model_id']}.md" for card in cards
    ]

    assert len(cards) == 4
    assert payload["card_count"] == 4
    assert len({card["model_id"] for card in cards}) == 4
    assert all(card["production_status"] == "not_production_ready" for card in cards)
    assert all(len(card["limitations"]) >= 6 for card in cards)
    assert all(len(card["evidence"]) == 5 for card in cards)
    assert all(path.is_file() and path.stat().st_size > 0 for path in markdown_cards)
    roles = {card["model_id"]: card["decision_role"] for card in cards}
    assert roles["random_forest"] == "selected_for_next_integration"
    assert roles["gradient_boosting"] == "measurement_leader_not_selected"

    print("OK - Sprint 2 Day 68 Model Cards check passed")
    print("Model Cards: 4")
    print("Selected role: Random Forest")
    print("Measurement-leader role: Gradient Boosting")
    print("Production status: not production ready")
    print("Day 69 report: not started")


if __name__ == "__main__":
    main()
