"""Tests for the versioned inventory snapshot contract."""

from __future__ import annotations

from datetime import date

import pytest

from inventory_decision.contract import (
    INVENTORY_SNAPSHOT_CONTRACT,
    InventoryContractError,
    validate_inventory_record,
)


def valid_record() -> dict[str, object]:
    return {
        "snapshot_id": "learning-2026-01-09",
        "snapshot_as_of_date": "2026-01-09",
        "observed_at": "2026-01-08",
        "product_id": "P001",
        "product_name": "Rice 1kg",
        "stock_on_hand": "29",
        "stock_unit": "units",
        "source_type": "latest_observed_stock",
        "lead_time_days": "",
    }


def test_contract_identity_is_frozen() -> None:
    assert INVENTORY_SNAPSHOT_CONTRACT.schema_version == "1.0"
    assert INVENTORY_SNAPSHOT_CONTRACT.quantity_unit == "units"
    assert INVENTORY_SNAPSHOT_CONTRACT.evidence_status == "synthetic_learning_snapshot"


def test_record_validation_preserves_provenance_and_dates() -> None:
    record = validate_inventory_record(valid_record())

    assert record["stock_on_hand"] == 29
    assert record["observed_at"] == date(2026, 1, 8)
    assert record["lead_time_days"] is None
    assert record["source_type"] == "latest_observed_stock"


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("stock_on_hand", "-1", "non-negative integer"),
        ("stock_unit", "cases", "must be units"),
        ("lead_time_days", "0", "positive integer"),
        ("snapshot_as_of_date", "01/09/2026", "YYYY-MM-DD"),
    ],
)
def test_record_validation_rejects_invalid_values(
    field: str, value: object, message: str
) -> None:
    record = valid_record()
    record[field] = value

    with pytest.raises(InventoryContractError, match=message):
        validate_inventory_record(record)


def test_record_validation_rejects_future_observation() -> None:
    record = valid_record()
    record["observed_at"] = "2026-01-10"

    with pytest.raises(InventoryContractError, match="cannot be after"):
        validate_inventory_record(record)


def test_record_validation_rejects_unknown_fields() -> None:
    record = valid_record()
    record["currency"] = "USD"

    with pytest.raises(InventoryContractError, match="Unexpected inventory fields"):
        validate_inventory_record(record)
