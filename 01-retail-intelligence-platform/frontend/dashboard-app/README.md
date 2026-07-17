# Demand Insight Dashboard

React dashboard completed through Sprint 1 Day 26.

## Responsibility

- Consume `GET /api/v1/demand-insights/summary` through the API client.
- Present summary metrics, leaders and five validated Insight Cards.
- Present the three validated analytical figures through allowlisted API URLs.
- Provide loading and unavailable states without fallback business values.
- Keep analytical calculations and filesystem access outside React.

## Local run

Start the backend from the repository root:

```powershell
.\scripts\run-backend.ps1
```

In a second terminal:

```powershell
.\scripts\run-frontend.ps1
```

Open `http://127.0.0.1:5173`.

For the first local setup, install the exact dependency tree from the lock file:

```powershell
cd frontend\dashboard-app
npm ci
```

Create the production bundle with:

```powershell
npm run build
```

Run the frontend contract tests with:

```powershell
npm test
```

The default build keeps output unminified so the repository gate remains stable
inside restricted Windows runners. `npm run build:minified` produces the compact
release bundle when child-process execution is available.

## Environment

The Vite development proxy sends `/api` requests to `http://127.0.0.1:8000`.
For a separately hosted API, set `VITE_API_BASE_URL` before building.

## Day 26 boundary

The dashboard presents the completed integration of cards and figures. Model
comparison and inventory views remain outside Sprint 1.

## Functional evidence

- React shell and responsive Demand Insight page under `src/`.
- Dedicated API client under `src/features/demand-summary/api/`.
- Loading, connected and unavailable service states.
- Client-side validation for schema version, required evidence and card count.
- Seven Node tests covering success, malformed responses, `503`, network failure
  and encoded figure identifiers.
- Metrics, four observed leaders and five Insight Cards rendered from the
  versioned response; no fallback business values are embedded in React.
- Three report figures delivered by the backend without copying analytical
  artifacts into the frontend.
- Reproducible dependency graph in `package-lock.json` and a successful Vite
  production build.
