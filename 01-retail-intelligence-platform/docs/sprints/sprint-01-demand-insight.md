
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