"""Readable Day 116 validation for inventory normalization."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "inventory-decision" / "src"
sys.path.insert(0, str(MODULE_SRC))

from inventory_decision.data.cleaner import run_inventory_cleaning  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source = PROJECT_ROOT / "data" / "raw" / "inventory" / "inventory_snapshot.csv"
    output = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "inventory-decision"
        / "inventory_snapshot_clean.csv"
    )
    source_hash = sha256(source)
    cleaned = run_inventory_cleaning(PROJECT_ROOT)
    first_bytes = output.read_bytes()
    run_inventory_cleaning(PROJECT_ROOT)

    assert sha256(source) == source_hash
    assert output.read_bytes() == first_bytes
    assert len(cleaned) == 6
    assert cleaned["stock_on_hand"].sum() == 99
    assert cleaned["lead_time_days"].isna().all()
    assert cleaned["freshness_days"].max() == 2
    assert not pd.read_csv(output)["stock_on_hand"].isna().any()

    print("OK - Sprint 3 Day 116 inventory cleaning check passed")
    print("Rows / observed stock: 6 / 99 units")
    print("Freshness range: 0-2 days")
    print("Lead time: preserved as missing policy input")
    print("Raw source: byte-identical")


if __name__ == "__main__":
    main()
