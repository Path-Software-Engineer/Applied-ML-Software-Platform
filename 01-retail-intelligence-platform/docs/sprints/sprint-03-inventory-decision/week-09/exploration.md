# Week 9 Exploration — Inventory, Data and Signals

## Problem

Demand and model evidence exist, but the platform cannot yet turn stock and an
identified demand signal into an inventory review queue. The new module must
support that decision without treating historical averages as forecasts or
creating operational orders.

## Current evidence

- six stable product identifiers exist in Demand Insight;
- the sales source contains stock observations whose timing was too ambiguous
  for Sprint 2 model training;
- product totals cover 2026-01-01 through 2026-01-09;
- Model Comparison remains learning-only and is not a production forecast.

## Alternatives considered

1. Use the selected Sprint 2 candidate as forecast demand. Rejected because the
   six-row holdout and synthetic data do not establish forecasting validity.
2. Use observed units per calendar day and label it explicitly. Selected as a
   transparent learning signal with traceable period and source.
3. Infer supplier lead times from the sales data. Rejected because no supplier
   or replenishment timing exists.
4. Require lead time in every raw row. Deferred; the first learning flow permits
   a versioned policy default and records its provenance.

## Selected boundary

The official signal is `observed_daily_average`, calculated over the complete
nine-day period for each product. Inventory uses the latest recorded stock value
per product as a synthetic learning snapshot and preserves its observation date.
Both sources share unit `units` through `product_id`.

## Adversarial scenarios

- missing or duplicate product identifiers;
- negative stock or lead time;
- incompatible units;
- demand-only and inventory-only products;
- zero observed demand;
- stale or corrupt canonical report;
- policy output below zero;
- risk score described incorrectly as probability.

## Architecture decision

`ai-services/inventory-decision` owns contracts, normalization, signals,
policies, risk, recommendations, reports and orchestration. Backend and frontend
remain read-only consumers. No new lab is created: production scenarios and
isolated tests provide the assigned evidence for this sprint.

## Day 113 result

Direction, inputs, units, boundaries, risks, stories and preliminary contracts
are defined. No calculation, endpoint or React feature is implemented on this
day.

