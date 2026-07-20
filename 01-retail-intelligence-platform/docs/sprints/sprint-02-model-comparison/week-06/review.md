# Sprint 2 — Week 6 Review

## Completed work

- froze the decision policy before selecting a candidate;
- consolidated four candidates under one comparable metric table;
- reviewed 24 prediction-level residual rows without causal claims;
- separated the observed metric leader from the integration candidate;
- documented all four candidates through versioned Model Cards;
- generated one composite JSON and Markdown comparison report;
- generated three structured Decision Cards for later API consumption.

## Evidence

- `reports/outputs/model-comparison/comparison_table.json`;
- `reports/outputs/model-comparison/error_analysis.json`;
- `reports/outputs/model-comparison/model_decision.json`;
- `reports/model-cards/model-comparison/model_cards.json`;
- `reports/outputs/model-comparison/model_comparison_report.json`;
- `reports/decision-cards/model-comparison/decision_cards.json`.

## Validation

The Week 6 closure gate passed 83 Python tests, 7 frontend contract tests,
frontend compilation and 37 manual checks. The report exposes four comparable
candidates and three Decision Cards under `schema_version: 1.0`.

## Decision

Gradient Boosting remains the observed MAE leader. Random Forest is selected
for the next platform-integration step because both candidates fall within the
frozen 0.25-unit practical-equivalence tolerance and Random Forest has lower
recorded complexity.

This selection is not a production recommendation. It authorizes only the
read-only integration work planned for Week 7.

## Week close

Week 6 is complete. All evidence remains `not_production_ready`, based on one
18-row synthetic dataset and one six-row chronological holdout. Week 7 may read
the canonical report; it may not retrain models or recompute the decision.
