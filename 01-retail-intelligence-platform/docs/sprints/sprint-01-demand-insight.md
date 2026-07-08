
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
