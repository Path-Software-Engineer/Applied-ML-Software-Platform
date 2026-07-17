"""Thin HTTP route for the Demand Summary resource."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.app.schemas.demand_summary import DemandSummaryResponse
from backend.api.app.services.demand_summary_service import (
    DemandSummaryError,
    DemandSummaryService,
)


router = APIRouter(prefix="/api/v1/demand-insights", tags=["Demand Insight"])


def get_demand_summary_service() -> DemandSummaryService:
    return DemandSummaryService()


@router.get(
    "/summary",
    response_model=DemandSummaryResponse,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Required Demand Insight evidence is unavailable or invalid."
        }
    },
    summary="Read the validated Demand Insight summary",
)
def read_demand_summary(
    service: Annotated[DemandSummaryService, Depends(get_demand_summary_service)],
) -> dict[str, object]:
    try:
        return service.get_summary()
    except DemandSummaryError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Demand summary evidence is unavailable or invalid.",
        ) from error
