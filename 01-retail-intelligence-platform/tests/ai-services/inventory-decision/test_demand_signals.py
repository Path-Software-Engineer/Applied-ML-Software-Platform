"""Tests for observed-demand signals and strict inventory joins."""

from __future__ import annotations

import pandas as pd
import pytest

from inventory_decision.signals import (
    DemandSignalError,
    build_observed_demand_signals,
    join_inventory_and_signals,
)


def sales() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": ["2026-01-01", "2026-01-03", "2026-01-03"],
            "product_id": ["P001", "P001", "P002"],
            "product_name": ["Rice", "Rice", "Milk"],
            "units_sold": [3, 6, 9],
        }
    )


def inventory() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "product_id": ["P001", "P002"],
            "product_name": ["Rice", "Milk"],
            "stock_unit": ["units", "units"],
            "stock_on_hand": [4, 5],
        }
    )


def signals() -> pd.DataFrame:
    return build_observed_demand_signals(
        sales(), source_artifact="controlled.csv", source_sha256="a" * 64
    )


def test_signal_uses_complete_calendar_period() -> None:
    result = signals()

    assert result["observation_days"].tolist() == [3, 3]
    assert result["signal_value"].tolist() == [3.0, 3.0]
    assert set(result["signal_type"]) == {"observed_daily_average"}
    assert set(result["signal_unit"]) == {"units_per_day"}


def test_signal_rejects_negative_observation() -> None:
    source = sales()
    source.loc[0, "units_sold"] = -1

    with pytest.raises(DemandSignalError, match="non-negative"):
        build_observed_demand_signals(
            source, source_artifact="controlled.csv", source_sha256="a" * 64
        )


def test_signal_rejects_ambiguous_product_name() -> None:
    source = sales()
    source.loc[1, "product_name"] = "Different"

    with pytest.raises(DemandSignalError, match="one product_name"):
        build_observed_demand_signals(
            source, source_artifact="controlled.csv", source_sha256="a" * 64
        )


def test_join_preserves_exact_product_coverage() -> None:
    joined = join_inventory_and_signals(inventory(), signals())

    assert joined["product_id"].tolist() == ["P001", "P002"]
    assert joined["product_name"].tolist() == ["Rice", "Milk"]


def test_join_reports_unmatched_products() -> None:
    source = inventory().iloc[:1].copy()

    with pytest.raises(DemandSignalError, match=r"signal_only=\['P002'\]"):
        join_inventory_and_signals(source, signals())


def test_join_rejects_incompatible_units() -> None:
    source = inventory()
    source.loc[0, "stock_unit"] = "cases"

    with pytest.raises(DemandSignalError, match="incompatible"):
        join_inventory_and_signals(source, signals())
