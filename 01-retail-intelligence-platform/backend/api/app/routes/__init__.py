"""HTTP routes exposed by the Retail Intelligence API."""

from .demand_summary import router as demand_summary_router
from .model_comparison import router as model_comparison_router
from .inventory_decision import router as inventory_decision_router

__all__ = [
    "demand_summary_router",
    "inventory_decision_router",
    "model_comparison_router",
]
