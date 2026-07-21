# Sprint 2 — Model Comparison Review

## Outcome

Sprint 2 builds a reproducible four-candidate regression comparison and carries
its frozen evidence through a strict FastAPI resource into a dedicated React
decision surface.

## Acceptance review

| Criterion | Status | Evidence |
|---|---|---|
| common dataset, split and metrics | passed | experiment contract and result artifacts |
| baseline plus three classical models | passed | four versioned result files |
| error analysis and explicit selection | passed | error and decision reports |
| Model Cards and Decision Cards | passed | four cards and three cards |
| read service, API and React integration | passed | cross-layer and HTTP smoke checks |
| Sprint 1 compatibility | passed | Demand Insight endpoint and gate checks |
| complete software quality gate | passed | 96 Python, 18 frontend and 51 manual checks |
| real desktop, tablet and mobile captures | accepted limitation | local URL rejected by browser policy |

## Product decision

Gradient Boosting is the observed MAE leader at 3.0884 units. Random Forest is
selected for the next integration step at 3.1258 MAE because it is within the
frozen 0.25-unit practical-equivalence tolerance and has lower recorded
complexity. Neither is production ready.

## Release readiness

The software and documentation gates pass. The user explicitly accepted the
missing real-app screenshots as a known release limitation and authorized the
release branch, `main` merge and annotated tag. No visual evidence is claimed.

## Next boundary

Sprint 3 is registered only as the next planning boundary. It is not started.
