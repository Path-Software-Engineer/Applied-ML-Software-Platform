# Day 114 — Inventory Data Contract Summary

- Contract and schema version: `inventory_snapshot` / `1.0`.
- Evidence status: `synthetic_learning_snapshot`.
- Stable product key: `product_id`.
- Stock unit: `units`.
- Official source rows: 6 products.
- Negative stock, future observations, incompatible units, invalid lead time,
  duplicate identities and unknown fields are rejected.
- Missing lead time remains `null`; this layer does not invent a source value.
