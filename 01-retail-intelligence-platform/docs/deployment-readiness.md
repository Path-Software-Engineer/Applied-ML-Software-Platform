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
store, cloud account or secret. The zero-byte `docker-compose.yml` remains an
unused initial placeholder and is not an executable deployment definition.

## Prepared GCP topology

```text
Cloud Build -> Artifact Registry
                  -> FastAPI image -> public API Cloud Run service
                  -> React image   -> public web Cloud Run service
```

Both Cloud Run services use request-based scaling with zero minimum instances
and one maximum instance for the initial portfolio deployment. CPU throttling
is explicit and startup CPU boost is disabled.

`deployment/gcp/deploy.ps1` provisions and updates this topology. The frontend
is built with the exact API HTTPS origin, and the backend validates an exact
`CORS_ALLOWED_ORIGINS` value. A dedicated runtime service account receives no
project role. This configuration is deployment-ready but remains unverified in
GCP until an authorized project and billing account are supplied.

## Configuration and startup

- Python dependencies are pinned in `requirements.txt`.
- Frontend dependencies and package-manager version are pinned in
  `frontend/dashboard-app/package-lock.json` and `package.json`.
- API and frontend startup commands are documented in `docs/runbook.md`.
- GCP build and deployment commands are documented in `deployment/gcp/README.md`.
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

- execute and verify the prepared deployment in an authorized GCP project;
- configure budgets, ownership, retention and operational alerting;
- introduce identity, authorization and tenant isolation;
- replace synthetic evidence with governed retail data;
- add external model validation and production monitoring;
- integrate live inventory and supplier systems before operational action;
- complete real-browser responsive and accessibility evidence.

These gaps are explicit acceptance boundaries, not hidden deployment work.
