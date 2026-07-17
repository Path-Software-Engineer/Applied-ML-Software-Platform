# Sprint 1 — Demand Insight User Stories

These stories describe only capabilities implemented and validated through the
official Sprint 1 close on Day 28.

## US-S1-001 — Load retail sales

**Story:** As a retail analyst, I want to load a local sales dataset so that I
can analyze a controlled and traceable source.

**Value:** Establishes a reproducible input for every later analysis.

**Acceptance criteria:**

- Given an existing non-empty CSV, when the loader runs, then it returns its rows and columns.
- Given a missing or empty file, when the loader runs, then it fails explicitly.
- Required sales columns can be verified before processing continues.

**Status:** Completed.

**Evidence:** `ai-services/demand-insight/src/data/data_loader.py`,
`ai-services/demand-insight/checks/check_data_loading.py`,
`tests/ai-services/demand-insight/test_data_processing.py`.

## US-S1-002 — Receive clean and valid sales data

**Story:** As a retail analyst, I want invalid sales records removed so that
the analysis is based on consistent dates, units, prices and product data.

**Value:** Prevents missing, duplicated or impossible values from contaminating results.

**Acceptance criteria:**

- Required columns are validated.
- Invalid dates, missing required values, duplicates and negative units or prices are removed.
- The resulting dataset is ordered and contains 18 valid rows for the official source.

**Status:** Completed.

**Evidence:** `ai-services/demand-insight/src/data/data_cleaner.py`,
`data/processed/demand-insight/sales_clean.csv`,
`reports/summaries/demand-insight/data_cleaning_summary.md`,
`tests/ai-services/demand-insight/test_data_processing.py`.

## US-S1-003 — Understand the general sales result

**Story:** As a retail operator, I want a general sales summary so that I can
understand the size and value of the observed period.

**Value:** Provides a concise starting point before product or date analysis.

**Acceptance criteria:**

- Given the processed Sprint 1 dataset, the summary reports 293 units and 747.65 in revenue.
- It reports 18 sales records, 6 products, 3 categories and the observed date range.
- Units and revenue are presented as related but distinct measures.

**Status:** Completed.

**Evidence:** `ai-services/demand-insight/src/analysis/sales_summary.py`,
`data/processed/demand-insight/sales_summary.csv`,
`reports/summaries/demand-insight/sales_summary.md`.

## US-S1-004 — Identify product leaders by demand and revenue

**Story:** As a retail operator, I want products ranked by units and revenue so
that I can compare observed demand with economic value.

**Value:** Makes clear that the most demanded product need not produce the most revenue.

**Acceptance criteria:**

- Given the processed dataset, when ranking by units, then Bread appears first with 105 units.
- When ranking by revenue, then Rice 1kg appears first with 220.50.
- Rankings preserve 293 units and 747.65 in revenue and use a deterministic tie-break.

**Status:** Completed.

**Evidence:** `ai-services/demand-insight/src/analysis/product_ranking.py`,
`data/processed/demand-insight/product_summary.csv`,
`data/processed/demand-insight/product_ranking_by_units.csv`,
`data/processed/demand-insight/product_ranking_by_revenue.csv`,
`ai-services/demand-insight/checks/check_product_ranking.py`,
`tests/ai-services/demand-insight/test_product_ranking.py`.

## US-S1-005 — Identify temporal sales leaders

**Story:** As a retail operator, I want to know which dates lead units and
revenue so that I can understand concentration in the observed period.

**Value:** Separates temporal demand volume from temporal economic value.

**Acceptance criteria:**

- The daily summary contains one chronologically ordered row per observed date.
- 2026-01-06 leads units sold with 45.
- 2026-01-08 leads revenue with 99.30.
- Daily aggregation preserves 293 units and 747.65 in revenue.

**Status:** Completed.

**Evidence:** `ai-services/demand-insight/src/analysis/temporal_sales_analysis.py`,
`data/processed/demand-insight/daily_sales_summary.csv`,
`reports/summaries/demand-insight/temporal_sales_analysis_summary.md`,
`ai-services/demand-insight/checks/check_temporal_sales_analysis.py`,
`tests/ai-services/demand-insight/test_temporal_sales_analysis.py`.

## US-S1-006 — Verify the analytical flow

**Story:** As a project maintainer, I want automated tests and manual checks so
that Sprint 1 results remain reproducible as the platform evolves.

**Value:** Provides regression protection and readable end-to-end evidence.

**Acceptance criteria:**

- Automated tests use controlled inputs and temporary output paths.
- Manual checks delegate business calculations to production modules.
- The repository gate verifies analytical code, backend contracts and frontend
  consumption without requiring later-sprint functionality.

**Status:** Completed.

**Evidence:** `tests/ai-services/demand-insight/`, `tests/backend/`,
`frontend/dashboard-app/tests/`, `checks/`, `scripts/run-quality-gate.ps1`,
`docs/architecture.md`.

## US-S1-007 — Understand analytical limitations

**Story:** As a decision-maker, I want limitations stated alongside results so
that I do not interpret descriptive evidence as prediction or recommendation.

**Value:** Reduces the risk of unsupported business conclusions.

**Acceptance criteria:**

- Documentation states that the dataset covers 2026-01-01 through 2026-01-09.
- Results are described as observed demand and revenue, not forecasts.
- No claim of profit, seasonality, inventory action or future performance is made.

**Status:** Completed.

**Evidence:** `reports/summaries/demand-insight/sales_summary.md`,
`reports/summaries/demand-insight/product_ranking_summary.md`,
`reports/summaries/demand-insight/temporal_sales_analysis_summary.md`,
`docs/sprints/sprint-01-demand-insight/README.md`.

## US-S1-008 — Review concise analytical evidence

**Story:** As a retail analyst, I want the validated findings presented as
concise cards and figures so that I can review the observed signals without
reading source code or raw tables.

**Value:** Makes the completed analysis understandable while preserving the
same analytical contracts for future software integration.

**Acceptance criteria:**

- Five structured cards cover total demand, product leaders and daily leaders.
- Every card includes a metric, interpretation, recommendation and limitation.
- Three PNG figures present daily sales and product rankings by units and revenue.
- The versioned API exposes the validated summary and allowlisted figure resources.
- The React dashboard presents the cards and figures with explicit loading and
  unavailable states.
- The visual report and dashboard do not claim forecasting or inventory decisions.

**Status:** Completed.

**Evidence:** `reports/insight-cards/`, `reports/figures/demand-insight/`,
`reports/outputs/demand-insight/sales_visual_report.md`,
`backend/api/app/routes/demand_summary.py`,
`frontend/dashboard-app/src/features/demand-summary/`.

## Explicitly not completed

Model comparison, inventory decisions, Sprint 2 and Sprint 3 are outside the
completed evidence represented here.
