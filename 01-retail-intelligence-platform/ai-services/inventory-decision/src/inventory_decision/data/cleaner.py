"""Deterministically normalize validated inventory snapshot records."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from inventory_decision.data.loader import InventoryDataError


CLEAN_COLUMNS = (
    "snapshot_id",
    "snapshot_as_of_date",
    "observed_at",
    "freshness_days",
    "product_id",
    "product_name",
    "stock_on_hand",
    "stock_unit",
    "source_type",
    "lead_time_days",
    "lead_time_source",
)


def clean_inventory_snapshot(snapshot: pd.DataFrame) -> pd.DataFrame:
    """Return a normalized copy without filling missing policy inputs."""
    required = {
        "snapshot_id",
        "snapshot_as_of_date",
        "observed_at",
        "product_id",
        "product_name",
        "stock_on_hand",
        "stock_unit",
        "source_type",
        "lead_time_days",
    }
    missing = sorted(required - set(snapshot.columns))
    if missing:
        raise InventoryDataError(f"Cannot clean inventory; missing columns: {missing}")
    if snapshot.empty:
        raise InventoryDataError("Cannot clean an empty inventory snapshot.")

    cleaned = snapshot.copy(deep=True)
    for column in ("snapshot_as_of_date", "observed_at"):
        cleaned[column] = pd.to_datetime(cleaned[column], errors="coerce")
    if cleaned[["snapshot_as_of_date", "observed_at"]].isna().any().any():
        raise InventoryDataError("Inventory cleaning found invalid dates.")

    cleaned["product_name"] = cleaned["product_name"].str.replace(
        r"\s+", " ", regex=True
    ).str.strip()
    if (cleaned["product_name"].str.len() == 0).any():
        raise InventoryDataError("product_name cannot be empty after normalization.")

    cleaned["stock_on_hand"] = pd.to_numeric(
        cleaned["stock_on_hand"], errors="coerce"
    ).astype("Int64")
    if cleaned["stock_on_hand"].isna().any() or (cleaned["stock_on_hand"] < 0).any():
        raise InventoryDataError("stock_on_hand must remain non-negative.")

    lead_time = pd.to_numeric(cleaned["lead_time_days"], errors="coerce").astype(
        "Int64"
    )
    if (lead_time.dropna() <= 0).any():
        raise InventoryDataError("lead_time_days must be positive when supplied.")
    cleaned["lead_time_days"] = lead_time
    cleaned["lead_time_source"] = lead_time.map(
        lambda value: "missing_policy_input" if pd.isna(value) else "source"
    )

    cleaned["freshness_days"] = (
        cleaned["snapshot_as_of_date"] - cleaned["observed_at"]
    ).dt.days.astype("Int64")
    if (cleaned["freshness_days"] < 0).any():
        raise InventoryDataError("Inventory observations cannot be from the future.")

    return cleaned.loc[:, CLEAN_COLUMNS].sort_values(
        "product_id", kind="stable"
    ).reset_index(drop=True)


def write_clean_inventory_snapshot(snapshot: pd.DataFrame, path: Path) -> None:
    """Persist a normalized snapshot with stable dates, order and line endings."""
    output = clean_inventory_snapshot(snapshot)
    for column in ("snapshot_as_of_date", "observed_at"):
        output[column] = output[column].dt.strftime("%Y-%m-%d")
    path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(path, index=False, lineterminator="\n")


def run_inventory_cleaning(project_root: Path) -> pd.DataFrame:
    """Generate the official processed inventory snapshot."""
    from inventory_decision.data.loader import load_inventory_snapshot

    source = project_root / "data" / "raw" / "inventory" / "inventory_snapshot.csv"
    output = (
        project_root
        / "data"
        / "processed"
        / "inventory-decision"
        / "inventory_snapshot_clean.csv"
    )
    snapshot = load_inventory_snapshot(source)
    write_clean_inventory_snapshot(snapshot, output)
    return clean_inventory_snapshot(snapshot)
