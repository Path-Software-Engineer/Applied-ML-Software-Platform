"""Build an identified observed-demand signal and strict inventory join."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


SCHEMA_VERSION = "1.0"
SIGNAL_TYPE = "observed_daily_average"
SIGNAL_UNIT = "units_per_day"


class DemandSignalError(ValueError):
    """Raised when descriptive demand evidence or its join is invalid."""


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_observed_demand_signals(
    sales: pd.DataFrame,
    *,
    source_artifact: str,
    source_sha256: str,
) -> pd.DataFrame:
    """Aggregate product units over the complete inclusive observed period."""
    required = {"date", "product_id", "product_name", "units_sold"}
    missing = sorted(required - set(sales.columns))
    if missing:
        raise DemandSignalError(f"Missing demand source columns: {missing}")
    if sales.empty:
        raise DemandSignalError("Demand source has no observations.")
    if len(source_sha256) != 64 or any(char not in "0123456789abcdef" for char in source_sha256):
        raise DemandSignalError("Demand source SHA-256 is invalid.")

    source = sales.copy(deep=True)
    source["date"] = pd.to_datetime(source["date"], errors="coerce")
    source["units_sold"] = pd.to_numeric(source["units_sold"], errors="coerce")
    if source[["date", "product_id", "product_name", "units_sold"]].isna().any().any():
        raise DemandSignalError("Demand source contains invalid required values.")
    if (source["units_sold"] < 0).any():
        raise DemandSignalError("Observed units must be non-negative.")

    name_counts = source.groupby("product_id")["product_name"].nunique()
    if (name_counts != 1).any():
        raise DemandSignalError("Each product_id must map to one product_name.")

    period_start = source["date"].min()
    period_end = source["date"].max()
    observation_days = int((period_end - period_start).days) + 1
    grouped = (
        source.groupby(["product_id", "product_name"], as_index=False)["units_sold"]
        .sum()
        .rename(columns={"units_sold": "observed_units"})
        .sort_values("product_id", kind="stable")
        .reset_index(drop=True)
    )
    grouped["signal_type"] = SIGNAL_TYPE
    grouped["signal_value"] = (grouped["observed_units"] / observation_days).round(6)
    grouped["signal_unit"] = SIGNAL_UNIT
    grouped["period_start"] = period_start.strftime("%Y-%m-%d")
    grouped["period_end"] = period_end.strftime("%Y-%m-%d")
    grouped["observation_days"] = observation_days
    grouped["observed_units"] = grouped["observed_units"].astype(int)
    grouped["source_artifact"] = source_artifact
    grouped["source_sha256"] = source_sha256
    return grouped[
        [
            "product_id",
            "product_name",
            "signal_type",
            "signal_value",
            "signal_unit",
            "period_start",
            "period_end",
            "observation_days",
            "observed_units",
            "source_artifact",
            "source_sha256",
        ]
    ]


def join_inventory_and_signals(
    inventory: pd.DataFrame, signals: pd.DataFrame
) -> pd.DataFrame:
    """Require exact one-to-one product coverage and compatible units."""
    inventory_ids = set(inventory["product_id"])
    signal_ids = set(signals["product_id"])
    inventory_only = sorted(inventory_ids - signal_ids)
    signal_only = sorted(signal_ids - inventory_ids)
    if inventory_only or signal_only:
        raise DemandSignalError(
            "Inventory and demand product sets differ: "
            f"inventory_only={inventory_only}, signal_only={signal_only}"
        )
    if inventory["product_id"].duplicated().any() or signals["product_id"].duplicated().any():
        raise DemandSignalError("Inventory and demand joins require unique product_id values.")
    if set(inventory["stock_unit"]) != {"units"} or set(signals["signal_unit"]) != {SIGNAL_UNIT}:
        raise DemandSignalError("Inventory and demand units are incompatible.")

    joined = inventory.merge(
        signals,
        on="product_id",
        how="inner",
        validate="one_to_one",
        suffixes=("_inventory", "_signal"),
    )
    if not (joined["product_name_inventory"] == joined["product_name_signal"]).all():
        raise DemandSignalError("Product names conflict across inventory and demand evidence.")
    joined = joined.drop(columns=["product_name_signal"]).rename(
        columns={"product_name_inventory": "product_name"}
    )
    return joined.sort_values("product_id", kind="stable").reset_index(drop=True)


def run_signal_integration(project_root: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, object]]:
    """Generate official signal, strict join and integration manifest artifacts."""
    from inventory_decision.data.cleaner import run_inventory_cleaning

    sales_path = project_root / "data" / "processed" / "demand-insight" / "sales_clean.csv"
    inventory_path = (
        project_root / "data" / "processed" / "inventory-decision" / "inventory_snapshot_clean.csv"
    )
    output_root = project_root / "data" / "processed" / "inventory-decision"
    signals_path = output_root / "demand_signals.csv"
    joined_path = output_root / "inventory_signal_snapshot.csv"
    manifest_path = output_root / "integration_manifest.json"

    inventory = run_inventory_cleaning(project_root)
    sales = pd.read_csv(sales_path)
    signals = build_observed_demand_signals(
        sales,
        source_artifact=sales_path.relative_to(project_root).as_posix(),
        source_sha256=file_sha256(sales_path),
    )
    joined = join_inventory_and_signals(inventory, signals)

    serializable_inventory = inventory.copy()
    for column in ("snapshot_as_of_date", "observed_at"):
        serializable_inventory[column] = serializable_inventory[column].dt.strftime("%Y-%m-%d")
    joined_output = join_inventory_and_signals(serializable_inventory, signals)
    signals.to_csv(signals_path, index=False, lineterminator="\n")
    joined_output.to_csv(joined_path, index=False, lineterminator="\n")

    manifest: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "module": "inventory_decision",
        "join_key": "product_id",
        "join_strategy": "strict_one_to_one",
        "inventory_source": inventory_path.relative_to(project_root).as_posix(),
        "inventory_sha256": file_sha256(inventory_path),
        "demand_source": sales_path.relative_to(project_root).as_posix(),
        "demand_source_sha256": file_sha256(sales_path),
        "signal_type": SIGNAL_TYPE,
        "signal_unit": SIGNAL_UNIT,
        "inventory_products": len(inventory),
        "signal_products": len(signals),
        "joined_products": len(joined),
        "inventory_only": [],
        "signal_only": [],
        "evidence_status": "descriptive_learning_evidence",
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return signals, joined, manifest
