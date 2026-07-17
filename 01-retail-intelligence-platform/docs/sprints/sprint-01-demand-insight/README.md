
# Sprint 1 — Demand Insight Module

## Objective

Build a traceable retail-sales analysis flow from a controlled CSV to validated
summaries of observed demand and economic value.

## User and value

The current sprint serves a retail analyst or small-store operator who needs to
understand sales totals, product leaders and temporal leaders without reading
implementation details.

## Scope through Day 27

```text
raw sales
→ validation and cleaning
→ temporal and revenue features
→ mean baseline and MAE
→ general sales summary
→ product rankings
→ temporal sales analysis
→ structured Insight Cards
→ reusable figures and visual report
→ consolidated quality gate and weekly closure
→ dashboard, API and user-flow exploration
→ internal Demand Summary service and structured output
→ versioned FastAPI endpoint and OpenAPI contract
→ React dashboard with cards and validated figures
→ cross-layer hardening, tests, review and retrospective
```

Days 1–27 are complete, Week 3 is closed and Week 4 implementation is complete.
The internal
service, FastAPI endpoint and React dashboard are implemented with the five
Insight Cards and three validated figures. Sprint 1 remains open only for the
Day 28 release flow. Model comparison and inventory decisions are not active scope.

## Official outputs

- Processed datasets under `data/processed/demand-insight/`.
- Production modules under `ai-services/demand-insight/src/`.
- Manual end-to-end checks under `ai-services/demand-insight/checks/`.
- Automated tests under `tests/ai-services/demand-insight/`.
- Evidence under `reports/summaries/demand-insight/`.
- Structured cards under `reports/insight-cards/`.
- Reusable figures under `reports/figures/demand-insight/`.
- Visual outputs under `reports/outputs/demand-insight/`.
- Versioned HTTP resources under `backend/api/app/`.
- User-facing presentation under `frontend/dashboard-app/`.

## Validation and decisions

The accumulated flow preserves 293 units and 747.65 in revenue. Bread leads
observed units with 105; Rice 1kg leads observed revenue with 220.50. The daily
leaders are 2026-01-06 by units and 2026-01-08 by revenue. Architectural and
data-contract decisions are registered in `docs/decisions.md`.

## Limitations

The evidence covers 18 records from 2026-01-01 through 2026-01-09. It describes
observed sales; it does not forecast demand, measure profit, establish
seasonality or justify inventory actions.

## Sprint documentation

- Week 1: [exploration](week-01/exploration.md), [plan](week-01/plan.md), [review](week-01/review.md)
- Week 2: [exploration](week-02/exploration.md), [plan](week-02/plan.md), [review](week-02/review.md)
- Week 3: [exploration](week-03/exploration.md), [plan](week-03/plan.md), [closed review](week-03/review.md)
- Week 4: [exploration](week-04/exploration.md), [plan](week-04/plan.md), [review](week-04/review.md)
- Sprint retrospective: [retrospective](retrospective.md)

## Closure criteria

- Production artifacts are reproducible.
- Automated tests and manual checks pass.
- Results preserve validated totals.
- Documentation distinguishes completed evidence from planned work.
- Completed status is supported by repository evidence and reproducible checks.

---

## Day 3 — Initial Dataset and Data Contract

### Goal

Create the initial raw dataset and document the expected data contract for the Demand Insight Module.

### Deliverables

```txt
data/raw/demand-insight/sales.csv
docs/data-contract.md
docs/decisions.md updated with Decision 002
```

### Dataset columns

```txt
sale_id
date
product_id
product_name
category
units_sold
unit_price
stock_available
```

### Why this matters

The project needs a stable input before building loading, cleaning, features, baseline and metrics.

The data contract prevents the project from depending on unclear or changing data assumptions.

### Status

Completed when the dataset exists and the contract is documented.

## Día 4 — Data Loading

### Objetivo

Crear el primer módulo técnico ejecutable para cargar el dataset raw de ventas.

### Entregables

- `ai-services/demand-insight/src/data/data_loader.py`
- `ai-services/demand-insight/checks/check_data_loading.py`
- `reports/summaries/demand-insight/data_loading_summary.md`

### Resultado

El dataset raw de ventas puede cargarse desde:


## Día 5 — Data Cleaning

### Objetivo

Crear la capa de limpieza del dataset de ventas para el Demand Insight Module.

### Resultado esperado

```txt
raw sales dataset
→ validation
→ cleaning rules
→ clean sales dataset
→ data cleaning summary
```

### Evidencia generada

```txt
ai-services/demand-insight/src/data/data_cleaner.py
ai-services/demand-insight/checks/check_data_cleaning.py
data/processed/demand-insight/sales_clean.csv
reports/summaries/demand-insight/data_cleaning_summary.md
```

### Definition of Done

- El dataset raw existe.
- Las columnas requeridas fueron validadas.
- El dataset limpio fue generado.
- No hay nulos en columnas requeridas.
- No hay duplicados después de la limpieza.
- No hay valores negativos en `units_sold` ni `unit_price`.
- El summary de limpieza fue generado.
- El check pasó sin errores.
<!-- DAY-06-FIRST-DATA-PIPELINE -->

## Day 6 — First Data Pipeline

### Goal

Connect data loading and data cleaning into a repeatable first pipeline.

### Flow

```txt
raw sales data
→ load dataset
→ validate columns
→ clean rows
→ export pipeline-ready dataset
→ generate summary
```

### Expected files

```txt
ai-services/demand-insight/src/pipelines/first_data_pipeline.py
ai-services/demand-insight/checks/check_first_data_pipeline.py
data/processed/demand-insight/sales_pipeline_ready.csv
reports/summaries/demand-insight/first_data_pipeline_summary.md
```

### Definition of Done

- The raw dataset can be loaded.
- Required columns are validated.
- Cleaning rules are applied inside the pipeline.
- A pipeline-ready dataset is generated.
- A technical summary is generated.
- The check script passes without errors.

<!-- DAY-07-WEEK-01-CLOSE -->

## Day 7 — Week 1 Close

### Goal

Close the first week of Sprint 1 with evidence, documentation and a clear checkpoint.

### Expected files

```txt
ai-services/demand-insight/checks/check_week_01_close.py
docs/sprints/sprint-01-demand-insight/week-01/review.md
reports/summaries/demand-insight/week_01_close_summary.md
```

### Definition of Done

- The week close check passes.
- Week 1 evidence is documented.
- Missing files are identified if something is incomplete.
- A Week 1 summary is generated.
- The project is ready for Week 2 only if the checklist is clean.

<!-- DAY-08-FEATURE-BASELINE-EXPLORATION -->

## Day 8 — Feature, Baseline and Metric Exploration

### Goal

Prepare Week 2 execution around temporal features, revenue, baseline and MAE.

### Definition of Done

- Week 2 exploration document exists.
- Execution map for Days 9–14 is documented.
- The day check generates a summary.

<!-- DAY-09-TEMPORAL-FEATURES -->

## Day 9 — Temporal Features

### Goal

Create temporal features from the sales date column.

### Expected files

```txt
ai-services/demand-insight/src/features/feature_engineering.py
ai-services/demand-insight/checks/check_temporal_features.py
data/processed/demand-insight/sales_temporal_features.csv
reports/summaries/demand-insight/temporal_features_summary.md
```

### Definition of Done

- Temporal features are generated.
- The processed temporal dataset exists.
- The check script passes.

<!-- DAY-10-REVENUE-PROCESSED-DATASET -->

## Day 10 — Revenue and Processed Dataset

### Goal

Create the revenue column and export a revenue-ready processed dataset.

### Expected files

```txt
ai-services/demand-insight/checks/check_revenue_processed_dataset.py
data/processed/demand-insight/sales_revenue.csv
reports/summaries/demand-insight/revenue_processed_dataset_summary.md
```

### Definition of Done

- Revenue is calculated from units and price.
- The revenue processed dataset exists.
- The check script passes.

<!-- DAY-11-FEATURE-ENGINEERING-INTEGRATION -->

## Day 11 — Feature Engineering Integration

### Goal

Combine temporal features and revenue into the final feature dataset.

### Expected files

```txt
ai-services/demand-insight/src/features/feature_engineering.py
ai-services/demand-insight/checks/check_feature_engineering.py
data/processed/demand-insight/sales_features.csv
reports/summaries/demand-insight/feature_engineering_summary.md
```

### Definition of Done

- The final feature dataset exists.
- Temporal features exist.
- Revenue exists.
- The check script passes.

<!-- DAY-12-EDA-FLOW-LAB -->

## Day 12 — EDA Flow Lab

### Goal

Compare the raw, clean and processed data flows.

### Expected files

```txt
labs/tec-labs/tec-sales-eda-lab/src/compare_eda_flows.py
labs/tec-labs/tec-sales-eda-lab/outputs/eda_flow_comparison.md
labs/tec-labs/tec-sales-eda-lab/README.md
ai-services/demand-insight/checks/check_eda_flow_lab.py
```

### Definition of Done

- The lab script runs.
- The EDA comparison report exists.
- The check script passes.

<!-- DAY-13-MEAN-BASELINE -->

## Day 13 — Mean Baseline

### Goal

Calculate the first baseline for `units_sold`.

### Expected files

```txt
ai-services/demand-insight/src/baselines/baseline.py
ai-services/demand-insight/checks/check_mean_baseline.py
reports/summaries/demand-insight/mean_baseline_summary.md
```

### Definition of Done

- Mean baseline is calculated.
- Baseline predictions are generated.
- The summary exists.
- The check script passes.

<!-- DAY-14-BASELINE-MAE -->

## Day 14 — Baseline MAE

### Goal

Calculate MAE for the mean baseline.

### Expected files

```txt
ai-services/demand-insight/src/baselines/baseline.py
ai-services/demand-insight/checks/check_baseline_mae.py
reports/summaries/demand-insight/baseline_mae_summary.md
```

### Definition of Done

- Baseline value is calculated.
- Baseline predictions are generated.
- MAE is calculated.
- The summary exists.
- The check script passes.

<!-- WEEK-02-MAP-ALIGNMENT -->

## Week 2 Map Alignment — Features, Baseline and Metric

### Purpose

Align Week 2 with the current Software Engineer map before starting Week 3.

### Official missing closures

```txt
Day 6 → Pipeline with features, baseline and metric
Day 7 → Initial technical report and documentation
```

### Evidence added

```txt
ai-services/demand-insight/src/pipelines/feature_baseline_metric_pipeline.py
ai-services/demand-insight/checks/check_week_02_map_alignment.py
docs/sprints/sprint-01-demand-insight/week-02/review.md
reports/summaries/demand-insight/feature_baseline_metric_pipeline_summary.md
reports/summaries/demand-insight/week_02_technical_report.md
```

### Rule

This is not a new project day.

This is a correction to make Week 2 compatible with the official map.

---

# Day 15 - Analysis and Insights Exploration

## Type

Exploration day.

## Goal

Define how the Demand Insight Module will transform processed sales data into business analysis, user-facing language and Insight Cards.

## Evidence created

- `docs/insight-card-methodology.md`
- `docs/sprints/sprint-01-demand-insight/week-03/plan.md`
- `reports/summaries/demand-insight/week_03_exploration_summary.md`

## Decisions

- An insight is not only a number.
- An insight is an interpreted metric that helps the user understand a business signal.
- Insight Cards must use user-facing retail language.
- Technical language such as baseline, MAE, feature engineering and pipeline should remain in technical documentation, not in user-facing cards.
- Sprint 2 and Sprint 3 documentation should not be maintained as active sprint files before those sprints officially start.

## Insight Card structure

Each Insight Card must contain:

- Title
- Metric
- Insight
- Recommendation
- Limitation

## Week 3 direction

Week 3 will move through:

- sales summary;
- product ranking;
- temporal sales analysis;
- Insight Cards;
- basic charts;
- documentation and week close.

---

# Day 16 - Sales Summary

## Type

Execution day.

## Goal

Create a general summary of observed sales using the processed Demand Insight dataset.

## Input

- `data/processed/demand-insight/sales_feature_baseline_metric_pipeline.csv`

## Outputs

- `ai-services/demand-insight/src/analysis/sales_summary.py`
- `data/processed/demand-insight/sales_summary.csv`
- `reports/summaries/demand-insight/sales_summary.md`

## Summary results

- Total observed demand: 293 units sold
- Total observed revenue: 747.65
- Sales records: 18
- Unique products: 6
- Unique categories: 3
- Date range: 2026-01-01 to 2026-01-09
- Average units per sale: 16.28
- Average revenue per sale: 41.54
- Average unit price: 3.10

## Interpretation

`units_sold` is used as observed demand because it represents the number of units actually purchased by customers.

`revenue` is used as observed economic value because it depends on both units sold and unit price.

These metrics are related, but they do not mean the same thing.

## Limitations

This summary describes only the current processed dataset.

It does not guarantee future demand.

It does not measure profit or profitability because the dataset does not include costs.

It does not replace product ranking, temporal analysis, insight cards or charts.

---

# Day 17 - Product Ranking

## Type

Execution day.

## Goal

Create a product-level summary and rank observed products by units sold and revenue.

## Input

- `data/processed/demand-insight/sales_feature_baseline_metric_pipeline.csv`

## Outputs

- `ai-services/demand-insight/src/analysis/product_ranking.py`
- `ai-services/demand-insight/checks/check_product_ranking.py`
- `data/processed/demand-insight/product_summary.csv`
- `data/processed/demand-insight/product_ranking_by_units.csv`
- `data/processed/demand-insight/product_ranking_by_revenue.csv`
- `reports/summaries/demand-insight/product_ranking_summary.md`

## Summary results

- Unique products: 6
- Top product by units sold: Bread with 105 units
- Top product by revenue: Rice 1kg with 220.50
- Coffee 250g and Orange Juice tied at 23 units
- Product ID was used as the deterministic tie-breaker

## Interpretation

Bread led observed demand by accumulated units sold.

Rice 1kg led observed economic value by accumulated revenue.

The two rankings do not tell the same story because revenue depends on both units sold and unit price.

The product summary provides a reusable product-level representation for rankings, future Insight Cards and dashboard outputs.

## Validation

The product ranking check confirmed:

- one summary row per product;
- no duplicated product identifiers;
- preservation of 293 total units sold;
- preservation of 747.65 total revenue;
- descending order in both rankings;
- consecutive ranking positions;
- reproducible output generation.

## Limitations

These rankings describe only the current observed dataset.

They do not predict future product demand.

They do not justify production, replenishment or promotional decisions without temporal, inventory and cost analysis.

They do not measure profit or profitability because product costs are unavailable.

---

# Day 18 - Temporal Sales Analysis

## Type

Execution day.

## Goal

Aggregate observed sales by date and identify temporal leaders in units sold and
revenue without inferring trends or seasonality from the limited period.

## Input

- `data/processed/demand-insight/sales_feature_baseline_metric_pipeline.csv`

## Outputs

- `ai-services/demand-insight/src/analysis/temporal_sales_analysis.py`
- `ai-services/demand-insight/checks/check_temporal_sales_analysis.py`
- `tests/ai-services/demand-insight/test_temporal_sales_analysis.py`
- `data/processed/demand-insight/daily_sales_summary.csv`
- `reports/summaries/demand-insight/temporal_sales_analysis_summary.md`

## Summary results

- Observed dates: 9
- Total units preserved: 293
- Total revenue preserved: 747.65
- Leading date by units sold: 2026-01-06 with 45 units
- Leading date by revenue: 2026-01-08 with 99.30

## Validation

Production generates the daily CSV, pytest verifies isolated behavior and the
manual check inspects the existing end-to-end artifact without rewriting it.

## Limitations

The analysis describes only the observed period from 2026-01-01 to 2026-01-09.
It does not establish seasonality, predict demand or justify inventory decisions.

---

# Day 19 - Structured Insight Cards

## Goal

Transform validated analytical signals into a stable, user-facing contract
without moving business interpretation into a future frontend.

## Outputs

- `ai-services/demand-insight/src/insights/insight_cards.py`
- `ai-services/demand-insight/checks/check_insight_cards.py`
- `tests/ai-services/demand-insight/test_insight_cards.py`
- `reports/insight-cards/demand_insight_cards.json`
- `reports/insight-cards/demand_insight_cards.md`

## Result

Five cards describe observed demand, product leaders and temporal leaders. Each
card exposes an identifier, title, metric, insight, recommendation and explicit
limitation.

---

# Day 20 - Sales Visual Report

## Goal

Generate reusable analytical figures and a reviewable report before introducing
React or browser concerns.

## Outputs

- `ai-services/demand-insight/src/visualization/sales_visual_report.py`
- `ai-services/demand-insight/checks/check_sales_visual_report.py`
- `tests/ai-services/demand-insight/test_sales_visual_report.py`
- `reports/figures/demand-insight/daily_sales.png`
- `reports/figures/demand-insight/product_units_ranking.png`
- `reports/figures/demand-insight/product_revenue_ranking.png`
- `reports/outputs/demand-insight/sales_visual_report.md`

## Result

Three valid PNG artifacts distinguish demand volume from observed economic value
and reuse the interpretations already validated by the Insight Card layer.

---

# Day 21 - Tests, Documentation and Week 3 Close

## Goal

Close Week 3 with one reproducible quality gate and documentation aligned with
the complete Days 15–20 evidence.

## Outputs

- `scripts/run-quality-gate.ps1`
- `scripts/update-project-structure.py`
- `ai-services/demand-insight/checks/check_week_03_close.py`
- `reports/summaries/demand-insight/week_03_close_summary.md`
- updated User Stories, Technical Stories and Week 3 review

## Validation

The project virtual environment reports 30 passing automated tests. The root
quality gate also compiles Python code and runs all manual checks in a stable
order. No backend endpoint or React dashboard is part of Day 21.

---

# Day 22 - Dashboard, API and User-Flow Exploration

## Goal

Define the product and integration path for Week 4 before implementing service,
HTTP or React code.

## Outputs

- `docs/sprints/sprint-01-demand-insight/week-04/exploration.md`
- `docs/sprints/sprint-01-demand-insight/week-04/plan.md`
- `docs/api-contract.md`
- `reports/summaries/demand-insight/week_04_exploration_summary.md`
- `ai-services/demand-insight/checks/check_week_04_exploration.py`

## Decision

The initial dashboard will consume `GET /api/v1/demand-insights/summary`. A thin
FastAPI route will delegate to an internal service that validates and assembles
the official analytical artifacts. React will not parse repository files or
recalculate metrics.

## Boundary

Day 22 is documentation and contract exploration only. Day 23 owns the service,
Day 24 owns the endpoint and Day 25 owns the initial dashboard. Figure
integration remains assigned to Day 26.

---

# Day 23 - Demand Summary Service

## Goal

Create the internal application service that exposes the completed analytical
evidence as one structured, versioned response.

## Outputs

- `backend/api/app/services/demand_summary_service.py`
- `tests/backend/test_demand_summary_service.py`
- `backend/api/checks/check_demand_summary_service.py`
- `reports/outputs/demand-insight/demand_summary.json`
- `reports/summaries/demand-insight/demand_summary_service_summary.md`
- `scripts/generate-demand-summary.ps1`

## Result

The service validates six official artifact sources, assembles schema version
`1.0` and preserves the validated totals, baseline, MAE, leaders and five
Insight Cards. Invalid or missing evidence raises `DemandSummaryError` instead
of returning partial business data.

## Boundary

The service has no FastAPI dependency and no route. HTTP schemas and endpoint
tests belong to Day 24; React remains Day 25 work.

---

# Day 24 - Backend Endpoint and API Contract

## Goal

Expose the Day 23 service through a minimal, versioned HTTP boundary without
moving analytical or artifact logic into the route.

## Outputs

- `backend/api/app/main.py`
- `backend/api/app/routes/demand_summary.py`
- `backend/api/app/schemas/demand_summary.py`
- `backend/api/requirements.txt`
- `backend/api/requirements-lock.txt`
- `tests/backend/test_demand_summary_api.py`
- `backend/api/checks/check_demand_summary_api.py`
- `scripts/run-backend.ps1`
- `scripts/check-backend-runtime.py`

## Result

`GET /api/v1/demand-insights/summary` returns schema version `1.0` with the
validated Demand Summary. `DemandSummaryError` becomes a public `503` without
leaking artifact details. `GET /health` reports process health, and OpenAPI
contains the documented resource and response schema.

## Validation

Endpoint tests cover health, success, unavailable evidence and OpenAPI. The
manual API check exercises the official service response through the ASGI
application. React remains Day 25 work; figure integration remains Day 26.

---

# Day 25 - Initial Demand Dashboard

## Goal

Create the first user-facing React view for Demand Insight while preserving the
validated API as the only business-data boundary.

## Outputs

- `frontend/dashboard-app/src/app/App.jsx`
- `frontend/dashboard-app/src/features/demand-summary/`
- `frontend/dashboard-app/src/styles.css`
- `frontend/dashboard-app/package.json`
- `frontend/dashboard-app/package-lock.json`
- `frontend/dashboard-app/README.md`
- `scripts/run-frontend.ps1`

## Result

The dashboard consumes `GET /api/v1/demand-insights/summary` through a dedicated
client and renders four summary metrics, four observed leaders and five validated
Insight Cards. Loading and unavailable states are explicit, and the error state
never substitutes fabricated business values.

## Validation

The dependency graph is pinned by the npm lock file and the Vite production build
passes. A local HTTP smoke check confirms the built preview, API health and the
versioned five-card response with the official totals. No screenshot is claimed
for Day 25; the functional README satisfies the documented evidence alternative.
Figure integration and visible capture evidence remain the Day 26 boundary.

---

# Day 26 - Figures and Cards Integration

## Goal

Connect the validated visual report to the initial dashboard without moving
artifact generation or analytical interpretation into React.

## Outputs

- `backend/api/app/services/demand_figure_service.py`
- `GET /api/v1/demand-insights/figures/{figure_id}`
- `tests/backend/test_demand_figure_service.py`
- integrated visual-report section in `frontend/dashboard-app/`
- `reports/summaries/demand-insight/dashboard_visual_integration_summary.md`

## Result

The backend serves exactly three allowlisted PNG artifacts after validating
their signatures. The dashboard renders the daily performance figure and both
product rankings alongside the five already validated Insight Cards.

## Validation

Service and route tests cover valid figures, unknown identifiers, missing
artifacts, invalid signatures and public error handling. The manual API check
confirms three `image/png` responses. Existing PNG outputs are the visible
evidence for Day 26; no unsupported browser screenshot is claimed.

---

# Day 27 - Hardening, Tests and Sprint Documentation

## Goal

Harden the completed cross-layer flow and prepare verifiable Sprint 1 review
evidence without starting the release operation.

## Outputs

- frontend contract validation and seven Node tests
- bounded and hardened figure responses
- extended project quality gate
- `week-04/review.md`
- `retrospective.md`
- `reports/summaries/demand-insight/sprint_01_hardening_summary.md`
- `checks/check_sprint_01_hardening.py`

## Result

Python, API and frontend responsibilities are covered by the root gate.
Malformed summary payloads, unavailable figures and unsafe figure sizes fail
explicitly. Week 4 implementation and Sprint 1 lessons are documented.

## Boundary

No release branch, `main` merge or tag is created on Day 27. Those operations
remain exclusive to Day 28.
