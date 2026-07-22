# Day 120 — Inventory Policy Exploration Summary

- Frozen policy: `inventory-review-policy/1.0`.
- Default lead time: two days, explicitly marked as a policy assumption.
- Safety horizon: one observed-demand day.
- Review period: three days.
- Reorder and target stock use ceiling to whole units.
- Risk combines shortage and coverage pressure as a priority index.
- The score is not a probability and no purchase order is created.
- Runtime implementation begins on Day 121.
