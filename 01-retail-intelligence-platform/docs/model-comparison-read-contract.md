# Model Comparison Read Contract

## Status

Finalized for Sprint 2 on global Day 81. The internal service, versioned FastAPI
endpoint, React request lifecycle, comparison view and three API-provided
Decision Cards are implemented and cross-layer validated. No request-time
training or client-side ranking belongs to this contract.

## Resource

```http
GET /api/v1/model-comparisons/summary
```

Version 1 accepts no query parameters and returns only evidence already frozen
in `reports/outputs/model-comparison/model_comparison_report.json`.

## Success resource

```json
{
  "schema_version": "1.0",
  "module": "model_comparison",
  "report_status": "learning_evidence_only",
  "experiment": {
    "dataset_sha256": "<64 lowercase hexadecimal characters>",
    "split_strategy": "chronological_holdout",
    "target": "units_sold",
    "target_unit": "units_per_sale_record",
    "train_rows": 12,
    "test_rows": 6
  },
  "candidates": [
    {
      "model_id": "gradient_boosting",
      "model_name": "Gradient Boosting",
      "model_family": "boosted_tree_ensemble",
      "mae_rank": 1,
      "mae_units": 3.0884,
      "rmse_units": 3.3323,
      "r2_contextual": 0.4539,
      "mae_improvement_vs_baseline_percent": 28.2686,
      "within_practical_equivalence": true,
      "production_status": "learning_evidence_only"
    }
  ],
  "decision": {
    "measurement_leader": {
      "model_id": "gradient_boosting",
      "model_name": "Gradient Boosting",
      "mae_units": 3.0884
    },
    "selected_candidate": {
      "model_id": "random_forest",
      "model_name": "Random Forest",
      "mae_units": 3.1258,
      "mae_improvement_vs_baseline_percent": 27.4009,
      "largest_observed_error_units": 4.4749
    },
    "practical_equivalence_units": 0.25,
    "rationale": ["Evidence-backed reason."],
    "production_status": "not_production_ready",
    "stability_status": "not_assessed"
  },
  "decision_cards": [
    {
      "card_id": "integration-candidate",
      "eyebrow": "Selected for next integration",
      "title": "Random Forest",
      "status": "selected_for_next_integration",
      "model_id": "random_forest",
      "primary_metric": {
        "label": "MAE",
        "value": 3.1258,
        "unit": "units",
        "direction": "lower_is_better"
      },
      "summary": "Evidence-backed summary.",
      "reasons": ["Evidence-backed reason."],
      "limitation": "Not production ready."
    }
  ],
  "limitations": ["Evidence limitation."]
}
```

The abbreviated example contains one candidate and one card. A successful
runtime response must contain exactly four unique candidates and three stable
card identifiers: `metric-leader`, `integration-candidate` and
`evidence-boundary`.

## Unavailable response

Status: `503 Service Unavailable`

```json
{
  "detail": "Model Comparison evidence is unavailable or invalid."
}
```

The public response must not include exception text, artifact paths or partial
metrics.

## Compatibility rules

- removing or renaming a required field requires a new schema version;
- candidate identifiers and card identifiers are stable within version `1.0`;
- numeric measures remain numeric;
- the service maps validated evidence but does not recalculate metrics;
- the frontend renders the resource and does not re-run selection policy.

## Verification

- `tests/backend/test_model_comparison_service.py`;
- `tests/backend/test_model_comparison_api.py`;
- `frontend/dashboard-app/tests/modelComparisonApi.test.js`;
- `checks/check_model_comparison_integration.py`;
- `checks/check_model_comparison_local_smoke.py`.
