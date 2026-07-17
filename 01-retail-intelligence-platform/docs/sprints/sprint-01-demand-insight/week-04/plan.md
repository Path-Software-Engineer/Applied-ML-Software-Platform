# Sprint 1 — Week 4 Plan

## Objective

Convert the validated Demand Insight module into a visible platform capability
while preserving the boundaries between analytics, service, API and frontend.

## Planned flow

```text
official analytical artifacts
→ Demand Summary service
→ versioned FastAPI endpoint
→ initial React dashboard
→ cards and figures integration
→ hardening and documentation
→ Sprint 1 release preparation
```

## Day 22 — Exploration

- Define user flow, API boundary and initial dashboard.
- Select the response shape and error behavior.
- Establish Sprint 1 closure criteria.

Expected evidence: exploration, API contract draft and exploration summary.

## Day 23 — Demand Summary service

- Implement a read-only internal service.
- Assemble a structured response from validated artifacts.
- Add isolated service tests and an end-to-end service check.

Expected evidence: service module, structured output, response contract and check.

## Day 24 — Backend endpoint and API contract

- Add the minimal FastAPI application and schemas.
- Expose `GET /api/v1/demand-insights/summary`.
- Add endpoint tests for success and unavailable evidence.

Expected evidence: route, schema, updated API contract and endpoint test.

## Day 25 — Initial dashboard

- Create the React application shell and Demand Insight page.
- Consume the API through a dedicated client.
- Show summary metrics, Insight Cards, loading and unavailable states.
- Provide functional README evidence and a production build.

Expected evidence: initial dashboard, visible cards, prepared frontend structure
and visual or functional evidence.

## Day 26 — Integrate figures and cards

- Connect the existing figures to the product flow.
- Complete the integrated card and chart presentation.
- Capture visible evidence.

## Day 27 — Hardening and Sprint documentation

- Run cross-layer tests and review runtime behavior.
- Update architecture, decisions, README, review and retrospective.

## Day 28 — Official Sprint 1 close

- Prepare `release/sprint-01-demand-insight`.
- Validate the release boundary.
- Merge and tag only under the release rules from the current map.

## Limits

- No Day 26 chart integration during Day 25.
- No release branch or `main` change before Day 28.
- No model comparison or inventory decision capability.
- No business formulas in routes or React components.
- No fake API response or silent fallback business data.
