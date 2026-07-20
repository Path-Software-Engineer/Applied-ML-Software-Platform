# Sprint 2 Model Comparison Report

## Decision summary

- Metric leader: **Gradient Boosting**.
- Selected for next integration: **Random Forest**.
- Production status: **not production ready**.

## Comparable metrics

| Rank | Candidate | MAE | RMSE | R² | Improvement vs baseline |
|---:|---|---:|---:|---:|---:|
| 1 | Gradient Boosting | 3.0884 | 3.3323 | 0.4539 | +28.27% |
| 2 | Random Forest | 3.1258 | 3.4413 | 0.4176 | +27.40% |
| 3 | Linear Regression | 3.5633 | 3.8418 | 0.2741 | +17.24% |
| 4 | Training Mean Baseline | 4.3056 | 4.8997 | -0.1807 | +0.00% |

## Decision Cards

### Observed metric leader — Gradient Boosting

**MAE:** 3.0884 units

Lowest observed MAE on the fixed chronological holdout.

- Ranks first by the frozen primary metric.
- Remains practically equivalent to Random Forest.

Limitation: Metric leadership on six test rows does not establish stability or production readiness.

### Selected for next integration — Random Forest

**MAE:** 3.1258 units

Chosen by the frozen practical-equivalence and lower-complexity rule.

- Falls within 0.25 MAE units of the observed leader.
- Improves baseline MAE by more than the required 10%.
- Has lower recorded complexity than the equivalent leader.

Limitation: Selection authorizes a later read-only platform integration, not deployment or inventory action.

### Evidence boundary — Learning evidence only

**Test observations:** 6.0000 rows

Every comparison result comes from one small synthetic snapshot.

- The experiment contains 18 observations in total.
- Only one chronological 12/6 split was evaluated.
- Repeatability is not stability or external validation.

Limitation: No production, generalization, forecasting or inventory claim is supported.

## Reuse boundary

Backend may read the JSON report as validated evidence. It must not
train models, recompute metrics or alter the decision during a request.

## Limitations

- The source contains 18 synthetic observations.
- Only one six-row chronological holdout was evaluated.
- No cross-validation or external validation was performed.
- The selected candidate is not production ready.
