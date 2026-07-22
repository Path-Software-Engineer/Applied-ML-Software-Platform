"""Calculate stock coverage and an explainable non-probabilistic priority index."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd


class RiskInputError(ValueError):
    """Raised when inventory risk inputs are incompatible or invalid."""


@dataclass(frozen=True)
class RiskResult:
    coverage_days: float | None
    shortage_ratio: float
    coverage_pressure: float
    risk_score: float
    risk_score_meaning: str


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def calculate_risk(
    *,
    stock_on_hand: int,
    observed_units: int,
    observation_days: int,
    lead_time_days: int,
    safety_days: int,
    reorder_point_units: int,
    reorder_required: bool,
) -> RiskResult:
    """Calculate priority using shortage and coverage pressure under policy 1.0."""
    integer_values = {
        "stock_on_hand": stock_on_hand,
        "observed_units": observed_units,
        "observation_days": observation_days,
        "lead_time_days": lead_time_days,
        "safety_days": safety_days,
        "reorder_point_units": reorder_point_units,
    }
    if any(isinstance(value, bool) or not isinstance(value, int) for value in integer_values.values()):
        raise RiskInputError("Risk quantities and horizons must be integers.")
    if stock_on_hand < 0 or observed_units < 0 or reorder_point_units < 0:
        raise RiskInputError("Risk quantities must be non-negative.")
    if observation_days <= 0 or lead_time_days <= 0 or safety_days < 0:
        raise RiskInputError("Risk horizons are invalid.")
    if not isinstance(reorder_required, bool):
        raise RiskInputError("reorder_required must be boolean.")

    if observed_units == 0:
        return RiskResult(
            coverage_days=None,
            shortage_ratio=0.0,
            coverage_pressure=0.0,
            risk_score=0.0,
            risk_score_meaning="priority_index_not_probability",
        )

    daily_demand = observed_units / observation_days
    coverage_days = stock_on_hand / daily_demand
    shortage_ratio = _clamp(
        (reorder_point_units - stock_on_hand) / max(reorder_point_units, 1)
    )
    protected_horizon = lead_time_days + safety_days
    coverage_pressure = _clamp(
        (protected_horizon - coverage_days) / protected_horizon
    )
    score = round(100 * (0.7 * shortage_ratio + 0.3 * coverage_pressure), 1)
    if stock_on_hand == 0:
        score = 100.0
    elif reorder_required:
        score = max(25.0, score)

    return RiskResult(
        coverage_days=round(coverage_days, 4),
        shortage_ratio=round(shortage_ratio, 4),
        coverage_pressure=round(coverage_pressure, 4),
        risk_score=score,
        risk_score_meaning="priority_index_not_probability",
    )


def apply_risk_scoring(replenishment: pd.DataFrame) -> pd.DataFrame:
    """Append risk measures while preserving replenishment evidence."""
    required = {
        "current_stock_units",
        "observed_units",
        "observation_days",
        "lead_time_days",
        "safety_days",
        "reorder_point_units",
        "reorder_required",
    }
    missing = sorted(required - set(replenishment.columns))
    if missing:
        raise RiskInputError(f"Risk input is missing columns: {missing}")

    rows: list[dict[str, object]] = []
    for record in replenishment.to_dict(orient="records"):
        result = calculate_risk(
            stock_on_hand=int(record["current_stock_units"]),
            observed_units=int(record["observed_units"]),
            observation_days=int(record["observation_days"]),
            lead_time_days=int(record["lead_time_days"]),
            safety_days=int(record["safety_days"]),
            reorder_point_units=int(record["reorder_point_units"]),
            reorder_required=bool(record["reorder_required"]),
        )
        rows.append({**record, **asdict(result)})
    return pd.DataFrame(rows).sort_values("product_id", kind="stable").reset_index(drop=True)


def run_risk_scoring(project_root: Path) -> pd.DataFrame:
    """Generate official coverage and priority-index evidence."""
    from inventory_decision.policies import run_replenishment_policy

    replenishment = run_replenishment_policy(project_root)
    results = apply_risk_scoring(replenishment)
    output = (
        project_root
        / "data"
        / "processed"
        / "inventory-decision"
        / "inventory_risk_scores.csv"
    )
    results.to_csv(output, index=False, lineterminator="\n")
    return results
