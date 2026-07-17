# Day 23 — Demand Summary Service Summary

## Status

Completed.

## Responsibility

The internal service validates the official Sprint 1 artifacts and assembles the
versioned Demand Summary contract. It contains no HTTP or presentation code.

## Input evidence

- general sales summary;
- integrated feature, baseline and error table;
- product rankings by units and revenue;
- daily sales summary;
- five validated Insight Cards.

## Structured output

- `reports/outputs/demand-insight/demand_summary.json`
- schema version `1.0`;
- period, sales summary, baseline, leaders, cards and limitations.

## Validation

- isolated tests use a temporary project root under the ignored `.runtime/` boundary;
- missing artifacts and invalid contracts fail explicitly;
- the manual check confirms 293 units, 747.65 revenue, baseline 16.28, MAE
  5.42 and the four validated leaders;
- the accumulated automated suite reports 35 passing tests;
- output generation is repeatable through `scripts/generate-demand-summary.ps1`.

## Boundary

The Day 23 service is independent from FastAPI. HTTP schemas, route behavior and
endpoint tests remain Day 24 work.
