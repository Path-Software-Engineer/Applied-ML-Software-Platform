"""Validate Sprint 3 Week 10 policy and report closure."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    required = (
        "docs/sprints/sprint-03-inventory-decision/week-10/exploration.md",
        "docs/sprints/sprint-03-inventory-decision/week-10/plan.md",
        "docs/sprints/sprint-03-inventory-decision/week-10/review.md",
        "reports/metrics/inventory-decision/risk_ranking.csv",
        "reports/recommendation-cards/inventory-decision/recommendation_cards.json",
        "reports/outputs/inventory-decision/inventory_decision_report.json",
        "reports/outputs/inventory-decision/inventory_decision_report.md",
    )
    for relative in required:
        assert (PROJECT_ROOT / relative).is_file(), f"Missing Week 10 evidence: {relative}"

    report = json.loads(
        (
            PROJECT_ROOT
            / "reports"
            / "outputs"
            / "inventory-decision"
            / "inventory_decision_report.json"
        ).read_text(encoding="utf-8")
    )
    assert report["policy"]["version"] == "inventory-review-policy/1.0"
    assert report["summary"]["products_requiring_replenishment_review"] == 2
    assert report["summary"]["suggested_review_quantity_units"] == 97
    assert report["ranking"][0]["product_id"] == "P003"
    assert report["ranking"][1]["product_id"] == "P002"
    assert all(card["limitation"] for card in report["recommendation_cards"])

    print("OK - Sprint 3 Day 126 Week 10 close check passed")
    print("Policy -> risk -> ranking -> cards -> canonical report: confirmed")
    print("Review queue / suggested units: 2 / 97")
    print("Week 11 transport and presentation: not started")


if __name__ == "__main__":
    main()
