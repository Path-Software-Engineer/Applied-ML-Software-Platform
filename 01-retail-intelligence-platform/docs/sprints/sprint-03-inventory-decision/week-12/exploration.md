# Week 12 Exploration — Scenarios, Traceability and Polish

## Questions

- Does the policy behave deterministically for healthy, low-stock, stockout,
  zero-demand and high-demand products?
- Which invalid inputs must stop the flow instead of producing a recommendation?
- Can every rendered action be traced to observed inputs and policy version?
- Do stale and unavailable states remain visible without fabricated fallback data?

## Scenario matrix

| Scenario | Controlled input | Oracle |
|---|---|---|
| Sufficient stock | stock above reorder point | monitor; zero suggested units |
| Low stock | positive stock at/below reorder point | replenish soon; non-negative quantity |
| Stockout | zero stock and positive demand | replenish now; critical priority |
| Zero demand | zero observed demand | monitor; zero reorder and suggestion |
| High demand | demand exceeds current protected coverage | deterministic reorder and target quantities |

## Invariants

- stock, demand, reorder point, target and suggested quantities are non-negative;
- suggested quantity is zero when stock is above the reorder point;
- ranking is deterministic for equivalent scores;
- risk is a priority index and never a probability;
- one product produces one ranking row and one Recommendation Card;
- missing, duplicate, incompatible or corrupt evidence fails closed;
- stale evidence is inspectable only with a prominent warning.

## Prioritized edge cases

1. missing or duplicate `product_id` and unmatched join keys;
2. negative stock, demand or lead time;
3. incompatible inventory and demand units;
4. absent lead time using only the explicit policy default;
5. corrupt, structurally incompatible or stale canonical reports;
6. unavailable API with no fallback recommendations.

## Scope boundary

Polish may improve hierarchy, accessibility, units, status communication and
documentation. It may not add purchase orders, suppliers, optimization,
forecasting or new model training.
