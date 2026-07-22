"""Tests for coverage and non-probabilistic inventory risk scoring."""

from __future__ import annotations

import pytest

from inventory_decision.risk import RiskInputError, calculate_risk


def calculate(**overrides: object):
    values = {
        "stock_on_hand": 9,
        "observed_units": 54,
        "observation_days": 9,
        "lead_time_days": 2,
        "safety_days": 1,
        "reorder_point_units": 18,
        "reorder_required": True,
    }
    values.update(overrides)
    return calculate_risk(**values)


def test_low_stock_combines_shortage_and_coverage_pressure() -> None:
    result = calculate()

    assert result.coverage_days == 1.5
    assert result.shortage_ratio == 0.5
    assert result.coverage_pressure == 0.5
    assert result.risk_score == 50.0
    assert result.risk_score_meaning == "priority_index_not_probability"


def test_stockout_with_demand_has_maximum_priority() -> None:
    result = calculate(
        stock_on_hand=0,
        observed_units=105,
        reorder_point_units=35,
    )

    assert result.coverage_days == 0.0
    assert result.risk_score == 100.0


def test_reorder_boundary_has_watch_floor() -> None:
    result = calculate(stock_on_hand=18)

    assert result.coverage_days == 3.0
    assert result.risk_score == 25.0


def test_sufficient_stock_has_zero_priority() -> None:
    result = calculate(
        stock_on_hand=29,
        observed_units=63,
        reorder_point_units=21,
        reorder_required=False,
    )

    assert result.coverage_days == 4.1429
    assert result.risk_score == 0.0


def test_zero_observed_demand_has_no_finite_coverage() -> None:
    result = calculate(
        stock_on_hand=0,
        observed_units=0,
        reorder_point_units=0,
        reorder_required=False,
    )

    assert result.coverage_days is None
    assert result.risk_score == 0.0


def test_risk_rejects_negative_stock() -> None:
    with pytest.raises(RiskInputError, match="non-negative"):
        calculate(stock_on_hand=-1)
