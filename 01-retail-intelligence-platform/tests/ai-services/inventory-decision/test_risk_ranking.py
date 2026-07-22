"""Tests for stable inventory labels and priority ranking."""

from __future__ import annotations

import pandas as pd
import pytest

from inventory_decision.risk import RiskInputError, classify_risk, rank_inventory_risk


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (100.0, ("critical", "replenish_now")),
        (75.0, ("critical", "replenish_now")),
        (74.9, ("high", "replenish_soon")),
        (50.0, ("high", "replenish_soon")),
        (25.0, ("watch", "review")),
        (24.9, ("healthy", "monitor")),
    ],
)
def test_risk_thresholds_are_inclusive(score: float, expected: tuple[str, str]) -> None:
    assert classify_risk(score) == expected


def rows() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "product_id": ["P002", "P001", "P003"],
            "product_name": ["Milk", "Rice", "Bread"],
            "current_stock_units": [9, 29, 0],
            "coverage_days": [1.5, 4.1429, 0.0],
            "risk_score": [50.0, 0.0, 100.0],
            "reorder_required": [True, False, True],
            "lead_time_days": [2, 2, 2],
            "safety_days": [1, 1, 1],
        }
    )


def test_ranking_orders_score_then_coverage_then_product() -> None:
    ranked = rank_inventory_risk(rows())

    assert ranked["product_id"].tolist() == ["P003", "P002", "P001"]
    assert ranked["priority_rank"].tolist() == [1, 2, 3]
    assert ranked["risk_label"].tolist() == ["critical", "high", "healthy"]


def test_ranking_preserves_a_reason() -> None:
    ranked = rank_inventory_risk(rows()).set_index("product_id")

    assert "stock is zero" in ranked.loc["P003", "reason"]
    assert "1.50 days" in ranked.loc["P002", "reason"]
    assert "above the policy reorder point" in ranked.loc["P001", "reason"]


def test_ranking_rejects_duplicate_products() -> None:
    duplicate = pd.concat([rows(), rows().iloc[[0]]], ignore_index=True)

    with pytest.raises(RiskInputError, match="unique product_id"):
        rank_inventory_risk(duplicate)
