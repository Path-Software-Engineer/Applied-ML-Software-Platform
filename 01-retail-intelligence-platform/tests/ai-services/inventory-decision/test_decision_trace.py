"""Tests for the auditable Inventory Decision trace."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from inventory_decision.reporting import build_decision_trace, run_decision_trace


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def canonical_report() -> dict[str, object]:
    return json.loads(
        (PROJECT_ROOT / "reports/outputs/inventory-decision/inventory_decision_report.json")
        .read_text(encoding="utf-8")
    )


def test_trace_preserves_top_decision_inputs_and_outcome() -> None:
    trace = build_decision_trace(canonical_report())
    bread = trace["decisions"][0]
    assert bread["product"] == {"product_id": "P003", "product_name": "Bread"}
    assert bread["observed_inputs"]["current_stock_units"] == 0
    assert bread["policy_calculations"]["reorder_point_units"] == 35
    assert bread["review_outcome"] == {
        "risk_label": "critical",
        "recommended_action": "replenish_now",
        "suggested_quantity_units": 70,
    }


def test_trace_rejects_card_and_ranking_conflict() -> None:
    report = canonical_report()
    report["recommendation_cards"][0]["priority_rank"] = 9
    with pytest.raises(ValueError, match="conflict"):
        build_decision_trace(report)


def test_trace_generation_is_byte_reproducible() -> None:
    run_decision_trace(PROJECT_ROOT)
    path = PROJECT_ROOT / "reports/outputs/inventory-decision/decision_trace.json"
    first = path.read_bytes()
    run_decision_trace(PROJECT_ROOT)
    assert path.read_bytes() == first
