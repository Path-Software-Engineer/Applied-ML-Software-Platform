# Model Comparison Day 74 Dashboard Summary

Day 74 adds a separate React Model Comparison feature with a dedicated API
client, request hook and presentation component. Hash navigation preserves the
existing Demand Insight view while exposing the new comparison workspace.

The view renders the fixed experiment, selected candidate, four-row comparison
table, rationale and limitations from the versioned API. Loading, connected and
unavailable states never embed fallback metrics. Decision Cards are validated
by the client but remain assigned to the Day 75 visual scope.
