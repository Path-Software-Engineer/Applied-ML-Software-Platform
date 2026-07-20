"""Thin HTTP route for the Model Comparison summary resource."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.app.schemas.model_comparison import ModelComparisonResponse
from backend.api.app.services.model_comparison_service import (
    ModelComparisonError,
    ModelComparisonService,
)


router = APIRouter(
    prefix="/api/v1/model-comparisons",
    tags=["Model Comparison"],
)


def get_model_comparison_service() -> ModelComparisonService:
    return ModelComparisonService()


@router.get(
    "/summary",
    response_model=ModelComparisonResponse,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Model Comparison evidence is unavailable or invalid."
        }
    },
    summary="Read the validated Model Comparison summary",
)
def read_model_comparison(
    service: Annotated[
        ModelComparisonService,
        Depends(get_model_comparison_service),
    ],
) -> dict[str, object]:
    try:
        return service.get_summary()
    except ModelComparisonError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model Comparison evidence is unavailable or invalid.",
        ) from error
