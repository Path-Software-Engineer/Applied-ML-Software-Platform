# Changelog

All notable changes to the Retail Intelligence Platform are documented here.

## [v0.2.0-sprint-02-model-comparison] — 2026-07-20

### Added

- reproducible chronological experiment for one baseline and three classical regressors;
- common MAE, RMSE and contextual R² result contract;
- comparison table, residual analysis and explicit selection policy;
- four Model Cards and three Decision Cards;
- validated Model Comparison read service and FastAPI endpoint;
- dedicated React comparison experience with honest request states;
- cross-layer contract gate, live HTTP smoke and safe operational logging;
- shared frontend platform shell and final Sprint 2 traceability.

### Decision

Gradient Boosting is the observed MAE leader at 3.0884 units. Random Forest is
selected for the next integration step at 3.1258 MAE under the frozen 0.25-unit
practical-equivalence and lower-complexity rule.

### Validation

- 96 Python tests passed;
- 18 frontend contract tests passed;
- deterministic frontend compilation passed;
- 51 manual repository checks passed.

### Limitations

The evidence uses 18 synthetic observations and a six-row chronological
holdout. It does not establish generalization, stability or production
readiness. Responsive browser captures remain unavailable and are explicitly
recorded as a known visual-evidence limitation; no mockups were substituted.

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
