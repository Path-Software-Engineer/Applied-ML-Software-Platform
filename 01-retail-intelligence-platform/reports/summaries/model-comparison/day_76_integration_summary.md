# Model Comparison Day 76 Integration Summary

Day 76 validates the complete read path:

```text
model_comparison_report.json
    -> ModelComparisonService
    -> GET /api/v1/model-comparisons/summary
    -> React contract validator
```

The check requires exact equality between the service and API resources and
confirms that candidate and Decision Card evidence still matches the canonical
report. The existing Demand Insight endpoint remains compatible with 293 units
and 747.65 revenue.

The reproducible local smoke starts the real Uvicorn application and a static
server for the compiled React shell. It verifies the HTML and JavaScript assets,
API health and the proxied Model Comparison resource before terminating both
processes. Browser-driven visual review is not claimed: the in-app browser
policy blocked the local URL during this run. No Week 7 closure is claimed on
Day 76.
