"""Build versioned Recommendation Cards from ranked inventory evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


CARD_SCHEMA_VERSION = "1.0"
LIMITATION = (
    "Learning evidence from a small synthetic period; review current stock, "
    "supplier lead time and recent demand before acting."
)


def _optional_number(value: object) -> float | None:
    return None if pd.isna(value) else float(value)


def _iso_date(value: object) -> str:
    """Serialize date-like evidence without inventing a time component."""
    if isinstance(value, pd.Timestamp):
        return value.date().isoformat()
    if hasattr(value, "isoformat"):
        return str(value.isoformat()).split("T", maxsplit=1)[0]
    return str(value).split("T", maxsplit=1)[0]


def build_recommendation_cards(ranked: pd.DataFrame) -> dict[str, Any]:
    """Map ranked policy evidence into an auditable presentation contract."""
    required = {
        "priority_rank",
        "product_id",
        "product_name",
        "risk_label",
        "risk_score",
        "risk_score_meaning",
        "current_stock_units",
        "observed_daily_demand",
        "demand_signal_type",
        "coverage_days",
        "reorder_point_units",
        "target_stock_units",
        "lead_time_days",
        "lead_time_source",
        "period_start",
        "period_end",
        "snapshot_as_of_date",
        "recommended_action",
        "suggested_quantity_units",
        "reason",
        "policy_version",
    }
    missing = sorted(required - set(ranked.columns))
    if missing:
        raise ValueError(f"Recommendation Card input is missing columns: {missing}")
    if ranked.empty or ranked["product_id"].duplicated().any():
        raise ValueError("Recommendation Cards require unique product rows.")

    cards: list[dict[str, Any]] = []
    for record in ranked.to_dict(orient="records"):
        cards.append(
            {
                "card_id": f"inventory-{record['product_id']}",
                "priority_rank": int(record["priority_rank"]),
                "product": {
                    "product_id": record["product_id"],
                    "product_name": record["product_name"],
                },
                "risk": {
                    "label": record["risk_label"],
                    "score": float(record["risk_score"]),
                    "meaning": record["risk_score_meaning"],
                },
                "evidence": {
                    "current_stock_units": int(record["current_stock_units"]),
                    "observed_daily_demand": float(record["observed_daily_demand"]),
                    "demand_signal_type": record["demand_signal_type"],
                    "coverage_days": _optional_number(record["coverage_days"]),
                    "reorder_point_units": int(record["reorder_point_units"]),
                    "target_stock_units": int(record["target_stock_units"]),
                    "lead_time_days": int(record["lead_time_days"]),
                    "lead_time_source": record["lead_time_source"],
                    "observed_period": {
                        "start": record["period_start"],
                        "end": record["period_end"],
                    },
                    "snapshot_as_of_date": _iso_date(record["snapshot_as_of_date"]),
                },
                "action": {
                    "code": record["recommended_action"],
                    "suggested_quantity_units": int(record["suggested_quantity_units"]),
                    "unit": "units",
                },
                "reason": record["reason"],
                "limitation": LIMITATION,
                "policy_version": record["policy_version"],
            }
        )

    card_ids = [card["card_id"] for card in cards]
    if len(card_ids) != len(set(card_ids)):
        raise ValueError("Recommendation Card identifiers must be unique.")
    return {
        "schema_version": CARD_SCHEMA_VERSION,
        "module": "inventory_decision",
        "policy_version": "inventory-review-policy/1.0",
        "cards": cards,
    }


def render_recommendation_cards(payload: dict[str, Any]) -> str:
    lines = ["# Inventory Recommendation Cards", ""]
    for card in payload["cards"]:
        evidence = card["evidence"]
        action = card["action"]
        lines.extend(
            [
                f"## {card['priority_rank']:02d} — {card['product']['product_name']}",
                "",
                f"- Risk: **{card['risk']['label']}** ({card['risk']['score']:.1f}/100 priority index).",
                f"- Stock / reorder point: {evidence['current_stock_units']} / {evidence['reorder_point_units']} units.",
                f"- Action: `{action['code']}`; suggested review quantity {action['suggested_quantity_units']} units.",
                f"- Reason: {card['reason']}",
                f"- Policy: `{card['policy_version']}`.",
                f"- Limitation: {card['limitation']}",
                "",
            ]
        )
    return "\n".join(lines)


def run_recommendation_cards(project_root: Path) -> dict[str, Any]:
    """Generate official structured and human-readable Recommendation Cards."""
    from inventory_decision.risk import run_risk_ranking

    payload = build_recommendation_cards(run_risk_ranking(project_root))
    output_root = (
        project_root
        / "reports"
        / "recommendation-cards"
        / "inventory-decision"
    )
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "recommendation_cards.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    (output_root / "recommendation_cards.md").write_text(
        render_recommendation_cards(payload), encoding="utf-8", newline="\n"
    )
    return payload
