"""HTTP contract tests for the Inventory Decision summary API."""

from __future__ import annotations

import asyncio
from copy import deepcopy
from datetime import date
from pathlib import Path

import httpx
from pydantic import ValidationError
import pytest

from backend.api.app.main import app
from backend.api.app.routes.inventory_decision import get_inventory_decision_service
from backend.api.app.schemas.inventory_decision import InventoryDecisionResponse
from backend.api.app.services.inventory_decision_service import (
    InventoryDecisionError,
    InventoryDecisionService,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def sample_response() -> dict[str, object]:
    return InventoryDecisionService(PROJECT_ROOT).get_summary(
        today=date(2026, 1, 12)
    )


class StubService:
    def get_summary(self) -> dict[str, object]:
        return sample_response()


class UnavailableService:
    def get_summary(self) -> dict[str, object]:
        raise InventoryDecisionError("private artifact path and parser detail")


async def request(path: str) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.get(path)


def test_inventory_endpoint_returns_versioned_contract() -> None:
    app.dependency_overrides[get_inventory_decision_service] = StubService
    try:
        response = asyncio.run(request("/api/v1/inventory-decisions/summary"))
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == sample_response()


def test_inventory_endpoint_maps_service_error_to_safe_503() -> None:
    app.dependency_overrides[get_inventory_decision_service] = UnavailableService
    try:
        response = asyncio.run(request("/api/v1/inventory-decisions/summary"))
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Inventory Decision evidence is unavailable or invalid."
    }
    assert "private artifact path" not in response.text


def test_inventory_schema_rejects_extra_fields() -> None:
    payload = deepcopy(sample_response())
    payload["unexpected"] = True

    with pytest.raises(ValidationError):
        InventoryDecisionResponse.model_validate(payload)


def test_inventory_schema_rejects_negative_suggested_quantity() -> None:
    payload = deepcopy(sample_response())
    payload["ranking"][0]["suggested_quantity_units"] = -1

    with pytest.raises(ValidationError):
        InventoryDecisionResponse.model_validate(payload)


def test_inventory_schema_rejects_probability_semantics() -> None:
    payload = deepcopy(sample_response())
    payload["recommendation_cards"][0]["risk"]["meaning"] = "probability"

    with pytest.raises(ValidationError):
        InventoryDecisionResponse.model_validate(payload)


def test_openapi_exposes_inventory_decision_resource() -> None:
    schema = asyncio.run(request("/openapi.json")).json()

    operation = schema["paths"]["/api/v1/inventory-decisions/summary"]["get"]
    assert operation["tags"] == ["Inventory Decision"]
    assert "200" in operation["responses"]
    assert "503" in operation["responses"]
    assert "InventoryDecisionResponse" in schema["components"]["schemas"]
