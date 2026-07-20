# Model Comparison Day 71 Integration Exploration Summary

Day 71 selects a read-only platform flow around the canonical Day 69 report.
The proposed resource is `GET /api/v1/model-comparisons/summary` with schema
version `1.0` and explicit `loading`, `connected` and `unavailable` frontend
states.

Training and decision ownership remain inside `ai-services/model-comparison`.
Backend validates and maps evidence, FastAPI owns transport, and React owns
presentation. No runtime integration is implemented on Day 71.
