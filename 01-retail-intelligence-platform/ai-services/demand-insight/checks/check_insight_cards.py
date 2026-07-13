"""Manual end-to-end check for the Day 19 Demand Insight Cards."""

from __future__ import annotations

import json
import sys
from pathlib import Path

MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.insights.insight_cards import (  # noqa: E402
    EXPECTED_CARD_IDS,
    JSON_OUTPUT_PATH,
    MARKDOWN_OUTPUT_PATH,
    build_insight_cards,
    load_artifacts,
)

REQUIRED_FIELDS = {
    "card_id",
    "title",
    "metric",
    "insight",
    "recommendation",
    "limitation",
}


def main() -> None:
    missing_outputs = [
        str(path)
        for path in (JSON_OUTPUT_PATH, MARKDOWN_OUTPUT_PATH)
        if not path.exists()
    ]
    if missing_outputs:
        raise AssertionError(
            "Missing Insight Card outputs. Run insight_cards.py first: "
            f"{missing_outputs}"
        )

    expected_cards = build_insight_cards(load_artifacts())
    actual_cards = json.loads(JSON_OUTPUT_PATH.read_text(encoding="utf-8"))
    markdown = MARKDOWN_OUTPUT_PATH.read_text(encoding="utf-8")

    if actual_cards != expected_cards:
        raise AssertionError(
            "Stored JSON cards do not match the validated source artifacts."
        )

    actual_ids = [card.get("card_id") for card in actual_cards]
    if len(actual_ids) != len(set(actual_ids)):
        raise AssertionError("Insight Card IDs must be unique.")
    if set(actual_ids) != EXPECTED_CARD_IDS:
        raise AssertionError("Stored Insight Card IDs violate the contract.")

    for card in actual_cards:
        if set(card) != REQUIRED_FIELDS:
            raise AssertionError(
                f"Card {card.get('card_id')} has an invalid field contract."
            )
        if not all(isinstance(card[field], str) and card[field].strip() for field in REQUIRED_FIELDS):
            raise AssertionError(
                f"Card {card['card_id']} contains an empty or non-text field."
            )
        if "no predice demanda futura" not in card["limitation"]:
            raise AssertionError(
                f"Card {card['card_id']} does not state the temporal limitation."
            )
        if card["title"] not in markdown or card["metric"] not in markdown:
            raise AssertionError(
                f"Markdown evidence is missing card {card['card_id']}."
            )

    cards_by_id = {card["card_id"]: card for card in actual_cards}
    expected_metrics = {
        "observed-demand": "293 unidades | 747.65 de revenue",
        "top-product-units": "Bread — 105 unidades",
        "top-product-revenue": "Rice 1kg — 220.50",
        "top-day-units": "2026-01-06 — 45 unidades",
        "top-day-revenue": "2026-01-08 — 99.30",
    }

    for card_id, expected_metric in expected_metrics.items():
        if cards_by_id[card_id]["metric"] != expected_metric:
            raise AssertionError(
                f"Unexpected metric for {card_id}: "
                f"{cards_by_id[card_id]['metric']}"
            )

    print("OK - Day 19 Demand Insight Cards check passed")
    print(f"Cards: {len(actual_cards)}")
    print(f"Unique card IDs: {len(set(actual_ids))}")
    print("Field contract: confirmed")
    print("Temporal limitations: confirmed")
    print(f"JSON: {JSON_OUTPUT_PATH}")
    print(f"Markdown: {MARKDOWN_OUTPUT_PATH}")
    for card in actual_cards:
        print(f"{card['card_id']}: {card['metric']}")


if __name__ == "__main__":
    main()