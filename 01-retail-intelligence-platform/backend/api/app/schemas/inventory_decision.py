"""Strict HTTP schemas for the Inventory Decision read resource."""

from typing import Literal

from pydantic import Field

from backend.api.app.schemas.demand_summary import StrictResponseModel


RiskLabel = Literal["critical", "high", "watch", "healthy"]
InventoryAction = Literal[
    "replenish_now", "replenish_soon", "review", "monitor"
]


class InventoryFreshnessResponse(StrictResponseModel):
    evidence_as_of_date: str = Field(min_length=10)
    age_days: int = Field(ge=0)
    stale_after_days: int = Field(ge=1)
    status: Literal["current", "stale"]


class InventorySnapshotResponse(StrictResponseModel):
    snapshot_id: str = Field(min_length=1)
    as_of_date: str = Field(min_length=10)
    products: int = Field(ge=1)
    stock_on_hand_units: int = Field(ge=0)
    zero_stock_products: int = Field(ge=0)
    oldest_observation_date: str = Field(min_length=10)
    maximum_freshness_days: int = Field(ge=0)
    products_missing_source_lead_time: int = Field(ge=0)


class InventoryDemandSignalResponse(StrictResponseModel):
    signal_type: Literal["observed_daily_average"]
    signal_unit: Literal["units_per_day"]
    period_start: str = Field(min_length=10)
    period_end: str = Field(min_length=10)
    products: int = Field(ge=1)


class InventoryIntegrationResponse(StrictResponseModel):
    join_key: Literal["product_id"]
    join_strategy: Literal["strict_one_to_one"]
    joined_products: int = Field(ge=1)
    unmatched_products: Literal[0]


class InventoryPolicyResponse(StrictResponseModel):
    version: Literal["inventory-review-policy/1.0"]
    default_lead_time_days: int = Field(ge=1)
    safety_days: int = Field(ge=0)
    review_period_days: int = Field(ge=0)
    rounding: Literal["ceiling_to_whole_units"]
    reorder_trigger: Literal["stock_at_or_below_reorder_point"]
    risk_score_meaning: Literal["priority_index_not_probability"]


class InventorySummaryResponse(StrictResponseModel):
    products: int = Field(ge=1)
    stock_on_hand_units: int = Field(ge=0)
    products_requiring_replenishment_review: int = Field(ge=0)
    critical_products: int = Field(ge=0)
    high_risk_products: int = Field(ge=0)
    watch_products: int = Field(ge=0)
    healthy_products: int = Field(ge=0)
    suggested_review_quantity_units: int = Field(ge=0)


class InventoryRankingItemResponse(StrictResponseModel):
    priority_rank: int = Field(ge=1)
    product_id: str = Field(min_length=1)
    product_name: str = Field(min_length=1)
    current_stock_units: int = Field(ge=0)
    observed_daily_demand: float = Field(ge=0)
    coverage_days: float | None = Field(default=None, ge=0)
    reorder_point_units: int = Field(ge=0)
    target_stock_units: int = Field(ge=0)
    suggested_quantity_units: int = Field(ge=0)
    risk_score: float = Field(ge=0, le=100)
    risk_score_meaning: Literal["priority_index_not_probability"]
    risk_label: RiskLabel
    recommended_action: InventoryAction
    reason: str = Field(min_length=1)
    policy_version: Literal["inventory-review-policy/1.0"]


class InventoryCardProductResponse(StrictResponseModel):
    product_id: str = Field(min_length=1)
    product_name: str = Field(min_length=1)


class InventoryCardRiskResponse(StrictResponseModel):
    label: RiskLabel
    score: float = Field(ge=0, le=100)
    meaning: Literal["priority_index_not_probability"]


class InventoryObservedPeriodResponse(StrictResponseModel):
    start: str = Field(min_length=10)
    end: str = Field(min_length=10)


class InventoryCardEvidenceResponse(StrictResponseModel):
    current_stock_units: int = Field(ge=0)
    observed_daily_demand: float = Field(ge=0)
    demand_signal_type: Literal["observed_daily_average"]
    coverage_days: float | None = Field(default=None, ge=0)
    reorder_point_units: int = Field(ge=0)
    target_stock_units: int = Field(ge=0)
    lead_time_days: int = Field(ge=1)
    lead_time_source: Literal["source", "policy_default"]
    observed_period: InventoryObservedPeriodResponse
    snapshot_as_of_date: str = Field(min_length=10)


class InventoryCardActionResponse(StrictResponseModel):
    code: InventoryAction
    suggested_quantity_units: int = Field(ge=0)
    unit: Literal["units"]


class InventoryRecommendationCardResponse(StrictResponseModel):
    card_id: str = Field(pattern=r"^inventory-[A-Z0-9_-]+$")
    priority_rank: int = Field(ge=1)
    product: InventoryCardProductResponse
    risk: InventoryCardRiskResponse
    evidence: InventoryCardEvidenceResponse
    action: InventoryCardActionResponse
    reason: str = Field(min_length=1)
    limitation: str = Field(min_length=1)
    policy_version: Literal["inventory-review-policy/1.0"]


class InventoryDecisionResponse(StrictResponseModel):
    schema_version: Literal["1.0"]
    module: Literal["inventory_decision"]
    report_status: Literal["learning_evidence_only"]
    freshness: InventoryFreshnessResponse
    snapshot: InventorySnapshotResponse
    demand_signal: InventoryDemandSignalResponse
    integration: InventoryIntegrationResponse
    policy: InventoryPolicyResponse
    summary: InventorySummaryResponse
    ranking: list[InventoryRankingItemResponse] = Field(min_length=1, max_length=1000)
    recommendation_cards: list[InventoryRecommendationCardResponse] = Field(
        min_length=1, max_length=1000
    )
    limitations: list[str] = Field(min_length=5, max_length=20)
