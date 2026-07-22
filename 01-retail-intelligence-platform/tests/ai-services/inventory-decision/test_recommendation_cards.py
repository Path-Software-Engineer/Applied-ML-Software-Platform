"""Tests for the Inventory Recommendation Card contract."""

from __future__ import annotations

import pandas as pd
import pytest

from inventory_decision.recommendations.cards import (
    LIMITATION,
    build_recommendation_cards,
    render_recommendation_cards,
)


def ranked() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "priority_rank": 1,
                "product_id": "P003",
                "product_name": "Bread",
                "risk_label": "critical",
                "risk_score": 100.0,
                "risk_score_meaning": "priority_index_not_probability",
                "current_stock_units": 0,
                "observed_daily_demand": 11.666667,
                "demand_signal_type": "observed_daily_average",
                "coverage_days": 0.0,
                "reorder_point_units": 35,
                "target_stock_units": 70,
                "lead_time_days": 2,
                "lead_time_source": "policy_default",
                "period_start": "2026-01-01",
                "period_end": "2026-01-09",
                "snapshot_as_of_date": "2026-01-09",
                "recommended_action": "replenish_now",
                "suggested_quantity_units": 70,
                "reason": "Observed stock is zero while observed demand is positive.",
                "policy_version": "inventory-review-policy/1.0",
            }
        ]
    )


def test_card_preserves_policy_evidence_and_limitation() -> None:
    payload = build_recommendation_cards(ranked())
    card = payload["cards"][0]

    assert payload["schema_version"] == "1.0"
    assert card["card_id"] == "inventory-P003"
    assert card["risk"]["meaning"] == "priority_index_not_probability"
    assert card["action"]["suggested_quantity_units"] == 70
    assert card["limitation"] == LIMITATION


def test_markdown_uses_review_language() -> None:
    markdown = render_recommendation_cards(build_recommendation_cards(ranked()))

    assert "suggested review quantity" in markdown
    assert "priority index" in markdown
    assert "Limitation" in markdown


def test_cards_reject_duplicate_product_identity() -> None:
    duplicated = pd.concat([ranked(), ranked()], ignore_index=True)

    with pytest.raises(ValueError, match="unique product rows"):
        build_recommendation_cards(duplicated)
