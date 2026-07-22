"""Adversarial evidence cases that must fail before recommendation output."""

from __future__ import annotations

import pandas as pd
import pytest

from inventory_decision.contract import InventoryContractError, validate_inventory_record
from inventory_decision.data import InventoryDataError, load_inventory_snapshot
from inventory_decision.policies import PolicyError, calculate_replenishment
from inventory_decision.signals import DemandSignalError, join_inventory_and_signals


def valid_record() -> dict[str, object]:
    return {
        "snapshot_id": "scenario-1",
        "snapshot_as_of_date": "2026-01-09",
        "observed_at": "2026-01-09",
        "product_id": "P001",
        "product_name": "Rice 1kg",
        "stock_on_hand": "10",
        "stock_unit": "units",
        "source_type": "controlled_test",
        "lead_time_days": "",
    }


@pytest.mark.parametrize("field", ["product_id", "stock_on_hand", "stock_unit"])
def test_missing_required_field_fails_closed(field: str) -> None:
    record = valid_record()
    record.pop(field)
    with pytest.raises(InventoryContractError, match="Missing inventory fields"):
        validate_inventory_record(record)


def test_unknown_field_fails_closed() -> None:
    with pytest.raises(InventoryContractError, match="Unexpected inventory fields"):
        validate_inventory_record({**valid_record(), "supplier_guess": "unknown"})


def test_negative_stock_and_invalid_lead_time_fail_closed() -> None:
    with pytest.raises(InventoryContractError, match="non-negative"):
        validate_inventory_record({**valid_record(), "stock_on_hand": "-1"})
    with pytest.raises(InventoryContractError, match="positive integer"):
        validate_inventory_record({**valid_record(), "lead_time_days": "0"})
    with pytest.raises(PolicyError, match="positive integer"):
        calculate_replenishment(
            stock_on_hand=10,
            observed_units=9,
            observation_days=9,
            source_lead_time_days=-2,
        )


def test_duplicate_inventory_key_fails_closed(tmp_path) -> None:
    source = tmp_path / "inventory.csv"
    pd.DataFrame([valid_record(), valid_record()]).to_csv(source, index=False)
    with pytest.raises(InventoryDataError, match="Duplicate inventory product_id"):
        load_inventory_snapshot(source)


def test_unmatched_and_incompatible_join_evidence_fails_closed() -> None:
    inventory = pd.DataFrame({"product_id": ["P001"], "stock_unit": ["units"]})
    signals = pd.DataFrame({"product_id": ["P002"], "signal_unit": ["units_per_day"]})
    with pytest.raises(DemandSignalError, match="product sets differ"):
        join_inventory_and_signals(inventory, signals)

    signals["product_id"] = "P001"
    signals["signal_unit"] = "currency_per_day"
    with pytest.raises(DemandSignalError, match="units are incompatible"):
        join_inventory_and_signals(inventory, signals)
