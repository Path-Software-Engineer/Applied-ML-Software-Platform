"""Validate the complete Week 3 evidence without duplicating production logic."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

REQUIRED_PATHS = (
    "ai-services/demand-insight/src/analysis/sales_summary.py",
    "ai-services/demand-insight/src/analysis/product_ranking.py",
    "ai-services/demand-insight/src/analysis/temporal_sales_analysis.py",
    "ai-services/demand-insight/src/insights/insight_cards.py",
    "ai-services/demand-insight/src/visualization/sales_visual_report.py",
    "data/processed/demand-insight/sales_summary.csv",
    "data/processed/demand-insight/product_summary.csv",
    "data/processed/demand-insight/daily_sales_summary.csv",
    "reports/insight-cards/demand_insight_cards.json",
    "reports/insight-cards/demand_insight_cards.md",
    "reports/outputs/demand-insight/sales_visual_report.md",
    "reports/summaries/demand-insight/week_03_close_summary.md",
    "docs/sprints/sprint-01-demand-insight/week-03/review.md",
)

FIGURE_PATHS = (
    "reports/figures/demand-insight/daily_sales.png",
    "reports/figures/demand-insight/product_units_ranking.png",
    "reports/figures/demand-insight/product_revenue_ranking.png",
)

EXPECTED_CARD_IDS = {
    "observed-demand",
    "top-product-units",
    "top-product-revenue",
    "top-day-units",
    "top-day-revenue",
}


def main() -> None:
    missing = [path for path in REQUIRED_PATHS if not (PROJECT_ROOT / path).is_file()]
    if missing:
        raise AssertionError(f"Incomplete Week 3 evidence: {missing}")

    invalid_figures = []
    for relative_path in FIGURE_PATHS:
        path = PROJECT_ROOT / relative_path
        if not path.is_file() or not path.read_bytes().startswith(PNG_SIGNATURE):
            invalid_figures.append(relative_path)
    if invalid_figures:
        raise AssertionError(f"Missing or invalid Week 3 figures: {invalid_figures}")

    cards_path = PROJECT_ROOT / "reports/insight-cards/demand_insight_cards.json"
    cards = json.loads(cards_path.read_text(encoding="utf-8"))
    card_ids = {card.get("card_id") for card in cards}
    if len(cards) != 5 or card_ids != EXPECTED_CARD_IDS:
        raise AssertionError(
            f"Unexpected Insight Card contract: count={len(cards)}, ids={card_ids}"
        )

    required_fields = {
        "card_id", "title", "metric", "insight", "recommendation", "limitation"
    }
    invalid_cards = [
        card.get("card_id", "<missing>")
        for card in cards
        if set(card) != required_fields or not all(card.values())
    ]
    if invalid_cards:
        raise AssertionError(f"Invalid Insight Cards: {invalid_cards}")

    review_path = (
        PROJECT_ROOT
        / "docs/sprints/sprint-01-demand-insight/week-03/review.md"
    )
    review = review_path.read_text(encoding="utf-8")
    required_review_statements = (
        "Completed through Day 21",
        "Week 3 is closed",
        "30 passing tests",
    )
    missing_statements = [
        statement for statement in required_review_statements if statement not in review
    ]
    if missing_statements:
        raise AssertionError(
            f"Week 3 review is not closed consistently: {missing_statements}"
        )

    print("OK - Sprint 1 Week 3 closure check passed")
    print(f"Evidence files: {len(REQUIRED_PATHS)}")
    print(f"Insight Cards: {len(cards)}")
    print(f"PNG figures: {len(FIGURE_PATHS)}")
    print("Automated suite baseline: 30 passing tests")
    print("Week 3 status: closed")


if __name__ == "__main__":
    main()
