# Sprint 1 — Week 1 Exploration

## Purpose

Define the minimum foundation required for a traceable Demand Insight module
before implementing analysis or user-facing functionality.

## Questions

- Which retail user and problem does the first sprint serve?
- What minimum sales schema supports demand and revenue analysis?
- How should raw, clean and processed data remain distinguishable?
- Which repository boundaries prevent data logic from mixing with future UI or API work?

## Alternatives considered

- Start with dashboard screens before validating the data flow.
- Use several unrelated datasets instead of one controlled contract.
- Keep loading, cleaning and reporting in one script.

These alternatives were rejected because they reduce traceability and make
later validation dependent on hidden manual steps.

## Constraints

- Work only inside Sprint 1 Demand Insight.
- Use a local, controlled CSV.
- Keep frontend, backend and later sprints outside the active scope.
- Produce explicit evidence for every completed technical step.

## Exploration decision

Establish the repository architecture, data contract and raw dataset first;
then implement loading, cleaning and one repeatable data pipeline.

## Evidence

- `docs/architecture.md`
- `docs/data-contract.md`
- `docs/decisions.md`
- `data/raw/demand-insight/sales.csv`

## Status

Completed as the exploration basis for Week 1.
