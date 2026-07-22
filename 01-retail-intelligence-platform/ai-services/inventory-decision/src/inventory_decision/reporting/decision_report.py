"""Assemble the canonical Inventory Decision read artifact."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from inventory_decision.policies import DEFAULT_INVENTORY_POLICY


LIMITATIONS = [
    "The inventory snapshot and sales period are small synthetic learning evidence.",
    "Observed daily average is descriptive and is not a validated demand forecast.",
    "Lead time is a versioned two-day policy default, not supplier evidence.",
    "Risk score is a prioritization index and is not a stockout probability.",
    "Suggested quantities require human review and do not create purchase orders.",
]


PUBLIC_RANKING_FIELDS = (
    "priority_rank",
    "product_id",
    "product_name",
    "current_stock_units",
    "observed_daily_demand",
    "coverage_days",
    "reorder_point_units",
    "target_stock_units",
    "suggested_quantity_units",
    "risk_score",
    "risk_score_meaning",
    "risk_label",
    "recommended_action",
    "reason",
    "policy_version",
)


def _json_value(value: object) -> object:
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def build_inventory_decision_report(
    *,
    snapshot_summary: dict[str, Any],
    integration_manifest: dict[str, Any],
    ranking: pd.DataFrame,
    cards_payload: dict[str, Any],
) -> dict[str, Any]:
    """Combine only already-generated, mutually consistent evidence."""
    if len(ranking) != 6 or ranking["product_id"].nunique() != 6:
        raise ValueError("Inventory decision report requires six unique products.")
    cards = cards_payload.get("cards")
    if not isinstance(cards, list) or len(cards) != len(ranking):
        raise ValueError("Inventory decision report cards do not match ranking.")
    ranking_ids = ranking["product_id"].tolist()
    card_ids = [card["product"]["product_id"] for card in cards]
    if ranking_ids != card_ids:
        raise ValueError("Inventory ranking and Recommendation Card order differ.")
    if integration_manifest.get("joined_products") != len(ranking):
        raise ValueError("Inventory integration manifest coverage is inconsistent.")

    ranking_records = [
        {field: _json_value(record[field]) for field in PUBLIC_RANKING_FIELDS}
        for record in ranking.to_dict(orient="records")
    ]
    label_counts = ranking["risk_label"].value_counts().to_dict()
    summary = {
        "products": int(len(ranking)),
        "stock_on_hand_units": int(ranking["current_stock_units"].sum()),
        "products_requiring_replenishment_review": int(ranking["reorder_required"].sum()),
        "critical_products": int(label_counts.get("critical", 0)),
        "high_risk_products": int(label_counts.get("high", 0)),
        "watch_products": int(label_counts.get("watch", 0)),
        "healthy_products": int(label_counts.get("healthy", 0)),
        "suggested_review_quantity_units": int(ranking["suggested_quantity_units"].sum()),
    }
    return {
        "schema_version": "1.0",
        "module": "inventory_decision",
        "report_status": "learning_evidence_only",
        "evidence_as_of_date": snapshot_summary["snapshot"]["as_of_date"],
        "snapshot": snapshot_summary["snapshot"],
        "demand_signal": snapshot_summary["demand_signal"],
        "integration": {
            "join_key": integration_manifest["join_key"],
            "join_strategy": integration_manifest["join_strategy"],
            "joined_products": integration_manifest["joined_products"],
            "unmatched_products": len(integration_manifest["inventory_only"])
            + len(integration_manifest["signal_only"]),
            "inventory_sha256": integration_manifest["inventory_sha256"],
            "demand_source_sha256": integration_manifest["demand_source_sha256"],
        },
        "policy": {
            "version": DEFAULT_INVENTORY_POLICY.version,
            "default_lead_time_days": DEFAULT_INVENTORY_POLICY.default_lead_time_days,
            "safety_days": DEFAULT_INVENTORY_POLICY.safety_days,
            "review_period_days": DEFAULT_INVENTORY_POLICY.review_period_days,
            "rounding": DEFAULT_INVENTORY_POLICY.rounding,
            "reorder_trigger": DEFAULT_INVENTORY_POLICY.reorder_trigger,
            "risk_score_meaning": "priority_index_not_probability",
        },
        "summary": summary,
        "ranking": ranking_records,
        "recommendation_cards": cards,
        "limitations": LIMITATIONS,
    }


def render_inventory_decision_report(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Inventory Decision Report",
        "",
        f"Status: **{report['report_status'].replace('_', ' ')}**",
        "",
        "## Review summary",
        "",
        f"- Products: {summary['products']}.",
        f"- Observed stock: {summary['stock_on_hand_units']} units.",
        (
            "- Replenishment review: "
            f"{summary['products_requiring_replenishment_review']} products."
        ),
        (
            "- Critical / high / watch / healthy: "
            f"{summary['critical_products']} / {summary['high_risk_products']} / "
            f"{summary['watch_products']} / {summary['healthy_products']}."
        ),
        f"- Suggested review quantity: {summary['suggested_review_quantity_units']} units.",
        "",
        "## Priority ranking",
        "",
        "| Rank | Product | Stock | Coverage | Reorder point | Suggested | Risk | Action |",
        "|---:|---|---:|---:|---:|---:|---|---|",
    ]
    for item in report["ranking"]:
        coverage = "n/a" if item["coverage_days"] is None else f"{item['coverage_days']:.2f} days"
        lines.append(
            f"| {item['priority_rank']} | {item['product_name']} | "
            f"{item['current_stock_units']} | {coverage} | "
            f"{item['reorder_point_units']} | {item['suggested_quantity_units']} | "
            f"{item['risk_label']} ({item['risk_score']:.1f}) | "
            f"{item['recommended_action']} |"
        )
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {limitation}" for limitation in report["limitations"])
    lines.extend(["", "The risk score is not a probability and no order was created.", ""])
    return "\n".join(lines)


def run_inventory_decision_report(project_root: Path) -> dict[str, Any]:
    """Generate canonical JSON, Markdown and tabular decision evidence."""
    from inventory_decision.recommendations import run_recommendation_cards
    from inventory_decision.reporting.snapshot_summary import run_snapshot_summary
    from inventory_decision.risk import run_risk_ranking

    snapshot_summary = run_snapshot_summary(project_root)
    ranking = run_risk_ranking(project_root)
    cards = run_recommendation_cards(project_root)
    manifest = json.loads(
        (
            project_root
            / "data"
            / "processed"
            / "inventory-decision"
            / "integration_manifest.json"
        ).read_text(encoding="utf-8")
    )
    report = build_inventory_decision_report(
        snapshot_summary=snapshot_summary,
        integration_manifest=manifest,
        ranking=ranking,
        cards_payload=cards,
    )
    output_root = project_root / "reports" / "outputs" / "inventory-decision"
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "inventory_decision_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    (output_root / "inventory_decision_report.md").write_text(
        render_inventory_decision_report(report), encoding="utf-8", newline="\n"
    )
    ranking.to_csv(output_root / "inventory_decisions.csv", index=False, lineterminator="\n")
    return report
