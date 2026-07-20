# Sprint 2 Model Error Analysis

| Candidate | Mean signed residual | Under | Over | Largest absolute error | Observation |
|---|---:|---:|---:|---:|---|
| Training Mean Baseline | -1.9167 | 2 | 4 | 7.9167 | 2026-01-08, Coffee 250g |
| Linear Regression | +0.6433 | 3 | 3 | 5.6500 | 2026-01-09, Rice 1kg |
| Random Forest | -0.7337 | 2 | 4 | 4.4749 | 2026-01-09, Rice 1kg |
| Gradient Boosting | -0.3247 | 3 | 3 | 5.1099 | 2026-01-09, Rice 1kg |

## Largest observed candidate-row errors

| Candidate | Date | Product | Actual | Predicted | Residual | Absolute error |
|---|---|---|---:|---:|---:|---:|
| Training Mean Baseline | 2026-01-08 | Coffee 250g | 9.00 | 16.92 | -7.92 | 7.92 |
| Training Mean Baseline | 2026-01-08 | Eggs 12 pack | 11.00 | 16.92 | -5.92 | 5.92 |
| Linear Regression | 2026-01-09 | Rice 1kg | 19.00 | 13.35 | +5.65 | 5.65 |
| Gradient Boosting | 2026-01-09 | Rice 1kg | 19.00 | 13.89 | +5.11 | 5.11 |
| Training Mean Baseline | 2026-01-09 | Bread | 22.00 | 16.92 | +5.08 | 5.08 |
| Linear Regression | 2026-01-07 | Orange Juice | 13.00 | 8.36 | +4.64 | 4.64 |
| Linear Regression | 2026-01-09 | Bread | 22.00 | 26.57 | -4.57 | 4.57 |
| Random Forest | 2026-01-09 | Rice 1kg | 19.00 | 14.53 | +4.47 | 4.47 |

Residual is `actual - predicted`: positive values are
under-predictions and negative values are over-predictions.

This analysis describes 24 observed candidate-row predictions from
one six-row holdout. It does not establish causes, stability or
generalization.
