"""Validate Sprint 3 Week 9 closure evidence and factual boundaries."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    required = (
        "docs/sprints/sprint-03-inventory-decision/week-09/exploration.md",
        "docs/sprints/sprint-03-inventory-decision/week-09/plan.md",
        "docs/sprints/sprint-03-inventory-decision/week-09/review.md",
        "data/processed/inventory-decision/inventory_snapshot_clean.csv",
        "data/processed/inventory-decision/demand_signals.csv",
        "data/processed/inventory-decision/inventory_signal_snapshot.csv",
        "data/processed/inventory-decision/integration_manifest.json",
        "reports/summaries/inventory-decision/inventory_snapshot_summary.json",
    )
    for relative in required:
        assert (PROJECT_ROOT / relative).is_file(), f"Missing Week 9 evidence: {relative}"

    joined = pd.read_csv(
        PROJECT_ROOT
        / "data"
        / "processed"
        / "inventory-decision"
        / "inventory_signal_snapshot.csv"
    )
    manifest = json.loads(
        (
            PROJECT_ROOT
            / "data"
            / "processed"
            / "inventory-decision"
            / "integration_manifest.json"
        ).read_text(encoding="utf-8")
    )
    summary = json.loads(
        (
            PROJECT_ROOT
            / "reports"
            / "summaries"
            / "inventory-decision"
            / "inventory_snapshot_summary.json"
        ).read_text(encoding="utf-8")
    )

    assert len(joined) == joined["product_id"].nunique() == 6
    assert joined["stock_on_hand"].sum() == 99
    assert joined["observed_units"].sum() == 293
    assert manifest["joined_products"] == 6
    assert summary["decision_status"] == "not_calculated"

    print("OK - Sprint 3 Day 119 Week 9 close check passed")
    print("Flow: contract -> loading -> cleaning -> signal -> strict join -> facts")
    print("Products / unmatched: 6 / 0")
    print("Week 10 policy calculations: not started")


if __name__ == "__main__":
    main()
