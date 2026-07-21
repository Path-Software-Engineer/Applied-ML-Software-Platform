"""Manual in-process check for the Model Comparison API."""

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
        response = await client.get("/api/v1/model-comparisons/summary")
        openapi = await client.get("/openapi.json")

    if response.status_code != 200:
        raise AssertionError(f"Unexpected Model Comparison response: {response.text}")
    payload = response.json()
    if payload["schema_version"] != "1.0":
        raise AssertionError("Unexpected Model Comparison schema version.")
    if len(payload["candidates"]) != 4 or len(payload["decision_cards"]) != 3:
        raise AssertionError("Unexpected Model Comparison collection sizes.")
    if payload["decision"]["selected_candidate"]["model_id"] != "random_forest":
        raise AssertionError("Unexpected selected integration candidate.")
    path = "/api/v1/model-comparisons/summary"
    if openapi.status_code != 200 or path not in openapi.json()["paths"]:
        raise AssertionError("Model Comparison resource is missing from OpenAPI.")

    print("OK - Sprint 2 Day 73 Model Comparison API check passed")
    print("GET /api/v1/model-comparisons/summary: 200")
    print("Schema version: 1.0")
    print("Candidates / Decision Cards: 4 / 3")
    print("OpenAPI contract: confirmed")


def main() -> None:
    asyncio.run(check_api())


if __name__ == "__main__":
    main()
