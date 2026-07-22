# Demand Signal Contract

Status: preliminary on global Day 113; implemented on Day 117.

## Identity

- signal type: `observed_daily_average`;
- source: validated Demand Insight sales evidence;
- period: explicit inclusive start and end dates;
- unit: `units_per_day`;
- product key: `product_id`;
- evidence status: `descriptive_learning_evidence`.

## Required fields

`product_id`, `product_name`, `signal_type`, `signal_value`, `signal_unit`,
`period_start`, `period_end`, `observation_days`, `source_artifact` and
`source_sha256`.

## Formula

For the first learning flow:

```text
signal_value = total observed units for product / calendar days in period
```

The denominator includes the complete observed period, not only dates on which
the product appears. The result is descriptive and is never named forecast.

## Join rule

Inventory and signal product identifiers must form an exact one-to-one set.
Unmatched identifiers fail the official pipeline and are recorded in the
integration manifest for controlled diagnostic runs.

