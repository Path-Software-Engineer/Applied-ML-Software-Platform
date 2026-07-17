# Changelog

All notable changes to the Retail Intelligence Platform are documented here.

## [v0.1.0-sprint-01-demand-insight] — 2026-07-17

### Added

- controlled retail-sales data contract, loading and cleaning;
- temporal and revenue feature engineering;
- mean baseline and MAE evaluation;
- general, product and temporal sales summaries;
- five structured Insight Cards with explicit limitations;
- three reproducible analytical figures;
- versioned Demand Summary service and FastAPI resources;
- React Demand Insight dashboard with cards, figures and honest failure states;
- cross-layer Python, Node and manual validation gate.

### Evidence

- 293 observed units and 747.65 observed revenue;
- Bread leads demand with 105 units;
- Rice 1kg leads revenue with 220.50;
- 2026-01-06 leads daily units with 45;
- 2026-01-08 leads daily revenue with 99.30;
- mean baseline 16.28 and MAE 5.42.

### Limitations

The release describes 18 observed records from 2026-01-01 through 2026-01-09.
It does not forecast future demand, establish seasonality, measure profit or
recommend inventory actions.
