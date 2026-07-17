# Week 3 Exploration Summary — Demand Insight Module

## Día

Sprint 1 — Week 3 — Day 15

## Tipo de día

Exploración.

## Objetivo

Definir cómo el módulo Demand Insight transformará ventas observadas en análisis entendible, insight cards y señales útiles para el usuario retail.

Este día no implementa código pesado.

El objetivo es fijar criterios antes de construir los análisis de la semana.

---

# Contexto previo

La Semana 2 dejó una base técnica lista:

- features temporales;
- revenue calculado;
- baseline promedio;
- MAE del baseline;
- pipeline con features, baseline y métrica;
- reporte técnico de Semana 2.

Con esa base, la Semana 3 puede enfocarse en interpretación de ventas.

---

# Decisión principal

El módulo no debe limitarse a mostrar números.

Debe traducir métricas en señales claras para el usuario.

Una métrica responde qué ocurrió.

Un insight explica por qué importa.

---

# Criterios definidos

Los análisis de Semana 3 deben cumplir:

- partir de datos procesados;
- calcular métricas simples y verificables;
- explicar las métricas en lenguaje de usuario;
- evitar lenguaje técnico innecesario;
- incluir recomendaciones simples;
- declarar limitaciones;
- preparar información útil para el dashboard inicial.

---

# Insight Card definida

Una Insight Card debe contener:

- Title;
- Metric;
- Insight;
- Recommendation;
- Limitation.

Esta estructura evita mostrar métricas aisladas y obliga a explicar el valor de cada señal.

---

# Lenguaje de usuario

Lenguaje permitido:

- demanda observada;
- unidades vendidas;
- revenue;
- producto con mayor demanda;
- producto con mayor valor económico;
- día con más movimiento;
- señal relevante;
- recomendación;
- limitación.

Lenguaje a evitar en cards de usuario:

- machine learning;
- modelo;
- predicción;
- baseline;
- MAE;
- feature engineering;
- pipeline;
- regresión;
- entrenamiento.

---

# Preguntas de negocio acordadas

La Semana 3 debe responder:

- ¿Cuál es la demanda observada total?
- ¿Cuál es el revenue observado total?
- ¿Qué producto vendió más unidades?
- ¿Qué producto generó más revenue?
- ¿Qué día tuvo mayor movimiento?
- ¿Qué señales deben convertirse en Insight Cards?
- ¿Qué limitaciones debe conocer el usuario?

---

# Plan de ejecución

Día 16:

Crear resumen de ventas.

Día 17:

Crear ranking de productos.

Día 18:

Analizar ventas en el tiempo.

Día 19:

Crear Insight Cards.

Día 20:

Crear gráficos básicos y reporte visual.

Día 21:

Validar, documentar y cerrar la semana.

---

# Resultado del día

El Día 15 deja lista la dirección conceptual de la Semana 3.

La siguiente ejecución debe comenzar con el resumen de ventas observadas.
