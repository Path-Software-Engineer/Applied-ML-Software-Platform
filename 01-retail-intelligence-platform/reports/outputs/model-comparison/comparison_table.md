# Sprint 2 Formal Model Comparison Table

| Rank | Candidate | MAE | RMSE | R² | Δ MAE vs baseline | Improvement | Equivalent |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | Gradient Boosting | 3.0884 | 3.3323 | 0.4539 | +1.2171 | +28.27% | yes |
| 2 | Random Forest | 3.1258 | 3.4413 | 0.4176 | +1.1798 | +27.40% | yes |
| 3 | Linear Regression | 3.5633 | 3.8418 | 0.2741 | +0.7422 | +17.24% | no |
| 4 | Training Mean Baseline | 4.3056 | 4.8997 | -0.1807 | +0.0000 | +0.00% | no |

MAE is the primary metric; lower is better. RMSE is a large-error
diagnostic; lower is better. R² is contextual on six test rows.

Practical equivalence means a learned candidate is within 0.25 MAE
units of the best learned result. The table does not select a model.
Error review and the frozen complexity tie-break belong to Days 66–67.
