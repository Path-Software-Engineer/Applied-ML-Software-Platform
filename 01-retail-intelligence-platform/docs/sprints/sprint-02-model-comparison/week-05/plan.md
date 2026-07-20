# Sprint 2 — Week 5 Plan

## Objective

Create the common experiment foundation and run one baseline plus three
classical regression candidates without selecting a final model this week.

## Daily scope

| Global day | Sprint day | Planned result |
|---:|---:|---|
| 57 | 1 | exploration, experiment direction and fairness rules |
| 58 | 2 | validated dataset loader, chronological split and manifest |
| 59 | 3 | training-mean baseline, metric registry and common result schema |
| 60 | 4 | reproducible Linear Regression candidate |
| 61 | 5 | reproducible Random Forest candidate |
| 62 | 6 | reproducible Gradient Boosting candidate |
| 63 | 7 | consolidated initial results and Week 5 close |

## Expected flow

```text
sales_features.csv
    -> validated experiment dataset
    -> 12-row train / 6-row test
    -> shared preprocessing contract
    -> baseline + three candidates
    -> common prediction and metric artifacts
```

## Expected evidence

- production functions under `ai-services/model-comparison/`;
- isolated pytest tests under `tests/ai-services/model-comparison/`;
- readable checks under `ai-services/model-comparison/checks/`;
- official data and reports generated only by production entry points;
- updated decisions, stories and Week 5 review.

## Limits

- No model is recommended before Week 6.
- No backend endpoint or React implementation.
- No inventory decision behavior.
- No target-derived revenue or ambiguous stock feature.
- No production-readiness claim from 18 rows.
