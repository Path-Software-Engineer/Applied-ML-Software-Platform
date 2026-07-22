"""Generate a factual inventory snapshot summary before decision policies."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def build_snapshot_summary(joined: pd.DataFrame) -> dict[str, Any]:
    """Summarize validated facts without classifying inventory risk."""
    required = {
        "snapshot_id",
        "snapshot_as_of_date",
        "observed_at",
        "freshness_days",
        "product_id",
        "stock_on_hand",
        "stock_unit",
        "lead_time_days",
        "signal_type",
        "signal_value",
        "signal_unit",
        "period_start",
        "period_end",
    }
    missing = sorted(required - set(joined.columns))
    if missing:
        raise ValueError(f"Snapshot summary is missing columns: {missing}")
    if joined.empty:
        raise ValueError("Snapshot summary requires product rows.")

    snapshot_dates = pd.to_datetime(joined["snapshot_as_of_date"], errors="coerce")
    observed_dates = pd.to_datetime(joined["observed_at"], errors="coerce")
    if snapshot_dates.isna().any() or observed_dates.isna().any():
        raise ValueError("Snapshot summary dates are invalid.")

    return {
        "schema_version": "1.0",
        "module": "inventory_decision",
        "summary_type": "validated_snapshot_facts",
        "snapshot": {
            "snapshot_id": str(joined["snapshot_id"].iloc[0]),
            "as_of_date": snapshot_dates.iloc[0].date().isoformat(),
            "products": int(len(joined)),
            "stock_on_hand_units": int(joined["stock_on_hand"].sum()),
            "zero_stock_products": int((joined["stock_on_hand"] == 0).sum()),
            "oldest_observation_date": observed_dates.min().date().isoformat(),
            "maximum_freshness_days": int(joined["freshness_days"].max()),
            "products_missing_source_lead_time": int(joined["lead_time_days"].isna().sum()),
        },
        "demand_signal": {
            "signal_type": str(joined["signal_type"].iloc[0]),
            "signal_unit": str(joined["signal_unit"].iloc[0]),
            "period_start": str(joined["period_start"].iloc[0]),
            "period_end": str(joined["period_end"].iloc[0]),
            "products": int(joined["product_id"].nunique()),
        },
        "coverage": {
            "inventory_products": int(joined["product_id"].nunique()),
            "signal_products": int(joined["product_id"].nunique()),
            "joined_products": int(len(joined)),
            "unmatched_products": 0,
        },
        "anomalies": [
            {
                "code": "SOURCE_LEAD_TIME_MISSING",
                "products": int(joined["lead_time_days"].isna().sum()),
                "meaning": "A later versioned policy must declare any default lead time.",
            },
            {
                "code": "ZERO_STOCK_OBSERVED",
                "products": int((joined["stock_on_hand"] == 0).sum()),
                "meaning": "Observed fact only; risk and action are not assigned in this summary.",
            },
        ],
        "decision_status": "not_calculated",
        "evidence_status": "descriptive_learning_evidence",
    }


def render_snapshot_summary(summary: dict[str, Any]) -> str:
    snapshot = summary["snapshot"]
    signal = summary["demand_signal"]
    coverage = summary["coverage"]
    return "\n".join(
        [
            "# Inventory Snapshot Summary",
            "",
            f"- Snapshot: `{snapshot['snapshot_id']}` as of {snapshot['as_of_date']}.",
            f"- Products: {snapshot['products']}.",
            f"- Observed stock: {snapshot['stock_on_hand_units']} units.",
            f"- Zero-stock observations: {snapshot['zero_stock_products']}.",
            f"- Maximum source freshness: {snapshot['maximum_freshness_days']} days.",
            f"- Products without source lead time: {snapshot['products_missing_source_lead_time']}.",
            f"- Demand signal: `{signal['signal_type']}` in `{signal['signal_unit']}`.",
            f"- Signal period: {signal['period_start']} through {signal['period_end']}.",
            (
                "- Product coverage: "
                f"{coverage['inventory_products']} inventory / "
                f"{coverage['signal_products']} signal / "
                f"{coverage['joined_products']} joined / "
                f"{coverage['unmatched_products']} unmatched."
            ),
            "",
            "## Evidence boundary",
            "",
            "These are validated snapshot facts. Reorder points, risk labels and",
            "recommendations have not been calculated in this artifact.",
            "",
        ]
    )


def run_snapshot_summary(project_root: Path) -> dict[str, Any]:
    """Generate official factual JSON and Markdown summary artifacts."""
    from inventory_decision.signals import run_signal_integration

    _, joined, _ = run_signal_integration(project_root)
    summary = build_snapshot_summary(joined)
    output_root = project_root / "reports" / "summaries" / "inventory-decision"
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "inventory_snapshot_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    (output_root / "inventory_snapshot_summary.md").write_text(
        render_snapshot_summary(summary), encoding="utf-8", newline="\n"
    )
    return summary
