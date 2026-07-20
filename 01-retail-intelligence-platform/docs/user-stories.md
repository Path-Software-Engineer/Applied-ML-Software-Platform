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

## Explicitly not completed after Sprint 1

Inventory decisions and Sprint 3 remain outside completed evidence. Sprint 2
starts below with planned stories; Day 57 does not mark model behavior complete.

## Sprint 2 — Model Comparison User Stories

### US-S2-001 — Compare models under the same experiment

**Story:** As a retail analyst, I want a baseline and classical models compared
under one data contract so that their metrics are technically comparable.

**Value:** Prevents a recommendation from being driven by different rows,
features, splits or evaluation rules.

**Acceptance criteria:**

- Every candidate uses the same validated dataset, target, features and split.
- The experiment records its chronological boundary and random seed.
- Target-derived and temporally ambiguous features are excluded explicitly.
- Results identify the model configuration and prediction unit.

**Status:** Completed on global Day 63.

**Evidence:** `docs/model-comparison-experiment-contract.md`,
`reports/outputs/model-comparison/split_manifest.json`,
`reports/outputs/model-comparison/initial_results.json`,
`docs/sprints/sprint-02-model-comparison/week-05/review.md`.

### US-S2-002 — Understand comparative model quality

**Story:** As a retail analyst, I want baseline and model errors presented in a
common table so that I can understand accuracy and large misses.

**Value:** Translates several model outputs into one reviewable measurement
surface.

**Acceptance criteria:**

- MAE is reported in units and lower values are identified as better.
- RMSE is reported as a large-error diagnostic.
- R² is labeled as contextual and not used alone on the six-row test set.
- Dataset, split and model identifiers accompany the metrics.

**Status:** Completed on global Day 65.

**Evidence:** `reports/outputs/model-comparison/comparison_table.csv`,
`reports/outputs/model-comparison/comparison_table.json`,
`reports/outputs/model-comparison/comparison_table.md`,
`ai-services/model-comparison/checks/check_comparison_table.py`.

### US-S2-003 — Review errors before accepting a candidate

**Story:** As a technical decision-maker, I want the largest prediction errors
and dataset limitations documented so that a strong aggregate metric is not
overinterpreted.

**Value:** Connects numerical ranking with the observations and risks behind it.

**Acceptance criteria:**

- Prediction-level residual and absolute-error evidence is reproducible.
- The largest misses are identified without inventing causal explanations.
- The small synthetic dataset remains visible as a decision limitation.

**Status:** Completed on global Day 66.

**Evidence:** `reports/outputs/model-comparison/error_analysis.csv`,
`reports/outputs/model-comparison/error_analysis.json`,
`reports/outputs/model-comparison/error_analysis.md`,
`ai-services/model-comparison/checks/check_error_analysis.py`.

### US-S2-004 — Receive an evidence-backed candidate rationale

**Story:** As a platform stakeholder, I want model cards and an explicit
selection rule so that the recommended candidate can be explained and audited.

**Value:** Separates “lowest metric” from a responsible technical decision.

**Acceptance criteria:**

- The rule considers primary error, simplicity, stability and interpretability.
- Every candidate has purpose, configuration, metrics and limitations.
- The recommendation is reproducible and does not claim production readiness.

**Status:** Completed on global Day 68.

**Evidence:** `reports/outputs/model-comparison/model_decision.json`,
`reports/outputs/model-comparison/model_decision.md`,
`reports/model-cards/model-comparison/model_cards.json`,
`reports/model-cards/model-comparison/README.md`,
`reports/outputs/model-comparison/model_comparison_report.json`,
`reports/decision-cards/model-comparison/decision_cards.json`.

### US-S2-005 — Read Model Comparison evidence through the platform

**Story:** As a retail analyst, I want the completed comparison evidence through
a versioned platform resource so that I can review it without repository access.

**Value:** Makes the frozen analytical decision reusable without moving model
training or metric ownership into the web request.

**Acceptance criteria:**

- A read-only resource returns exactly four candidates and three Decision Cards.
- The response identifies its schema version and learning-only status.
- Missing or invalid evidence returns an explicit unavailable response with no
  partial values or local paths.
- Demand Insight behavior remains unchanged.

**Status:** Completed on global Day 73.

**Evidence:** `docs/model-comparison-read-contract.md`,
`backend/api/app/services/model_comparison_service.py`,
`backend/api/app/routes/model_comparison.py`,
`tests/backend/test_model_comparison_api.py`.

### US-S2-006 — Review the model decision in the dashboard

**Story:** As a retail analyst, I want a dedicated comparison view so that I can
review candidates, the selected integration candidate and its limitations.

**Value:** Presents technical evidence as an understandable decision surface
without hiding the small-dataset boundary.

**Acceptance criteria:**

- The view distinguishes loading, connected and unavailable states.
- Candidate metrics remain numeric API evidence formatted only for display.
- Decision Cards show the observed leader, selected candidate and evidence limit.
- The browser does not recalculate metrics or selection logic.

**Status:** In progress on global Day 74. The comparison view and request states
are implemented; visual Decision Cards remain assigned to Day 75.

**Evidence:** `docs/model-comparison-read-contract.md`,
`frontend/dashboard-app/src/features/model-comparison/`,
`frontend/dashboard-app/tests/modelComparisonApi.test.js`.
