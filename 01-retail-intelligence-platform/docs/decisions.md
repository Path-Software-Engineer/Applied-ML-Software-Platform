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

## Decision 006 — First data pipeline for Demand Insight

### Context

The Demand Insight Module already has data loading and data cleaning pieces.

The next step is to connect those pieces into a repeatable pipeline that creates a pipeline-ready dataset and a technical summary.

### Decision

Create a first data pipeline responsible for:

```txt
raw sales data
→ validation
→ cleaning
→ pipeline-ready output
→ summary report
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

## Decision 007 — Close Week 1 with evidence checklist

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

## Decision 008 — Explore features, baseline and MAE before building reports

### Context

Week 1 created the data foundation for the Demand Insight Module.

Week 2 needs a clear technical map before execution continues.

### Decision

Use Day 8 to define the next execution flow:

```txt
processed data
→ temporal features
→ revenue
→ baseline
→ MAE
→ technical summary
```

### Why

Feature engineering and baseline metrics should be connected by intent, not added as isolated files.

### Status

Accepted.

<!-- DAY-09-TEMPORAL-FEATURES -->

## Decision 009 — Add temporal features to sales data

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

## Decision 010 — Add revenue as a business signal

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

## Decision 011 — Build a final feature engineering output

### Context

Temporal features and revenue exist as separate enrichments.

### Decision

Create a feature engineering integration step that produces the final feature dataset for the Demand Insight Module.

### Why

Later baseline and metric work should use one clear feature output.

### Status

Accepted.

<!-- DAY-12-EDA-FLOW-LAB -->

## Decision 012 — Compare raw, clean and processed EDA flows

### Context

The project now has multiple data stages.

### Decision

Create a technical lab that compares raw, clean and processed data.

### Why

The lab makes the data transformation story visible and easier to explain.

### Status

Accepted.

<!-- DAY-13-MEAN-BASELINE -->

## Decision 013 — Use mean baseline as first prediction reference

### Context

Before comparing models, the Demand Insight Module needs a basic reference prediction.

### Decision

Use the mean of `units_sold` as the first baseline.

### Why

A baseline provides a minimum standard that future models must beat.

### Status

Accepted.

<!-- DAY-14-BASELINE-MAE -->

## Decision 014 — Evaluate the baseline with MAE

### Context

A baseline value alone does not say how wrong the prediction is.

### Decision

Use Mean Absolute Error to evaluate the mean baseline.

### Why

MAE gives an understandable average error in the same unit as the target: units sold.

### Status

Accepted.

<!-- WEEK-02-MAP-ALIGNMENT -->

## Correction 001 — Align Sprint 1 Week 2 with the current Software Engineer map

### Context

Week 2 had useful technical work, but the sequence must be aligned with the current Software Engineer map before starting Week 3.

### Decision

Close Week 2 with explicit evidence for:

```txt
Pipeline with features, baseline and metric
Initial technical report and documentation
```

### Why

The plan is the boundary of the project.

The correction must not create extra days or extend the sprint.

### Consequences

Week 3 can start only after the integrated pipeline and technical report are verified.

### Status

Accepted.

---

## Decision 018 — Separate production, automated tests and manual checks

### Decision

- `src/` contains production logic.
- `tests/` contains automated tests executed with pytest.
- `checks/` contains manual end-to-end verification and readable evidence.

### Historical debt

The historical checks mixed generation, validation and documentation. The
validation-architecture correction after Day 18 moved generation behind
production functions and retained checks as manual end-to-end verification.

### Status

Accepted and completed for the Demand Insight scope built through Day 18.

---

## Decision 019 — Keep analytical interpretation in a structured card contract

### Context

Days 16–18 produced validated analytical signals, but future delivery channels
must not reconstruct their meaning independently.

### Decision

Represent the five initial findings as versioned JSON and Markdown Insight Cards
with a fixed identifier, metric, interpretation, recommendation and limitation.

### Consequences

Future services and interfaces can consume a stable contract while analytical
language remains testable outside the UI.

### Status

Accepted and implemented on Day 19.

## Decision 020 — Generate visual evidence independently from the dashboard

### Context

Analytical figures require validation before React integration begins.

### Decision

Generate PNG figures and the Markdown visual report in the Demand Insight
production module. Keep units and revenue in separate figures or axes.

### Consequences

The dashboard can later present validated assets without owning chart
calculation or business interpretation.

### Status

Accepted and implemented on Day 20.

## Decision 021 — Use one project-level quality gate for Week 3 closure

### Context

Tests and readable checks existed, but weekly closure needed one reproducible
entry point using the declared project environment.

### Decision

Use `scripts/run-quality-gate.ps1` to compile Python code, run the complete
pytest suite and execute all manual checks in deterministic order. Isolate local
Matplotlib state under the ignored `.runtime/` directory.

### Consequences

Week 3 closure can be reproduced with one command without committing machine
specific runtime state.

### Status

Accepted and implemented on Day 21.

## Decision 022 — Assemble validated evidence behind a versioned read API

### Context

Week 4 must make Demand Insight visible without coupling React to repository
artifacts or duplicating analytical calculations in the HTTP layer.

### Decision

Use an internal Demand Summary service to validate and assemble official
artifacts. Expose it through the planned read-only endpoint
`GET /api/v1/demand-insights/summary` with schema version `1.0`. Keep routes
thin and make the dashboard consume only the API contract.

### Alternatives rejected

- Direct CSV and JSON access from React because it leaks storage concerns.
- Recalculation inside the API because it duplicates validated production logic.
- Fabricated fallback metrics because they would misrepresent unavailable evidence.

### Status

Accepted as the Day 22 design. Implementation begins on Day 23 according to the map.

## Decision 023 — Keep the Demand Summary service independent from HTTP

### Context

The Day 23 output must be testable before FastAPI is introduced and must fail
honestly when official analytical evidence is incomplete.

### Decision

Implement `DemandSummaryService` as a standard-library application service. It
validates required CSV and JSON artifacts, assembles schema version `1.0` and
persists the same JSON it returns. Express artifact failures through the typed
`DemandSummaryError` boundary.

### Consequences

Service behavior can be tested with an isolated temporary project root. Day 24
can map the domain-facing error to HTTP `503` without changing service logic.

### Status

Accepted and implemented on Day 23.

## Decision 024 — Keep the FastAPI route thin and the response schema strict

### Context

The Day 24 endpoint must expose the internal service safely and provide a stable
contract for React without leaking local artifact details.

### Decision

Use FastAPI with strict Pydantic response models. Resolve the internal service
through dependency injection, translate `DemandSummaryError` into a generic
HTTP `503`, and validate the endpoint with HTTPX ASGI tests. Restrict local CORS
to the planned Vite origins.

### Consequences

Routes remain transport-only, tests can replace the service without filesystem
access, and the public error contract does not reveal repository paths.

### Status

Accepted and implemented on Day 24.

## Decision 025 — Keep React presentation behind a dedicated API client

### Context

The Day 25 dashboard must make Demand Insight visible without allowing React to
read analytical files, duplicate formulas or display invented values when the API
is unavailable.

### Decision

Organize the initial dashboard by feature. Use a dedicated API client for the
versioned HTTP contract, a hook for request lifecycle state and presentation
components for rendering. Show loading and unavailable states explicitly and keep
figure integration outside Day 25.

### Consequences

The frontend remains replaceable and testable at its boundary, business meaning
continues to originate in validated artifacts, and API failures cannot silently
become plausible-looking dashboard data.

### Status

Accepted and implemented on Day 25.

## Decision 026 — Deliver figures through an allowlisted API boundary

### Context

Day 26 must connect the validated PNG report to the dashboard without copying
generated artifacts into React or accepting arbitrary filesystem paths over HTTP.

### Decision

Expose three stable figure identifiers below the existing Demand Insight route.
Resolve them in `DemandFigureService`, reject unknown identifiers, verify the PNG
signature and let the thin route return the file inline. Keep titles and generic
accessible descriptions in the presentation layer.

### Consequences

The analytical pipeline remains the sole figure producer, the frontend receives
browser-safe URLs and path traversal is excluded by construction. Missing or
invalid figures fail explicitly instead of producing broken substitute content.

### Status

Accepted and implemented on Day 26.

## Decision 027 — Harden the cross-layer contract before release

### Context

Sprint 1 must not enter its release flow with unchecked browser payloads,
unbounded figure responses or a gate that ignores frontend behavior.

### Decision

Validate the Demand Summary again at the frontend boundary, add dependency-free
Node contract tests, bound figure size, return `nosniff`, expose an honest image
failure state and extend the root gate across Python and frontend responsibilities.

### Consequences

Malformed responses fail before rendering, known figures cannot grow without a
defined limit and the release gate covers both product layers. The deterministic
frontend compiler keeps the gate usable in restricted Windows runners.

### Status

Accepted and implemented on Day 27.

## Decision 028 — Close Sprint 1 through a gated release boundary

### Context

Sprint 1 needs one stable product version without allowing documentation-only
confidence, unfinished Gitflow or Sprint 2 work to enter the release.

### Decision

Require the complete repository gate before and after release preparation. Move
the validated `develop` state through `release/sprint-01-demand-insight`, merge
that release into `main`, create the annotated tag
`v0.1.0-sprint-01-demand-insight` and synchronize `main` back to `develop`.
Record the delivered scope and limitations in versioned release notes.

### Consequences

The stable branch, tag, release evidence and continued integration branch refer
to the same Sprint 1 capability. Sprint 2 remains inactive until a later,
explicitly authorized feature branch is opened.

### Status

Accepted and implemented on Day 28.

## Decision 029 — Open Sprint 2 behind a fair experiment contract

### Context

The platform must compare classical regression models without reopening Sprint
1, leaking target-derived information or changing the dataset between
candidates. The available dataset contains only 18 artificial observations.

### Decision

Use `units_sold` as a continuous target measured in units per sale record.
Compare a training-mean baseline, Linear Regression, Random Forest and Gradient
Boosting on one chronological split. Every candidate must receive the same
rows, target, feature contract, preprocessing boundary and metrics.

Allow `product_id`, `category`, `unit_price`, `day_of_week` and `is_weekend` as
candidate features. Exclude identifiers, raw date, product-name duplication,
constant columns, target-derived revenue and ambiguous post/near-sale stock.

Use MAE as the primary metric, RMSE as a large-error diagnostic and R² only as
context. A six-row test set and synthetic source cannot establish production
generalization.

### Consequences

Sprint 2 gains an auditable comparison boundary before dependencies or models
are added. Backend and React remain unchanged until Week 7. Model ranking may
support an initial candidate decision, but cannot authorize production use.

### Status

Accepted as the global Day 57 exploration decision.

## Decision 030 — Freeze one chronological split manifest

### Context

Every candidate needs identical training and test evidence. A random split could
mix adjacent dates and make the already small result harder to audit.

### Decision

Train on observations through 2026-01-06 and test on observations from
2026-01-07 through 2026-01-09. Persist the 12/6 row identifiers, source
checksum, feature contract, excluded columns and seed in one JSON manifest.

### Consequences

Later candidates cannot choose more favorable rows or preprocessing inputs.
The six-row holdout is sufficient for software-contract verification but not
for a production generalization claim.

### Status

Accepted and implemented on global Day 58.

## Decision 031 — Evaluate every candidate through one metric registry

### Context

Checks and model-specific scripts must not use different formulas or result
shapes. The Sprint 1 full-dataset baseline is not valid for the new holdout.

### Decision

Fit a fresh training-mean baseline on the 12 training targets only. Calculate
MAE, RMSE and contextual R² in one production metric module and persist every
candidate through the same result and prediction contracts.

### Consequences

Later models can be compared without formula drift. R² remains diagnostic
because six test observations cannot support a strong goodness-of-fit claim.

### Status

Accepted and implemented on global Day 59.

## Decision 032 — Fit preprocessing inside each candidate pipeline

### Context

Categorical encoding or numeric scaling performed before the experiment split
would expose test-partition information and weaken comparison fairness.

### Decision

Use one scikit-learn `Pipeline` with a shared `ColumnTransformer`. Fit one-hot
encoding and numeric standardization on the training partition only, then
evaluate Linear Regression on the untouched test partition. Pin the local
model-comparison dependencies to exact versions.

### Consequences

Later candidates reuse the same preprocessing and result boundaries. Unknown
test categories remain processable, while the six-row test set and synthetic
source still prevent production-readiness claims.

### Status

Accepted and implemented on global Day 60.

## Decision 033 — Bound and seed the Random Forest candidate

### Context

An unrestricted ensemble can memorize a 12-row training partition, while
parallel execution and an unrecorded seed weaken reproducibility.

### Decision

Evaluate a 200-tree `RandomForestRegressor` with maximum depth 4, minimum leaf
size 2, `random_state=42` and one worker. Reuse the common preprocessing,
prediction and metric contracts without tuning on the test set.

### Consequences

The candidate is repeatable and its capacity is constrained, but the chosen
parameters are experiment configuration rather than optimized values. The
small holdout still prevents stability or production claims.

### Status

Accepted and implemented on global Day 61.

## Decision 034 — Add Gradient Boosting without test-driven tuning

### Context

The third learned candidate must represent sequential boosting while remaining
comparable and bounded on the 12-row training partition.

### Decision

Evaluate `GradientBoostingRegressor` with 100 stages, learning rate 0.05,
maximum tree depth 2, minimum leaf size 2, squared-error loss and
`random_state=42`. Do not search parameters against the official test rows.

### Consequences

The experiment now contains the baseline and all three planned model families.
Configuration is reproducible, but it is not optimized and cannot establish
stability or production performance.

### Status

Accepted and implemented on global Day 62.

## Decision 035 — Close Week 5 without selecting a model

### Context

The four candidates now have common metrics, but aggregate values alone do not
cover practical equivalence, error concentration, simplicity, stability or
interpretability.

### Decision

Consolidate all candidate results after validating shared experiment metadata.
Do not rank, recommend or label a winner during Week 5. Reserve formal
comparison, error analysis and selection for Week 6.

### Consequences

Week 5 has reviewable evidence without turning a small observed difference into
an unsupported decision. The platform preserves a clear boundary between
metric generation and decision reasoning.

### Status

Accepted and implemented on global Day 63.

## Decision 036 — Freeze practical equivalence and selection criteria

### Context

The lowest observed MAE may differ only marginally from a more explainable
candidate. A selection rule written after error review could be adjusted to
justify a preferred outcome.

### Decision

Use MAE as primary metric, require at least 10% improvement over the baseline,
and treat learned candidates within 0.25 MAE units of the measurement leader as
practically equivalent. Prefer the lower-complexity eligible candidate inside
that tolerance. Report RMSE, contextual R² and error evidence separately.

### Consequences

Day 67 can reproduce both the measurement leader and integration choice from a
policy frozen on Day 64. Repeatability is not mislabeled as stability, and the
choice cannot be labeled production ready.

### Status

Accepted on global Day 64; execution is scheduled for Day 67.
