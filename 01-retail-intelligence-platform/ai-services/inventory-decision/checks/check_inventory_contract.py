"""Readable validation for the official inventory snapshot contract."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "inventory-decision" / "src"
sys.path.insert(0, str(MODULE_SRC))

from inventory_decision.contract import (  # noqa: E402
    INVENTORY_SNAPSHOT_CONTRACT,
    validate_inventory_record,
)


def main() -> None:
    schema_path = (
        PROJECT_ROOT
        / "ai-services"
        / "inventory-decision"
        / "contracts"
        / "inventory-snapshot.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert schema["$schema"].endswith("2020-12/schema")
    assert schema["properties"]["schema_version"]["const"] == "1.0"
    assert schema["properties"]["records"]["x-unique-key"] == "product_id"

    source = PROJECT_ROOT / "data" / "raw" / "inventory" / "inventory_snapshot.csv"
    with source.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    validated = [validate_inventory_record(row) for row in rows]
    product_ids = [row["product_id"] for row in validated]
    assert len(validated) == 6
    assert len(set(product_ids)) == len(product_ids)
    assert {row["stock_unit"] for row in validated} == {"units"}

    print("OK - Sprint 3 Day 114 inventory contract check passed")
    print(f"Schema version: {INVENTORY_SNAPSHOT_CONTRACT.schema_version}")
    print(f"Inventory rows / products: {len(validated)} / {len(product_ids)}")
    print("Lead time source: optional; policy default not applied by contract")


if __name__ == "__main__":
    main()
