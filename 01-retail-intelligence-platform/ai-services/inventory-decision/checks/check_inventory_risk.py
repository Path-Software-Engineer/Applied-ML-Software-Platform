"""Readable Day 122 validation for coverage and priority scoring."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "inventory-decision" / "src"
sys.path.insert(0, str(MODULE_SRC))

from inventory_decision.risk import run_risk_scoring  # noqa: E402


def main() -> None:
    results = run_risk_scoring(PROJECT_ROOT)
    indexed = results.set_index("product_id")

    assert len(results) == 6
    assert indexed.loc["P003", "coverage_days"] == 0.0
    assert indexed.loc["P003", "risk_score"] == 100.0
    assert indexed.loc["P002", "coverage_days"] == 1.5
    assert indexed.loc["P002", "risk_score"] == 50.0
    assert (results["risk_score"] >= 0).all() and (results["risk_score"] <= 100).all()
    assert set(results["risk_score_meaning"]) == {"priority_index_not_probability"}

    print("OK - Sprint 3 Day 122 inventory risk check passed")
    print("Bread coverage / score: 0.0 days / 100.0")
    print("Milk coverage / score: 1.5 days / 50.0")
    print("Score meaning: priority index, not probability")


if __name__ == "__main__":
    main()
