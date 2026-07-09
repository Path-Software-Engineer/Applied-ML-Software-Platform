
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

## Day 6 â€” First Data Pipeline

### Goal

Connect data loading and data cleaning into a repeatable first pipeline.

### Flow

```txt
raw sales data
â†’ load dataset
â†’ validate columns
â†’ clean rows
â†’ export pipeline-ready dataset
â†’ generate summary
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

## Day 7 â€” Week 1 Close

### Goal

Close the first week of Sprint 1 with evidence, documentation and a clear checkpoint.

### Expected files

```txt
ai-services/demand-insight/checks/check_week_01_close.py
docs/sprints/sprint-01-week-01-review.md
reports/summaries/demand-insight/week_01_close_summary.md
```

### Definition of Done

- The week close check passes.
- Week 1 evidence is documented.
- Missing files are identified if something is incomplete.
- A Week 1 summary is generated.
- The project is ready for Week 2 only if the checklist is clean.

<!-- DAY-08-FEATURE-BASELINE-EXPLORATION -->

## Day 8 â€” Feature, Baseline and Metric Exploration

### Goal

Prepare Week 2 execution around temporal features, revenue, baseline and MAE.

### Definition of Done

- Week 2 exploration document exists.
- Execution map for Days 9â€“14 is documented.
- The day check generates a summary.

<!-- DAY-09-TEMPORAL-FEATURES -->

## Day 9 â€” Temporal Features

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

## Day 10 â€” Revenue and Processed Dataset

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

## Day 11 â€” Feature Engineering Integration

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

## Day 12 â€” EDA Flow Lab

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

## Day 13 â€” Mean Baseline

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

## Day 14 â€” Baseline MAE

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

## Week 2 Map Alignment â€” Features, Baseline and Metric

### Purpose

Align Week 2 with the current Software Engineer map before starting Week 3.

### Official missing closures

```txt
Day 6 â†’ Pipeline with features, baseline and metric
Day 7 â†’ Initial technical report and documentation
```

### Evidence added

```txt
ai-services/demand-insight/src/pipelines/feature_baseline_metric_pipeline.py
ai-services/demand-insight/checks/check_week_02_map_alignment.py
docs/sprints/sprint-01-week-02-review.md
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
- `docs/sprints/sprint-01-week-03-plan.md`
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
