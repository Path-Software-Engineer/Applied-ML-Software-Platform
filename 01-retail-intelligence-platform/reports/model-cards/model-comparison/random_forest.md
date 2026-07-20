# Model Card — Random Forest

**Model ID:** `random_forest`  
**Family:** `tree_ensemble`  
**Decision role:** `selected_for_next_integration`  
**Production status:** `not_production_ready`

## Purpose

Test a bounded bagged-tree ensemble that can represent nonlinear feature interactions under a reproducible seed.

## Experiment boundary

- Target: `units_sold` (units_per_sale_record).
- Split: `chronological_holdout` with 12 train and 6 test rows.
- Dataset SHA-256: `5db700f851c1ab73a7b3c0706582115c80b51e6c21fcf6f76f4ff5a3b1e0ec86`.

## Configuration

- `n_estimators`: `200`.
- `max_depth`: `4`.
- `min_samples_leaf`: `2`.
- `random_state`: `42`.
- `n_jobs`: `1`.
- Categorical preprocessing: one-hot encoding.
- Numeric preprocessing: standard scaling.
- Preprocessing fit scope: training partition only.

## Observed performance

- MAE: 3.1258 units (rank 2).
- RMSE: 3.4413 units.
- R²: 0.4176, contextual only.
- MAE improvement versus baseline: 27.40%.
- Inside practical-equivalence tolerance: yes.

## Observed error profile

- Mean signed residual: -0.7337.
- Under-/over-predictions: 2/4.
- Largest absolute error: 4.4749 units on 2026-01-09 for Rice 1kg.
- Interpretation: six-row descriptive evidence, no causal claim.

## Observed strengths

- Falls inside the best candidate's practical-equivalence tolerance.
- Improves observed MAE over the baseline by more than 10%.
- Has lower recorded complexity than the equivalent boosted ensemble.

## Limitations

- Uses a fixed, untuned 200-tree configuration.
- Feature effects are less direct than in Linear Regression.
- 18 synthetic observations with 12 training and 6 test rows.
- One chronological holdout and no cross-validation or external validation.
- No stability, confidence interval or real-retail generalization evidence.
- No model authorizes forecasting, inventory action or production deployment.

## Risks

- A tree ensemble can still overfit a 12-row training partition.
- Selection for integration does not establish production readiness.

## Evidence

- `reports/outputs/model-comparison/results/random_forest.json`
- `reports/outputs/model-comparison/predictions/random_forest.csv`
- `reports/outputs/model-comparison/comparison_table.json`
- `reports/outputs/model-comparison/error_analysis.json`
- `reports/outputs/model-comparison/model_decision.json`
