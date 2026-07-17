# Day 24 — Demand Summary API Summary

## Status

Completed.

## Endpoints

- `GET /health` — process health.
- `GET /api/v1/demand-insights/summary` — versioned Demand Summary.
- `GET /openapi.json` — generated HTTP contract.

## Boundaries

- routes own HTTP translation only;
- schemas own public response validation;
- the Day 23 service owns artifact validation and response assembly;
- analytical production modules continue to own metrics and evidence;
- React remains a separate consumer.

## Error behavior

Missing or invalid analytical evidence produces `503 Service Unavailable` with
a stable public detail. Internal paths and service exception messages are not
returned to clients.

## Validation

- four isolated endpoint tests cover health, success, 503 and OpenAPI;
- the manual ASGI check confirms 293 units, 747.65 revenue and five cards from
  the official service;
- dependency versions are pinned in runtime and lock files and verified against
  the active environment;
- the API starts through `scripts/run-backend.ps1`.
- `scripts/check-backend-runtime.py` verifies a real local Uvicorn process and
  shuts it down after the smoke check.

## Boundary for the next day

Day 25 may consume the endpoint from the initial React dashboard. Existing PNG
figures are not integrated until Day 26.
