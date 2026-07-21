# Docs Lab — Model Comparison Report Template

## Question

Which report structure is most reusable by both technical reviewers and a
future read-only backend service?

## Alternatives

- narrative-first: readable, but difficult to validate structurally;
- table-only: comparable, but loses rationale and limitations;
- evidence-first composite: versioned JSON plus human-readable Markdown.

## Decision

Use the evidence-first composite. JSON is the machine-readable source; Markdown
is a generated review surface. Decision Cards remain structured data rather
than manually copied UI prose.

## Boundary

This lab evaluates documentation structure only. It does not create official
metrics or change the selected model.
