# Model Comparison Day 58 Experiment Split Summary

## Result

The validated 18-row Sprint 1 feature dataset is divided through one fixed
chronological boundary:

- training: 12 rows, 2026-01-01 through 2026-01-06;
- test: 6 rows, 2026-01-07 through 2026-01-09;
- overlap: none;
- target: `units_sold`;
- stochastic-model seed: 42.

## Evidence

- `data/processed/model-comparison/train.csv`;
- `data/processed/model-comparison/test.csv`;
- `reports/outputs/model-comparison/split_manifest.json`.

The manifest records the source checksum, row identifiers, features, excluded
columns and fairness rule. No model has been trained.
