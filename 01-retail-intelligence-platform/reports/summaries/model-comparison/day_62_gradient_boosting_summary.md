# Model Comparison Day 62 Gradient Boosting Summary

## Scope

Gradient Boosting completes the three learned candidates evaluated through the
official experiment contract.

## Configuration

- 100 boosting stages;
- learning rate of 0.05;
- tree depth of 2;
- minimum of 2 training observations per leaf;
- squared-error loss;
- `random_state=42`.

Official values are generated in:

- `reports/outputs/model-comparison/results/gradient_boosting.json`;
- `reports/outputs/model-comparison/predictions/gradient_boosting.csv`.

No test-driven parameter search was performed. The evidence remains
`learning_evidence_only`; consolidation belongs to Day 63 and formal selection
belongs to Week 6.
