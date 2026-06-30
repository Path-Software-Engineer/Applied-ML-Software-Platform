# Building Projects Roadmap — Plan 1

## 🧠 Applied ML Microproducts

Esta organización reúne los proyectos del **Plan 1 — Applied ML Microproducts** dentro de **Building Projects**.

Este plan acompaña directamente al:

```txt id="bp1-ai-relation"
AI Engineer Plan 1 — Machine Learning Engineering & Software Foundations
```

La idea central es construir proyectos propios más pequeños, visibles y terminables, alineados con proyectos específicos de AI Engineer.

Building Projects no reemplaza AI Engineer.

Building Projects convierte el aprendizaje técnico profundo en evidencia aplicada.

```txt id="bp1-core"
AI Engineer = profundidad técnica
Building Projects = aplicación visible
```

---

# 🎯 Objetivo general

Construir microproductos de IA aplicada capaces de:

* Convertir datos en insights.
* Crear reportes visuales.
* Comparar modelos de forma entendible.
* Crear dashboards ligeros.
* Traducir resultados técnicos a lenguaje de usuario.
* Generar evidencia para GitHub.
* Documentar decisiones.
* Crear capturas y outputs.
* Acompañar la ruta principal sin inflar el alcance.

---

# 🔗 Regla de match del Plan 1

Building Projects hará match solo con los proyectos impares de AI Engineer.

```txt id="bp1-match-rule"
Proyecto 1 IA → Proyecto 1 Building
Proyecto 2 IA → Nada
Proyecto 3 IA → Proyecto 2 Building
Proyecto 4 IA → Nada
Proyecto 5 IA → Proyecto 3 Building
Proyecto 6 IA → Nada
```

Esto significa que este plan tendrá **3 proyectos**, no 6.

Cada proyecto Building toma como referencia la duración del proyecto IA correspondiente.

---

# 🗺️ Cronograma Plan 1

| Semana Building |                             Proyecto Building | Match IA |  Duración | Objetivo                                     |
| --------------- | --------------------------------------------: | -------: | --------: | -------------------------------------------- |
| 1-4             |              `01-product-demand-insight-lite` |    IA 01 | 4 semanas | Insights de demanda y ventas                 |
| 5-8             | `02-classical-model-comparison-visual-report` |    IA 03 | 4 semanas | Comparación visual de modelos clásicos       |
| 9-13            |        `03-inventory-decision-dashboard-lite` |    IA 05 | 5 semanas | Dashboard ligero de decisiones de inventario |

Duración total del Plan 1:

```txt id="bp1-duration"
13 semanas
```

---

# 🧭 Filosofía de trabajo

Cada proyecto debe cerrar con evidencia visible.

Regla central:

```txt id="bp1-philosophy"
No basta con que el código funcione.
Debe verse, entenderse y poder explicarse.
```

Un Building Project debe ser:

```txt id="bp1-values"
pequeño
útil
visual
documentado
terminable
publicable
```

No debe convertirse en el proyecto grande de AI Engineer.

---

# 🧩 Conceptos base

## Proyecto propio aplicado

Un proyecto propio aplicado es un repositorio pequeño o mediano de GitHub.

Debe demostrar una habilidad concreta y visible.

Puede incluir:

* README.
* Datos de ejemplo.
* Notebook.
* Scripts.
* Dashboard.
* Gráficos.
* Reportes.
* Capturas.
* Labs pequeños.
* Demo local.

---

## Módulo

Un módulo es una parte funcional del proyecto.

Ejemplo:

```txt id="bp1-module-example"
Módulo: Insight Cards
```

Significa:

```txt id="bp1-module-meaning"
Tomo resultados técnicos.
Los convierto en tarjetas claras.
Explico qué significan.
Hago que una persona no técnica entienda el valor.
```

---

## Lab

Un lab es un experimento pequeño y cerrado.

En Building Projects, los labs deben fortalecer el proyecto sin hacerlo pesado.

Tipos de labs:

```txt id="bp1-lab-types"
tec-labs
cloud-labs
docs-labs
product-labs
```

Regla:

```txt id="bp1-lab-rule"
El lab debe dejar una comparación, una conclusión y una evidencia.
```

---

# 📁 Proyectos del Plan 1

---

## 01 — product-demand-insight-lite

### Match

```txt id="bp01-match"
AI Engineer Proyecto 01 — retail-demand-prediction-api
```

### Duración

```txt id="bp01-duration"
4 semanas
```

---

## 🧠 Descripción

Microproducto aplicado para analizar ventas de productos y generar insights básicos de demanda.

Este proyecto acompaña al primer proyecto grande de AI Engineer, pero con un alcance más pequeño.

Mientras AI Engineer construye un sistema ML profesional con modelo, inferencia, API, tests y documentación, Building Projects construye una herramienta visual y terminable centrada en análisis, insights, gráficos y dashboard ligero.

---

## 🎯 Objetivo

Crear una herramienta ligera que analice ventas de productos y genere evidencia visible sobre demanda observada.

El objetivo es convertir datos simples en:

```txt id="bp01-output"
análisis
→ baseline
→ métrica
→ insights
→ gráficos
→ dashboard ligero
→ README
```

---

## 👤 Usuario objetivo

* Dueño de tienda pequeña.
* Analista junior.
* Persona que quiere entender ventas.
* Reclutador técnico viendo evidencia aplicada.
* Yo mismo como constructor de portafolio.

---

## 🧱 Arquitectura esperada

```txt id="bp01-architecture"
CSV / dataset pequeño
      ↓
Carga de datos
      ↓
Limpieza
      ↓
Features simples
      ↓
Baseline
      ↓
MAE
      ↓
Análisis de ventas
      ↓
Insight cards
      ↓
Gráficos
      ↓
Dashboard ligero
```

---

## 🔁 Flujo técnico

```txt id="bp01-flow"
data/raw
→ load_data
→ clean_data
→ feature_engineering
→ baseline
→ metrics
→ analysis
→ insight_cards
→ charts
→ dashboard
→ README
```

---

## 🧩 Módulos

### Módulo 1 — Data Loading

Cargar datos de ventas desde CSV.

Incluye:

* Leer dataset.
* Validar ruta.
* Revisar columnas.
* Revisar primeras filas.
* Mantener data/raw sin modificar.

---

### Módulo 2 — Data Cleaning

Limpiar datos básicos sin destruir información.

Incluye:

* Convertir fechas.
* Revisar nulos.
* Revisar valores imposibles.
* Validar unidades vendidas.
* Validar precios.

---

### Módulo 3 — Feature Engineering

Crear señales simples.

Incluye:

* `day_of_week`.
* `month`.
* `year`.
* `is_weekend`.
* `revenue`.

---

### Módulo 4 — Baseline and MAE

Crear referencia mínima.

Incluye:

* Baseline promedio.
* Predicción simple.
* MAE.
* Interpretación en lenguaje simple.

---

### Módulo 5 — Sales Analysis

Calcular resultados principales.

Incluye:

* Producto más vendido.
* Producto con mayor revenue.
* Revenue total.
* Unidades totales.
* Mejor día de ventas.

---

### Módulo 6 — Insight Cards

Convertir resultados en tarjetas entendibles.

Incluye:

* Título.
* Valor.
* Explicación.
* Recomendación.
* Limitación.

---

### Módulo 7 — Visual Report

Crear gráficos simples.

Incluye:

* Unidades por producto.
* Revenue por producto.
* Unidades por día.
* Comparación visual.

---

### Módulo 8 — Dashboard Lite

Crear una vista ligera del producto.

Puede ser:

* `dashboard/README.md`;
* Streamlit simple;
* notebook visual;
* HTML ligero.

---

## 🧪 Labs

### tec-labs

* `tec-sales-eda-lab`
* `tec-product-ranking-lab`
* `tec-basic-demand-insight-lab`

### cloud-labs

* `cloud-local-csv-to-gcp-cloud-storage-lab`
* `cloud-local-csv-to-aws-s3-lab`
* `cloud-local-csv-to-azure-blob-lab`

---

## 📊 Métricas / señales de análisis

* Total de unidades vendidas.
* Revenue total.
* Producto líder por unidades.
* Producto líder por revenue.
* Mejor día de ventas.
* Baseline promedio.
* MAE del baseline.
* Número de insights generados.
* Número de gráficos generados.

---

## 📌 Próximos pasos

* Cerrar pipeline de datos.
* Crear features.
* Calcular baseline.
* Generar análisis principal.
* Crear insight cards.
* Crear gráficos.
* Preparar dashboard ligero.
* Cerrar labs.
* Actualizar README.
* Agregar capturas.
* Publicar en GitHub.

---

## ✅ Entregable final

Al terminar este proyecto debe existir:

* Microproducto de demanda.
* Dataset pequeño.
* Pipeline local.
* Baseline.
* MAE.
* Análisis de ventas.
* Insight cards.
* Gráficos.
* Dashboard ligero.
* Labs documentados.
* README profesional.
* Capturas o outputs visibles.

---

## 🧭 Regla final

```txt id="bp01-rule"
Este proyecto no compite con la API grande de AI Engineer.
Este proyecto convierte la base común en evidencia visible.

Datos → análisis → insights → gráficos → dashboard.
```

---

# 02 — classical-model-comparison-visual-report

### Match

```txt id="bp02-match"
AI Engineer Proyecto 03 — classical-model-comparison-suite
```

### Duración

```txt id="bp02-duration"
4 semanas
```

---

## 🧠 Descripción

Microproducto para comparar modelos clásicos de Machine Learning de forma visual, entendible y documentada.

Este proyecto acompaña al proyecto grande de AI Engineer enfocado en comparación de modelos clásicos.

Mientras AI Engineer profundiza en entrenamiento, evaluación, estructura, tests y comparación técnica, Building Projects convierte esa comparación en un reporte visual claro.

---

## 🎯 Objetivo

Crear una herramienta que permita comparar baseline y modelos clásicos mediante métricas, tablas, visuales y tarjetas de decisión.

El objetivo es responder:

```txt id="bp02-question"
¿Qué modelo funcionó mejor?
¿Por qué?
¿Qué métrica lo demuestra?
Qué limitaciones tiene la comparación?
Qué modelo elegiría para esta versión?
```

---

## 👤 Usuario objetivo

* AI Engineer en formación.
* Analista de datos.
* Reclutador técnico.
* Persona que quiere entender model comparison sin leer todo el código.
* Usuario que necesita una recomendación clara de modelo.

---

## 🧱 Arquitectura esperada

```txt id="bp02-architecture"
Dataset pequeño
      ↓
Baseline
      ↓
Modelo 1
      ↓
Modelo 2
      ↓
Modelo 3
      ↓
Métricas
      ↓
Tabla comparativa
      ↓
Error notes
      ↓
Decision cards
      ↓
Visual report
```

---

## 🔁 Flujo técnico

```txt id="bp02-flow"
data
→ train/test split
→ baseline
→ train classical models
→ calculate metrics
→ compare results
→ generate decision cards
→ export report
```

---

## 🧩 Módulos

### Módulo 1 — Dataset Setup

Preparar dataset pequeño para comparación.

Incluye:

* Cargar datos.
* Separar features y target.
* Crear train/test split.
* Documentar limitaciones.

---

### Módulo 2 — Baseline Summary

Crear referencia mínima.

Incluye:

* Baseline simple.
* Métrica base.
* Interpretación.
* Por qué el baseline importa.

---

### Módulo 3 — Classical Models

Entrenar o registrar modelos clásicos.

Puede incluir:

* Linear Regression.
* Decision Tree.
* Random Forest.
* Logistic Regression si es clasificación.
* SVM si aplica.

---

### Módulo 4 — Metrics Table

Crear tabla comparativa.

Incluye:

* MAE.
* RMSE.
* Accuracy.
* Precision.
* Recall.
* F1.
* Tiempo de entrenamiento si aplica.

---

### Módulo 5 — Error Notes

Documentar errores principales.

Incluye:

* Casos donde falla.
* Casos donde mejora.
* Riesgo de overfitting.
* Dataset pequeño.
* Limitaciones.

---

### Módulo 6 — Decision Cards

Crear tarjetas de decisión.

Incluye:

* Mejor modelo.
* Modelo más simple.
* Modelo más riesgoso.
* Modelo recomendado.
* Justificación.

---

### Módulo 7 — Visual Report

Crear reporte visual final.

Incluye:

* Tabla.
* Gráficos.
* Tarjetas.
* Conclusión técnica.
* Siguiente paso.

---

## 🧪 Labs

### tec-labs

* `tec-baseline-vs-model-lab`
* `tec-metrics-comparison-lab`
* `tec-error-analysis-card-lab`
* `tec-model-decision-card-lab`

### docs-labs

* `docs-model-comparison-report-template-lab`
* `docs-technical-storytelling-lab`

### cloud-labs

* `cloud-model-report-to-gcp-storage-lab`
* `cloud-model-report-to-aws-s3-lab`
* `cloud-model-report-to-azure-blob-lab`

---

## 📊 Métricas / señales de análisis

Según el tipo de problema:

### Regresión

* MAE.
* RMSE.
* R².
* Error promedio.
* Error máximo.

### Clasificación

* Accuracy.
* Precision.
* Recall.
* F1-score.
* Confusion matrix.

### Señales de decisión

* Mejor métrica.
* Simplicidad.
* Interpretabilidad.
* Riesgo de sobreajuste.
* Facilidad de explicar.
* Calidad del reporte.

---

## 📌 Próximos pasos

* Elegir dataset pequeño.
* Definir problema.
* Crear baseline.
* Entrenar modelos clásicos.
* Calcular métricas.
* Crear tabla comparativa.
* Crear notas de error.
* Crear decision cards.
* Exportar reporte.
* Documentar limitaciones.
* Actualizar README.
* Agregar capturas.

---

## ✅ Entregable final

Al terminar este proyecto debe existir:

* Reporte visual de comparación.
* Baseline.
* Modelos clásicos comparados.
* Tabla de métricas.
* Error notes.
* Decision cards.
* Recomendación final.
* README profesional.
* Capturas.
* Labs documentados.

---

## 🧭 Regla final

```txt id="bp02-rule"
Comparar modelos no es mirar quién gana una métrica.
Es entender rendimiento, simplicidad, riesgo y decisión técnica.

Un reporte claro vale más que una tabla sin explicación.
```

---

# 03 — inventory-decision-dashboard-lite

### Match

```txt id="bp03-match"
AI Engineer Proyecto 05 — inventory-optimization-ml-service
```

### Duración

```txt id="bp03-duration"
5 semanas
```

---

## 🧠 Descripción

Dashboard ligero para explicar decisiones básicas de inventario usando demanda observada, stock, reglas de reorder y tarjetas de riesgo.

Este proyecto acompaña al proyecto grande de AI Engineer sobre optimización de inventario con ML.

Mientras AI Engineer construye un servicio ML más completo, Building Projects crea una herramienta visual para entender decisiones de inventario de forma práctica.

---

## 🎯 Objetivo

Crear un dashboard ligero que ayude a responder:

```txt id="bp03-questions"
¿Qué productos parecen tener más demanda?
Qué productos tienen riesgo de falta?
Qué productos podrían necesitar reposición?
Qué regla simple puedo usar para sugerir reorder?
Qué limitaciones tiene esta recomendación?
```

---

## 👤 Usuario objetivo

* Dueño de tienda.
* Analista de inventario.
* Operador de negocio.
* Estudiante de AI aplicada.
* Reclutador técnico viendo evidencia de producto.

---

## 🧱 Arquitectura esperada

```txt id="bp03-architecture"
Datos de ventas / inventario
      ↓
Carga y limpieza
      ↓
Demanda observada
      ↓
Stock actual
      ↓
Regla de reorder
      ↓
Risk scoring simple
      ↓
Recommendation cards
      ↓
Dashboard ligero
```

---

## 🔁 Flujo técnico

```txt id="bp03-flow"
data
→ demand summary
→ stock summary
→ reorder rule
→ risk score
→ recommendation cards
→ charts
→ dashboard
→ README
```

---

## 🧩 Módulos

### Módulo 1 — Inventory Inputs

Preparar datos básicos.

Incluye:

* Producto.
* Categoría.
* Unidades vendidas.
* Stock actual.
* Precio.
* Fecha si aplica.

---

### Módulo 2 — Demand Summary

Calcular demanda observada.

Incluye:

* Unidades vendidas por producto.
* Promedio de ventas.
* Tendencia simple.
* Producto con mayor demanda.

---

### Módulo 3 — Stock Summary

Analizar inventario actual.

Incluye:

* Stock por producto.
* Stock bajo.
* Stock suficiente.
* Stock crítico.

---

### Módulo 4 — Reorder Rule

Crear regla simple de reposición.

Ejemplo:

```txt id="bp03-reorder-example"
Si stock actual < demanda promedio estimada × factor de seguridad
→ sugerir reposición
```

Incluye:

* Reorder point.
* Safety factor.
* Umbral.
* Recomendación.

---

### Módulo 5 — Risk Cards

Crear tarjetas de riesgo.

Incluye:

* Riesgo bajo.
* Riesgo medio.
* Riesgo alto.
* Explicación.
* Recomendación.

---

### Módulo 6 — Recommendation Dashboard

Mostrar resultados en dashboard.

Incluye:

* Tabla de productos.
* Estado de inventario.
* Recomendación.
* Gráficos.
* Limitaciones.

---

## 🧪 Labs

### tec-labs

* `tec-reorder-point-lab`
* `tec-stock-risk-card-lab`
* `tec-inventory-recommendation-lab`
* `tec-demand-vs-stock-lab`

### product-labs

* `product-inventory-user-card-lab`
* `product-recommendation-language-lab`

### cloud-labs

* `cloud-inventory-report-to-gcp-storage-lab`
* `cloud-inventory-report-to-aws-s3-lab`
* `cloud-inventory-report-to-azure-blob-lab`

---

## 📊 Métricas / señales de análisis

* Unidades vendidas por producto.
* Stock actual.
* Demanda promedio.
* Reorder point.
* Safety factor.
* Riesgo de stockout.
* Número de productos en riesgo.
* Recomendaciones generadas.
* Productos priorizados.

---

## 📌 Próximos pasos

* Definir dataset pequeño.
* Agregar columna de stock.
* Calcular demanda observada.
* Calcular stock actual.
* Crear regla de reorder.
* Crear risk cards.
* Crear dashboard.
* Agregar gráficos.
* Documentar limitaciones.
* Preparar README.
* Agregar capturas.
* Publicar en GitHub.

---

## ✅ Entregable final

Al terminar este proyecto debe existir:

* Dashboard de inventario.
* Dataset pequeño.
* Demanda observada.
* Stock summary.
* Reorder rule.
* Risk cards.
* Recommendation cards.
* Gráficos.
* README profesional.
* Labs documentados.
* Capturas o outputs visibles.

---

## 🧭 Regla final

```txt id="bp03-rule"
Una recomendación de inventario no debe sonar como verdad absoluta.
Debe explicar la regla, el riesgo y la limitación.

Building Projects convierte la optimización en una decisión visible.
```

---

# 🧱 Ciclo general de cada proyecto

Cada proyecto del Plan 1 sigue este ciclo:

```txt id="bp1-cycle"
1. Definir problema.
2. Definir usuario.
3. Definir valor.
4. Definir alcance pequeño.
5. Crear README inicial.
6. Crear estructura de carpetas.
7. Crear primera versión funcional o documental.
8. Agregar módulos.
9. Crear labs pequeños.
10. Probar si aplica.
11. Documentar decisiones.
12. Agregar capturas.
13. Preparar demo o evidencia.
14. Escribir aprendizajes.
15. Definir limitaciones.
16. Definir siguiente paso.
17. Publicar en GitHub.
18. Conectar con el proyecto IA correspondiente.
```

---

# 🗂️ Estructura recomendada del repositorio

```txt id="bp1-repo-structure"
Applied-ML-Microproducts/
├── 01-product-demand-insight-lite/
│   ├── data/
│   ├── src/
│   ├── checks/
│   ├── reports/
│   ├── dashboard/
│   ├── docs/
│   ├── labs/
│   ├── scripts/
│   └── README.md
│
├── 02-classical-model-comparison-visual-report/
│   ├── data/
│   ├── src/
│   ├── reports/
│   ├── dashboard/
│   ├── docs/
│   ├── labs/
│   └── README.md
│
├── 03-inventory-decision-dashboard-lite/
│   ├── data/
│   ├── src/
│   ├── reports/
│   ├── dashboard/
│   ├── docs/
│   ├── labs/
│   └── README.md
│
└── README.md
```

---

# 📊 Nivel esperado al terminar Plan 1

| Área                                  | Nivel esperado |
| ------------------------------------- | -------------: |
| EDA aplicada                          |           8/10 |
| Pandas práctico                       |           8/10 |
| Limpieza de datos simple              |           8/10 |
| Feature engineering simple            |           8/10 |
| Baseline y métricas básicas           |           8/10 |
| Model comparison visual               |           8/10 |
| Error analysis básico                 |         7.5/10 |
| Dashboards ligeros                    |         8.5/10 |
| Insight cards                         |         8.5/10 |
| Recomendaciones de inventario simples |           8/10 |
| Storytelling técnico                  |         8.5/10 |
| Documentación de proyectos pequeños   |         8.5/10 |
| Evidencia visual de aprendizaje       |         8.5/10 |

---

# 🧠 Resultado esperado del Plan 1

Al completar este plan, podré decir:

```txt id="bp1-result"
Sé construir microproductos de IA aplicada.
Sé convertir datos en insights.
Sé cargar, limpiar y analizar datasets pequeños.
Sé crear baseline y métricas simples.
Sé comparar modelos de forma visual.
Sé crear reportes de decisión técnica.
Sé crear dashboards ligeros.
Sé traducir resultados técnicos a lenguaje de usuario.
Sé crear recomendaciones simples de inventario.
Sé convertir aprendizaje técnico en evidencia visible.
```

---

# 🧭 Regla final de avance

```txt id="bp1-final-rule"
Exploro antes de ejecutar.
Ejecuto con mapa.
Cierro cada lab.
Documento cada avance.
Comparo antes de mejorar.
No construyo por copiar.
Construyo para entender.
```

Frase guía:

```txt id="bp1-final-phrase"
Aprendo profundo en Path-AI-Engineer.
Construyo visible en Building Projects.

Uno me forma.
El otro me muestra.
```

---

# 👤 Autor

**Jean Franck Loa Rojas**

Building Projects Path Builder
Applied ML • Microproducts • Dashboards • Visual Reports • Inventory Decisions • Technical Storytelling
