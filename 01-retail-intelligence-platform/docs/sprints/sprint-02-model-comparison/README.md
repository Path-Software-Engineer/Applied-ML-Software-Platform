# Sprint 2 — Model Comparison Module

## Objective

Compare a transparent baseline and three classical regression models under one
reproducible experiment contract, then translate their metrics and errors into
an auditable technical decision.

## Scope

```text
validated Sprint 1 features
    -> experiment contract
    -> chronological train/test split
    -> training-mean baseline
    -> Linear Regression
    -> Random Forest
    -> Gradient Boosting
    -> common metrics
    -> error analysis
    -> decision rule
    -> model cards
    -> comparison report
    -> read service / API / dashboard
```

## User

The primary user is a retail analyst reviewing which classical candidate is
most defensible for continued platform development. A technical stakeholder
needs traceable configuration, metrics, errors and limitations.

## Current state

- Sprint 1 remains closed at `v0.1.0-sprint-01-demand-insight`.
- Global Days 57–67 / Sprint 2 Days 1–11 are complete.
- Target, features, metrics and fairness rules are documented.
- The official 12-row training and 6-row test partitions are generated with a
  source checksum and explicit chronological boundary.
- The training-mean baseline and common MAE/RMSE/R² result contract are
  implemented without using test targets during fitting.
- Linear Regression is evaluated through shared training-only preprocessing.
- Random Forest is evaluated with a fixed seed and bounded configuration.
- Gradient Boosting completes the three learned comparison candidates.
- Week 5 closes with four validated, comparable result rows.
- Week 6 decision criteria are frozen before formal selection evidence.
- The formal comparison table records ranks and baseline-relative metrics.
- Residuals and largest observed errors are documented without causal claims.
- Random Forest is selected for the next integration step under the frozen rule.
- The candidate is not production ready; no endpoint or React feature exists yet.

## Weeks

| Week | Global days | Scope |
|---|---:|---|
| Week 5 | 57–63 | completed: experiment setup, baseline and three candidates |
| Week 6 | 64–70 | metrics, errors, decision, cards and report |
| Week 7 | 71–77 | backend and dashboard integration |
| Week 8 | 78–84 | hardening, evidence and Sprint 2 release |

## Official outputs

Planned output families:

- prepared train/test partitions and split manifest;
- prediction and metric evidence per candidate;
- comparison table;
- structured error notes;
- selection decision;
- model cards and Decision Cards;
- technical and visual report;
- versioned backend resource and frontend presentation in Week 7.

## Limits

- The dataset has only 18 synthetic observations.
- The test partition has six observations.
- Model quality cannot be generalized to real retail operations.
- No hyperparameter search, forecasting or inventory action belongs here.
- Backend and frontend work cannot begin before Week 7.
- Sprint 3 remains inactive.

## Closure criteria

Sprint 2 closes only after the common experiment is reproducible, errors and
limitations are visible, API and dashboard integration pass the repository gate
and release `v0.2.0-sprint-02-model-comparison` is prepared through Gitflow.
