"""HTTP contract tests for the Demand Summary API."""

from __future__ import annotations

import asyncio
from pathlib import Path

import httpx

from backend.api.app.main import app
from backend.api.app.routes.demand_summary import (
    get_demand_figure_service,
    get_demand_summary_service,
)
from backend.api.app.services.demand_figure_service import (
    PNG_SIGNATURE,
    DemandFigureError,
    UnknownDemandFigureError,
)
from backend.api.app.services.demand_summary_service import DemandSummaryError


def sample_response() -> dict[str, object]:
    card = {
        "card_id": "observed-demand",
        "title": "Observed demand",
        "metric": "30 units",
        "insight": "A controlled result.",
        "recommendation": "Review with more periods.",
        "limitation": "Observed period only.",
    }
    card_ids = (
        "observed-demand",
        "top-product-units",
        "top-product-revenue",
        "top-day-units",
        "top-day-revenue",
    )
    cards = [{**card, "card_id": card_id} for card_id in card_ids]
    return {
        "schema_version": "1.0",
        "period": {
            "start_date": "2026-02-01",
            "end_date": "2026-02-02",
            "observed_days": 2,
        },
        "sales_summary": {
            "total_units_sold": 30,
            "total_revenue": 75.5,
            "sales_count": 2,
            "unique_products": 2,
            "unique_categories": 1,
        },
        "baseline": {"mean_units_prediction": 15.0, "mae": 4.0},
        "leaders": {
            "product_by_units": {"name": "Bread", "value": 20, "unit": "units"},
            "product_by_revenue": {"name": "Milk", "value": 45.5, "unit": "revenue"},
            "date_by_units": {"name": "2026-02-02", "value": 18, "unit": "units"},
            "date_by_revenue": {"name": "2026-02-02", "value": 42.5, "unit": "revenue"},
        },
        "insight_cards": cards,
        "limitations": ["Observed sales only."],
    }


class StubService:
    def get_summary(self) -> dict[str, object]:
        return sample_response()


class UnavailableService:
    def get_summary(self) -> dict[str, object]:
        raise DemandSummaryError("private artifact detail")


class StubFigureService:
    def __init__(self, path: Path) -> None:
        self.path = path

    def get_figure_path(self, figure_id: str) -> Path:
        assert figure_id == "daily-sales"
        return self.path


class UnknownFigureService:
    def get_figure_path(self, figure_id: str) -> Path:
        raise UnknownDemandFigureError(f"private unknown detail: {figure_id}")


class UnavailableFigureService:
    def get_figure_path(self, figure_id: str) -> Path:
        raise DemandFigureError(f"private path detail: {figure_id}")


async def request(path: str) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        return await client.get(path)


def test_health_endpoint_reports_process_health() -> None:
    response = asyncio.run(request("/health"))

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "retail-intelligence-api",
    }


def test_demand_summary_endpoint_returns_versioned_contract() -> None:
    app.dependency_overrides[get_demand_summary_service] = StubService
    try:
        response = asyncio.run(request("/api/v1/demand-insights/summary"))
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == sample_response()


def test_demand_summary_endpoint_maps_service_error_to_503() -> None:
    app.dependency_overrides[get_demand_summary_service] = UnavailableService
    try:
        response = asyncio.run(request("/api/v1/demand-insights/summary"))
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Demand summary evidence is unavailable or invalid."
    }
    assert "private artifact detail" not in response.text


def test_figure_endpoint_returns_inline_png(tmp_path: Path) -> None:
    figure = tmp_path / "daily_sales.png"
    figure.write_bytes(PNG_SIGNATURE + b"controlled-content")
    app.dependency_overrides[get_demand_figure_service] = lambda: StubFigureService(
        figure
    )
    try:
        response = asyncio.run(
            request("/api/v1/demand-insights/figures/daily-sales")
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert response.headers["cache-control"] == "public, max-age=300"
    assert "content-disposition" not in response.headers
    assert response.content.startswith(PNG_SIGNATURE)


def test_figure_endpoint_maps_unknown_identifier_to_404() -> None:
    app.dependency_overrides[get_demand_figure_service] = UnknownFigureService
    try:
        response = asyncio.run(
            request("/api/v1/demand-insights/figures/private")
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Demand Insight figure was not found."
    }
    assert "private unknown detail" not in response.text


def test_figure_endpoint_maps_invalid_artifact_to_503() -> None:
    app.dependency_overrides[get_demand_figure_service] = UnavailableFigureService
    try:
        response = asyncio.run(
            request("/api/v1/demand-insights/figures/daily-sales")
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Demand Insight figure is unavailable or invalid."
    }
    assert "private path detail" not in response.text


def test_openapi_exposes_documented_demand_summary_resource() -> None:
    schema = asyncio.run(request("/openapi.json")).json()

    operation = schema["paths"]["/api/v1/demand-insights/summary"]["get"]
    assert operation["tags"] == ["Demand Insight"]
    assert "200" in operation["responses"]
    assert "503" in operation["responses"]
    assert "DemandSummaryResponse" in schema["components"]["schemas"]
    figure_operation = schema["paths"][
        "/api/v1/demand-insights/figures/{figure_id}"
    ]["get"]
    assert "200" in figure_operation["responses"]
    assert "404" in figure_operation["responses"]
    assert "503" in figure_operation["responses"]
