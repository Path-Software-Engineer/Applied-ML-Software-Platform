# Day 127 — Inventory Integration Exploration Summary

- Canonical report remains the only backend source.
- Proposed endpoint: `GET /api/v1/inventory-decisions/summary`.
- States: loading, connected, stale and unavailable.
- Stale evidence remains visible with an explicit refresh warning.
- Service validates and maps; route transports; React presents.
- No policy calculation is allowed in backend request or browser code.
- Runtime implementation starts on Day 128.
