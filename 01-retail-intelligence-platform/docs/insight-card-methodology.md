# Insight Card Methodology — Demand Insight Module

## Objetivo

Definir cómo el módulo Demand Insight convertirá datos y métricas en explicaciones claras para un usuario retail.

Una insight card no debe ser solo un número.

Una insight card debe ayudar al usuario a entender una señal del negocio y tomar una decisión simple.

---

# Diferencia entre dato, métrica e insight

## Dato

Un dato es un valor observado dentro del dataset.

Ejemplo:

Producto A vendió 30 unidades.

## Métrica

Una métrica resume o calcula algo a partir de los datos.

Ejemplo:

Producto A fue el producto con mayor número de unidades vendidas.

## Insight

Un insight interpreta una métrica para explicar una señal útil.

Ejemplo:

Producto A concentra la mayor demanda observada. Conviene vigilar su stock y destacarlo en el dashboard.

---

# Regla principal

Un insight no es solo un número.

Un insight es un número interpretado para ayudar al usuario a entender una señal.

---

# Usuario objetivo

El usuario principal del módulo es una persona que necesita entender ventas retail sin leer código ni lenguaje técnico.

El usuario necesita saber:

- cuál fue la demanda observada;
- qué productos vendieron más unidades;
- qué productos generaron más revenue;
- qué días tuvieron más movimiento;
- qué señales merecen atención;
- qué limitaciones tiene el análisis.

---

# Lenguaje permitido

Las cards deben usar lenguaje simple:

- demanda observada
- unidades vendidas
- revenue
- producto con mayor movimiento
- producto con mayor valor económico
- día con más ventas
- señal relevante
- recomendación
- limitación

---

# Lenguaje a evitar en cards de usuario

Las cards no deben usar como lenguaje principal:

- machine learning
- modelo
- predicción
- baseline
- MAE
- feature engineering
- pipeline
- regresión
- entrenamiento

Estos términos pueden existir en documentación técnica, pero no deben dominar la explicación al usuario final.

---

# Estructura de una Insight Card

Cada Insight Card debe contener:

- Title
- Metric
- Insight
- Recommendation
- Limitation

## Title

Nombre corto de la señal.

Ejemplo:

Producto con mayor demanda.

## Metric

Número o resultado observado.

Ejemplo:

Producto A — 30 unidades vendidas.

## Insight

Interpretación de la métrica.

Ejemplo:

Este producto concentra la mayor demanda observada dentro del dataset.

## Recommendation

Acción simple sugerida.

Ejemplo:

Vigilar stock y mostrarlo como producto prioritario en el dashboard.

## Limitation

Advertencia honesta sobre el análisis.

Ejemplo:

El análisis usa datos históricos pequeños y no garantiza demanda futura.

---

# Preguntas de negocio para Semana 3

El módulo debe responder:

- ¿Cuál es la demanda observada total?
- ¿Qué producto vendió más unidades?
- ¿Qué producto generó más revenue?
- ¿Qué día tuvo mayor movimiento?
- ¿Qué señales deben convertirse en Insight Cards?
- ¿Qué limitaciones tiene este análisis?

---

# Regla de calidad

Una Insight Card es válida si una persona no técnica puede entender:

- qué ocurrió;
- por qué importa;
- qué podría hacer;
- qué limitación tiene la conclusión.

---

# Conclusión

El módulo Demand Insight no debe mostrar únicamente métricas.

Debe transformar datos y métricas en información útil para apoyar decisiones simples del usuario retail.

---

# Contrato de implementación

La implementación oficial se encuentra en:

```text
ai-services/demand-insight/src/insights/insight_cards.py
```

Consume únicamente artefactos procesados y validados:

```text
sales_summary.csv
product_ranking_by_units.csv
product_ranking_by_revenue.csv
daily_sales_summary.csv
```

No vuelve a calcular métricas desde las ventas crudas.

Cada card expone:

```text
card_id
title
metric
insight
recommendation
limitation
```

`card_id` proporciona una identidad estable para futuras integraciones con API y React.

## Outputs

```text
reports/insight-cards/demand_insight_cards.json
reports/insight-cards/demand_insight_cards.md
```

El JSON constituye el contrato consumible por software.

El Markdown constituye evidencia legible para revisión humana.

## Alcance actual

Las cards describen únicamente el periodo observado.

No predicen demanda futura.

No justifican por sí solas decisiones definitivas de inventario, producción o promoción.

La presentación visual en React pertenece a una fase posterior y no debe duplicar la lógica que construye las cards.