"""Tests for the canonical Inventory Decision report."""

from __future__ import annotations

import json
from pathlib import Path

from inventory_decision.reporting.decision_report import (
    LIMITATIONS,
    render_inventory_decision_report,
    run_inventory_decision_report,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def test_canonical_report_is_internally_consistent() -> None:
    report = run_inventory_decision_report(PROJECT_ROOT)

    assert report["schema_version"] == "1.0"
    assert report["report_status"] == "learning_evidence_only"
    assert report["summary"]["products"] == 6
    assert report["summary"]["products_requiring_replenishment_review"] == 2
    assert report["summary"]["suggested_review_quantity_units"] == 97
    assert [row["product_id"] for row in report["ranking"]] == [
        card["product"]["product_id"] for card in report["recommendation_cards"]
    ]
    assert report["limitations"] == LIMITATIONS


def test_canonical_report_generation_is_reproducible() -> None:
    first = run_inventory_decision_report(PROJECT_ROOT)
    path = PROJECT_ROOT / "reports" / "outputs" / "inventory-decision" / "inventory_decision_report.json"
    first_bytes = path.read_bytes()
    second = run_inventory_decision_report(PROJECT_ROOT)

    assert first == second
    assert path.read_bytes() == first_bytes
    assert json.loads(path.read_text(encoding="utf-8")) == first


def test_markdown_preserves_priority_and_limitations() -> None:
    markdown = render_inventory_decision_report(run_inventory_decision_report(PROJECT_ROOT))

    assert "Bread" in markdown
    assert "Milk 1L" in markdown
    assert "Suggested review quantity: 97 units" in markdown
    assert "not a probability" in markdown
    assert "no order was created" in markdown
