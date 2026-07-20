# Model Card — Linear Regression

**Model ID:** `linear_regression`  
**Family:** `linear_model`  
**Decision role:** `evaluated_candidate`  
**Production status:** `not_production_ready`

## Purpose

Test whether one transparent linear relationship over the shared encoded features improves the training-mean reference.

## Experiment boundary

- Target: `units_sold` (units_per_sale_record).
- Split: `chronological_holdout` with 12 train and 6 test rows.
- Dataset SHA-256: `5db700f851c1ab73a7b3c0706582115c80b51e6c21fcf6f76f4ff5a3b1e0ec86`.

## Configuration

- `fit_intercept`: `True`.
- `positive`: `False`.
- Categorical preprocessing: one-hot encoding.
- Numeric preprocessing: standard scaling.
- Preprocessing fit scope: training partition only.

## Observed performance

- MAE: 3.5633 units (rank 3).
- RMSE: 3.8418 units.
- R²: 0.2741, contextual only.
- MAE improvement versus baseline: 17.24%.
- Inside practical-equivalence tolerance: no.

## Observed error profile

- Mean signed residual: +0.6433.
- Under-/over-predictions: 3/3.
- Largest absolute error: 5.6500 units on 2026-01-09 for Rice 1kg.
- Interpretation: six-row descriptive evidence, no causal claim.

## Observed strengths

- Improves observed MAE over the baseline on the fixed holdout.
- Has the lowest recorded complexity among learned candidates.

## Limitations

- Represents additive linear relationships after preprocessing.
- Was evaluated with one fixed configuration and no tuning.
- 18 synthetic observations with 12 training and 6 test rows.
- One chronological holdout and no cross-validation or external validation.
- No stability, confidence interval or real-retail generalization evidence.
- No model authorizes forecasting, inventory action or production deployment.

## Risks

- Linear assumptions may miss interactions in future data.
- Coefficients are not stable or generalizable from 12 training rows.

## Evidence

- `reports/outputs/model-comparison/results/linear_regression.json`
- `reports/outputs/model-comparison/predictions/linear_regression.csv`
- `reports/outputs/model-comparison/comparison_table.json`
- `reports/outputs/model-comparison/error_analysis.json`
- `reports/outputs/model-comparison/model_decision.json`
