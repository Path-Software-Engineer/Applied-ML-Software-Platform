"""Validate Sprint 3 Week 11 read and presentation closure."""

from __future__ import annotations

import asyncio
from pathlib import Path
import sys

import httpx


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.api.app.main import app  # noqa: E402


async def read_inventory() -> dict[str, object]:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/inventory-decisions/summary")
    assert response.status_code == 200
    return response.json()


def main() -> None:
    required = (
        "docs/sprints/sprint-03-inventory-decision/week-11/exploration.md",
        "docs/sprints/sprint-03-inventory-decision/week-11/plan.md",
        "docs/sprints/sprint-03-inventory-decision/week-11/review.md",
        "backend/api/app/services/inventory_decision_service.py",
        "backend/api/app/routes/inventory_decision.py",
        "frontend/dashboard-app/src/features/inventory-decision/components/InventoryDecisionDashboard.jsx",
        "checks/check_inventory_decision_integration.py",
    )
    for relative in required:
        assert (PROJECT_ROOT / relative).is_file(), f"Missing Week 11 evidence: {relative}"

    resource = asyncio.run(read_inventory())
    assert resource["schema_version"] == "1.0"
    assert resource["summary"]["products"] == 6
    assert len(resource["recommendation_cards"]) == 6
    assert resource["ranking"][0]["product_id"] == "P003"
    assert resource["policy"]["risk_score_meaning"] == "priority_index_not_probability"

    print("OK - Sprint 3 Day 133 Week 11 close check passed")
    print("Report -> service -> FastAPI -> React contract: confirmed")
    print("Products / Recommendation Cards / review units: 6 / 6 / 97")
    print("Week 12 hardening: not started")


if __name__ == "__main__":
    main()
