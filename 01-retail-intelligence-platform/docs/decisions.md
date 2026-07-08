# Technical Decisions

## Decision 001 — Base platform architecture

### Context

The project is moving from small applied ML projects into a stronger software platform.

The platform needs to support demand insights, model comparison, inventory decisions, API integration, dashboard views, documentation, labs and future deployment.

### Decision

Use a modular project structure with separated responsibilities:

- frontend/
- backend/
- ai-services/
- data/
- models/
- reports/
- docs/
- labs/
- tests/
- scripts/
- deployment/

### Why

This separation keeps the project clean and prevents mixing responsibilities.

The AI logic should not be mixed with the frontend.

The API layer should not be mixed with notebooks or reports.

The documentation should live in its own place.

Reports and generated outputs should be easy to find.

### Consequences

The project can grow sprint by sprint without becoming messy.

Sprint 1 can focus on the Demand Insight Module.

Sprint 2 can add Model Comparison without breaking the first module.

Sprint 3 can add Inventory Decision logic while reusing the same structure.

### Status

Accepted.

---

## Decision 002 — Demand Insight dataset contract

### Context

The Demand Insight Module needs a stable initial dataset before implementing data loading, validation, cleaning, feature engineering and baseline evaluation.

Without a clear data contract, the project can become inconsistent when columns, types or rules change.

### Decision

Create a small controlled retail sales dataset at:

```txt
data/raw/demand-insight/sales.csv
```

Create a data contract at:

```txt
docs/data-contract.md
```

The initial dataset must include these columns:

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

### Why

The project needs a predictable input before building the data pipeline.

The data contract defines what the system expects.

It also makes future validation, cleaning, feature engineering and reporting easier.

### Consequences

The Day 4 data loading module can read a known CSV file.

The Day 5 cleaning step can validate against documented rules.

The Day 6 pipeline can rely on stable column names.

Future changes to the dataset must update the data contract.

### Status

Accepted.

## Decision 003 — Standard raw sales data path

### Context

Sprint 1 needs a stable location for the raw sales dataset before cleaning, feature engineering, baseline calculation and metric evaluation.

### Decision

Use the following standard raw data path for the Demand Insight Module:

```txt
data/raw/demand-insight/sales.csv
```

### Why

A stable path makes the pipeline easier to run and avoids mixing data files with source code, reports or documentation.

### Consequences

All demand insight scripts and checks should load the raw sales dataset from this path unless a future decision changes the data contract.

### Status

Accepted.

## Decision 004 — Data cleaning rules for Demand Insight Module

### Context

The Demand Insight Module needs a reliable cleaned dataset before feature engineering, baseline calculation or dashboard work.

Raw data may contain missing values, invalid types, duplicates or negative numeric values.

### Decision

Create a dedicated data cleaning layer in:

```txt
ai-services/demand-insight/src/data/data_cleaner.py
```

The cleaning process will:

- validate required columns;
- convert dates;
- convert numeric fields;
- trim text fields;
- remove invalid rows;
- remove duplicates;
- save the clean dataset in `data/processed/demand-insight/`.

### Why

Feature engineering and baseline metrics should not run directly on raw data.

A clean dataset creates a safer foundation for later pipeline steps.

### Consequences

The project now has a clear separation between:

```txt
raw data
clean data
processed / feature-ready data
```

### Status

Accepted.
