"""Pure reorder-point and target-stock calculations for policy 1.0."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from math import ceil
from pathlib import Path

import pandas as pd


class PolicyError(ValueError):
    """Raised when policy inputs or configuration are invalid."""


@dataclass(frozen=True)
class InventoryPolicy:
    version: str
    default_lead_time_days: int
    safety_days: int
    review_period_days: int
    rounding: str
    reorder_trigger: str


DEFAULT_INVENTORY_POLICY = InventoryPolicy(
    version="inventory-review-policy/1.0",
    default_lead_time_days=2,
    safety_days=1,
    review_period_days=3,
    rounding="ceiling_to_whole_units",
    reorder_trigger="stock_at_or_below_reorder_point",
)


@dataclass(frozen=True)
class ReplenishmentResult:
    lead_time_days: int
    lead_time_source: str
    reorder_point_units: int
    target_stock_units: int
    reorder_required: bool
    suggested_quantity_units: int
    policy_version: str


def _positive_integer(value: object, *, field: str) -> int:
    if isinstance(value, bool):
        raise PolicyError(f"{field} must be a positive integer.")
    try:
        parsed = int(value)
    except (TypeError, ValueError) as error:
        raise PolicyError(f"{field} must be a positive integer.") from error
    if parsed <= 0 or parsed != value:
        raise PolicyError(f"{field} must be a positive integer.")
    return parsed


def calculate_replenishment(
    *,
    stock_on_hand: int,
    observed_units: int,
    observation_days: int,
    source_lead_time_days: int | None,
    policy: InventoryPolicy = DEFAULT_INVENTORY_POLICY,
) -> ReplenishmentResult:
    """Calculate whole-unit replenishment from an exact observed-demand ratio."""
    if isinstance(stock_on_hand, bool) or not isinstance(stock_on_hand, int) or stock_on_hand < 0:
        raise PolicyError("stock_on_hand must be a non-negative integer.")
    if isinstance(observed_units, bool) or not isinstance(observed_units, int) or observed_units < 0:
        raise PolicyError("observed_units must be a non-negative integer.")
    observation_days = _positive_integer(observation_days, field="observation_days")
    if policy.default_lead_time_days <= 0 or policy.safety_days < 0 or policy.review_period_days < 0:
        raise PolicyError("Policy horizons must be non-negative with positive lead time.")

    if source_lead_time_days is None or pd.isna(source_lead_time_days):
        lead_time_days = policy.default_lead_time_days
        lead_time_source = "policy_default"
    else:
        lead_time_days = _positive_integer(
            source_lead_time_days, field="source_lead_time_days"
        )
        lead_time_source = "source"

    daily_demand = Fraction(observed_units, observation_days)
    reorder_point = ceil(
        daily_demand * (lead_time_days + policy.safety_days)
    )
    target_stock = ceil(
        daily_demand
        * (lead_time_days + policy.safety_days + policy.review_period_days)
    )
    reorder_required = observed_units > 0 and stock_on_hand <= reorder_point
    suggested_quantity = (
        max(0, target_stock - stock_on_hand) if reorder_required else 0
    )
    return ReplenishmentResult(
        lead_time_days=lead_time_days,
        lead_time_source=lead_time_source,
        reorder_point_units=reorder_point,
        target_stock_units=target_stock,
        reorder_required=reorder_required,
        suggested_quantity_units=suggested_quantity,
        policy_version=policy.version,
    )


def apply_replenishment_policy(
    joined: pd.DataFrame,
    *,
    policy: InventoryPolicy = DEFAULT_INVENTORY_POLICY,
) -> pd.DataFrame:
    """Apply the pure calculation to validated joined product evidence."""
    required = {
        "product_id",
        "product_name",
        "stock_on_hand",
        "stock_unit",
        "lead_time_days",
        "signal_type",
        "signal_value",
        "signal_unit",
        "observed_units",
        "observation_days",
    }
    missing = sorted(required - set(joined.columns))
    if missing:
        raise PolicyError(f"Replenishment input is missing columns: {missing}")

    rows: list[dict[str, object]] = []
    for record in joined.to_dict(orient="records"):
        result = calculate_replenishment(
            stock_on_hand=int(record["stock_on_hand"]),
            observed_units=int(record["observed_units"]),
            observation_days=int(record["observation_days"]),
            source_lead_time_days=record["lead_time_days"],
            policy=policy,
        )
        rows.append(
            {
                "product_id": record["product_id"],
                "product_name": record["product_name"],
                "current_stock_units": int(record["stock_on_hand"]),
                "stock_unit": record["stock_unit"],
                "observed_daily_demand": float(record["signal_value"]),
                "demand_signal_type": record["signal_type"],
                "demand_signal_unit": record["signal_unit"],
                "observed_units": int(record["observed_units"]),
                "observation_days": int(record["observation_days"]),
                "safety_days": policy.safety_days,
                "review_period_days": policy.review_period_days,
                **asdict(result),
            }
        )
    return pd.DataFrame(rows).sort_values("product_id", kind="stable").reset_index(drop=True)


def run_replenishment_policy(project_root: Path) -> pd.DataFrame:
    """Generate official product-level replenishment evidence."""
    from inventory_decision.signals import run_signal_integration

    _, joined, _ = run_signal_integration(project_root)
    results = apply_replenishment_policy(joined)
    output = (
        project_root
        / "data"
        / "processed"
        / "inventory-decision"
        / "inventory_replenishment.csv"
    )
    results.to_csv(output, index=False, lineterminator="\n")
    return results
