# Model Comparison Day 59 Baseline and Metrics Summary

## Scope

The comparison registry defines one result schema for every candidate:

- MAE in units, lower is better;
- RMSE in units, lower is better;
- R² as a contextual, unitless diagnostic.

## Baseline

The baseline is the mean of the 12 training targets. Test targets do not
participate in fitting the reference value.

Official values are generated in:

- `reports/outputs/model-comparison/results/training_mean.json`;
- `reports/outputs/model-comparison/predictions/training_mean.csv`.

The result remains `learning_evidence_only`. A model recommendation is outside
Day 59.
