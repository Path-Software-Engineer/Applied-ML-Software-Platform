"""Tests for strict inventory snapshot loading."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from inventory_decision.data.loader import InventoryDataError, load_inventory_snapshot


def valid_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "snapshot_id": "S1",
                "snapshot_as_of_date": "2026-01-09",
                "observed_at": "2026-01-09",
                "product_id": "P002",
                "product_name": "Milk",
                "stock_on_hand": 9,
                "stock_unit": "units",
                "source_type": "controlled_test",
                "lead_time_days": "",
            },
            {
                "snapshot_id": "S1",
                "snapshot_as_of_date": "2026-01-09",
                "observed_at": "2026-01-08",
                "product_id": "P001",
                "product_name": "Rice",
                "stock_on_hand": 29,
                "stock_unit": "units",
                "source_type": "controlled_test",
                "lead_time_days": 3,
            },
        ]
    )


def write(rows: pd.DataFrame, path: Path) -> Path:
    rows.to_csv(path, index=False)
    return path


def test_loader_types_and_orders_inventory(tmp_path: Path) -> None:
    loaded = load_inventory_snapshot(write(valid_rows(), tmp_path / "snapshot.csv"))

    assert loaded["product_id"].tolist() == ["P001", "P002"]
    assert loaded["stock_on_hand"].tolist() == [29, 9]
    assert loaded.loc[0, "lead_time_days"] == 3
    assert pd.isna(loaded.loc[1, "lead_time_days"])


def test_loader_rejects_duplicate_products(tmp_path: Path) -> None:
    rows = valid_rows()
    rows.loc[1, "product_id"] = "P002"

    with pytest.raises(InventoryDataError, match="Duplicate inventory product_id"):
        load_inventory_snapshot(write(rows, tmp_path / "duplicate.csv"))


def test_loader_rejects_missing_column(tmp_path: Path) -> None:
    rows = valid_rows().drop(columns=["source_type"])

    with pytest.raises(InventoryDataError, match="Missing inventory columns"):
        load_inventory_snapshot(write(rows, tmp_path / "missing.csv"))


def test_loader_rejects_mixed_snapshot_identity(tmp_path: Path) -> None:
    rows = valid_rows()
    rows.loc[1, "snapshot_id"] = "S2"

    with pytest.raises(InventoryDataError, match="share one snapshot_id"):
        load_inventory_snapshot(write(rows, tmp_path / "mixed.csv"))


def test_loader_reports_invalid_row_number(tmp_path: Path) -> None:
    rows = valid_rows()
    rows.loc[1, "stock_on_hand"] = -1

    with pytest.raises(InventoryDataError, match="Inventory row 3"):
        load_inventory_snapshot(write(rows, tmp_path / "invalid.csv"))


def test_loader_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(InventoryDataError, match="not found"):
        load_inventory_snapshot(tmp_path / "absent.csv")
