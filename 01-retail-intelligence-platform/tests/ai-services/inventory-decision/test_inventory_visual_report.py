"""Tests for report-driven Inventory Decision figures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from inventory_decision.reporting import generate_inventory_figures


PROJECT_ROOT = Path(__file__).resolve().parents[3]
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def test_visual_report_generates_three_valid_figures(tmp_path: Path) -> None:
    report = json.loads(
        (PROJECT_ROOT / "reports/outputs/inventory-decision/inventory_decision_report.json")
        .read_text(encoding="utf-8")
    )
    figures = generate_inventory_figures(report, tmp_path)
    assert [item["id"] for item in figures] == [
        "priority-index",
        "stock-policy-levels",
        "coverage-days",
    ]
    for item in figures:
        assert (tmp_path / item["path"]).read_bytes().startswith(PNG_SIGNATURE)


def test_visual_report_rejects_missing_ranking(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="ranked evidence"):
        generate_inventory_figures({"ranking": []}, tmp_path)
