# Model Comparison Experiment Contract

## Status

Preliminary contract accepted on global Day 57. Runtime implementation begins
on Day 58 and must preserve this boundary unless a later decision documents a
change.

## User decision

A retail analyst needs to compare transparent regression candidates for
estimating observed units per sale record and select an initial technical
candidate for further product integration.

This is a controlled model-comparison exercise. It is not a demand forecast,
inventory recommendation or production model evaluation.

## Dataset

- source: `data/processed/demand-insight/sales_features.csv`;
- rows: 18;
- observed period: 2026-01-01 through 2026-01-09;
- source type: deterministic synthetic learning data;
- target: `units_sold`;
- unit: units per sale record.

## Feature contract

Allowed candidate features:

| Feature | Role | Rationale |
|---|---|---|
| `product_id` | categorical | identifies the observed product |
| `category` | categorical | provides a broader product grouping |
| `unit_price` | numeric | known commercial attribute in the record |
| `day_of_week` | numeric | known calendar attribute |
| `is_weekend` | binary | known calendar attribute |

Excluded:

| Feature | Reason |
|---|---|
| `sale_id` | row identifier, not an explanatory signal |
| `date` | split key; raw date is not a model input |
| `product_name` | duplicate semantic identity of `product_id` |
| `month`, `year` | constant in the current snapshot |
| `revenue` | directly derived from `units_sold`, causing target leakage |
| `stock_available` | defined as after or near sale; timing is ambiguous |
| baseline prediction/error | derived using the target |

## Split contract

- strategy: chronological holdout;
- training dates: 2026-01-01 through 2026-01-06;
- test dates: 2026-01-07 through 2026-01-09;
- expected rows: 12 train and 6 test;
- random seed: 42 for stochastic models, not for chronological row selection;
- no row or date overlap;
- the test target is unavailable to preprocessing and fitting.

## Candidate registry

| Candidate | Purpose | Initial configuration boundary |
|---|---|---|
| Training mean | transparent reference | mean of training targets only |
| Linear Regression | simple interpretable learned reference | default deterministic solver |
| Random Forest | nonlinear ensemble | fixed seed and bounded tree configuration |
| Gradient Boosting | sequential nonlinear ensemble | fixed seed and bounded boosting configuration |

No hyperparameter search is planned for the 18-row source.

## Metrics

| Metric | Direction | Unit | Use |
|---|---|---|---|
| MAE | lower is better | units | primary comparison |
| RMSE | lower is better | units | large-error diagnostic |
| R² | higher is better | unitless | contextual diagnostic only |

R² can be negative and is unstable with six test observations. It must not
override MAE or limitations.

## Fairness rules

Every candidate must use:

- the same source checksum;
- the same training and test row identifiers;
- the same target;
- the same allowed features;
- the same categorical handling boundary;
- the same metric functions;
- the same result schema.

Checks validate evidence but never recalculate formulas independently.

## Decision boundary

No final recommendation is made before:

1. baseline and all three candidates produce valid predictions;
2. common metrics are consolidated;
3. observation-level errors are reviewed;
4. the selection rule is applied;
5. limitations and model cards are complete.

Even then, the result is an initial candidate for this synthetic snapshot, not
a production-ready model.
