# Sprint 2 — Week 8 Exploration

## Question

What must be hardened, evidenced and packaged before Sprint 2 can become the
`v0.2.0-sprint-02-model-comparison` learning release?

## Real module inventory

| Module | Current responsibility | Release concern |
|---|---|---|
| `ai-services/model-comparison` | experiment, models, metrics and reports | reproducibility and immutable evidence |
| `backend/api` | strict read resources | safe logging and stable OpenAPI |
| `frontend/dashboard-app` | Demand Insight and Model Comparison views | shared shell, accessibility and responsive evidence |
| `checks` | cross-layer and documentation gates | complete Sprint 2 closure gate |
| `reports` | analytical and decision evidence | portfolio manifest and honest limitations |

## Prioritized debt and risk

1. Duplicate shell and brand markup across the two React features.
2. No release-level quality summary joining Python, frontend and manual gates.
3. No explicit safe operational log for the Model Comparison read event.
4. Final documentation and traceability still describe an active sprint.
5. Browser screenshots cannot be claimed while the local-browser policy blocks
   the application URL.
6. The 18-row synthetic dataset and six-row test split remain the dominant
   model-readiness limitation.

## Alternatives

### Expand modeling scope

Rejected. Tuning, additional models, cross-validation and Sprint 3 work would
invalidate the frozen release boundary.

### Replace the frontend for release polish

Rejected. Week 8 hardens the integrated product; it does not redesign or
regenerate it.

### Refactor shared responsibilities and strengthen evidence

Selected. This reduces drift without changing public contracts or analytical
results.

## Frozen release scope

- preserve all Sprint 1 contracts and evidence;
- preserve the four candidates, metrics and selection rule;
- preserve `GET /api/v1/model-comparisons/summary` schema `1.0`;
- centralize only duplicated frontend shell responsibilities;
- add safe logs, final tests, documentation and portfolio evidence;
- do not start Sprint 3.

## Acceptance boundary

Sprint 2 may close only when the complete gate passes, release documentation is
traceable, Git release flow succeeds and no unsupported screenshot or
production-readiness claim is present.
