# Model Comparison Day 61 Random Forest Summary

## Scope

Random Forest is evaluated as the second learned candidate through the same
training-only preprocessing, chronological holdout and metric registry.

## Configuration

- 200 trees;
- maximum depth of 4;
- minimum of 2 training observations per leaf;
- `random_state=42`;
- one worker for deterministic local execution.

Official values are generated in:

- `reports/outputs/model-comparison/results/random_forest.json`;
- `reports/outputs/model-comparison/predictions/random_forest.csv`.

The configuration is intentionally bounded rather than tuned against the test
set. Day 61 records comparable evidence and does not select a model or claim
production readiness.
