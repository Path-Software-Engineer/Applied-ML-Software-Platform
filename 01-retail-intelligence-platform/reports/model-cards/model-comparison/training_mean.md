# Model Card — Training Mean Baseline

- **Model ID:** `training_mean`
- **Family:** `baseline`
- **Decision role:** `comparison_baseline`
- **Production status:** `not_production_ready`

## Purpose

Provide a transparent reference that predicts the mean training target for every test observation.

## Experiment boundary

- Target: `units_sold` (units_per_sale_record).
- Split: `chronological_holdout` with 12 train and 6 test rows.
- Dataset SHA-256: `5db700f851c1ab73a7b3c0706582115c80b51e6c21fcf6f76f4ff5a3b1e0ec86`.

## Configuration

- Strategy: `mean_of_training_target`.

## Observed performance

- MAE: 4.3056 units (rank 4).
- RMSE: 4.8997 units.
- R²: -0.1807, contextual only.
- MAE improvement versus baseline: 0.00%.
- Inside practical-equivalence tolerance: no.

## Observed error profile

- Mean signed residual: -1.9167.
- Under-/over-predictions: 2/4.
- Largest absolute error: 7.9167 units on 2026-01-08 for Coffee 250g.
- Interpretation: six-row descriptive evidence, no causal claim.

## Observed strengths

- Creates a minimum comparison reference with no learned feature use.
- Configuration and prediction behavior are directly explainable.

## Limitations

- Cannot represent product, category, price or temporal differences.
- Uses one constant prediction for every observation.
- 18 synthetic observations with 12 training and 6 test rows.
- One chronological holdout and no cross-validation or external validation.
- No stability, confidence interval or real-retail generalization evidence.
- No model authorizes forecasting, inventory action or production deployment.

## Risks

- May underfit structured demand variation.
- A simple reference must not be presented as a deployment candidate.

## Evidence

- `reports/outputs/model-comparison/results/training_mean.json`
- `reports/outputs/model-comparison/predictions/training_mean.csv`
- `reports/outputs/model-comparison/comparison_table.json`
- `reports/outputs/model-comparison/error_analysis.json`
- `reports/outputs/model-comparison/model_decision.json`
