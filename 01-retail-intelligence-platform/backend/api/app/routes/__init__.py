"""HTTP routes exposed by the Retail Intelligence API."""

from .demand_summary import router as demand_summary_router

__all__ = ["demand_summary_router"]
