"""Recalculate and verify the tracked Week 12 scenario evidence."""

from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "ai-services/inventory-decision/src"))

from inventory_decision.policies import calculate_replenishment  # noqa: E402
from inventory_decision.risk import calculate_risk, classify_risk  # noqa: E402


def main() -> None:
    payload = json.loads(
        (PROJECT_ROOT / "reports/scenarios/inventory-decision/policy_scenarios.json")
        .read_text(encoding="utf-8")
    )
    assert payload["schema_version"] == "1.0"
    assert payload["policy_version"] == "inventory-review-policy/1.0"
    assert len(payload["scenarios"]) == 5

    for expected in payload["scenarios"]:
        replenishment = calculate_replenishment(
            stock_on_hand=expected["stock"],
            observed_units=expected["observed_units"],
            observation_days=payload["observation_days"],
            source_lead_time_days=None,
        )
        risk = calculate_risk(
            stock_on_hand=expected["stock"],
            observed_units=expected["observed_units"],
            observation_days=payload["observation_days"],
            lead_time_days=replenishment.lead_time_days,
            safety_days=1,
            reorder_point_units=replenishment.reorder_point_units,
            reorder_required=replenishment.reorder_required,
        )
        label, action = classify_risk(risk.risk_score)
        actual = {
            "reorder_point": replenishment.reorder_point_units,
            "target_stock": replenishment.target_stock_units,
            "suggested_quantity": replenishment.suggested_quantity_units,
            "risk_score": risk.risk_score,
            "risk_label": label,
            "action": action,
        }
        assert actual == {key: expected[key] for key in actual}, expected["id"]

    print("OK - Sprint 3 Day 135 inventory scenario check passed")
    print("Scenarios: 5 deterministic oracles")
    print("Policy / score meaning: inventory-review-policy/1.0 / priority index")


if __name__ == "__main__":
    main()
