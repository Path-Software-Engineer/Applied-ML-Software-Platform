# 01-retail-intelligence-platform

## 🧠 Descripción

**Retail Intelligence Platform** es una aplicación de software aplicada a inteligencia artificial para analizar ventas, comparar modelos clásicos y apoyar decisiones simples de inventario.

Este proyecto pertenece a:

```txt
Path Software Engineer
Plan 1 — Applied ML Software Platform
```

y acompaña directamente al:

```txt
Path AI Engineer
Plan 1 — Machine Learning Engineering & Software Foundations
```

Este proyecto nace como evolución de los antiguos proyectos de Building Projects:

```txt
01-product-demand-insight-lite
02-classical-model-comparison-visual-report
03-inventory-decision-dashboard-lite
```

Ahora esos proyectos ya no vivirán como repositorios separados.

Se convierten en **3 sprints principales** dentro de una sola aplicación de software más robusta, documentada y orientada a producto.

---

# 🎯 Objetivo general

Construir una plataforma retail aplicada que permita:

```txt
analizar ventas
→ generar insights de demanda
→ comparar modelos clásicos
→ visualizar métricas
→ evaluar errores
→ analizar inventario
→ generar recomendaciones simples
→ mostrar resultados en dashboard
```

El objetivo no es construir un sistema empresarial gigante desde el inicio.

El objetivo es crear una aplicación sólida, clara y progresiva que conecte:

```txt
datos
→ análisis
→ modelos
→ decisiones
→ software
→ evidencia profesional
```

---

# 🧭 Relación con Path AI Engineer

Este proyecto acompaña los proyectos impares del Plan 1 de Path AI Engineer:

```txt
Path AI Engineer Proyecto 01
→ retail-demand-prediction-api

Path AI Engineer Proyecto 03
→ classical-model-comparison-suite

Path AI Engineer Proyecto 05
→ inventory-optimization-ml-service
```

Cada uno se convierte en un sprint dentro de esta plataforma.

```txt
Sprint 1 → Demand Insight Module
Sprint 2 → Model Comparison Module
Sprint 3 → Inventory Decision Module
```

---

# 🧩 Estructura por sprints

## Sprint 1 — Demand Insight Module

### Match

```txt
Path AI Engineer Proyecto 01 — retail-demand-prediction-api
```

### Base anterior

```txt
01-product-demand-insight-lite
```

### Objetivo

Crear el primer módulo de la plataforma para analizar ventas de productos y generar insights básicos de demanda.

Flujo:

```txt
CSV local
→ carga
→ limpieza
→ features
→ baseline
→ MAE
→ análisis de ventas
→ insight cards
→ gráficos
→ dashboard inicial
```

### Resultado esperado

Al finalizar este sprint, la plataforma debe permitir ver:

```txt
total de unidades vendidas
revenue total
producto más vendido
producto con mayor revenue
mejor día de ventas
baseline promedio
MAE del baseline
insight cards
gráficos básicos
```

---

## Sprint 2 — Model Comparison Module

### Match

```txt
Path AI Engineer Proyecto 03 — classical-model-comparison-suite
```

### Base anterior

```txt
02-classical-model-comparison-visual-report
```

### Objetivo

Agregar un módulo para comparar modelos clásicos de Machine Learning y convertir los resultados en una decisión visual entendible.

Flujo:

```txt
dataset preparado
→ train/test split
→ baseline
→ modelos clásicos
→ métricas
→ tabla comparativa
→ error notes
→ decision cards
→ visual report
```

### Resultado esperado

Al finalizar este sprint, la plataforma debe permitir ver:

```txt
baseline vs modelos
tabla de métricas
modelo con mejor resultado
modelo más simple
modelo más interpretable
modelo más riesgoso
notas de error
tarjetas de decisión
recomendación técnica
```

---

## Sprint 3 — Inventory Decision Module

### Match

```txt
Path AI Engineer Proyecto 05 — inventory-optimization-ml-service
```

### Base anterior

```txt
03-inventory-decision-dashboard-lite
```

### Objetivo

Agregar un módulo de decisiones simples de inventario usando demanda observada, stock actual, regla de reposición y tarjetas de riesgo.

Flujo:

```txt
ventas / inventario
→ demanda observada
→ stock actual
→ regla de reorder
→ risk score
→ recommendation cards
→ inventory dashboard
```

### Resultado esperado

Al finalizar este sprint, la plataforma debe permitir ver:

```txt
demanda por producto
stock actual
productos con stock bajo
productos en riesgo
reorder point simple
risk score
recommendation cards
dashboard de inventario
limitaciones de la recomendación
```

---

# 👤 Usuario objetivo

Esta plataforma está pensada para:

```txt
dueño de tienda pequeña
analista de ventas
analista de inventario
equipo comercial
equipo de operaciones
reclutador técnico
constructor de portafolio aplicado
```

El usuario debe poder abrir la aplicación o el README y entender:

```txt
qué productos se venden más
qué modelo funciona mejor
qué productos podrían necesitar reposición
qué decisiones se pueden tomar
qué limitaciones tiene el sistema
```

---

# 🏗️ Arquitectura general esperada

```txt
Retail Intelligence Platform
│
├── Frontend
│   └── Dashboard visual
│
├── Backend
│   └── API para resultados, insights, métricas y recomendaciones
│
├── AI Services
│   └── análisis, baseline, modelos, métricas e inferencia
│
├── Data Layer
│   └── datos raw y processed
│
├── Reports
│   └── gráficos, tablas, summaries y outputs
│
└── Docs
    └── user stories, technical stories, decisiones y arquitectura
```

---

# 🔁 Flujo general de la plataforma

```txt
data/raw
→ data loading
→ data cleaning
→ feature engineering
→ demand analysis
→ baseline
→ metrics
→ model comparison
→ inventory analysis
→ recommendation engine
→ API
→ frontend dashboard
→ reports
→ documentation
```

---

# 🧱 Módulos principales

## 1. Data Loading

Responsabilidad:

```txt
Cargar datasets desde data/raw y devolver estructuras limpias para el sistema.
```

Incluye:

```txt
lectura de CSV
validación de rutas
validación de columnas
primeras verificaciones
```

---

## 2. Data Cleaning

Responsabilidad:

```txt
Limpiar datos sin alterar el significado del dataset.
```

Incluye:

```txt
conversión de fechas
validación de nulos
validación de unidades vendidas
validación de precios
validación de stock
control de valores imposibles
```

---

## 3. Feature Engineering

Responsabilidad:

```txt
Crear columnas útiles para análisis, modelos y decisiones.
```

Incluye:

```txt
day_of_week
month
year
is_weekend
revenue
stock_gap
demand_level
risk_level
```

---

## 4. Demand Insight Engine

Responsabilidad:

```txt
Convertir datos de ventas en insights básicos de demanda.
```

Incluye:

```txt
producto más vendido
producto con mayor revenue
mejor día de ventas
unidades totales
revenue total
insight cards
```

---

## 5. Baseline and Metrics

Responsabilidad:

```txt
Crear referencias mínimas para comparar resultados.
```

Incluye:

```txt
baseline promedio
MAE
RMSE si aplica
interpretación de métricas
resumen técnico
```

---

## 6. Model Comparison Engine

Responsabilidad:

```txt
Comparar modelos clásicos y generar una decisión técnica.
```

Puede incluir:

```txt
Linear Regression
Decision Tree
Random Forest
Gradient Boosting
Logistic Regression si aplica
SVM si aplica
```

Genera:

```txt
tabla de métricas
error notes
decision cards
modelo recomendado
limitaciones
```

---

## 7. Inventory Decision Engine

Responsabilidad:

```txt
Analizar stock, demanda y riesgo para generar recomendaciones simples.
```

Incluye:

```txt
stock actual
demanda observada
reorder point
safety factor
risk score
recommendation cards
```

---

## 8. Visual Dashboard

Responsabilidad:

```txt
Mostrar resultados de forma clara para el usuario.
```

Debe incluir:

```txt
resumen de ventas
insights de demanda
comparación de modelos
dashboard de inventario
gráficos
tarjetas de decisión
recomendaciones
limitaciones
```

---

# 📁 Estructura recomendada del repositorio

```txt
01-retail-intelligence-platform/
│
├── README.md
├── project-structure.txt
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── frontend/
│   └── app/
│       ├── README.md
│       ├── package.json
│       └── src/
│
├── backend/
│   └── api/
│       ├── README.md
│       ├── requirements.txt
│       └── app/
│           ├── main.py
│           ├── api/
│           ├── schemas/
│           └── services/
│
├── ai-services/
│   └── retail-ml-service/
│       ├── README.md
│       ├── src/
│       │   ├── data/
│       │   ├── features/
│       │   ├── baselines/
│       │   ├── models/
│       │   ├── analysis/
│       │   ├── insights/
│       │   ├── inventory/
│       │   └── pipeline.py
│       └── checks/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
│
├── models/
│   ├── artifacts/
│   └── metadata/
│
├── reports/
│   ├── figures/
│   ├── summaries/
│   ├── metrics/
│   ├── insight_cards/
│   ├── decision_cards/
│   └── outputs/
│
├── docs/
│   ├── architecture.md
│   ├── decisions.md
│   ├── api-contract.md
│   ├── user-stories.md
│   ├── technical-stories.md
│   ├── sprint-01-demand-insight/
│   │   ├── README.md
│   │   ├── week-01/
│   │   │   ├── exploration.md
│   │   │   ├── plan.md
│   │   │   └── review.md
│   │   ├── week-02/
│   │   │   ├── exploration.md
│   │   │   ├── plan.md
│   │   │   └── review.md
│   │   └── week-03/
│   │       ├── exploration.md
│   │       ├── plan.md
│   │       └── review.md
│   ├── sprint-02-model-comparison.md
│   ├── sprint-03-inventory-decision.md
│   └── product-notes.md
│
├── labs/
│   ├── tec-labs/
│   ├── cloud-labs/
│   ├── product-labs/
│   └── docs-labs/
│
├── tests/
│   ├── frontend/
│   ├── backend/
│   └── ai-services/
│
├── scripts/
│   ├── run_frontend.ps1
│   ├── run_backend.ps1
│   ├── run_ai_service.ps1
│   ├── run_pipeline.ps1
│   └── generate_report.ps1
│
└── deployment/
    ├── docker/
    └── gcp/
```

Regla:

```txt
La estructura debe servir al proyecto.
No el proyecto a la estructura.
```

No todas las carpetas deben estar completas desde el día uno.

---

# 🧾 Sistema de documentación

Este proyecto se trabajará con documentación profesional basada en:

```txt
US — User Stories
TS — Technical Stories
AC — Acceptance Criteria
DoD — Definition of Done
Sprint Review
Sprint Retrospective
```

---

# 📌 User Stories

Formato:

```txt
US-001

Como [tipo de usuario],
quiero [funcionalidad],
para [beneficio].
```

Ejemplo:

```txt
US-001

Como analista retail,
quiero ver un resumen de demanda por producto,
para identificar qué productos tienen mayor movimiento de ventas.
```

---

# 🛠️ Technical Stories

Formato:

```txt
TS-001

Implementar [componente técnico]
para permitir [resultado técnico].
```

Ejemplo:

```txt
TS-001

Implementar un servicio de análisis de demanda
para calcular unidades totales, revenue total, producto líder y mejor día de ventas.
```

---

# ✅ Acceptance Criteria

Ejemplo:

```txt
Acceptance Criteria:

- El sistema carga datos desde data/raw.
- El sistema valida columnas mínimas.
- El sistema calcula unidades totales.
- El sistema calcula revenue total.
- El sistema genera al menos una insight card.
- El resultado puede mostrarse en el dashboard.
```

---

# 🏁 Definition of Done

Una tarea no termina solo cuando el código funciona.

Termina cuando deja evidencia.

```txt
Código implementado
Prueba mínima realizada
Historia documentada
Decisión registrada
Resultado visible
README actualizado si aplica
Sin archivos basura
Sin responsabilidades mezcladas
```

---

# 🧪 Labs del proyecto

## Sprint 1 — Demand Insight Labs

```txt
tec-sales-eda-lab
tec-product-ranking-lab
tec-basic-demand-insight-lab
cloud-local-csv-to-gcp-cloud-storage-lab
cloud-local-csv-to-aws-s3-lab
cloud-local-csv-to-azure-blob-lab
```

---

## Sprint 2 — Model Comparison Labs

```txt
tec-baseline-vs-model-lab
tec-metrics-comparison-lab
tec-error-analysis-card-lab
tec-model-decision-card-lab
docs-model-comparison-report-template-lab
docs-technical-storytelling-lab
cloud-model-report-to-gcp-storage-lab
cloud-model-report-to-aws-s3-lab
cloud-model-report-to-azure-blob-lab
```

---

## Sprint 3 — Inventory Decision Labs

```txt
tec-demand-vs-stock-lab
tec-reorder-point-lab
tec-stock-risk-card-lab
tec-inventory-recommendation-lab
product-inventory-user-card-lab
product-recommendation-language-lab
cloud-inventory-report-to-gcp-storage-lab
cloud-inventory-report-to-aws-s3-lab
cloud-inventory-report-to-azure-blob-lab
```

---

# 📊 Métricas y evidencia esperada

## Demand Insight

```txt
total de unidades vendidas
revenue total
producto más vendido
producto con mayor revenue
mejor día de ventas
baseline promedio
MAE del baseline
insight cards
gráficos exportados
```

## Model Comparison

```txt
baseline vs modelos
MAE / RMSE / R² si es regresión
accuracy / precision / recall / F1 si es clasificación
tabla comparativa
error notes
decision cards
modelo recomendado
```

## Inventory Decision

```txt
stock actual
demanda observada
stock gap
reorder point
risk score
productos en riesgo
recommendation cards
dashboard de inventario
```

---

# 🖥️ Dashboard esperado

La plataforma debe incluir una vista visual con secciones como:

```txt
Overview
Demand Insights
Model Comparison
Inventory Decisions
Reports
Limitations
```

Cada sección debe mostrar resultados claros sin obligar al usuario a leer el código.

---

# 🚀 Deploy esperado

El proyecto puede comenzar local.

Más adelante podrá desplegarse con:

```txt
Frontend → Firebase Hosting / Cloud Storage / Vercel
Backend → Cloud Run
AI Service → Cloud Run
Reports → Cloud Storage
Artifacts → Cloud Storage
```

La regla es:

```txt
Primero local funcionando.
Luego Docker.
Luego deploy simple.
Después CI/CD.
```

---

# 🧭 Ciclo de avance

```txt
Sprint 1 → Demand Insight Module
Sprint 2 → Model Comparison Module
Sprint 3 → Inventory Decision Module
```

Cada sprint debe cerrar con:

```txt
módulo funcional
historias documentadas
resultados visibles
reports actualizados
README actualizado
sprint review
sprint retrospective
conexión con Path AI Engineer
```

---

# 📌 Próximos pasos

## Estado actual

Sprint 1 está oficialmente cerrado en el Día 28. Week 3 y Week 4 se encuentran
cerradas. El módulo
ya cuenta con un Demand Summary service, un endpoint FastAPI versionado y un
dashboard React que consume el contrato real. Las cinco Insight Cards y las tres
figuras validadas están integradas; el hardening, tests, documentación y release
quedaron preparados para `v0.1.0-sprint-01-demand-insight`.

## Sprint 1

```txt
[completed] Definir problema y usuario
[completed] Crear estructura base
[completed] Crear dataset inicial
[completed] Crear data loading
[completed] Crear data cleaning
[completed] Crear features
[completed] Calcular revenue
[completed] Crear baseline
[completed] Calcular MAE
[completed] Crear análisis de ventas
[completed] Crear Insight Cards
[completed] Crear gráficos
[completed] Crear API interna y dashboard inicial
[completed] Documentar labs y evolución semanal
[completed] Mantener README y trazabilidad
[completed] Cerrar Sprint 1 y preparar v0.1.0
```

Release notes:
[`v0.1.0-sprint-01-demand-insight`](docs/releases/v0.1.0-sprint-01-demand-insight.md).

Sprint 2 has advanced through global Day 77. The common experiment compares a
training-mean baseline, Linear Regression, Random Forest and Gradient Boosting
on one frozen chronological split. Gradient Boosting is the observed metric
leader; Random Forest is selected only for the next integration step under the
documented practical-equivalence rule. All evidence remains
`not_production_ready`, and no Sprint 1 public contract has changed.

## Sprint 2

```txt
[completed] Definir dataset y split para comparación
[completed] Crear baseline de comparación
[completed] Entrenar tres modelos clásicos
[completed] Calcular métricas comunes
[completed] Crear tabla comparativa
[completed] Crear análisis de errores
[completed] Aplicar criterio de selección reproducible
[completed] Crear cuatro Model Cards
[completed] Documentar labs asignados hasta el Día 69
[completed] Crear Decision Cards y comparison report
[completed] Cerrar Week 6 con revisión y gate completo
[completed] Definir el contrato y plan de integración de Week 7
[completed] Implementar el servicio interno de lectura del Día 72
[completed] Implementar el endpoint y OpenAPI del Día 73
[completed] Implementar la vista comparativa del Día 74
[completed] Presentar Decision Cards desde el API en el Día 75
[completed] Validar integración cross-layer y smoke en el Día 76
[completed] Cerrar Week 7 en el Día 77
[pending] Ejecutar hardening y cierre de Week 8
```

Current evidence:

- [`docs/sprints/sprint-02-model-comparison/README.md`](docs/sprints/sprint-02-model-comparison/README.md);
- [`docs/model-comparison-experiment-contract.md`](docs/model-comparison-experiment-contract.md);
- [`reports/outputs/model-comparison/comparison_table.md`](reports/outputs/model-comparison/comparison_table.md);
- [`reports/outputs/model-comparison/error_analysis.md`](reports/outputs/model-comparison/error_analysis.md);
- [`reports/outputs/model-comparison/model_decision.md`](reports/outputs/model-comparison/model_decision.md);
- [`reports/model-cards/model-comparison/README.md`](reports/model-cards/model-comparison/README.md);
- [`reports/outputs/model-comparison/model_comparison_report.md`](reports/outputs/model-comparison/model_comparison_report.md);
- [`docs/sprints/sprint-02-model-comparison/week-06/review.md`](docs/sprints/sprint-02-model-comparison/week-06/review.md);
- [`docs/model-comparison-read-contract.md`](docs/model-comparison-read-contract.md);
- global Days 57–77 / Sprint 2 Days 1–21 completed.

Install the pinned Model Comparison runtime before running its checks:

```powershell
.\.venv\Scripts\python.exe -m pip install -r ai-services\model-comparison\requirements.txt
```

## Sprint 3

```txt
Agregar datos de inventario
Calcular stock summary
Calcular demand summary
Crear reorder rule
Crear risk score
Crear recommendation cards
Crear inventory dashboard
Documentar limitaciones
Actualizar README final
Preparar capturas
Cerrar proyecto
```

---

# ✅ Entregable final

Al terminar este proyecto debe existir:

```txt
Aplicación retail aplicada
Dashboard funcional
Backend/API si aplica
Servicio de análisis/ML
Dataset de ejemplo
Pipeline reproducible
Demand insight module
Model comparison module
Inventory decision module
User stories
Technical stories
Acceptance criteria
Sprint docs
Reports
Gráficos
Insight cards
Decision cards
Recommendation cards
Labs documentados
README profesional
Evidencia visual
Deploy o guía de deploy
```

---

# 🧠 Resultado esperado

Al terminar este proyecto podré decir:

```txt
Construí una aplicación de software aplicada a IA.

No solo analicé datos.
No solo comparé modelos.
No solo hice un dashboard.

Integré ventas, demanda, modelos clásicos, métricas, inventario, recomendaciones, frontend, backend, documentación, sprints e historias en una sola plataforma.
```

---

# 🧭 Regla final

```txt
Este proyecto no será software vacío.

Será software aplicado a inteligencia artificial.

No construiré módulos sueltos por copiar.

Construiré una plataforma donde cada sprint agrega una capacidad real.

Path AI Engineer me da la profundidad.
Path Software Engineer convierte esa profundidad en producto.
```

---

# 👤 Autor

## Validation architecture

Demand Insight uses three distinct verification surfaces:

- `src/` owns production logic and official artifact generation.
- `tests/` contains isolated pytest tests and writes only to temporary paths.
- `checks/` contains readable manual end-to-end verification.
- `reports/` stores evidence generated by production flows, never by tests.
- `scripts/generate-report.ps1` provides a repeatable operational entry point.

Run automated verification with:

```powershell
python -m pytest -q
```

Run every manual check with:

```powershell
Get-ChildItem ai-services/demand-insight/checks/check_*.py |
    ForEach-Object { python $_.FullName }
```

# 👤 Autor

**Jean Franck Loa Rojas**

Path Software Engineer Builder
Applied AI Software Systems • Full-Stack Development • Machine Learning • Dashboards • APIs • Product Architecture • Cloud • Technical Documentation
