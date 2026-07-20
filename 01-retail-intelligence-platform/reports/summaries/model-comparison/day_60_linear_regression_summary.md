# Model Comparison Day 60 Linear Regression Summary

## Scope

Linear Regression is the first learned candidate evaluated against the official
chronological holdout. It uses the same target, features, split and metric
registry as the training-mean baseline.

## Pipeline

- categorical features: one-hot encoding with unknown values ignored;
- numeric features: standard scaling;
- preprocessing fit: training partition only;
- estimator: `LinearRegression(fit_intercept=True, positive=False)`;
- evaluation: six official test observations.

Official values are generated in:

- `reports/outputs/model-comparison/results/linear_regression.json`;
- `reports/outputs/model-comparison/predictions/linear_regression.csv`.

This is comparison evidence from a tiny synthetic dataset. It is not a
production-quality or generalization claim, and Day 60 does not select a model.
