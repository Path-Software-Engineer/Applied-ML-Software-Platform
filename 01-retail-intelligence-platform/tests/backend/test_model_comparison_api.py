"""HTTP contract tests for the Model Comparison summary API."""

from __future__ import annotations

import asyncio
from copy import deepcopy

import httpx
from pydantic import ValidationError
import pytest

from backend.api.app.main import app
from backend.api.app.routes.model_comparison import get_model_comparison_service
from backend.api.app.schemas.model_comparison import ModelComparisonResponse
from backend.api.app.services.model_comparison_service import ModelComparisonError


def sample_response() -> dict[str, object]:
    model_specs = (
        ("gradient_boosting", "Gradient Boosting", "boosted_tree_ensemble"),
        ("random_forest", "Random Forest", "bagged_tree_ensemble"),
        ("linear_regression", "Linear Regression", "linear_model"),
        ("training_mean", "Training Mean Baseline", "constant_baseline"),
    )
    candidates = [
        {
            "model_id": model_id,
            "model_name": name,
            "model_family": family,
            "mae_rank": rank,
            "mae_units": 3.0 + rank / 10,
            "rmse_units": 3.5 + rank / 10,
            "r2_contextual": 0.5 - rank / 10,
            "mae_improvement_vs_baseline_percent": 20.0,
            "within_practical_equivalence": rank <= 2,
            "production_status": "learning_evidence_only",
        }
        for rank, (model_id, name, family) in enumerate(model_specs, start=1)
    ]
    cards = [
        {
            "card_id": card_id,
            "eyebrow": "Evidence",
            "title": title,
            "status": status,
            "model_id": model_id,
            "primary_metric": {
                "label": "MAE" if model_id else "Test observations",
                "value": 3.2 if model_id else 6,
                "unit": "units" if model_id else "rows",
                "direction": "lower_is_better" if model_id else "context_only",
            },
            "summary": "Controlled evidence.",
            "reasons": ["Controlled reason."],
            "limitation": "Controlled limitation.",
        }
        for card_id, model_id, title, status in (
            (
                "metric-leader",
                "gradient_boosting",
                "Gradient Boosting",
                "measurement_leader_not_selected",
            ),
            (
                "integration-candidate",
                "random_forest",
                "Random Forest",
                "selected_for_next_integration",
            ),
            (
                "evidence-boundary",
                None,
                "Learning evidence only",
                "not_production_ready",
            ),
        )
    ]
    return {
        "schema_version": "1.0",
        "module": "model_comparison",
        "report_status": "learning_evidence_only",
        "experiment": {
            "dataset_sha256": "a" * 64,
            "split_strategy": "chronological_holdout",
            "target": "units_sold",
            "target_unit": "units_per_sale_record",
            "train_rows": 12,
            "test_rows": 6,
        },
        "candidates": candidates,
        "decision": {
            "measurement_leader": {
                "model_id": "gradient_boosting",
                "model_name": "Gradient Boosting",
                "mae_units": 3.1,
            },
            "selected_candidate": {
                "model_id": "random_forest",
                "model_name": "Random Forest",
                "mae_units": 3.2,
                "mae_improvement_vs_baseline_percent": 20.0,
                "largest_observed_error_units": 4.5,
            },
            "practical_equivalence_units": 0.25,
            "rationale": ["Controlled rationale."],
            "production_status": "not_production_ready",
            "stability_status": "not_assessed",
        },
        "decision_cards": cards,
        "limitations": ["one", "two", "three", "four"],
    }


class StubService:
    def get_summary(self) -> dict[str, object]:
        return sample_response()


class UnavailableService:
    def get_summary(self) -> dict[str, object]:
        raise ModelComparisonError("private path and validation details")


async def request(path: str) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        return await client.get(path)


def test_model_comparison_endpoint_returns_versioned_contract() -> None:
    app.dependency_overrides[get_model_comparison_service] = StubService
    try:
        response = asyncio.run(request("/api/v1/model-comparisons/summary"))
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == sample_response()


def test_model_comparison_endpoint_maps_service_error_to_503() -> None:
    app.dependency_overrides[get_model_comparison_service] = UnavailableService
    try:
        response = asyncio.run(request("/api/v1/model-comparisons/summary"))
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Model Comparison evidence is unavailable or invalid."
    }
    assert "private path" not in response.text


def test_model_comparison_schema_rejects_extra_fields() -> None:
    payload = deepcopy(sample_response())
    payload["unexpected"] = True

    with pytest.raises(ValidationError):
        ModelComparisonResponse.model_validate(payload)


def test_model_comparison_schema_rejects_incomplete_candidates() -> None:
    payload = deepcopy(sample_response())
    payload["candidates"] = payload["candidates"][:3]

    with pytest.raises(ValidationError):
        ModelComparisonResponse.model_validate(payload)


def test_openapi_exposes_model_comparison_resource() -> None:
    schema = asyncio.run(request("/openapi.json")).json()

    operation = schema["paths"]["/api/v1/model-comparisons/summary"]["get"]
    assert operation["tags"] == ["Model Comparison"]
    assert "200" in operation["responses"]
    assert "503" in operation["responses"]
    assert "ModelComparisonResponse" in schema["components"]["schemas"]
