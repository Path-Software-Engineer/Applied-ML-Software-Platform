# Inventory Decision Read Contract

Status: implemented and validated on global Day 129.

## Endpoint

`GET /api/v1/inventory-decisions/summary`

## Success

HTTP `200` returns schema `1.0`, report status `learning_evidence_only`,
freshness metadata, six ranked products, six Recommendation Cards and all
canonical limitations.

Freshness is evaluated at read time from `evidence_as_of_date`. Evidence older
than seven days is marked `stale`; it remains inspectable but cannot be presented
as current stock.

## Failure

Missing, unreadable, incompatible or internally inconsistent evidence returns
HTTP `503` with a stable public detail. No local path, JSON parser detail,
internal field name or partial business value is exposed.

## Ownership

The endpoint does not run the inventory pipeline. The frontend does not read
CSV or Markdown and does not reproduce policy calculations.

## Implementation evidence

- `backend/api/app/services/inventory_decision_service.py`;
- `backend/api/app/schemas/inventory_decision.py`;
- `backend/api/app/routes/inventory_decision.py`;
- `tests/backend/test_inventory_decision_service.py`;
- `tests/backend/test_inventory_decision_api.py`.

