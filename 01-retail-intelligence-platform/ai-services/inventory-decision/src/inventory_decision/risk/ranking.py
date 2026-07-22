"""Assign stable risk labels, actions, reasons and deterministic priority."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from inventory_decision.risk.scoring import RiskInputError


def classify_risk(score: float) -> tuple[str, str]:
    """Map the frozen priority-index thresholds to label and review action."""
    if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 100:
        raise RiskInputError("risk_score must be numeric between 0 and 100.")
    if score >= 75:
        return "critical", "replenish_now"
    if score >= 50:
        return "high", "replenish_soon"
    if score >= 25:
        return "watch", "review"
    return "healthy", "monitor"


def risk_reason(record: dict[str, object], label: str) -> str:
    """Build one evidence-backed reason without claiming causality."""
    if label == "critical" and int(record["current_stock_units"]) == 0:
        return "Observed stock is zero while observed demand is positive."
    if label in {"critical", "high"}:
        return (
            f"Observed stock covers {float(record['coverage_days']):.2f} days, "
            f"below the {int(record['lead_time_days']) + int(record['safety_days'])}-day "
            "protected horizon."
        )
    if label == "watch":
        return "Observed stock is at or below the policy reorder point."
    return "Observed stock remains above the policy reorder point."


def rank_inventory_risk(scored: pd.DataFrame) -> pd.DataFrame:
    """Classify and rank products with a stable documented tie-break."""
    required = {
        "product_id",
        "current_stock_units",
        "coverage_days",
        "risk_score",
        "reorder_required",
        "lead_time_days",
        "safety_days",
    }
    missing = sorted(required - set(scored.columns))
    if missing:
        raise RiskInputError(f"Risk ranking input is missing columns: {missing}")
    if scored["product_id"].duplicated().any():
        raise RiskInputError("Risk ranking requires unique product_id values.")

    output = scored.copy(deep=True)
    classifications = output["risk_score"].map(classify_risk)
    output["risk_label"] = classifications.map(lambda value: value[0])
    output["recommended_action"] = classifications.map(lambda value: value[1])
    output["reason"] = [
        risk_reason(record, label)
        for record, label in zip(
            output.to_dict(orient="records"), output["risk_label"], strict=True
        )
    ]
    output["_coverage_sort"] = output["coverage_days"].fillna(float("inf"))
    output = output.sort_values(
        ["risk_score", "_coverage_sort", "product_id"],
        ascending=[False, True, True],
        kind="stable",
    ).drop(columns=["_coverage_sort"]).reset_index(drop=True)
    output.insert(0, "priority_rank", range(1, len(output) + 1))
    return output


def run_risk_ranking(project_root: Path) -> pd.DataFrame:
    """Generate the official product risk ranking."""
    from inventory_decision.risk.scoring import run_risk_scoring

    ranked = rank_inventory_risk(run_risk_scoring(project_root))
    output_root = project_root / "reports" / "metrics" / "inventory-decision"
    output_root.mkdir(parents=True, exist_ok=True)
    ranked.to_csv(output_root / "risk_ranking.csv", index=False, lineterminator="\n")
    return ranked
