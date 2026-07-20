# Sprint 2 Week 5 Initial Model Results

All rows use the same 18-observation synthetic dataset, 12/6
chronological split, target, feature contract and metric registry.

| Candidate | MAE (units) | RMSE (units) | R² (contextual) |
|---|---:|---:|---:|
| Training Mean Baseline | 4.3056 | 4.8997 | -0.1807 |
| Linear Regression | 3.5633 | 3.8418 | 0.2741 |
| Random Forest | 3.1258 | 3.4413 | 0.4176 |
| Gradient Boosting | 3.0884 | 3.3323 | 0.4539 |

Dataset SHA-256: `5db700f851c1ab73a7b3c0706582115c80b51e6c21fcf6f76f4ff5a3b1e0ec86`.

These are initial observed metrics, not a final recommendation.
Formal comparison criteria, error review and model selection belong
to Week 6. No row is evidence of production readiness or
generalization beyond the controlled snapshot.
