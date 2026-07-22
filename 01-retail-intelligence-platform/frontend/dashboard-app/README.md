# Retail Intelligence Dashboard

React presentation for the three API-backed product stages:

- Demand Insight;
- Model Comparison;
- Inventory Decision.

Each feature owns its API adapter, request hook and components. The shared shell
owns platform navigation, brand and connection status. React formats public
values but does not calculate metrics, select models, rank inventory or create
fallback business evidence.

## Local commands

From the repository root, start the API first:

```powershell
.\scripts\run-backend.ps1
```

Then start this app:

```powershell
.\scripts\run-frontend.ps1
```

Open `http://127.0.0.1:5173`.

For a clean dependency setup and validation:

```powershell
Set-Location frontend\dashboard-app
npm ci
npm test
npm run build
```

The development proxy sends `/api` to `http://127.0.0.1:8000`. Set
`VITE_API_BASE_URL` before a separately hosted build.

## Runtime states

Every stage exposes loading, connected and unavailable states. Inventory
Decision additionally shows stale evidence prominently while preserving the
validated response for inspection. An unavailable or invalid response displays
no fallback metrics or recommendations.

## Accessibility and responsive behavior

- semantic landmarks, tables, headings and live status regions;
- keyboard-operable expandable stage navigation and skip link;
- visible focus treatment;
- reduced-motion support;
- responsive layouts for desktop, tablet and mobile widths.
