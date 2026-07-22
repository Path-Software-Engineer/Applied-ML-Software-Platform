# Day 129 — Inventory Decision API Summary

- `GET /api/v1/inventory-decisions/summary` returns strict schema `1.0`.
- Pydantic forbids extra fields and negative quantities.
- Risk semantics allow only `priority_index_not_probability`.
- The route delegates to the read service and never runs the pipeline.
- Invalid evidence maps to a stable `503` without internal details.
- OpenAPI exposes the success and unavailable contracts.
