"""Pydantic response schemas for the Demand Summary resource."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictResponseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PeriodResponse(StrictResponseModel):
    start_date: str
    end_date: str
    observed_days: int = Field(ge=1)


class SalesSummaryResponse(StrictResponseModel):
    total_units_sold: int = Field(ge=0)
    total_revenue: float = Field(ge=0)
    sales_count: int = Field(ge=1)
    unique_products: int = Field(ge=1)
    unique_categories: int = Field(ge=1)


class BaselineResponse(StrictResponseModel):
    mean_units_prediction: float = Field(ge=0)
    mae: float = Field(ge=0)


class LeaderResponse(StrictResponseModel):
    name: str = Field(min_length=1)
    value: int | float = Field(ge=0)
    unit: Literal["units", "revenue"]


class LeadersResponse(StrictResponseModel):
    product_by_units: LeaderResponse
    product_by_revenue: LeaderResponse
    date_by_units: LeaderResponse
    date_by_revenue: LeaderResponse


class InsightCardResponse(StrictResponseModel):
    card_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    metric: str = Field(min_length=1)
    insight: str = Field(min_length=1)
    recommendation: str = Field(min_length=1)
    limitation: str = Field(min_length=1)


class DemandSummaryResponse(StrictResponseModel):
    schema_version: Literal["1.0"]
    period: PeriodResponse
    sales_summary: SalesSummaryResponse
    baseline: BaselineResponse
    leaders: LeadersResponse
    insight_cards: list[InsightCardResponse] = Field(min_length=5, max_length=5)
    limitations: list[str] = Field(min_length=1)


class HealthResponse(StrictResponseModel):
    status: Literal["ok"]
    service: Literal["retail-intelligence-api"]
