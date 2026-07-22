# Demand Insight API Contract

## Status

Implemented through Day 26. The response contract was planned on Day 22, the
internal service and structured output were implemented on Day 23, and the
FastAPI endpoint plus HTTP schemas were implemented and tested on Day 24.
Day 26 adds allowlisted delivery of the three validated PNG figures.
Day 27 adds response hardening and client-side contract validation.

## Resource

```http
GET /api/v1/demand-insights/summary
```

The resource exposes the validated Sprint 1 demand summary for a read-only
dashboard. It accepts no query parameters in version 1.0.

## Process health

```http
GET /health
```

Status: `200 OK`

```json
{
  "status": "ok",
  "service": "retail-intelligence-api"
}
```

This endpoint reports process availability only. Analytical evidence is
validated by the Demand Summary resource itself.

## Success response

Status: `200 OK`

```json
{
  "schema_version": "1.0",
  "period": {
    "start_date": "2026-01-01",
    "end_date": "2026-01-09",
    "observed_days": 9
  },
  "sales_summary": {
    "total_units_sold": 293,
    "total_revenue": 747.65,
    "sales_count": 18,
    "unique_products": 6,
    "unique_categories": 3
  },
  "baseline": {
    "mean_units_prediction": 16.28,
    "mae": 5.42
  },
  "leaders": {
    "product_by_units": {
      "name": "Bread",
      "value": 105,
      "unit": "units"
    },
    "product_by_revenue": {
      "name": "Rice 1kg",
      "value": 220.50,
      "unit": "revenue"
    },
    "date_by_units": {
      "name": "2026-01-06",
      "value": 45,
      "unit": "units"
    },
    "date_by_revenue": {
      "name": "2026-01-08",
      "value": 99.30,
      "unit": "revenue"
    }
  },
  "insight_cards": [
    {
      "card_id": "observed-demand",
      "title": "Demanda observada",
      "metric": "293 unidades | 747.65 de revenue",
      "insight": "El periodo analizado va de 2026-01-01 a 2026-01-09.",
      "recommendation": "Usar estos totales como contexto general para interpretar las demás señales del dashboard.",
      "limitation": "Describe únicamente las ventas observadas entre 2026-01-01 y 2026-01-09; no predice demanda futura."
    }
  ],
  "limitations": [
    "The response describes observed sales and does not forecast future demand.",
    "The source covers 18 records from 2026-01-01 through 2026-01-09."
  ]
}
```

The example abbreviates `insight_cards`; the runtime response must include all
five validated cards.

## Unavailable response

Status: `503 Service Unavailable`

```json
{
  "detail": "Demand summary evidence is unavailable or invalid."
}
```

The API must not return partial or fabricated business values when required
evidence is unavailable.

## Figure resources

```http
GET /api/v1/demand-insights/figures/{figure_id}
```

Public identifiers:

- `daily-sales`;
- `product-units-ranking`;
- `product-revenue-ranking`.

A successful request returns `200 OK`, `Content-Type: image/png` and an inline
PNG body with `X-Content-Type-Options: nosniff`. Unknown identifiers return
`404 Not Found`. A known figure whose
artifact is missing or invalid returns `503 Service Unavailable`.

The API resolves identifiers through an allowlist and validates the PNG
signature. Filesystem paths and arbitrary filenames are never accepted from the
request. Empty or oversized known artifacts are rejected before delivery.

## Ownership

- `ai-services/` owns calculations and analytical artifact generation.
- `backend/api/app/services/` owns response assembly and artifact validation.
- `backend/api/app/schemas/` owns HTTP response schemas.
- `backend/api/app/routes/` owns HTTP transport only.
- `frontend/dashboard-app/` consumes the resource and does not parse repository files.

## Compatibility rules

- New optional fields may be added within schema version 1.0.
- Removing or renaming a field requires a new schema version.
- Numeric measures remain numeric; display formatting belongs to the frontend.
- Units and revenue remain distinct values with explicit units.
- Every Insight Card retains its limitation.
- Public figure identifiers are stable within the `/api/v1` contract.

## Local development

Runtime dependencies are pinned in `backend/api/requirements.txt` and fully
resolved in `backend/api/requirements-lock.txt`.

```powershell
.\scripts\run-backend.ps1
```

The local API listens on `http://127.0.0.1:8000` by default. When
`CORS_ALLOWED_ORIGINS` is not set, development CORS allows only
`http://localhost:5173` and `http://127.0.0.1:5173`. A deployment must provide
the exact HTTPS web origin through that environment variable; wildcard origins
and origins containing paths, credentials, queries or fragments are rejected.

## Model Comparison resource

```http
GET /api/v1/model-comparisons/summary
```

Implemented on global Day 73. This read-only resource validates and maps the
canonical Model Comparison report. It returns schema version `1.0`, the fixed
experiment, exactly four candidates, the frozen decision, exactly three
Decision Cards and explicit limitations.

Invalid or unavailable evidence returns `503 Service Unavailable` with:

```json
{
  "detail": "Model Comparison evidence is unavailable or invalid."
}
```

The complete response shape and compatibility rules live in
`docs/model-comparison-read-contract.md`. The route never trains models,
calculates metrics or returns repository paths.
