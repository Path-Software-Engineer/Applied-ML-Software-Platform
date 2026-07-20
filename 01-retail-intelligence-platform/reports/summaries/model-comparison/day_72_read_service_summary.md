# Model Comparison Day 72 Read Service Summary

Day 72 adds an internal `ModelComparisonService` that reads only the canonical
Day 69 report, validates its version, experiment, four candidates, frozen
decision, three Decision Cards and limitations, then maps a narrower public
resource.

The service does not import model training code and does not expose HTTP
behavior. Missing, malformed or internally inconsistent evidence produces one
controlled `ModelComparisonError`. Isolated tests write only below temporary
paths.
