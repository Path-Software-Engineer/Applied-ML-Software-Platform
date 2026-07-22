# Week 10 Review — Replenishment and Risk Policy

## Completed

- compared simple and statistical replenishment alternatives;
- froze `inventory-review-policy/1.0` before runtime implementation;
- implemented exact-ratio reorder and target-stock calculations;
- preserved policy-default lead-time provenance;
- calculated stock coverage and a non-probabilistic priority index;
- assigned stable risk labels, actions, reasons and deterministic ranking;
- generated six Recommendation Cards and one canonical report;
- kept backend and React outside the analytical boundary.

## Official result

| Product | Stock | Coverage | Reorder point | Suggested | Risk | Action |
|---|---:|---:|---:|---:|---|---|
| Bread | 0 | 0.00 days | 35 | 70 | critical / 100.0 | replenish now |
| Milk 1L | 9 | 1.50 days | 18 | 27 | high / 50.0 | replenish soon |

The other four products remain above their policy reorder points and receive a
zero suggested quantity. Total suggested review quantity is 97 units.

## Evidence boundary

- observed daily demand is not a forecast;
- the two-day lead time is a policy default, not supplier evidence;
- risk score is not a probability;
- suggested quantities do not create purchase orders;
- the source remains small synthetic learning evidence.

## Validation

Pure policy, risk, ranking, card and report tests pass. Manual checks regenerate
all official artifacts and confirm byte-identical canonical JSON.

## Closure

Week 10 is closed on global Day 126. Week 11 is the next boundary: expose the
canonical report through a read-only service, strict FastAPI contract and a
dedicated React presentation.

