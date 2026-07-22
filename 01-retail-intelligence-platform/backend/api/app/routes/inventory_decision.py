"""Thin HTTP route for the Inventory Decision summary resource."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.app.schemas.inventory_decision import InventoryDecisionResponse
from backend.api.app.services.inventory_decision_service import (
    InventoryDecisionError,
    InventoryDecisionService,
)


router = APIRouter(
    prefix="/api/v1/inventory-decisions",
    tags=["Inventory Decision"],
)


def get_inventory_decision_service() -> InventoryDecisionService:
    return InventoryDecisionService()


@router.get(
    "/summary",
    response_model=InventoryDecisionResponse,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Inventory Decision evidence is unavailable or invalid."
        }
    },
    summary="Read the validated Inventory Decision summary",
)
def read_inventory_decision(
    service: Annotated[
        InventoryDecisionService,
        Depends(get_inventory_decision_service),
    ],
) -> dict[str, object]:
    try:
        return service.get_summary()
    except InventoryDecisionError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Inventory Decision evidence is unavailable or invalid.",
        ) from error
