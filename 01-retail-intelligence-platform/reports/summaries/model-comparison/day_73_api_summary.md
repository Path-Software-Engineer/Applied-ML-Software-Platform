# Model Comparison Day 73 API Summary

Day 73 exposes the validated read resource at
`GET /api/v1/model-comparisons/summary`. Strict Pydantic schemas reject extra
fields and constrain the experiment, four candidates, frozen decision, three
Decision Cards and limitations.

The route delegates to `ModelComparisonService`, performs no training or metric
calculation, and maps controlled service failures to a public `503` without
revealing paths or exception details. HTTP tests and the manual in-process check
validate the resource and its OpenAPI registration.
