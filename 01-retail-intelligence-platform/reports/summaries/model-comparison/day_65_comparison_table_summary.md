# Model Comparison Day 65 Formal Metrics Summary

The formal comparison table ranks all four comparable candidates by MAE and
records RMSE, contextual R², delta versus baseline and percentage improvement.

Outputs:

- `reports/outputs/model-comparison/comparison_table.csv`;
- `reports/outputs/model-comparison/comparison_table.json`;
- `reports/outputs/model-comparison/comparison_table.md`.

The table identifies the observed metric leader and candidates inside the
0.25-unit practical-equivalence tolerance. It deliberately records
`selection_status: not_selected`; error review and the frozen complexity rule
remain required.

The separate metrics lab demonstrates why RMSE exposes a concentrated miss more
strongly than MAE without reusing official candidate results.
