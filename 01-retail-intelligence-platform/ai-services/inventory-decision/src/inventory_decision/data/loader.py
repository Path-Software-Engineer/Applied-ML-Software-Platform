"""Load inventory snapshot CSV evidence without applying decision policy."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from inventory_decision.contract import (
    INVENTORY_SNAPSHOT_CONTRACT,
    InventoryContractError,
    validate_inventory_record,
)


PRODUCT_ID_PATTERN = re.compile(r"^[A-Z0-9_-]+$")
MAX_SOURCE_BYTES = 2 * 1024 * 1024


class InventoryDataError(ValueError):
    """Raised when inventory source evidence cannot satisfy the data boundary."""


def load_inventory_snapshot(path: Path) -> pd.DataFrame:
    """Read, structurally validate and type one inventory snapshot."""
    source = Path(path)
    if not source.is_file():
        raise InventoryDataError(f"Inventory snapshot not found: {source}")
    if source.stat().st_size == 0:
        raise InventoryDataError("Inventory snapshot is empty.")
    if source.stat().st_size > MAX_SOURCE_BYTES:
        raise InventoryDataError("Inventory snapshot exceeds the 2 MiB boundary.")

    try:
        data = pd.read_csv(source, dtype=str, keep_default_na=False, encoding="utf-8")
    except (OSError, UnicodeError, pd.errors.ParserError) as error:
        raise InventoryDataError("Inventory snapshot cannot be read as UTF-8 CSV.") from error

    required = list(INVENTORY_SNAPSHOT_CONTRACT.required_fields)
    allowed = list(
        INVENTORY_SNAPSHOT_CONTRACT.required_fields
        + INVENTORY_SNAPSHOT_CONTRACT.optional_fields
    )
    missing = [field for field in required if field not in data.columns]
    unexpected = [field for field in data.columns if field not in allowed]
    if missing:
        raise InventoryDataError(f"Missing inventory columns: {missing}")
    if unexpected:
        raise InventoryDataError(f"Unexpected inventory columns: {unexpected}")
    if data.empty:
        raise InventoryDataError("Inventory snapshot has no rows.")
    if "lead_time_days" not in data.columns:
        data["lead_time_days"] = ""

    records: list[dict[str, object]] = []
    for row_number, record in enumerate(data.to_dict(orient="records"), start=2):
        try:
            records.append(validate_inventory_record(record))
        except InventoryContractError as error:
            raise InventoryDataError(f"Inventory row {row_number}: {error}") from error

    loaded = pd.DataFrame(records)
    if loaded["product_id"].duplicated().any():
        duplicates = sorted(
            loaded.loc[loaded["product_id"].duplicated(False), "product_id"].unique()
        )
        raise InventoryDataError(f"Duplicate inventory product_id values: {duplicates}")
    if not loaded["product_id"].map(lambda value: bool(PRODUCT_ID_PATTERN.fullmatch(value))).all():
        raise InventoryDataError("product_id values must use A-Z, 0-9, underscore or hyphen.")
    if loaded["snapshot_id"].nunique() != 1:
        raise InventoryDataError("Inventory rows must share one snapshot_id.")
    if loaded["snapshot_as_of_date"].nunique() != 1:
        raise InventoryDataError("Inventory rows must share one snapshot_as_of_date.")

    return loaded.sort_values("product_id", kind="stable").reset_index(drop=True)
