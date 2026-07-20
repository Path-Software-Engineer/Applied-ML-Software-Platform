# Sprint 2 — Week 5 Exploration

## Problem

Sprint 1 describes observed sales but does not compare learned models. Sprint 2
must establish a fair experiment before adding scikit-learn or producing model
metrics.

## Questions and decisions

| Question | Decision |
|---|---|
| User decision | Select an initial regression candidate for continued platform development |
| Target | `units_sold`, measured in units per sale record |
| Dataset | validated `sales_features.csv`, 18 synthetic rows |
| Split | chronological: train through 2026-01-06, test from 2026-01-07 |
| Baseline | training-target mean |
| Candidates | Linear Regression, Random Forest, Gradient Boosting |
| Primary metric | MAE in units |
| Diagnostics | RMSE and contextual R² |
| Fairness | same rows, features, preprocessing, split, metrics and schema |
| Recommendation boundary | only after metrics, errors, rule and model cards |

## Leakage review

Revenue is excluded because `revenue = units_sold * unit_price`. Stock is
excluded because the contract describes it as available after or near the sale,
so its timing relative to the target is ambiguous.

## Alternatives considered

- A random split was rejected because adjacent dates would be mixed and the
  result would be harder to interpret.
- Classification was rejected because the current business target is numeric.
- Cross-validation and hyperparameter search were deferred because the source
  is too small for a convincing search result.
- Reusing the full-dataset Sprint 1 mean prediction was rejected because the
  test targets would influence the baseline.

## Lab allocation

Labs remain separate and are not substitutes for production evidence:

- `tec-baseline-vs-model-lab`: Day 63, after all candidates exist;
- `tec-metrics-comparison-lab`: Day 65;
- `tec-error-analysis-card-lab`: Day 66;
- `tec-model-decision-card-lab`: Day 67;
- `docs-model-comparison-report-template-lab`: Day 69;
- `docs-technical-storytelling-lab`: Day 70;
- `product-model-comparison-ux-lab`: Day 71.

Cloud report labs remain unassigned because the map provides no authorized
cloud execution day before a validated comparison report exists.

## Day 57 close

Exploration is complete. No dependency, training code, model output, backend
route or React view was added.
