"""FastAPI entry point for the Retail Intelligence backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.app.routes import demand_summary_router
from backend.api.app.schemas.demand_summary import HealthResponse


app = FastAPI(
    title="Retail Intelligence API",
    version="0.1.0",
    description="Read-only Sprint 1 API for validated Demand Insight evidence.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["Accept", "Content-Type"],
)

app.include_router(demand_summary_router)


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Operations"],
    summary="Read API process health",
)
def read_health() -> dict[str, str]:
    return {"status": "ok", "service": "retail-intelligence-api"}
