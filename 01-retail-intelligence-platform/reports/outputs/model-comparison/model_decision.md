# Sprint 2 Model Selection Decision

## Outcome

- Measurement leader: **Gradient Boosting** (MAE 3.0884 units).
- Candidate selected for next integration: **Random Forest** (MAE 3.1258 units).
- Practically equivalent candidates: Random Forest, Gradient Boosting.
- Production status: **not production ready**.

## Why the two outcomes differ

Gradient Boosting has the lowest observed MAE. Random Forest is only
0.0374 MAE units higher,
inside the frozen 0.25-unit tolerance, and has lower recorded
operational and explanation complexity. The Day 64 rule therefore
selects Random Forest for the next integration step.

## Error review

Random Forest's largest observed absolute error is 4.4749 units. Gradient
Boosting's is 5.1099 units.
These six-row observations are descriptive and do not establish
causality or stability.

## Limits

- 18 synthetic observations and one six-row chronological holdout;
- no cross-validation, external validation or hyperparameter search;
- repeatability does not demonstrate stability;
- selection authorizes only later platform integration, not deployment
  or inventory action.
