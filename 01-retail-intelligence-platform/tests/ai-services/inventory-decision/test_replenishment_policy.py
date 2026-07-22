"""Tests for pure reorder and target-stock calculations."""

from __future__ import annotations

import pytest

from inventory_decision.policies import PolicyError, calculate_replenishment


def test_policy_uses_exact_ratio_and_explicit_default() -> None:
    result = calculate_replenishment(
        stock_on_hand=0,
        observed_units=105,
        observation_days=9,
        source_lead_time_days=None,
    )

    assert result.lead_time_days == 2
    assert result.lead_time_source == "policy_default"
    assert result.reorder_point_units == 35
    assert result.target_stock_units == 70
    assert result.suggested_quantity_units == 70


def test_stock_equal_to_reorder_point_triggers_review() -> None:
    result = calculate_replenishment(
        stock_on_hand=18,
        observed_units=54,
        observation_days=9,
        source_lead_time_days=None,
    )

    assert result.reorder_point_units == 18
    assert result.reorder_required is True
    assert result.suggested_quantity_units == 18


def test_sufficient_stock_has_zero_suggested_quantity() -> None:
    result = calculate_replenishment(
        stock_on_hand=29,
        observed_units=63,
        observation_days=9,
        source_lead_time_days=None,
    )

    assert result.reorder_point_units == 21
    assert result.reorder_required is False
    assert result.suggested_quantity_units == 0


def test_zero_demand_never_creates_replenishment() -> None:
    result = calculate_replenishment(
        stock_on_hand=0,
        observed_units=0,
        observation_days=9,
        source_lead_time_days=4,
    )

    assert result.reorder_point_units == 0
    assert result.target_stock_units == 0
    assert result.reorder_required is False
    assert result.suggested_quantity_units == 0
    assert result.lead_time_source == "source"


@pytest.mark.parametrize(
    "values",
    [
        {"stock_on_hand": -1, "observed_units": 1, "observation_days": 1},
        {"stock_on_hand": 1, "observed_units": -1, "observation_days": 1},
        {"stock_on_hand": 1, "observed_units": 1, "observation_days": 0},
    ],
)
def test_policy_rejects_invalid_quantities(values: dict[str, int]) -> None:
    with pytest.raises(PolicyError):
        calculate_replenishment(source_lead_time_days=None, **values)
