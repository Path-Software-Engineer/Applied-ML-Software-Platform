"""Tests for deterministic inventory normalization."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from inventory_decision.data.cleaner import (
    clean_inventory_snapshot,
    write_clean_inventory_snapshot,
)
from inventory_decision.data.loader import InventoryDataError


def source_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "snapshot_id": ["S1", "S1"],
            "snapshot_as_of_date": [pd.Timestamp("2026-01-09")] * 2,
            "observed_at": [pd.Timestamp("2026-01-09"), pd.Timestamp("2026-01-07")],
            "product_id": ["P002", "P001"],
            "product_name": ["  Milk   1L ", "Rice 1kg"],
            "stock_on_hand": [9, 29],
            "stock_unit": ["units", "units"],
            "source_type": ["test", "test"],
            "lead_time_days": [None, 3],
        }
    )


def test_cleaner_is_deterministic_and_does_not_mutate_input() -> None:
    source = source_frame()
    original = source.copy(deep=True)

    first = clean_inventory_snapshot(source)
    second = clean_inventory_snapshot(source)

    pd.testing.assert_frame_equal(source, original)
    pd.testing.assert_frame_equal(first, second)
    assert first["product_id"].tolist() == ["P001", "P002"]
    assert first["freshness_days"].tolist() == [2, 0]
    assert first["lead_time_source"].tolist() == ["source", "missing_policy_input"]
    assert first.loc[1, "product_name"] == "Milk 1L"


def test_cleaner_preserves_missing_lead_time() -> None:
    cleaned = clean_inventory_snapshot(source_frame())

    assert pd.isna(cleaned.loc[1, "lead_time_days"])
    assert cleaned.loc[1, "lead_time_source"] == "missing_policy_input"


def test_cleaner_rejects_invalid_lead_time() -> None:
    source = source_frame()
    source.loc[0, "lead_time_days"] = 0

    with pytest.raises(InventoryDataError, match="positive when supplied"):
        clean_inventory_snapshot(source)


def test_writer_is_byte_reproducible(tmp_path: Path) -> None:
    first = tmp_path / "first.csv"
    second = tmp_path / "second.csv"

    write_clean_inventory_snapshot(source_frame(), first)
    write_clean_inventory_snapshot(source_frame(), second)

    assert first.read_bytes() == second.read_bytes()
    assert b"missing_policy_input" in first.read_bytes()
