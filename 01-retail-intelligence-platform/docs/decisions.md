# Technical Decisions

## Decision 001 — Base platform architecture

### Context

The project is moving from small applied ML projects into a stronger software platform.

The platform needs to support demand insights, model comparison, inventory decisions, API integration, dashboard views, documentation, labs and future deployment.

### Decision

Use a modular project structure with separated responsibilities:

- frontend/
- backend/
- ai-services/
- data/
- models/
- reports/
- docs/
- labs/
- tests/
- scripts/
- deployment/

### Why

This separation keeps the project clean and prevents mixing responsibilities.

The AI logic should not be mixed with the frontend.

The API layer should not be mixed with notebooks or reports.

The documentation should live in its own place.

Reports and generated outputs should be easy to find.

### Consequences

The project can grow sprint by sprint without becoming messy.

Sprint 1 can focus on the Demand Insight Module.

Sprint 2 can add Model Comparison without breaking the first module.

Sprint 3 can add Inventory Decision logic while reusing the same structure.

### Status

Accepted.
