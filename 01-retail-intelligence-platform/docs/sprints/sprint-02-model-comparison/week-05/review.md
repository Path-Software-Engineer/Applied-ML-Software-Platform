# Sprint 2 — Week 5 Review

## Completed work

- froze the dataset, target, feature and chronological split contracts;
- generated 12 training and 6 test observations with source checksum;
- implemented a training-mean baseline and common MAE/RMSE/R² registry;
- implemented shared training-only preprocessing;
- evaluated Linear Regression, Random Forest and Gradient Boosting;
- persisted one result JSON and one prediction CSV per candidate;
- consolidated four comparable rows without selecting a model;
- completed the separate baseline-versus-model laboratory.

## Evidence

- `reports/outputs/model-comparison/split_manifest.json`;
- `reports/outputs/model-comparison/results/`;
- `reports/outputs/model-comparison/predictions/`;
- `reports/outputs/model-comparison/initial_results.csv`;
- `reports/outputs/model-comparison/initial_results.json`;
- `reports/outputs/model-comparison/initial_results.md`;
- `labs/tec-labs/tec-baseline-vs-model-lab/`.

## Validation

Every result shares the dataset checksum, chronological split strategy,
`units_sold` target, units-per-sale-record contract, 12 training rows, 6 test
rows and `learning_evidence_only` status. Stochastic candidates reproduce their
prediction files with `random_state=42`.

## Decisions

Preprocessing is fit inside each candidate pipeline on training rows only.
Candidate configurations are bounded and recorded. No test-driven
hyperparameter search is permitted.

## Week close

Week 5 is complete. The metrics are initial observed evidence only. Week 6 must
define decision criteria, create the formal metric table, inspect errors and
write model cards before any recommendation is considered.

The 18-row synthetic snapshot and six-row test holdout do not demonstrate
stability, generalization or production readiness.
