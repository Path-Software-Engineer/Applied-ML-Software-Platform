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

<!-- DAY-06-FIRST-DATA-PIPELINE -->

## Decision 006 â€” First data pipeline for Demand Insight

### Context

The Demand Insight Module already has data loading and data cleaning pieces.

The next step is to connect those pieces into a repeatable pipeline that creates a pipeline-ready dataset and a technical summary.

### Decision

Create a first data pipeline responsible for:

```txt
raw sales data
â†’ validation
â†’ cleaning
â†’ pipeline-ready output
â†’ summary report
```

### Why

A pipeline makes the data workflow repeatable and prevents manual steps from becoming hidden requirements.

Later work such as feature engineering, baseline calculation, MAE and insight cards should depend on a clear processed output.

### Consequences

The project now has a stronger base for Sprint 1.

Future modules can reuse the pipeline output instead of reading raw data directly.

### Status

Accepted.

<!-- DAY-07-WEEK-01-CLOSE -->

## Decision 007 â€” Close Week 1 with evidence checklist

### Context

The first week created the base of the Demand Insight Module.

Before moving into features, baseline and metrics, the project needs a checkpoint that confirms evidence exists.

### Decision

Use a Week 1 close check that verifies core files, raw data, data loading, data cleaning, first pipeline and summaries.

### Why

A week close prevents silent gaps from moving forward into later work.

### Consequences

The project can start Week 2 with a clearer foundation.

### Status

Accepted.

<!-- DAY-08-FEATURE-BASELINE-EXPLORATION -->

## Decision 008 â€” Explore features, baseline and MAE before building reports

### Context

Week 1 created the data foundation for the Demand Insight Module.

Week 2 needs a clear technical map before execution continues.

### Decision

Use Day 8 to define the next execution flow:

```txt
processed data
â†’ temporal features
â†’ revenue
â†’ baseline
â†’ MAE
â†’ technical summary
```

### Why

Feature engineering and baseline metrics should be connected by intent, not added as isolated files.

### Status

Accepted.

<!-- DAY-09-TEMPORAL-FEATURES -->

## Decision 009 â€” Add temporal features to sales data

### Context

Sales data contains dates, but raw dates alone are not enough for demand analysis.

### Decision

Create temporal features from the date column:

```txt
day_of_week
month
year
is_weekend
```

### Why

Temporal signals help explain sales behavior across days, months and weekends.

### Status

Accepted.

<!-- DAY-10-REVENUE-PROCESSED-DATASET -->

## Decision 010 â€” Add revenue as a business signal

### Context

Units sold explain volume, but retail analysis also needs monetary value.

### Decision

Create a revenue column using:

```txt
revenue = units_sold * unit_price
```

### Why

Revenue allows the Demand Insight Module to compare products by business value, not only by units sold.

### Status

Accepted.

<!-- DAY-11-FEATURE-ENGINEERING-INTEGRATION -->

## Decision 011 â€” Build a final feature engineering output

### Context

Temporal features and revenue exist as separate enrichments.

### Decision

Create a feature engineering integration step that produces the final feature dataset for the Demand Insight Module.

### Why

Later baseline and metric work should use one clear feature output.

### Status

Accepted.

<!-- DAY-12-EDA-FLOW-LAB -->

## Decision 012 â€” Compare raw, clean and processed EDA flows

### Context

The project now has multiple data stages.

### Decision

Create a technical lab that compares raw, clean and processed data.

### Why

The lab makes the data transformation story visible and easier to explain.

### Status

Accepted.

<!-- DAY-13-MEAN-BASELINE -->

## Decision 013 â€” Use mean baseline as first prediction reference

### Context

Before comparing models, the Demand Insight Module needs a basic reference prediction.

### Decision

Use the mean of `units_sold` as the first baseline.

### Why

A baseline provides a minimum standard that future models must beat.

### Status

Accepted.
