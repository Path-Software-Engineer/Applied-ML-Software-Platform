"""Validate three-module contracts, navigation and unified generation commands."""

from __future__ import annotations

import asyncio
from pathlib import Path
import sys

import httpx


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.api.app.main import app  # noqa: E402


async def read_resources() -> dict[str, dict[str, object]]:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        responses = {
            "demand": await client.get("/api/v1/demand-insights/summary"),
            "comparison": await client.get("/api/v1/model-comparisons/summary"),
            "inventory": await client.get("/api/v1/inventory-decisions/summary"),
        }
    assert all(response.status_code == 200 for response in responses.values())
    return {name: response.json() for name, response in responses.items()}


def main() -> None:
    resources = asyncio.run(read_resources())
    assert resources["demand"]["schema_version"] == "1.0"
    assert resources["comparison"]["schema_version"] == "1.0"
    assert resources["inventory"]["schema_version"] == "1.0"
    assert resources["demand"]["sales_summary"]["total_units_sold"] == 293
    assert resources["comparison"]["decision"]["selected_candidate"]["model_id"] == "random_forest"
    assert resources["inventory"]["summary"]["suggested_review_quantity_units"] == 97

    generator = (PROJECT_ROOT / "scripts/generate-platform-evidence.ps1").read_text(encoding="utf-8")
    navigation = (PROJECT_ROOT / "frontend/dashboard-app/src/shared/navigation/platformNavigation.js").read_text(encoding="utf-8")
    for phrase in ("Demand Insight", "Model Comparison", "Inventory Decision"):
        assert phrase in generator
    for stage_id in ("demand-insight", "model-comparison", "inventory-decision"):
        assert stage_id in navigation

    print("OK - Sprint 3 Day 142 platform integration check passed")
    print("Resources: Demand Insight | Model Comparison | Inventory Decision")
    print("Contract version: 1.0 across three modules")
    print("Unified evidence generation and staged navigation: confirmed")


if __name__ == "__main__":
    main()
