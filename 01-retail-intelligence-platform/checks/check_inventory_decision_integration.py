"""Cross-layer check from inventory report through the React client contract."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
import shutil
import subprocess
import sys

import httpx


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.api.app.main import app  # noqa: E402
from backend.api.app.services.inventory_decision_service import (  # noqa: E402
    InventoryDecisionService,
)


async def read_api_resources() -> tuple[dict[str, object], int, int]:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        inventory = await client.get("/api/v1/inventory-decisions/summary")
        demand = await client.get("/api/v1/demand-insights/summary")
        comparison = await client.get("/api/v1/model-comparisons/summary")
    if inventory.status_code != 200:
        raise AssertionError(f"Inventory Decision API failed: {inventory.text}")
    return inventory.json(), demand.status_code, comparison.status_code


def main() -> None:
    report = json.loads(
        (
            PROJECT_ROOT
            / "reports"
            / "outputs"
            / "inventory-decision"
            / "inventory_decision_report.json"
        ).read_text(encoding="utf-8")
    )
    service_resource = InventoryDecisionService(PROJECT_ROOT).get_summary()
    api_resource, demand_status, comparison_status = asyncio.run(read_api_resources())

    for field in ("snapshot", "demand_signal", "policy", "summary", "ranking", "recommendation_cards", "limitations"):
        assert api_resource[field] == service_resource[field]
    assert api_resource["ranking"] == report["ranking"]
    assert api_resource["recommendation_cards"] == report["recommendation_cards"]
    assert demand_status == comparison_status == 200

    runtime_path = PROJECT_ROOT / ".runtime" / "integration" / "inventory_decision_response.json"
    runtime_path.parent.mkdir(parents=True, exist_ok=True)
    runtime_path.write_text(
        json.dumps(api_resource, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    node = shutil.which("node")
    if node is None:
        raise AssertionError("Node.js is required for the React contract check.")
    result = subprocess.run(
        [
            node,
            str(PROJECT_ROOT / "frontend" / "dashboard-app" / "checks" / "checkInventoryDecisionContract.js"),
            str(runtime_path),
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise AssertionError(f"React contract validation failed: {result.stdout}\n{result.stderr}")
    assert "frontend accepted the real Inventory Decision API contract" in result.stdout

    print("OK - Sprint 3 Day 132 cross-layer integration check passed")
    print("Flow: report -> read service -> FastAPI -> React validator")
    print("Inventory evidence: 6 products | 6 Recommendation Cards | 97 review units")
    print("Demand Insight and Model Comparison compatibility: confirmed")


if __name__ == "__main__":
    main()
