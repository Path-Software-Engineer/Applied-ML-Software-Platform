# Building Projects Roadmap — Plan 1

## 🧠 Descripción

Esta organización reúne los proyectos del **Plan 1 — IA Aplicada / Microproductos ML**.

El objetivo de esta ruta es construir una base práctica de proyectos propios como complemento directo del camino principal de **AI Engineer**, no creando sistemas grandes, sino herramientas pequeñas, terminables, visibles y útiles.

Esta ruta convierte conceptos de Machine Learning, datos, dashboards, reportes, RAG ligero, costos, latencia y portafolio técnico en evidencia aplicada.

```txt
datos → análisis → features simples → baseline → visualización → dashboard → reporte → demo → evidencia
```

La idea central de este plan es construir microproductos de IA aplicada, documentarlos, hacerlos visibles y convertirlos en evidencia de portafolio.

---

## 🎯 Objetivo general

Construir proyectos propios capaces de:

* Convertir datos en insights.
* Crear dashboards ligeros.
* Analizar ventas y demanda.
* Crear reportes de calidad de modelos.
* Construir herramientas RAG pequeñas.
* Medir costos y latencia de respuestas IA.
* Crear portales simples de evidencia técnica.
* Documentar aprendizajes.
* Generar capturas, demos y README claros.
* Acompañar la ruta principal de AI Engineer con evidencia visible.

---

## 🧭 Filosofía de trabajo

Cada proyecto se trabaja con un ciclo de estudio de 4 días:

```txt
Día 1 → Exploración
Día 2 → Ejecución
Día 3 → Ejecución
Día 4 → Ejecución
```

### Día de exploración

Sirve para:

* Entender el tema.
* Investigar conceptos.
* Definir el mapa de los próximos 3 días.
* Identificar módulos y labs.
* Preparar el criterio práctico antes de construir.
* Conectar el proyecto propio con el proyecto grande correspondiente.

### Días de ejecución

Sirven para:

* Implementar.
* Probar.
* Corregir errores.
* Documentar.
* Cerrar labs.
* Generar evidencia visible.

---

## 🧩 Conceptos base

### Proyecto propio aplicado

Un proyecto propio aplicado es un repositorio pequeño o mediano de GitHub.

Debe demostrar una habilidad concreta y visible.

No tiene que ser tan grande como un proyecto principal de AI Engineer.

Debe ser terminable, útil y publicable, y tener, según corresponda:

* README.
* Frontend simple.
* Backend simple si aplica.
* Notebook si aplica.
* Datos de ejemplo.
* Dashboard.
* Demo.
* Capturas.
* Documentación.
* Labs pequeños.

### Módulo

Un módulo es una parte funcional o técnica del proyecto.

Ejemplo:

```txt
Módulo: Insight Cards
```

Significa:

```txt
Tomo resultados de datos.
Los convierto en tarjetas visuales.
Explico qué significan.
Hago que el usuario entienda el resultado.
```

### Lab

Un lab es un experimento pequeño y cerrado.

Regla personal:

```txt
Un lab debe durar 1 día de horario.
```

Un lab no debe quedar suelto. Debe conectarse al proyecto propio y al proyecto grande correspondiente.

---

## 🧪 Tipos de labs

### ml-labs

Laboratorios de Machine Learning.

Ejemplos:

* Sales EDA.
* Product ranking.
* Basic demand insight.
* Naive forecast.
* Moving average.
* Forecast error.
* Model metrics report.

### rag-labs

Laboratorios de RAG y embeddings.

Ejemplos:

* Chunking básico.
* Semantic search.
* Source display.

### tec-labs

Laboratorios técnicos.

Ejemplos:

* Latency table.
* Prompt comparison.
* Cost estimation.
* Dashboard cards.
* Demo links.

### docs-labs

Laboratorios de documentación.

Ejemplos:

* Cloud architecture notes.
* GCP / AWS / Azure map.
* Model report template.
* README storytelling.

### portal-labs

Laboratorios de portales.

Ejemplos:

* Project gallery.
* Learning notes.
* Demo links.

---

## 🗺️ Cronograma Plan 1

| Semana | Proyecto                               | Objetivo                                |
| ------ | -------------------------------------- | --------------------------------------- |
| 1-4    | `01-product-demand-insight-lite`       | Insights básicos de demanda             |
| 5-8    | `02-mini-sales-forecast-dashboard`     | Forecasting ligero de ventas            |
| 9-13   | `03-cloud-ml-pipeline-notes-dashboard` | Notas visuales de pipeline ML cloud     |
| 14-18  | `04-model-quality-report-generator`    | Reportes simples de calidad ML          |
| 19-24  | `05-personal-document-search-rag-lite` | Buscador semántico ligero               |
| 25-27  | `06-ai-response-cost-latency-notebook` | Medición de costos y latencia IA        |
| 28-36  | `07-ai-portfolio-platform-lite`        | Portal ligero de proyectos y evidencias |

---

# 📁 Proyectos del Plan 1

## 01 — product-demand-insight-lite

### Objetivo

Crear una herramienta ligera que analice ventas de productos y genere insights básicos de demanda.

### Flujo

```txt
CSV / dataset pequeño → Pandas → análisis → features simples → baseline → métricas → gráficos → insight cards → README
```

### Aprendizajes principales

* Pandas.
* EDA.
* Agrupaciones.
* Promedios.
* Features simples.
* Baseline.
* Métricas simples.
* Tendencias simples.
* Visualización.
* Insight cards.
* README.

### Módulos

* Data Loading.
* Basic Sales Analysis.
* Simple Baseline.
* Insight Cards.
* Visual Report.

### Labs

* `ml-sales-eda-lab`
* `ml-product-ranking-lab`
* `ml-basic-demand-insight-lab`

---

## 02 — mini-sales-forecast-dashboard

### Objetivo

Crear un dashboard pequeño que proyecte ventas futuras usando métodos simples.

### Aprendizajes principales

* Forecasting básico.
* Media móvil.
* Naive forecast.
* Lags simples.
* MAE.
* Gráficos de serie temporal.
* Dashboard.
* README.

### Módulos

* Time Series Preparation.
* Naive Forecast.
* Moving Average Forecast.
* Forecast Dashboard.

### Labs

* `ml-naive-forecast-lab`
* `ml-moving-average-lab`
* `ml-forecast-error-lab`

---

## 03 — cloud-ml-pipeline-notes-dashboard

### Objetivo

Crear una herramienta ligera para documentar y visualizar un flujo ML cloud.

### Aprendizajes principales

* Cloud architecture.
* BigQuery conceptual.
* Cloud Storage conceptual.
* MLflow conceptual.
* Cloud Run conceptual.
* AWS equivalents.
* Azure equivalents.
* Documentación técnica.
* Diagramas simples.

### Módulos

* Cloud Architecture Notes.
* GCP / AWS / Azure Map.
* MLflow Artifact Notes.
* Visual Architecture Dashboard.

### Labs

* `docs-cloud-architecture-notes-lab`
* `docs-gcp-aws-azure-map-lab`
* `docs-mlflow-artifact-notes-lab`

---

## 04 — model-quality-report-generator

### Objetivo

Crear una herramienta que genere reportes simples de calidad de modelos ML.

### Aprendizajes principales

* Métricas.
* Model performance.
* Monitoring conceptual.
* Error analysis.
* Reportes técnicos.
* Markdown reports.
* Visualización.
* README.

### Módulos

* Metrics Input.
* Model Quality Summary.
* Error Summary.
* Report Generator.

### Labs

* `ml-model-metrics-report-lab`
* `ml-error-summary-lab`
* `docs-model-report-template-lab`

---

## 05 — personal-document-search-rag-lite

### Objetivo

Crear un buscador semántico pequeño para documentos personales o notas técnicas.

### Aprendizajes principales

* Embeddings.
* Chunks.
* Vector search.
* RAG ligero.
* Fuentes.
* UI de búsqueda.
* Evaluación básica.
* README.

### Módulos

* Document Ingestion.
* Chunking.
* Semantic Search.
* Source Display.

### Labs

* `rag-chunking-basic-lab`
* `rag-semantic-search-lab`
* `rag-source-display-lab`

---

## 06 — ai-response-cost-latency-notebook

### Objetivo

Crear un notebook o mini dashboard para medir costo y latencia de respuestas IA.

### Aprendizajes principales

* Latencia.
* Costo estimado.
* Tokens.
* Tiempo de respuesta.
* Comparación de prompts.
* Registro de resultados.
* Optimización ligera.
* README.

### Módulos

* Prompt Set.
* Latency Logging.
* Cost Table.
* Recommendation Notes.

### Labs

* `tec-latency-table-lab`
* `tec-prompt-comparison-lab`
* `tec-cost-estimation-lite-lab`

---

## 07 — ai-portfolio-platform-lite

### Objetivo

Crear un portal ligero que agrupe proyectos, aprendizajes, demos y evidencias del Plan 1.

### Aprendizajes principales

* Frontend ligero.
* Portafolio técnico.
* Project gallery.
* Storytelling técnico.
* Dashboard simple.
* Documentación.
* Capturas.
* Demo links.

### Módulos

* Portal Structure.
* Project Gallery.
* Learning Notes.
* Demo Links.

### Labs

* `portal-project-gallery-lab`
* `portal-learning-notes-lab`
* `portal-demo-links-lab`

---

# 🧱 Ciclo general de cada proyecto

Cada proyecto del Plan 1 sigue este ciclo:

```txt
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
18. Conectar con el proyecto grande correspondiente.
```

---

# 🗂️ Estructura recomendada del repositorio

```txt
Applied-AI/
├── 01-product-demand-insight-lite/
│   ├── labs/
│   ├── data/
│   ├── notebooks/
│   ├── src/
│   └── README.md
│
├── 02-mini-sales-forecast-dashboard/
│   ├── labs/
│   ├── data/
│   ├── notebooks/
│   ├── dashboard/
│   └── README.md
│
├── 03-cloud-ml-pipeline-notes-dashboard/
│   ├── labs/
│   ├── docs/
│   ├── diagrams/
│   └── README.md
│
├── 04-model-quality-report-generator/
│   ├── labs/
│   ├── src/
│   ├── reports/
│   └── README.md
│
├── 05-personal-document-search-rag-lite/
│   ├── labs/
│   ├── documents/
│   ├── src/
│   └── README.md
│
├── 06-ai-response-cost-latency-notebook/
│   ├── labs/
│   ├── notebooks/
│   ├── reports/
│   └── README.md
│
├── 07-ai-portfolio-platform-lite/
│   ├── labs/
│   ├── frontend/
│   ├── docs/
│   └── README.md
│
└── README.md
```

---

# 📊 Nivel esperado al terminar Plan 1

| Área                                      | Nivel esperado |
| ----------------------------------------- | -------------: |
| EDA aplicada                              |           8/10 |
| Pandas práctico                           |           8/10 |
| Visualización                             |           8/10 |
| Dashboards ligeros                        |         8.5/10 |
| Forecasting básico                        |         7.5/10 |
| Segmentación o análisis de comportamiento |         7.5/10 |
| Métricas de modelos                       |           8/10 |
| Reportes ML                               |         8.5/10 |
| Interpretación de resultados              |           8/10 |
| Storytelling técnico                      |         8.5/10 |
| Documentación de proyectos pequeños       |         8.5/10 |
| Evidencia visual de aprendizaje           |         8.5/10 |

---

# 🧠 Resultado esperado del Plan 1

Al completar este plan, podré decir:

```txt
Sé construir microproductos de IA aplicada.
Sé convertir datos en insights.
Sé cargar, limpiar y analizar datasets pequeños.
Sé crear dashboards ligeros.
Sé hacer forecasting básico.
Sé crear reportes de modelos.
Sé crear buscadores semánticos pequeños.
Sé medir costos y latencia de respuestas IA.
Sé crear portales técnicos ligeros.
Sé convertir aprendizaje técnico en evidencia visible.
```

---

# 🧭 Regla final de avance

```txt
Exploro antes de ejecutar.
Ejecuto con mapa.
Cierro cada lab.
Documento cada avance.
Comparo antes de mejorar.
No construyo por copiar.
Construyo para entender.
```

Frase guía:

```txt
Aprendo profundo en Path-AI-Engineer.
Construyo visible en Building-Projects.
Uno me forma.
El otro me muestra.
```
