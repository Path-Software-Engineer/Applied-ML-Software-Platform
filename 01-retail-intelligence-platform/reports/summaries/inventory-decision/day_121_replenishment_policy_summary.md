# Day 121 — Replenishment Policy Summary

- `inventory-review-policy/1.0` is implemented as pure calculations.
- Exact observed-unit ratios avoid floating-point ceiling drift.
- All six products use the explicit two-day policy default for missing lead time.
- Milk and Bread meet the inclusive reorder trigger.
- Bread: 35-unit reorder point, 70-unit target and 70 suggested units.
- Milk: 18-unit reorder point and 27 suggested units.
- Suggested quantities are whole units and never negative.
