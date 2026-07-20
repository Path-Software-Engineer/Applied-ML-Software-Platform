# Model Card — Gradient Boosting

**Model ID:** `gradient_boosting`  
**Family:** `boosted_tree_ensemble`  
**Decision role:** `measurement_leader_not_selected`  
**Production status:** `not_production_ready`

## Purpose

Test a bounded sequential tree ensemble as the third learned candidate under the common comparison contract.

## Experiment boundary

- Target: `units_sold` (units_per_sale_record).
- Split: `chronological_holdout` with 12 train and 6 test rows.
- Dataset SHA-256: `5db700f851c1ab73a7b3c0706582115c80b51e6c21fcf6f76f4ff5a3b1e0ec86`.

## Configuration

- `n_estimators`: `100`.
- `learning_rate`: `0.05`.
- `max_depth`: `2`.
- `min_samples_leaf`: `2`.
- `loss`: `squared_error`.
- `random_state`: `42`.
- Categorical preprocessing: one-hot encoding.
- Numeric preprocessing: standard scaling.
- Preprocessing fit scope: training partition only.

## Observed performance

- MAE: 3.0884 units (rank 1).
- RMSE: 3.3323 units.
- R²: 0.4539, contextual only.
- MAE improvement versus baseline: 28.27%.
- Inside practical-equivalence tolerance: yes.

## Observed error profile

- Mean signed residual: -0.3247.
- Under-/over-predictions: 3/3.
- Largest absolute error: 5.1099 units on 2026-01-09 for Rice 1kg.
- Interpretation: six-row descriptive evidence, no causal claim.

## Observed strengths

- Has the lowest observed MAE and RMSE in the fixed holdout.
- Improves observed MAE over the baseline by more than 10%.

## Limitations

- Uses a fixed configuration without hyperparameter search.
- Sequential boosting has higher recorded explanation complexity.
- 18 synthetic observations with 12 training and 6 test rows.
- One chronological holdout and no cross-validation or external validation.
- No stability, confidence interval or real-retail generalization evidence.
- No model authorizes forecasting, inventory action or production deployment.

## Risks

- Small-sample metric leadership may not persist on new data.
- The lowest observed metric is not evidence of production readiness.

## Evidence

- `reports/outputs/model-comparison/results/gradient_boosting.json`
- `reports/outputs/model-comparison/predictions/gradient_boosting.csv`
- `reports/outputs/model-comparison/comparison_table.json`
- `reports/outputs/model-comparison/error_analysis.json`
- `reports/outputs/model-comparison/model_decision.json`
