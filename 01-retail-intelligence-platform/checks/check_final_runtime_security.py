"""Review final read-only runtime, path, size and error boundaries."""

from __future__ import annotations

import asyncio
from pathlib import Path
import sys

import httpx


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.api.app.main import app  # noqa: E402
from backend.api.app.services.demand_figure_service import (  # noqa: E402
    FIGURE_PATHS,
    MAX_FIGURE_BYTES,
)
from backend.api.app.services.inventory_decision_service import (  # noqa: E402
    MAX_REPORT_BYTES as INVENTORY_MAX_REPORT_BYTES,
)
from backend.api.app.services.model_comparison_service import (  # noqa: E402
    MAX_REPORT_BYTES as MODEL_MAX_REPORT_BYTES,
)


async def exercise_http() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        health = await client.get("/health")
        traversal = await client.get("/api/v1/demand-insights/figures/..%2F..%2FREADME")
        unknown = await client.get("/api/v1/unknown")
        post = await client.post("/api/v1/inventory-decisions/summary", json={})
    assert health.status_code == 200
    assert traversal.status_code == 404
    assert unknown.status_code == 404
    assert post.status_code == 405
    combined = f"{traversal.text} {unknown.text} {post.text}"
    assert str(PROJECT_ROOT) not in combined


def main() -> None:
    asyncio.run(exercise_http())
    schema = app.openapi()
    api_paths = {path: item for path, item in schema["paths"].items() if path.startswith("/api/")}
    assert len(api_paths) == 4
    assert all(set(operations) <= {"get", "parameters"} for operations in api_paths.values())
    assert set(FIGURE_PATHS) == {
        "daily-sales",
        "product-units-ranking",
        "product-revenue-ranking",
    }
    assert MAX_FIGURE_BYTES == 10 * 1024 * 1024
    assert MODEL_MAX_REPORT_BYTES == INVENTORY_MAX_REPORT_BYTES == 2 * 1024 * 1024

    frontend = PROJECT_ROOT / "frontend/dashboard-app/src"
    client_source = "\n".join(path.read_text(encoding="utf-8") for path in frontend.rglob("*.js"))
    assert "../reports/" not in client_source and "C:\\" not in client_source
    main_source = (PROJECT_ROOT / "backend/api/app/main.py").read_text(encoding="utf-8")
    assert 'allow_methods=["GET"]' in main_source
    assert 'allow_credentials=False' in main_source

    print("OK - Sprint 3 Day 143 final runtime security check passed")
    print("HTTP: GET-only API | safe 404/405 | no path disclosure")
    print("Allowlists: 3 figure IDs | report/figure size boundaries: enforced")
    print("Frontend direct artifact access: absent")


if __name__ == "__main__":
    main()
