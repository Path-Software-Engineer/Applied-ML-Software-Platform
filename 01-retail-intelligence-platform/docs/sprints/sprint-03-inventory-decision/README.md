# Sprint 3 — Inventory Decision Module

## Objective

Complete the Retail Intelligence Platform with explainable, read-only inventory
recommendations. The module joins an identified observed-demand signal with an
inventory snapshot, applies a versioned replenishment policy and exposes the
result without presenting rules as forecasts or probabilities.

## User and decision

The primary user is a small-retail inventory analyst. The supported decision is
whether a product should be monitored, replenished soon or replenished now, and
which non-negative quantity the current policy suggests for review.

The module does not place purchase orders, choose suppliers, infer costs or
promise service levels.

## End-to-end boundary

```text
inventory snapshot + observed daily demand
    -> strict validation and normalized units
    -> versioned reorder and target-stock policy
    -> coverage, risk label and deterministic priority
    -> Recommendation Cards and canonical report
    -> read-only service and versioned FastAPI resource
    -> dedicated React decision view
```

Production code generates official artifacts. The backend validates and reads
one canonical report. React presents the API resource and does not calculate
reorder points, risk or suggested quantities.

## Inputs

- stable `product_id` shared with Demand Insight;
- non-negative stock on hand and its observation date;
- explicit inventory unit;
- observed-demand signal with source, period, type and unit;
- optional source lead time, otherwise an explicit policy default.

The repository learning snapshot is derived from the latest stock observation
available per product in the existing synthetic sales data. It is not claimed
to be a live warehouse system.

## Policy boundary

- `reorder_point = ceil(daily_demand × (lead_time_days + safety_days))`;
- `target_stock = ceil(daily_demand × (lead_time_days + safety_days + review_period_days))`;
- suggested quantity is zero unless stock is at or below the reorder point;
- suggested quantity is never negative;
- risk score is a prioritization index, not a probability;
- every recommendation preserves the inputs and policy version used.

The precise defaults and thresholds are frozen during Week 10, not during the
Day 113 exploration.

## Weeks

| Week | Global days | Scope | Status |
|---|---:|---|---|
| Week 9 | 113–119 | contracts, inventory data and observed-demand signal | completed |
| Week 10 | 120–126 | policies, risk, recommendations and report | completed |
| Week 11 | 127–133 | read service, API and React dashboard | completed |
| Week 12 | 134–140 | adversarial scenarios, traceability and polish | planned |
| Week 13 | 141–147 | final integration, evidence and release | planned |

## Definition of Done

- inventory, signal, policy and public read contracts are versioned;
- joins fail visibly on missing or ambiguous products;
- all quantities use compatible units and non-negative values;
- every recommendation is explainable and carries a limitation;
- production, tests, checks, reports, scripts, backend and frontend keep distinct
  responsibilities;
- Demand Insight and Model Comparison contracts remain stable;
- the complete repository quality gate passes;
- release `v1.0.0-retail-intelligence-platform` is prepared through Gitflow.

## Known limits

- source data is a small synthetic learning dataset;
- stock observations are not live inventory transactions;
- the demand signal is an observed period average, not a forecast;
- default lead time and safety horizon are policy assumptions, not supplier facts;
- no cost, supplier, purchase-order or production-readiness claim is included.

