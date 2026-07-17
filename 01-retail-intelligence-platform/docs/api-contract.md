# Demand Insight API Contract

## Status

Planned on Day 22. The endpoint is not implemented until Day 24.

## Resource

```http
GET /api/v1/demand-insights/summary
```

The resource exposes the validated Sprint 1 demand summary for a read-only
dashboard. It accepts no query parameters in version 1.0.

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
