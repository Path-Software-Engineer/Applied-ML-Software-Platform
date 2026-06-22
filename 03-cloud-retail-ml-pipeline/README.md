# 03-cloud-retail-ml-pipeline

## 🧠 Descripción

Pipeline ML retail orientado a cloud, usando GCP como nube principal.

Este proyecto migra el flujo de Machine Learning desde un entorno local hacia una arquitectura cloud empresarial.

---

## 🎯 Objetivo

Construir un pipeline ML conectado con servicios cloud:

```txt
BigQuery → Python → MLflow → Cloud Storage → API → Cloud Run / Render
```

---

## 👤 Usuario objetivo

* Equipo de datos.
* ML Engineer.
* Cloud Engineer.
* Empresa retail que necesita pipeline reproducible.

---

## 🧱 Arquitectura esperada

```txt
BigQuery
   ↓
Feature Queries
   ↓
Python Training
   ↓
MLflow Tracking
   ↓
Cloud Storage Artifacts
   ↓
API
   ↓
Render / Cloud Run
```

---

## 🧩 Módulos

### Módulo 1 — BigQuery Data Modeling

Diseñar tablas y features en BigQuery.

### Módulo 2 — MLflow Tracking

Registrar parámetros, métricas y artefactos.

### Módulo 3 — Cloud Deployment

Comparar Render vs Cloud Run.

### Módulo 4 — Cloud Architecture Mapping

Traducir GCP hacia AWS y Azure.

---

## 🧪 Labs

* `tec-bigquery-feature-engineering-lab`
* `tec-mlflow-experiment-tracking-lab`
* `tec-cloud-api-error-handling-lab`
* `cloud-bigquery-to-aws-redshift-athena-lab`
* `cloud-cloud-storage-to-aws-s3-lab`
* `cloud-cloud-storage-to-azure-blob-lab`

---

## 📊 Métricas / Evidencia

* Dataset en BigQuery.
* Modelo entrenado con datos cloud.
* Experimentos registrados en MLflow.
* Artefactos guardados.
* API desplegada.
* Diagrama de arquitectura.
* Tabla multi-cloud.

---

## 🚀 Estado actual

Pendiente.

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

* Crear dataset cloud.
* Diseñar tablas.
* Consultar BigQuery desde Python.
* Entrenar modelo cloud.
* Registrar experimento con MLflow.
* Guardar artefactos.
* Preparar API desplegada.
* Documentar equivalencias AWS/Azure.
* Grabar demo.
* Actualizar LinkedIn y CV.

