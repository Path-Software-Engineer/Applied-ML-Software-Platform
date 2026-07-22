"""Generate and verify the Day 137 decision trace."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "ai-services/inventory-decision/src"))

from inventory_decision.reporting import run_decision_trace  # noqa: E402


def main() -> None:
    trace = run_decision_trace(PROJECT_ROOT)
    assert trace["policy_version"] == "inventory-review-policy/1.0"
    assert trace["risk_score_meaning"] == "priority_index_not_probability"
    assert trace["decision_count"] == 6
    bread = trace["decisions"][0]
    assert bread["product"]["product_id"] == "P003"
    assert bread["review_outcome"]["suggested_quantity_units"] == 70
    assert all(item["reason"] and item["limitation"] for item in trace["decisions"])

    print("OK - Sprint 3 Day 137 decision trace check passed")
    print("Decisions / policy: 6 / inventory-review-policy/1.0")
    print("Inputs, calculations, outcomes, reasons and limitations: traceable")


if __name__ == "__main__":
    main()
