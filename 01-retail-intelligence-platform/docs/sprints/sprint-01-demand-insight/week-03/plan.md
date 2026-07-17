# Sprint 1 - Week 3 Plan

## Contexto

La Semana 3 pertenece al Sprint 1: Demand Insight Module.

Después de completar carga de datos, limpieza, features, revenue, baseline, MAE y pipeline técnico, esta semana se enfoca en traducir datos procesados en análisis entendible para el usuario retail.

El objetivo no es entrenar un modelo nuevo.

El objetivo es convertir ventas observadas en señales de negocio.

---

# Objetivo de la Semana 3

Construir la capa de análisis e insights del módulo Demand Insight.

La semana debe avanzar desde resumen de ventas hasta insight cards y visualización básica.

Flujo esperado:

datos procesados
→ resumen de ventas
→ rankings
→ análisis temporal
→ insight cards
→ gráficos básicos
→ documentación y cierre

---

# Día 15 — Exploración de análisis e insights

Objetivo:

Definir cómo se analizarán las ventas y cómo se comunicarán los resultados al usuario.

Debe dejar como evidencia:

- criterios de análisis;
- definición de Insight Card;
- lenguaje de usuario;
- preguntas de negocio;
- plan de Semana 3.

No debe producir código pesado.

---

# Día 16 — Sales Summary

Objetivo:

Crear un resumen de ventas observadas.

Debe responder:

- demanda observada total;
- revenue total;
- cantidad de registros analizados;
- productos observados;
- rango temporal disponible.

Evidencia esperada:

- archivo de resumen de ventas;
- documentación breve del resultado;
- validación básica.

---

# Día 17 — Product Ranking

Objetivo:

Identificar productos destacados por unidades vendidas y revenue.

Debe responder:

- qué producto vendió más unidades;
- qué producto generó más revenue;
- si la demanda y el revenue cuentan la misma historia;
- qué productos deben aparecer primero en el dashboard.

Evidencia esperada:

- ranking por unidades;
- ranking por revenue;
- resumen interpretativo.

---

# Día 18 — Temporal Sales Analysis

Objetivo:

Analizar el comportamiento de ventas según el tiempo disponible en el dataset.

Debe responder:

- qué día tuvo más ventas;
- qué día generó más revenue;
- si hay concentración temporal;
- qué señales temporales deben mostrarse al usuario.

Evidencia esperada:

- resumen temporal;
- interpretación de señales;
- limitaciones del análisis temporal.

---

# Día 19 — Insight Cards

Objetivo:

Crear las primeras Insight Cards del módulo Demand Insight.

Cada card debe contener:

- Title;
- Metric;
- Insight;
- Recommendation;
- Limitation.

Evidencia esperada:

- archivo estructurado de insight cards;
- documentación de cards;
- validación de campos mínimos.

---

# Día 20 — Basic Charts and Visual Report

Objetivo:

Crear gráficos básicos para apoyar las insight cards y preparar el dashboard inicial.

Debe incluir visualizaciones simples como:

- ventas por producto;
- revenue por producto;
- ventas por día;
- comparación básica entre demanda y revenue.

Evidencia esperada:

- figuras generadas;
- reporte visual básico;
- conexión clara entre gráfico e insight.

---

# Día 21 — Tests, Documentation and Week Close

Objetivo:

Cerrar la Semana 3 con validación, documentación y evidencia ordenada.

Debe confirmar:

- que los análisis existen;
- que las insight cards tienen estructura válida;
- que los gráficos fueron generados;
- que las conclusiones tienen limitaciones;
- que la documentación explica el flujo de la semana.

Evidencia esperada:

- checks mínimos;
- actualización de documentación;
- resumen de cierre semanal.

---

# Criterios de análisis

Durante la Semana 3, cada análisis debe cumplir:

- usar datos procesados;
- producir una métrica clara;
- explicar qué significa la métrica;
- evitar lenguaje técnico innecesario;
- incluir limitaciones;
- preparar información útil para dashboard.

---

# Preguntas de negocio

La Semana 3 debe responder:

- ¿Cuál es la demanda observada total?
- ¿Cuál es el revenue observado total?
- ¿Qué producto vendió más unidades?
- ¿Qué producto generó más revenue?
- ¿Qué día tuvo mayor movimiento?
- ¿Qué señales deben convertirse en Insight Cards?
- ¿Qué limitaciones debe conocer el usuario?

---

# Regla de producto

El usuario final no debe sentir que está leyendo un reporte técnico de machine learning.

Debe sentir que está viendo un resumen claro de su negocio.

---

# Resultado esperado de la semana

Al final de la Semana 3, el módulo Demand Insight debe tener una primera capa de análisis capaz de alimentar el dashboard inicial del Sprint 1.

---

# Sprint Boundary Rule

During Sprint 1, the repository must document only active Sprint 1 work.

Sprint 2 and Sprint 3 documentation should not be maintained as active sprint files before those sprints officially start.

This keeps the project aligned with Gitflow and release discipline:

- Sprint 1 documentation belongs to Sprint 1;
- Sprint 2 documentation starts when Sprint 2 opens;
- Sprint 3 documentation starts when Sprint 3 opens;
- future sprint files should not create the impression that later sprint scope is already active.

This rule follows the same discipline used for releases: each sprint must earn its own documentation, evidence and closure.
