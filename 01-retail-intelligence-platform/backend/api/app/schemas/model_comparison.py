"""Strict HTTP schemas for the Model Comparison summary resource."""

from typing import Literal

from pydantic import Field

from backend.api.app.schemas.demand_summary import StrictResponseModel


ModelId = Literal[
    "training_mean",
    "linear_regression",
    "random_forest",
    "gradient_boosting",
]


class ModelComparisonExperimentResponse(StrictResponseModel):
    dataset_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    split_strategy: Literal["chronological_holdout"]
    target: Literal["units_sold"]
    target_unit: Literal["units_per_sale_record"]
    train_rows: Literal[12]
    test_rows: Literal[6]


class CandidateResponse(StrictResponseModel):
    model_id: ModelId
    model_name: str = Field(min_length=1)
    model_family: str = Field(min_length=1)
    mae_rank: int = Field(ge=1, le=4)
    mae_units: float = Field(ge=0)
    rmse_units: float = Field(ge=0)
    r2_contextual: float
    mae_improvement_vs_baseline_percent: float
    within_practical_equivalence: bool
    production_status: Literal["learning_evidence_only"]


class MeasurementLeaderResponse(StrictResponseModel):
    model_id: ModelId
    model_name: str = Field(min_length=1)
    mae_units: float = Field(ge=0)


class SelectedCandidateResponse(MeasurementLeaderResponse):
    mae_improvement_vs_baseline_percent: float
    largest_observed_error_units: float = Field(ge=0)


class ModelDecisionResponse(StrictResponseModel):
    measurement_leader: MeasurementLeaderResponse
    selected_candidate: SelectedCandidateResponse
    practical_equivalence_units: float = Field(ge=0)
    rationale: list[str] = Field(min_length=1)
    production_status: Literal["not_production_ready"]
    stability_status: Literal["not_assessed"]


class CardMetricResponse(StrictResponseModel):
    label: str = Field(min_length=1)
    value: float = Field(ge=0)
    unit: Literal["units", "rows"]
    direction: Literal["lower_is_better", "context_only"]


class DecisionCardResponse(StrictResponseModel):
    card_id: Literal[
        "metric-leader",
        "integration-candidate",
        "evidence-boundary",
    ]
    eyebrow: str = Field(min_length=1)
    title: str = Field(min_length=1)
    status: Literal[
        "measurement_leader_not_selected",
        "selected_for_next_integration",
        "not_production_ready",
    ]
    model_id: ModelId | None
    primary_metric: CardMetricResponse
    summary: str = Field(min_length=1)
    reasons: list[str] = Field(min_length=1)
    limitation: str = Field(min_length=1)


class ModelComparisonResponse(StrictResponseModel):
    schema_version: Literal["1.0"]
    module: Literal["model_comparison"]
    report_status: Literal["learning_evidence_only"]
    experiment: ModelComparisonExperimentResponse
    candidates: list[CandidateResponse] = Field(min_length=4, max_length=4)
    decision: ModelDecisionResponse
    decision_cards: list[DecisionCardResponse] = Field(min_length=3, max_length=3)
    limitations: list[str] = Field(min_length=4)
