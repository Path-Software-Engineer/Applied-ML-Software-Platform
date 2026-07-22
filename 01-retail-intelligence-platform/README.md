# Retail Intelligence Platform

An evidence-first retail decision-support application built across three
incremental product modules:

1. **Demand Insight** — validates sales, summarizes observed demand and revenue,
   and publishes explainable Insight Cards.
2. **Model Comparison** — evaluates four classical regression candidates on one
   chronological holdout and records a controlled integration decision.
3. **Inventory Decision** — joins observed demand with a stock snapshot and
   produces traceable, human-reviewed replenishment recommendations.

The platform combines Python analytical services, a read-only FastAPI boundary
and a responsive React dashboard. It is a portfolio-grade learning system, not
a production inventory or ordering service.

## Current evidence

| Module | Canonical result | Status |
|---|---|---|
| Demand Insight | 293 units, 747.65 revenue, five Insight Cards | completed |
| Model Comparison | four candidates, Random Forest selected for next integration | completed; learning evidence only |
| Inventory Decision | six products, two in review queue, 97 suggested review units | completed; human review required |

Bread is the observed units leader and first inventory priority. Rice 1kg is the
observed revenue leader. The inventory risk score is a priority index—not a
stockout probability—and no workflow creates purchase orders.

## Architecture

```text
data/raw
  -> analytical services and versioned policies
  -> reproducible CSV, JSON, Markdown and PNG evidence
  -> validating FastAPI read services
  -> strict public response schemas
  -> React feature adapters and three-stage dashboard
```

Responsibilities remain separated:

- `ai-services/` owns analytical and policy calculations;
- `backend/api/` validates canonical artifacts and exposes read-only resources;
- `frontend/dashboard-app/` presents API evidence without recomputing it;
- `checks/`, `tests/` and `reports/` preserve reproducible acceptance evidence;
- `docs/` records contracts, decisions, stories, sprint plans and limitations.

See [architecture.md](docs/architecture.md), [decisions.md](docs/decisions.md),
[runbook.md](docs/runbook.md) and [project-structure.txt](project-structure.txt)
for the detailed boundary and operating procedure.

## Requirements

- Python 3.12
- Node.js 24 and npm 11
- Windows PowerShell 5.1 or newer

## Setup from a clean checkout

Run from this project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install `
  -r ai-services\demand-insight\requirements.txt `
  -r ai-services\model-comparison\requirements.txt `
  -r ai-services\inventory-decision\requirements.txt `
  -r backend\api\requirements-lock.txt

Set-Location frontend\dashboard-app
npm ci
Set-Location ..\..
```

## Run locally

Terminal 1 — API on `http://127.0.0.1:8000`:

```powershell
.\scripts\run-backend.ps1
```

Terminal 2 — dashboard on `http://127.0.0.1:5173`:

```powershell
.\scripts\run-frontend.ps1
```

The Vite proxy forwards same-origin `/api` requests to the local FastAPI
service. Use the expandable sidebar to move between all three modules.

## Prepare a GCP deployment

The repository includes two non-root container images, Cloud Build definitions
and an idempotent PowerShell workflow for Artifact Registry and Cloud Run. The
workflow does not store credentials and is not executed by the quality gate.

After configuring an authorized GCP project, follow
[deployment/gcp/README.md](deployment/gcp/README.md). The deployment command is:

```powershell
.\deployment\gcp\deploy.ps1 -ProjectId "YOUR_GCP_PROJECT_ID"
```

Do not run it before reviewing billing, IAM and public-access policy.

## Public read endpoints

```text
GET /health
GET /api/v1/demand-insights/summary
GET /api/v1/demand-insights/figures/{figure_id}
GET /api/v1/model-comparisons/summary
GET /api/v1/inventory-decisions/summary
```

FastAPI documents the running contract at `http://127.0.0.1:8000/docs`.

## Validate the repository

```powershell
.\scripts\run-quality-gate.ps1
git diff --check
git status -sb
```

The root gate verifies the structure inventory, compiles Python, runs all
Python and frontend tests, compiles the React bundle, builds the local smoke
dashboard and executes every manual check.

Regenerate every official module artifact in dependency order with:

```powershell
.\scripts\generate-platform-evidence.ps1
```

## Evidence and traceability

- Demand output: `reports/outputs/demand-insight/`
- Model comparison output: `reports/outputs/model-comparison/`
- Inventory report and trace: `reports/outputs/inventory-decision/`
- Inventory Recommendation Cards: `reports/recommendation-cards/inventory-decision/`
- Inventory figures: `reports/figures/inventory-decision/`
- User and technical stories: `docs/user-stories.md` and `docs/technical-stories.md`

## Honest limitations

- The source contains only 18 synthetic sales observations.
- Model Comparison uses one six-row chronological holdout; it has no
  cross-validation or external validation.
- Observed daily demand is descriptive, not a validated forecast.
- Inventory lead time uses a documented policy default when source evidence is
  absent.
- Stock is a learning snapshot, not a live transaction feed.
- Recommendations require human review and are not production ready.

## Release line

- `v0.1.0-sprint-01-demand-insight`
- `v0.2.0-sprint-02-model-comparison`
- `v1.0.0-retail-intelligence-platform` — final Sprint 3 target

The project follows feature branches into `develop`, a release branch into
`main`, an annotated release tag and synchronization back to `develop`.
