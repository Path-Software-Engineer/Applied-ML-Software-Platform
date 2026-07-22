"""End-to-end pure-policy scenarios for the Week 12 decision oracles."""

from __future__ import annotations

import pytest

from inventory_decision.policies import calculate_replenishment
from inventory_decision.risk import calculate_risk, classify_risk


SCENARIOS = (
    ("sufficient_stock", 50, 90, 30, 60, 0, 0.0, "healthy", "monitor"),
    ("low_stock", 15, 90, 30, 60, 45, 50.0, "high", "replenish_soon"),
    ("stockout", 0, 90, 30, 60, 60, 100.0, "critical", "replenish_now"),
    ("zero_demand", 0, 0, 0, 0, 0, 0.0, "healthy", "monitor"),
    ("high_demand", 20, 180, 60, 120, 100, 66.7, "high", "replenish_soon"),
)


@pytest.mark.parametrize(
    (
        "scenario",
        "stock",
        "observed_units",
        "expected_reorder",
        "expected_target",
        "expected_suggested",
        "expected_score",
        "expected_label",
        "expected_action",
    ),
    SCENARIOS,
)
def test_inventory_scenario_oracles(
    scenario: str,
    stock: int,
    observed_units: int,
    expected_reorder: int,
    expected_target: int,
    expected_suggested: int,
    expected_score: float,
    expected_label: str,
    expected_action: str,
) -> None:
    replenishment = calculate_replenishment(
        stock_on_hand=stock,
        observed_units=observed_units,
        observation_days=9,
        source_lead_time_days=None,
    )
    risk = calculate_risk(
        stock_on_hand=stock,
        observed_units=observed_units,
        observation_days=9,
        lead_time_days=replenishment.lead_time_days,
        safety_days=1,
        reorder_point_units=replenishment.reorder_point_units,
        reorder_required=replenishment.reorder_required,
    )
    label, action = classify_risk(risk.risk_score)

    assert replenishment.reorder_point_units == expected_reorder, scenario
    assert replenishment.target_stock_units == expected_target, scenario
    assert replenishment.suggested_quantity_units == expected_suggested, scenario
    assert risk.risk_score == expected_score, scenario
    assert risk.risk_score_meaning == "priority_index_not_probability"
    assert (label, action) == (expected_label, expected_action), scenario
