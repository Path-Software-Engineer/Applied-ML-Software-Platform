"""Versioned contract primitives for inventory snapshot evidence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Mapping


class InventoryContractError(ValueError):
    """Raised when a source record violates the inventory contract."""


@dataclass(frozen=True)
class InventorySnapshotContract:
    schema_version: str
    contract_id: str
    quantity_unit: str
    evidence_status: str
    required_fields: tuple[str, ...]
    optional_fields: tuple[str, ...]


INVENTORY_SNAPSHOT_CONTRACT = InventorySnapshotContract(
    schema_version="1.0",
    contract_id="inventory_snapshot",
    quantity_unit="units",
    evidence_status="synthetic_learning_snapshot",
    required_fields=(
        "snapshot_id",
        "snapshot_as_of_date",
        "observed_at",
        "product_id",
        "product_name",
        "stock_on_hand",
        "stock_unit",
        "source_type",
    ),
    optional_fields=("lead_time_days",),
)


def parse_iso_date(value: object, *, field: str) -> date:
    """Parse one strict ISO date with a domain-readable error."""
    if not isinstance(value, str) or not value.strip():
        raise InventoryContractError(f"{field} must be a non-empty ISO date.")
    try:
        return date.fromisoformat(value.strip())
    except ValueError as error:
        raise InventoryContractError(f"{field} must use YYYY-MM-DD.") from error


def validate_inventory_record(record: Mapping[str, object]) -> dict[str, object]:
    """Validate one record without performing file loading or cleaning."""
    missing = [
        field
        for field in INVENTORY_SNAPSHOT_CONTRACT.required_fields
        if field not in record
    ]
    if missing:
        raise InventoryContractError(f"Missing inventory fields: {missing}")

    unknown = set(record) - set(
        INVENTORY_SNAPSHOT_CONTRACT.required_fields
        + INVENTORY_SNAPSHOT_CONTRACT.optional_fields
    )
    if unknown:
        raise InventoryContractError(
            f"Unexpected inventory fields: {sorted(unknown)}"
        )

    normalized: dict[str, object] = {}
    for field in ("snapshot_id", "product_id", "product_name", "source_type"):
        value = record[field]
        if not isinstance(value, str) or not value.strip():
            raise InventoryContractError(f"{field} must be non-empty text.")
        normalized[field] = value.strip()

    snapshot_date = parse_iso_date(
        record["snapshot_as_of_date"], field="snapshot_as_of_date"
    )
    observed_at = parse_iso_date(record["observed_at"], field="observed_at")
    if observed_at > snapshot_date:
        raise InventoryContractError(
            "observed_at cannot be after snapshot_as_of_date."
        )
    normalized["snapshot_as_of_date"] = snapshot_date
    normalized["observed_at"] = observed_at

    stock = record["stock_on_hand"]
    if isinstance(stock, bool):
        raise InventoryContractError("stock_on_hand must be an integer.")
    try:
        parsed_stock = int(str(stock).strip())
    except (TypeError, ValueError) as error:
        raise InventoryContractError("stock_on_hand must be an integer.") from error
    if str(parsed_stock) != str(stock).strip() or parsed_stock < 0:
        raise InventoryContractError(
            "stock_on_hand must be a non-negative integer."
        )
    normalized["stock_on_hand"] = parsed_stock

    unit = record["stock_unit"]
    if unit != INVENTORY_SNAPSHOT_CONTRACT.quantity_unit:
        raise InventoryContractError("stock_unit must be units for schema 1.0.")
    normalized["stock_unit"] = unit

    lead_time = record.get("lead_time_days")
    if lead_time in (None, ""):
        normalized["lead_time_days"] = None
    else:
        if isinstance(lead_time, bool):
            raise InventoryContractError("lead_time_days must be a positive integer.")
        try:
            parsed_lead_time = int(str(lead_time).strip())
        except (TypeError, ValueError) as error:
            raise InventoryContractError(
                "lead_time_days must be a positive integer."
            ) from error
        if str(parsed_lead_time) != str(lead_time).strip() or parsed_lead_time <= 0:
            raise InventoryContractError(
                "lead_time_days must be a positive integer."
            )
        normalized["lead_time_days"] = parsed_lead_time

    return normalized
