# Sprint 1 — Demand Insight Retrospective

## Outcome

Sprint 1 converted a controlled retail CSV into a traceable product capability:
validated analytical evidence, a versioned read API and a React dashboard with
contextual cards and figures.

## What worked well

- Daily feature branches and non-fast-forward merges preserved traceability.
- Production logic, tests, checks and evidence retained distinct responsibilities.
- Analytical meaning was validated before API and frontend integration.
- Explicit limitations prevented observed sales from being presented as forecasts.
- Contract-first integration kept React independent from repository files.

## Challenges

- Windows process restrictions made child-process-based frontend commands
  intermittent inside the engineering runner.
- Visual browser capture was unavailable in the active localhost session.
- Dependency and runtime locks required separate Python and npm workflows.

## Improvements adopted

- The root gate now runs Python and frontend contract tests.
- Frontend compilation uses a deterministic local compiler path in the gate.
- Figure delivery is allowlisted, size-bounded and protected with `nosniff`.
- Client-side contract validation rejects malformed responses before rendering.
- Broken figure requests display an honest unavailable state.

## Carry-forward

- Preserve the Demand Insight API contract when Sprint 2 begins.
- Do not mix model-comparison calculations into Sprint 1 services.
- Add browser capture evidence when the localhost browser policy permits it.
- Keep release tags tied only to a fully passing repository gate.
