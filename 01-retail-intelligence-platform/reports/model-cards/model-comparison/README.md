# Sprint 2 Model Cards

| Candidate | MAE rank | Decision role | Production status |
|---|---:|---|---|
| [Training Mean Baseline](./training_mean.md) | 4 | `comparison_baseline` | `not_production_ready` |
| [Linear Regression](./linear_regression.md) | 3 | `evaluated_candidate` | `not_production_ready` |
| [Random Forest](./random_forest.md) | 2 | `selected_for_next_integration` | `not_production_ready` |
| [Gradient Boosting](./gradient_boosting.md) | 1 | `measurement_leader_not_selected` | `not_production_ready` |

These cards describe evidence from 18 synthetic observations and
one six-row holdout. They do not establish stability,
generalization or production readiness.

Random Forest is selected only for the next integration step. Gradient Boosting
remains the observed MAE leader. The difference is intentional and follows the
frozen practical-equivalence and lower-complexity rule.

For platform consumption and final verification, see:

- `reports/outputs/model-comparison/model_comparison_report.json`;
- `docs/model-comparison-read-contract.md`;
- `frontend/dashboard-app/src/features/model-comparison/`;
- `reports/quality/model-comparison/sprint_02_quality_gate.md`.

These are final Sprint 2 learning cards. They are not deployment approval,
production monitoring evidence or a claim about real retail generalization.
