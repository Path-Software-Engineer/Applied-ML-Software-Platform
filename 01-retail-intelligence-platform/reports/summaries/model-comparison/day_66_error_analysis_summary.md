# Model Comparison Day 66 Error Analysis Summary

The four prediction artifacts are validated against the same six official test
rows and expanded into 24 candidate-row observations.

Outputs:

- `reports/outputs/model-comparison/error_analysis.csv`;
- `reports/outputs/model-comparison/error_analysis.json`;
- `reports/outputs/model-comparison/error_analysis.md`.

Each row records `actual - predicted` residual, absolute error, squared error
and direction. Per-candidate notes identify the largest observed miss with date
and product context.

The analysis is descriptive. It does not assign causes, prove stability or
change the Day 64 selection policy.
