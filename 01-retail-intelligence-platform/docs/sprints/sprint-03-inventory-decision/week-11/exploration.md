# Week 11 Exploration — Read Service, API and Dashboard

## User flow

An inventory analyst opens the third platform stage, sees whether the evidence is
connected and current enough for review, then inspects the priority queue,
Recommendation Cards, policy assumptions and limitations.

## Separation of responsibilities

```text
inventory_decision_report.json
    -> InventoryDecisionService validates and maps
    -> GET /api/v1/inventory-decisions/summary
    -> inventoryDecisionApi validates public response
    -> useInventoryDecision owns request lifecycle
    -> InventoryDecisionDashboard presents evidence
```

- production code already owns policy, risk and Recommendation Cards;
- the service reads one canonical report and does not import production policy;
- the route translates controlled read failures to a safe `503`;
- React formats and presents values but does not calculate decisions.

## Proposed resource

- schema version and module identity;
- report and evidence status;
- freshness metadata with source cutoff, age and stale threshold;
- snapshot and observed-demand boundaries;
- policy version and assumptions;
- product summary and ordered ranking;
- six Recommendation Cards;
- explicit limitations.

## Runtime states

| State | Meaning | Presentation |
|---|---|---|
| loading | request is pending | skeleton and no values |
| connected | validated non-stale response | full evidence |
| stale | validated response exceeds freshness threshold | full evidence with prominent warning |
| unavailable | request or contract failed | safe error, retry and no fallback values |

Stale evidence is not silently unavailable: the analyst may inspect it, but the
screen must state that current stock should be refreshed before acting.

## Compatibility

Demand Insight and Model Comparison routers, schemas, clients and views remain
unchanged. The stage navigation receives a third group but does not merge the
three domain lifecycles.

## Day 127 boundary

The resource, states and integration responsibilities are agreed. No backend
service, endpoint or React feature is implemented on this exploration day.

