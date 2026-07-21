"""Cross-layer Day 76 check from analytical report through the React client."""

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
from backend.api.app.services.model_comparison_service import (  # noqa: E402
    PUBLIC_CANDIDATE_FIELDS,
    ModelComparisonService,
)


async def read_api_resources() -> tuple[dict[str, object], dict[str, object]]:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        comparison = await client.get("/api/v1/model-comparisons/summary")
        demand = await client.get("/api/v1/demand-insights/summary")
    if comparison.status_code != 200:
        raise AssertionError(f"Model Comparison API failed: {comparison.text}")
    if demand.status_code != 200:
        raise AssertionError(f"Demand Insight compatibility failed: {demand.text}")
    return comparison.json(), demand.json()


def main() -> None:
    report_path = (
        PROJECT_ROOT
        / "reports"
        / "outputs"
        / "model-comparison"
        / "model_comparison_report.json"
    )
    report = json.loads(report_path.read_text(encoding="utf-8"))
    service_resource = ModelComparisonService(PROJECT_ROOT).get_summary()
    api_resource, demand_resource = asyncio.run(read_api_resources())

    expected_candidates = [
        {field: row[field] for field in PUBLIC_CANDIDATE_FIELDS}
        for row in report["comparison"]["rows"]
    ]
    assert service_resource["candidates"] == expected_candidates
    assert service_resource["decision_cards"] == report["decision_cards"]
    assert api_resource == service_resource
    assert demand_resource["sales_summary"]["total_units_sold"] == 293
    assert demand_resource["sales_summary"]["total_revenue"] == 747.65

    runtime_path = (
        PROJECT_ROOT
        / ".runtime"
        / "integration"
        / "model_comparison_response.json"
    )
    runtime_path.parent.mkdir(parents=True, exist_ok=True)
    runtime_path.write_text(
        json.dumps(api_resource, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    node = shutil.which("node")
    if node is None:
        raise AssertionError("Node.js is required for the React contract check.")
    frontend_check = (
        PROJECT_ROOT
        / "frontend"
        / "dashboard-app"
        / "checks"
        / "checkModelComparisonContract.js"
    )
    result = subprocess.run(
        [node, str(frontend_check), str(runtime_path)],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise AssertionError(
            "React contract validation failed: "
            f"{result.stdout}\n{result.stderr}"
        )
    if "frontend accepted the real Model Comparison API contract" not in result.stdout:
        raise AssertionError("Frontend contract confirmation is missing.")

    print("OK - Sprint 2 Day 76 cross-layer integration check passed")
    print("Flow: report -> read service -> FastAPI -> React validator")
    print("Model Comparison response equality: confirmed")
    print("Demand Insight compatibility: 293 units | 747.65 revenue")
    print("Frontend contract: accepted real API response")


if __name__ == "__main__":
    main()
