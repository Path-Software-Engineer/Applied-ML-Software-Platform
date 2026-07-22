# Inventory Decision Release Scope

## Included in `v1.0.0-retail-intelligence-platform`

- versioned inventory, demand-signal, policy and HTTP contracts;
- validated inventory snapshot and strict product join;
- deterministic replenishment, priority ranking and Recommendation Cards;
- canonical JSON, CSV, Markdown, trace and PNG evidence;
- read-only FastAPI service and endpoint;
- responsive React Inventory Decision stage;
- scenario, adversarial, integration and repository quality gates.

## Explicitly excluded

- live inventory transactions or warehouse integration;
- demand forecasting claims for the observed-average signal;
- stockout probabilities or probabilistic service levels;
- supplier, cost, purchase-order or automatic replenishment workflows;
- authentication, authorization, multi-tenancy or production deployment;
- Sprint 4 or a new product feature.

The release is an integrated, reproducible learning platform. Human review and
the documented evidence limitations remain part of the product contract.
