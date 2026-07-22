# Deployment Readiness

## Release boundary

`v1.0.0-retail-intelligence-platform` is a reproducible local learning release.
It is ready to run from a clean checkout with the documented Python and Node.js
prerequisites. It is not a production deployment approval.

## Supported local topology

```text
browser :5173
  -> React dashboard
  -> FastAPI :8000
  -> validated, versioned reports on the local filesystem
```

The API is read-only. It does not require a database, message broker, object
store, cloud account or secret. `docker-compose.yml` and the `deployment/`
subdirectories are empty placeholders inherited from the initial repository
scaffold; they are not an executable deployment definition and are excluded
from the release claim.

## Configuration and startup

- Python dependencies are pinned in `requirements.txt`.
- Frontend dependencies and package-manager version are pinned in
  `frontend/dashboard-app/package-lock.json` and `package.json`.
- API and frontend startup commands are documented in `docs/runbook.md`.
- Canonical evidence is regenerated with `scripts/generate-platform-evidence.ps1`.
- Release acceptance is executed with `scripts/run-quality-gate.ps1`.

No credentials, tokens or environment-specific absolute paths are required by
the supported local flow.

## Operational checks

| Check | Expected result | Evidence |
|---|---|---|
| API process | `GET /health` returns HTTP 200 | `checks/check_final_platform_smoke.py` |
| Demand resource | schema 1.0 and 293 observed units | same live HTTP smoke |
| Comparison resource | schema 1.0 and Random Forest selection | same live HTTP smoke |
| Inventory resource | schema 1.0 and 97 review units | same live HTTP smoke |
| Frontend | compiled shell serves and references all stages | same live HTTP smoke |
| Full repository | all tests, bundles and manual checks pass | root quality gate |

## Production gaps

- choose and document a real hosting target;
- add production container images and orchestration only for that target;
- introduce identity, authorization and tenant isolation;
- replace synthetic evidence with governed retail data;
- add external model validation and production monitoring;
- integrate live inventory and supplier systems before operational action;
- complete real-browser responsive and accessibility evidence.

These gaps are explicit acceptance boundaries, not hidden deployment work.
