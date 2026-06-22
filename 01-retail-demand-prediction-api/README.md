# 01-retail-demand-prediction-api

## 🧠 Descripción

API de predicción de demanda retail construida como primer proyecto del Plan 1 — AI / Machine Learning Engineering.

El proyecto busca predecir cuántas unidades de un producto podrían venderse usando datos como producto, tienda, promoción, stock, precio y variables temporales.

---

## 🎯 Objetivo

Construir una aplicación completa de predicción de demanda:

```txt
SQL local → features → baseline → modelo → FastAPI → frontend simple → tests → Render
```

---

## 👤 Usuario objetivo

* Analista retail.
* Pequeña tienda.
* Equipo de operaciones.
* Reclutador técnico que quiere ver un sistema ML completo.

---

## 🧱 Arquitectura esperada

```txt
CSV / SQL local
      ↓
Pandas / Feature Engineering
      ↓
Modelo ML clásico
      ↓
Modelo guardado
      ↓
FastAPI
      ↓
Frontend simple
      ↓
Render
```

---

## 🧩 Módulos

### Módulo 1 — Feature Engineering

Crear variables como día de semana, promoción, stock, precio y promedio de ventas.

### Módulo 2 — Model Comparison

Comparar baseline, Linear Regression, Random Forest y Gradient Boosting.

### Módulo 3 — Interpretability ligera

Explicar variables importantes del modelo.

### Módulo 4 — Error Analysis básico

Ver dónde falla más el modelo: producto, tienda, día o promoción.

---

## 🧪 Labs

### tec-feature-engineering-lab

CSV manual → DataFrame → features → X/y → baseline → MAE.

### tec-model-comparison-lab

Comparación baseline vs modelos clásicos.

### tec-interpretability-lab

Explicación simple de variables importantes.

### cloud-local-sql-to-gcp-bigquery-lab

Traducción conceptual de SQL local hacia BigQuery.

### cloud-model-artifact-to-aws-s3-lab

Guardar artefactos de modelo en AWS S3.

### cloud-model-artifact-to-azure-blob-lab

Guardar artefactos de modelo en Azure Blob Storage.

---

## 📊 Métricas

Métrica principal inicial:

```txt
MAE — Mean Absolute Error
```

Baseline inicial:

```txt
Baseline prediction: 22.8
Baseline MAE: 5.63
```

---

## 🚀 Estado actual

* FastAPI base creada.
* Rutas con APIRouter.
* Schemas con Pydantic.
* Endpoint `/api/v1/predict`.
* Mock dinámico.
* Servicio separado.
* Lab de Feature Engineering iniciado.
* Baseline y MAE calculados.

---

## 🧭 Ciclo de trabajo

```txt
Día 1 → Exploración
Día 2 → Ejecución
Día 3 → Ejecución
Día 4 → Ejecución
```

---

## 📌 Próximos pasos

* Cerrar README del lab.
* Crear `tec-model-comparison-lab`.
* Entrenar Linear Regression.
* Comparar contra baseline.
* Entrenar Random Forest.
* Elegir modelo inicial.
* Guardar modelo.
* Conectar FastAPI con modelo real.
* Crear frontend simple.
* Agregar tests mínimos.
* Desplegar en Render.
* Grabar demo.
* Actualizar LinkedIn y CV.

