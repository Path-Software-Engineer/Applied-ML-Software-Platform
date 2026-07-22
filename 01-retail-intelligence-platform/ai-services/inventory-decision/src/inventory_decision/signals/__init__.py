"""Observed-demand signal and inventory integration boundary."""

from .observed_demand import (
    DemandSignalError,
    build_observed_demand_signals,
    join_inventory_and_signals,
    run_signal_integration,
)

__all__ = [
    "DemandSignalError",
    "build_observed_demand_signals",
    "join_inventory_and_signals",
    "run_signal_integration",
]
