# Sprint 1 — Week 4 Exploration

## Exploration status

Completed on Day 22. No backend or frontend functionality was implemented.

## Problem

Week 3 produced validated analytical artifacts, but a retail analyst still has
to open JSON, Markdown or PNG files directly. Week 4 must expose the same
meaning through a small product flow without moving analytical rules into the
API or dashboard.

## User flow

```text
retail analyst opens the dashboard
→ frontend requests the demand summary
→ API delegates to the internal service
→ service assembles validated artifacts
→ API returns the versioned response
→ dashboard presents summary and Insight Cards
```

The dashboard must show a loading state, an honest unavailable state and the
observed-period limitation. It must not fabricate fallback business results.

## Questions explored

1. Which layer owns the consolidated demand response?
2. Should the API recompute metrics or consume validated artifacts?
3. Which fields are required for the initial dashboard?
4. How should missing or invalid evidence fail?
5. Which visual work belongs to Day 25 and which belongs to Day 26?
6. What evidence is required before Sprint 1 can close?

## Alternatives

### Alternative A — Frontend reads repository artifacts directly

This is simple but couples the UI to file paths, CSV parsing and analytical
storage details. It also bypasses an application boundary and is rejected.

### Alternative B — API recalculates every analytical result

This gives the API control of the response but duplicates tested production
logic and risks differences between reports and the dashboard. It is rejected.

### Alternative C — Internal service assembles validated artifacts

The internal service reads the official processed outputs, verifies their
minimum contract and returns one structured demand summary. A thin API exposes
that result, and React presents it. This is the selected approach.

## Decisions

- Use one read-only endpoint: `GET /api/v1/demand-insights/summary`.
- Use `schema_version: "1.0"` in the response.
- Keep response assembly in `backend/api/app/services/`.
- Keep HTTP schemas and serialization in `backend/api/app/schemas/`.
- Keep routing in `backend/api/app/routes/`.
- Keep the initial React view under `frontend/dashboard-app/`.
- Do not make the frontend read CSV, Markdown or filesystem paths.
- Do not make the API own analytical formulas already validated in `ai-services/`.
- Exclude PNG integration from Day 25; it belongs to Day 26.

## Risks and controls

| Risk | Control |
|---|---|
| Stale analytical artifacts | Service validates required files and response invariants. |
| API and report disagreement | Service consumes official artifacts and adds no new business calculation. |
| UI invents fallback values | Unavailable state contains no fabricated metrics. |
| Contract drift | Versioned schema, API test and documented example. |
| Frontend begins too early | Day 22 remains documentation-only; Day 25 owns React implementation. |
| Premature chart integration | Day 26 remains the explicit integration boundary. |

## Sprint 1 closure criteria

Sprint 1 cannot close before all of the following are evidenced:

- internal Demand Summary service and check;
- versioned API response and endpoint test;
- initial React dashboard consuming the endpoint;
- cards and figures integrated according to the map;
- loading, error and limitation states reviewed;
- full backend, frontend and analytical gates passing;
- Week 4 review, retrospective and release preparation completed on their days;
- no Sprint 2 capability represented as active.
