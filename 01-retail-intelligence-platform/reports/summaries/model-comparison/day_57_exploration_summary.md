# Model Comparison Day 57 Exploration Summary

## Status

Global Day 57 / Sprint 2 Day 1 is complete as documentation-only exploration.

## Decisions

- target: `units_sold`;
- unit: units per observed sale record;
- source: 18-row synthetic Sprint 1 feature dataset;
- split direction: chronological;
- baseline: training mean;
- candidates: Linear Regression, Random Forest and Gradient Boosting;
- metrics: MAE primary, RMSE and R² diagnostic;
- fairness: identical data, split, features, preprocessing and metrics.

## Boundary

No model was trained, no dependency was installed, and Sprint 1 production
contracts remain unchanged.
