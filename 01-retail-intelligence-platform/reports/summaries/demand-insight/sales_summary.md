# Sales Summary — Demand Insight Module

## Día

Sprint 1 — Week 3 — Day 16

## Objetivo

Crear un resumen general de ventas observadas a partir del dataset procesado del módulo Demand Insight.

Este resumen responde:

¿Qué ocurrió en el conjunto de ventas observado?

---

# Entrada

Archivo usado:

`data/processed/demand-insight/sales_feature_baseline_metric_pipeline.csv`

Este archivo contiene ventas procesadas con features, revenue, baseline y error absoluto del baseline.

---

# Salida

Archivo generado:

`data/processed/demand-insight/sales_summary.csv`

---

# Resultados principales

| Métrica | Valor |
|---|---:|
| Demanda observada total | 293 unidades |
| Revenue observado total | 747.65 |
| Cantidad de registros | 18 |
| Productos únicos | 6 |
| Categorías únicas | 3 |
| Fecha inicial | 2026-01-01 |
| Fecha final | 2026-01-09 |
| Promedio de unidades por venta | 16.28 |
| Promedio de revenue por venta | 41.54 |
| Precio unitario promedio | 3.10 |

---

# Interpretación

El dataset contiene 18 registros de ventas observadas entre 2026-01-01 y 2026-01-09.

Durante ese periodo, se observaron 293 unidades vendidas y un revenue total de 747.65.

El promedio de unidades por venta fue 16.28, lo que coincide con el baseline promedio usado en la Semana 2.

El resumen incluye 6 productos únicos y 3 categorías, por lo que permite una primera vista general del comportamiento de ventas.

---

# Diferencia entre demanda y revenue

`units_sold` representa demanda observada porque indica cuántas unidades fueron compradas por los clientes.

`revenue` representa valor económico observado porque depende tanto de las unidades vendidas como del precio unitario.

Ambas métricas son importantes, pero no significan lo mismo.

Un producto puede vender muchas unidades y no generar el mayor revenue si su precio es bajo.

Un producto puede vender menos unidades y generar más revenue si su precio es alto.

---

# Limitaciones

Este resumen describe únicamente el dataset actual.

No garantiza demanda futura.

No mide ganancia o rentabilidad, porque el dataset no incluye costos.

No reemplaza rankings, análisis temporal, insight cards ni visualizaciones.

Es una primera fotografía global de las ventas observadas.
