# Week 9 Plan — Inventory, Data and Signals

## Planned flow

```text
source contract
    -> validated inventory loader
    -> deterministic normalization
    -> observed-demand signal
    -> complete product join and manifest
    -> snapshot summary
    -> Week 9 gate
```

## Daily scope

| Global day | Result |
|---:|---|
| 113 | exploration, architecture and initial traceability |
| 114 | versioned inventory snapshot contract |
| 115 | loader and readable validation errors |
| 116 | deterministic cleaning and processed snapshot |
| 117 | observed-demand contract, join and manifest |
| 118 | factual snapshot summary |
| 119 | isolated suite, documentation and Week 9 closure |

## Expected outputs

- `data/raw/inventory/inventory_snapshot.csv`;
- `data/processed/inventory-decision/inventory_snapshot_clean.csv`;
- `data/processed/inventory-decision/demand_signals.csv`;
- `data/processed/inventory-decision/inventory_signal_snapshot.csv`;
- `data/processed/inventory-decision/integration_manifest.json`;
- factual summary under `reports/summaries/inventory-decision/`.

## Limits

Week 9 does not implement reorder calculations, risk labels, Recommendation
Cards, HTTP resources or React. It prepares validated facts only.

