"""Manual in-process check for the Day 24 Demand Summary API."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import httpx


PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.api.app.main import app  # noqa: E402


async def check_api() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        health = await client.get("/health")
        response = await client.get("/api/v1/demand-insights/summary")
        openapi = await client.get("/openapi.json")

    if health.status_code != 200 or health.json().get("status") != "ok":
        raise AssertionError(f"Unexpected health response: {health.text}")
    if response.status_code != 200:
        raise AssertionError(f"Unexpected Demand Summary response: {response.text}")
    payload = response.json()
    if payload["schema_version"] != "1.0":
        raise AssertionError("Unexpected Demand Summary schema version.")
    if payload["sales_summary"]["total_units_sold"] != 293:
        raise AssertionError("Unexpected API units total.")
    if payload["sales_summary"]["total_revenue"] != 747.65:
        raise AssertionError("Unexpected API revenue total.")
    if len(payload["insight_cards"]) != 5:
        raise AssertionError("API must expose five Insight Cards.")
    if openapi.status_code != 200:
        raise AssertionError("OpenAPI schema is unavailable.")
    if "/api/v1/demand-insights/summary" not in openapi.json()["paths"]:
        raise AssertionError("Demand Summary resource is missing from OpenAPI.")

    print("OK - Day 24 Demand Summary API check passed")
    print("GET /health: 200")
    print("GET /api/v1/demand-insights/summary: 200")
    print("Schema version: 1.0")
    print("Totals: 293 units | 747.65 revenue")
    print("Insight Cards: 5")
    print("OpenAPI contract: confirmed")


def main() -> None:
    asyncio.run(check_api())


if __name__ == "__main__":
    main()
