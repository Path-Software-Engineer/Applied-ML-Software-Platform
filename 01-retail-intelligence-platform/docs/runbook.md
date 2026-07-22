# Local Runbook

## Prerequisites

- Python 3.12 available as `python`;
- Node.js 24 and npm 11;
- PowerShell 5.1 or newer;
- ports 8000 and 5173 available on loopback.

## Clean setup

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install `
  -r ai-services\demand-insight\requirements.txt `
  -r ai-services\model-comparison\requirements.txt `
  -r ai-services\inventory-decision\requirements.txt `
  -r backend\api\requirements-lock.txt
npm ci --prefix frontend\dashboard-app
```

## Regenerate evidence

```powershell
.\scripts\generate-platform-evidence.ps1
```

This runs Demand Insight first, then Model Comparison, then Inventory Decision.
Stop on the first failure; do not run backend or frontend with partial evidence.

## Start locally

Terminal 1:

```powershell
.\scripts\run-backend.ps1
```

Terminal 2:

```powershell
.\scripts\run-frontend.ps1
```

Open `http://127.0.0.1:5173`. API health is available at
`http://127.0.0.1:8000/health` and OpenAPI at `http://127.0.0.1:8000/docs`.

## Validate

```powershell
.\scripts\run-quality-gate.ps1
git diff --check
git status -sb
```

The gate must pass before release preparation. Generated outputs should remain
byte-equivalent; inspect any real diff before staging it.

## Common failures

- **Missing `.venv`:** create it and install all four pinned requirement files.
- **Missing `node_modules`:** run `npm ci --prefix frontend\dashboard-app`.
- **Port in use:** pass another backend/frontend port to the individual run
  script, then configure the matching proxy or API base URL.
- **Stale inventory warning:** expected for the committed historical snapshot;
  refresh valid source evidence before operational use.
- **Vite `spawn EPERM`:** the repository gate uses the pinned local esbuild
  binary; treat browser/Vite execution as separately blocked if policy denies it.

## Shutdown

Use `Ctrl+C` in each runtime terminal. Both services are local foreground
processes; no database, worker or external service is required.
