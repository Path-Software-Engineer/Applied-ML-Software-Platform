"""Create a compact, versioned audit trace from canonical decision evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_decision_trace(report: dict[str, Any]) -> dict[str, Any]:
    """Map canonical rankings and cards into one trace per product."""
    ranking = report.get("ranking")
    cards = report.get("recommendation_cards")
    if not isinstance(ranking, list) or not isinstance(cards, list):
        raise ValueError("Decision trace requires ranking and Recommendation Cards.")
    card_by_product = {card["product"]["product_id"]: card for card in cards}
    if len(card_by_product) != len(ranking):
        raise ValueError("Decision trace requires one unique card per ranking row.")

    decisions: list[dict[str, Any]] = []
    for item in ranking:
        card = card_by_product.get(item["product_id"])
        if card is None or card["priority_rank"] != item["priority_rank"]:
            raise ValueError("Ranking and Recommendation Card traces conflict.")
        decisions.append(
            {
                "priority_rank": item["priority_rank"],
                "product": {
                    "product_id": item["product_id"],
                    "product_name": item["product_name"],
                },
                "observed_inputs": {
                    "snapshot_as_of_date": card["evidence"]["snapshot_as_of_date"],
                    "current_stock_units": item["current_stock_units"],
                    "observed_daily_demand": item["observed_daily_demand"],
                    "coverage_days": item["coverage_days"],
                    "lead_time_days": card["evidence"]["lead_time_days"],
                    "lead_time_source": card["evidence"]["lead_time_source"],
                },
                "policy_calculations": {
                    "reorder_point_units": item["reorder_point_units"],
                    "target_stock_units": item["target_stock_units"],
                    "risk_score": item["risk_score"],
                    "risk_score_meaning": item["risk_score_meaning"],
                },
                "review_outcome": {
                    "risk_label": item["risk_label"],
                    "recommended_action": item["recommended_action"],
                    "suggested_quantity_units": item["suggested_quantity_units"],
                },
                "reason": item["reason"],
                "limitation": card["limitation"],
            }
        )
    return {
        "schema_version": "1.0",
        "module": "inventory_decision",
        "evidence_as_of_date": report["evidence_as_of_date"],
        "policy_version": report["policy"]["version"],
        "risk_score_meaning": "priority_index_not_probability",
        "decision_count": len(decisions),
        "decisions": decisions,
    }


def render_decision_trace(trace: dict[str, Any]) -> str:
    lines = [
        "# Inventory Decision Trace",
        "",
        f"Policy: `{trace['policy_version']}`  ",
        f"Evidence date: `{trace['evidence_as_of_date']}`  ",
        "Risk score meaning: priority index, not probability.",
        "",
    ]
    for decision in trace["decisions"]:
        inputs = decision["observed_inputs"]
        calculations = decision["policy_calculations"]
        outcome = decision["review_outcome"]
        lines.extend(
            [
                f"## {decision['priority_rank']:02d} — {decision['product']['product_name']}",
                "",
                f"- Inputs: stock {inputs['current_stock_units']} units; observed demand {inputs['observed_daily_demand']} units/day; lead time {inputs['lead_time_days']} days ({inputs['lead_time_source']}).",
                f"- Policy: reorder point {calculations['reorder_point_units']} units; target {calculations['target_stock_units']} units; priority index {calculations['risk_score']}.",
                f"- Review outcome: `{outcome['recommended_action']}`; suggested {outcome['suggested_quantity_units']} units.",
                f"- Reason: {decision['reason']}",
                f"- Limitation: {decision['limitation']}",
                "",
            ]
        )
    return "\n".join(lines)


def run_decision_trace(project_root: Path) -> dict[str, Any]:
    report_path = project_root / "reports/outputs/inventory-decision/inventory_decision_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    trace = build_decision_trace(report)
    output_root = project_root / "reports/outputs/inventory-decision"
    (output_root / "decision_trace.json").write_text(
        json.dumps(trace, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    (output_root / "decision_trace.md").write_text(
        render_decision_trace(trace), encoding="utf-8", newline="\n"
    )
    return trace
