"""Thin HTTP route for the Demand Summary resource."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from backend.api.app.schemas.demand_summary import DemandSummaryResponse
from backend.api.app.services.demand_figure_service import (
    DemandFigureError,
    DemandFigureService,
    UnknownDemandFigureError,
)
from backend.api.app.services.demand_summary_service import (
    DemandSummaryError,
    DemandSummaryService,
)


router = APIRouter(prefix="/api/v1/demand-insights", tags=["Demand Insight"])


def get_demand_summary_service() -> DemandSummaryService:
    return DemandSummaryService()


def get_demand_figure_service() -> DemandFigureService:
    return DemandFigureService()


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


@router.get(
    "/figures/{figure_id}",
    response_class=FileResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The requested figure identifier is not public."
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "The validated figure artifact is unavailable."
        },
    },
    summary="Read a validated Demand Insight figure",
)
def read_demand_figure(
    figure_id: str,
    service: Annotated[DemandFigureService, Depends(get_demand_figure_service)],
) -> FileResponse:
    try:
        path = service.get_figure_path(figure_id)
    except UnknownDemandFigureError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demand Insight figure was not found.",
        ) from error
    except DemandFigureError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Demand Insight figure is unavailable or invalid.",
        ) from error

    return FileResponse(
        path,
        media_type="image/png",
        headers={
            "Cache-Control": "public, max-age=300",
            "X-Content-Type-Options": "nosniff",
        },
    )
