# Inventory Decision Policy Card

## Identity

- Policy: `inventory-review-policy/1.0`
- Purpose: prioritize product-level inventory review from observed evidence.
- Status: deterministic learning policy; not production ready.

## Inputs and formulas

- observed stock in whole units;
- observed daily demand in units per day;
- source lead time when valid, otherwise a documented two-day default;
- one safety day and a three-day review period;
- reorder point = ceiling(daily demand × (lead time + safety days));
- target stock = ceiling(daily demand × (lead time + safety days + review period)).

Suggested quantity is `max(0, target stock - current stock)` only when current
stock is at or below the reorder point and observed demand is positive.

## Priority semantics

The score combines shortage and protected-horizon coverage pressure. It is a
review priority index from 0 to 100, not a stockout probability. Labels map to
`monitor`, `review`, `replenish_soon` and `replenish_now` actions.

## Governance and limitations

Each result preserves observed inputs, policy version, reason and limitation in
`reports/outputs/inventory-decision/decision_trace.json`. A human must verify
current stock, supplier lead time and recent demand. The policy does not select
suppliers, estimate costs or create purchase orders.
