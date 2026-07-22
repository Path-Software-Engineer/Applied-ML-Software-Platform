"""Readable Day 117 validation for demand signals and inventory join."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "inventory-decision" / "src"
sys.path.insert(0, str(MODULE_SRC))

from inventory_decision.signals import run_signal_integration  # noqa: E402


def main() -> None:
    signals, joined, manifest = run_signal_integration(PROJECT_ROOT)
    output_root = PROJECT_ROOT / "data" / "processed" / "inventory-decision"
    persisted = pd.read_csv(output_root / "inventory_signal_snapshot.csv")
    persisted_manifest = json.loads(
        (output_root / "integration_manifest.json").read_text(encoding="utf-8")
    )

    assert len(signals) == len(joined) == len(persisted) == 6
    assert signals["observed_units"].sum() == 293
    assert signals["observation_days"].nunique() == 1
    assert signals["observation_days"].iloc[0] == 9
    assert manifest == persisted_manifest
    assert manifest["inventory_only"] == manifest["signal_only"] == []
    assert manifest["signal_type"] == "observed_daily_average"
    assert manifest["evidence_status"] == "descriptive_learning_evidence"

    bread = signals.loc[signals["product_id"] == "P003"].iloc[0]
    assert bread["signal_value"] == 11.666667

    print("OK - Sprint 3 Day 117 demand signal join check passed")
    print("Products joined: 6 / 6")
    print("Observed units / period: 293 / 9 days")
    print("Bread signal: 11.666667 units/day")
    print("Signal type: observed daily average; not forecast")


if __name__ == "__main__":
    main()
