# Inventory Snapshot Data Contract

Status: preliminary on global Day 113; frozen and machine-validated on Day 114.

## Identity

- contract: `inventory_snapshot`;
- schema version: `1.0`;
- stable join key: `product_id`;
- quantity unit: `units`;
- evidence status: `synthetic_learning_snapshot`.

## Required source fields

| Field | Type | Rule |
|---|---|---|
| `snapshot_id` | string | non-empty snapshot identity |
| `snapshot_as_of_date` | ISO date | common review cutoff |
| `observed_at` | ISO date | date of the stock observation |
| `product_id` | string | unique and shared with Demand Insight |
| `product_name` | string | non-empty display label |
| `stock_on_hand` | integer | zero or greater |
| `stock_unit` | string | exactly `units` in version 1.0 |
| `source_type` | string | provenance, never inferred silently |

`lead_time_days` is optional. When absent, later policy code may use a versioned
default and must expose `lead_time_source=policy_default`.

## Invalid examples

- duplicated `product_id` within a snapshot;
- `stock_on_hand=-1`;
- `stock_unit=cases` when demand is in units and no conversion exists;
- `observed_at` after `snapshot_as_of_date`;
- missing source provenance.

## Evidence boundary

The first repository snapshot is derived learning evidence, not a live stock
ledger. Normalization must not overwrite the raw file.

