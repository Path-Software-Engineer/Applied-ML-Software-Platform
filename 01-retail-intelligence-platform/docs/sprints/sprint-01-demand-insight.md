
---

## Day 3 — Initial Dataset and Data Contract

### Goal

Create the initial raw dataset and document the expected data contract for the Demand Insight Module.

### Deliverables

```txt
data/raw/demand-insight/sales.csv
docs/data-contract.md
docs/decisions.md updated with Decision 002
```

### Dataset columns

```txt
sale_id
date
product_id
product_name
category
units_sold
unit_price
stock_available
```

### Why this matters

The project needs a stable input before building loading, cleaning, features, baseline and metrics.

The data contract prevents the project from depending on unclear or changing data assumptions.

### Status

Completed when the dataset exists and the contract is documented.
