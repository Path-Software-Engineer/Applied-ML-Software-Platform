# Sprint 1 — Demand Insight User Stories

These stories describe only capabilities supported by evidence through Day 18.

## US-S1-001 — Load retail sales

**Story:** As a retail analyst, I want to load a local sales dataset so that I
can analyze a controlled and traceable source.

**Value:** Establishes a reproducible input for every later analysis.

**Acceptance criteria:**

- Given an existing non-empty CSV, when the loader runs, then it returns its rows and columns.
- Given a missing or empty file, when the loader runs, then it fails explicitly.
- Required sales columns can be verified before processing continues.

**Status:** Completed.

**Evidence:** `src/data/data_loader.py`, `check_data_loading.py`, automated data-processing tests.

## US-S1-002 — Receive clean and valid sales data

**Story:** As a retail analyst, I want invalid sales records removed so that
the analysis is based on consistent dates, units, prices and product data.

**Value:** Prevents missing, duplicated or impossible values from contaminating results.

**Acceptance criteria:**

- Required columns are validated.
- Invalid dates, missing required values, duplicates and negative units or prices are removed.
- The resulting dataset is ordered and contains 18 valid rows for the official source.

**Status:** Completed.

**Evidence:** `src/data/data_cleaner.py`, `sales_clean.csv`, `data_cleaning_summary.md`, pytest cleaning tests.

## US-S1-003 — Understand the general sales result

**Story:** As a retail operator, I want a general sales summary so that I can
understand the size and value of the observed period.

**Value:** Provides a concise starting point before product or date analysis.

**Acceptance criteria:**

- Given the processed Sprint 1 dataset, the summary reports 293 units and 747.65 in revenue.
- It reports 18 sales records, 6 products, 3 categories and the observed date range.
- Units and revenue are presented as related but distinct measures.

**Status:** Completed.

**Evidence:** `src/analysis/sales_summary.py`, `sales_summary.csv`, `sales_summary.md`.

## US-S1-004 — Identify product leaders by demand and revenue

**Story:** As a retail operator, I want products ranked by units and revenue so
that I can compare observed demand with economic value.

**Value:** Makes clear that the most demanded product need not produce the most revenue.

**Acceptance criteria:**

- Given the processed dataset, when ranking by units, then Bread appears first with 105 units.
- When ranking by revenue, then Rice 1kg appears first with 220.50.
- Rankings preserve 293 units and 747.65 in revenue and use a deterministic tie-break.

**Status:** Completed.

**Evidence:** product-ranking production module, three ranking CSVs, manual check and pytest ranking tests.

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

**Evidence:** temporal-analysis production module, `daily_sales_summary.csv`, report, check and pytest suite.

## US-S1-006 — Verify the analytical flow

**Story:** As a project maintainer, I want automated tests and manual checks so
that Sprint 1 results remain reproducible as the platform evolves.

**Value:** Provides regression protection and readable end-to-end evidence.

**Acceptance criteria:**

- Automated tests use controlled inputs and temporary output paths.
- Manual checks delegate business calculations to production modules.
- Verification does not require frontend, backend or later-sprint functionality.

**Status:** Completed through Day 18.

**Evidence:** `tests/ai-services/demand-insight/`, `checks/`, `docs/architecture.md`.

## US-S1-007 — Understand analytical limitations

**Story:** As a decision-maker, I want limitations stated alongside results so
that I do not interpret descriptive evidence as prediction or recommendation.

**Value:** Reduces the risk of unsupported business conclusions.

**Acceptance criteria:**

- Documentation states that the dataset covers 2026-01-01 through 2026-01-09.
- Results are described as observed demand and revenue, not forecasts.
- No claim of profit, seasonality, inventory action or future performance is made.

**Status:** Completed.

**Evidence:** sales, product-ranking and temporal-analysis summaries; Sprint 1 README.

## Explicitly not completed

Insight Cards, charts, API, dashboard, model comparison, inventory decisions,
Sprint 2 and Sprint 3 are outside the completed evidence represented here.
