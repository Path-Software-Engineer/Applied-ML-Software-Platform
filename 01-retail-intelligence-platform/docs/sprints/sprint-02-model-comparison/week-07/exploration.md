# Sprint 2 — Week 7 Exploration

## Question

How should the completed Model Comparison evidence enter the platform without
moving training, metric or selection responsibility into FastAPI or React?

## User and read flow

The primary reader is a retail analyst comparing model evidence before a later
engineering integration. The supported flow is:

```text
analyst opens Model Comparison
    -> React enters loading
    -> GET /api/v1/model-comparisons/summary
    -> FastAPI delegates to a read-only service
    -> service validates the canonical Day 69 report
    -> React presents candidates, decision and limitations
```

## Alternatives

### Backend joins individual artifacts

Rejected. Joining comparison, error, decision and card files at request time
duplicates analytical assembly and increases inconsistency risk.

### Backend imports the training module

Rejected. HTTP requests must never train models or execute analytical policy.

### Backend validates one composite report

Selected. The Day 69 report is already versioned, complete and reusable. The
service can validate and map it into a narrower public resource without
recalculating evidence.

## Responsibility boundaries

- `ai-services/model-comparison`: training, metrics, error analysis, selection
  and report generation;
- `backend/api/app/services`: report availability, structural validation and
  public read-resource mapping;
- `backend/api/app/schemas`: strict HTTP response types;
- `backend/api/app/routes`: status codes and transport only;
- `frontend/dashboard-app`: request lifecycle and presentation only.

## Product states

- `loading`: the first request is pending and no business value is rendered;
- `connected`: the versioned resource passed client validation;
- `unavailable`: the request or contract failed and no fallback evidence is
  invented.

## Constraints

- preserve the existing Demand Insight routes and feature;
- add one read-only endpoint with no request-time training;
- expose numeric metrics as numbers and format them only in presentation;
- keep the six-row holdout and `not_production_ready` limitation visible;
- do not implement inventory actions, Sprint 3 behavior or production claims.
