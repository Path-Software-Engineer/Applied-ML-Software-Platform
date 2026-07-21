# Sprint 2 — Week 7 Plan

## Objective

Expose the frozen Model Comparison evidence through an isolated read service,
versioned FastAPI resource and honest React presentation while preserving the
stable Demand Insight flow.

## Daily scope

| Global day | Sprint day | Planned result |
|---:|---:|---|
| 71 | 15 | integration exploration, public resource proposal and Week 7 plan |
| 72 | 16 | internal read-only Model Comparison service |
| 73 | 17 | strict schemas, versioned endpoint and HTTP validation |
| 74 | 18 | frontend comparison view with honest request states |
| 75 | 19 | API-driven Decision Cards and accessibility evidence |
| 76 | 20 | cross-layer contract checks and local smoke validation |
| 77 | 21 | Week 7 review, visual evidence and close |

## Planned flow

```text
model_comparison_report.json
    -> internal validation and resource mapping
    -> GET /api/v1/model-comparisons/summary
    -> frontend API client and loading hook
    -> comparison table
    -> Decision Cards
```

## Expected results through Day 75

- a service that reads one canonical artifact and returns schema version `1.0`;
- safe unavailable errors with no local path leakage;
- a thin FastAPI route that never trains models;
- a separate React feature with loading, connected and unavailable states;
- Decision Cards consumed from the API without client-side decision logic.

## Limits

Day 76 owns cross-layer smoke and integration checks. Day 77 owns the Week 7
review and visual evidence. Neither belongs to the Day 71–75 implementation
window. Deployment, inventory decisions and production claims remain excluded.
