# Sprint 2 — Week 6 Exploration

## Objective

Translate comparable metrics into an auditable learning decision without
turning six test observations into a production recommendation.

## Questions

### What does each metric answer?

- MAE: the average absolute miss in units per sale record; primary criterion.
- RMSE: whether larger misses increase the candidate's error burden; diagnostic.
- R²: contextual fit against variation in the six test rows; never decisive alone.

### What is the simplest adequate candidate?

Complexity order for tie-breaking:

1. training-mean baseline;
2. Linear Regression;
3. Random Forest;
4. Gradient Boosting.

This order reflects operational and explanation burden for this platform, not a
universal ranking of algorithms.

### What stability evidence exists?

None beyond deterministic repetition on one fixed chronological holdout.
`random_state=42` proves repeatability, not stability. Cross-validation,
multiple time windows and external data are unavailable and cannot be implied.

### How is interpretability considered?

Interpretability is a tie-breaker after primary error and practical
equivalence. A simpler candidate is preferred when its MAE is no more than
0.25 units above the best eligible learned candidate.

### Which errors must be inspected?

- largest absolute error per candidate;
- signed residuals to expose over- and under-prediction;
- dates and products associated with the largest misses;
- concentration of errors, described without causal claims.

## Frozen decision policy

1. Reject evidence if dataset checksum, split, target, unit or row counts differ.
2. Identify the measurement leader by lowest MAE.
3. A learned candidate must improve baseline MAE by at least 10% to remain
   eligible for continued integration.
4. Treat learned candidates within 0.25 MAE units of the measurement leader as
   practically equivalent.
5. Among practically equivalent candidates, prefer the lower-complexity model.
6. Report RMSE, contextual R² and largest errors; none independently overrides
   the rule.
7. Label the result `selected_for_next_integration`, never production ready.

## Restrictions

- No hyperparameter search against the official test partition.
- No invented stability score or confidence interval.
- No causal explanation of residuals.
- No backend, API or React work during Week 6.
- No inventory decision or Sprint 3 behavior.
