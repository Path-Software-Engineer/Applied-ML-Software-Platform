"""Readable Day 129 HTTP and OpenAPI validation for Inventory Decision."""

from __future__ import annotations

import asyncio
from pathlib import Path
import sys

import httpx


PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.api.app.main import app  # noqa: E402


async def validate() -> tuple[dict[str, object], dict[str, object]]:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/inventory-decisions/summary")
        schema = (await client.get("/openapi.json")).json()
    assert response.status_code == 200
    return response.json(), schema


def main() -> None:
    payload, schema = asyncio.run(validate())
    operation = schema["paths"]["/api/v1/inventory-decisions/summary"]["get"]

    assert payload["schema_version"] == "1.0"
    assert payload["module"] == "inventory_decision"
    assert payload["summary"]["products"] == 6
    assert payload["freshness"]["status"] == "stale"
    assert operation["tags"] == ["Inventory Decision"]
    assert "503" in operation["responses"]

    print("OK - Sprint 3 Day 129 Inventory Decision API check passed")
    print("GET /api/v1/inventory-decisions/summary: 200")
    print("Schema / products / freshness: 1.0 / 6 / stale")
    print("OpenAPI and safe 503 contract: confirmed")


if __name__ == "__main__":
    main()
