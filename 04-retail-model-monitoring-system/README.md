# 04-retail-model-monitoring-system

## 🧠 Descripción

Sistema de monitoreo MLOps para modelos retail.

Este proyecto se enfoca en observar modelos después del entrenamiento: logs, drift, rendimiento, cambios en datos y preparación de retraining.

---

## 🎯 Objetivo

Crear un sistema que permita monitorear predicciones, detectar cambios en datos/modelo y preparar un flujo básico de retraining.

---

## 👤 Usuario objetivo

* ML Engineer.
* Data Scientist.
* Equipo MLOps.
* Empresa que tiene modelos en producción.
* Reclutador técnico interesado en monitoreo de modelos.

---

## 🧱 Arquitectura esperada

```txt
Prediction API
      ↓
Prediction Logs
      ↓
Metrics Store
      ↓
Data Drift Detection
      ↓
Model Drift Analysis
      ↓
Monitoring Dashboard
      ↓
Retraining Script
```

---

## 🧩 Módulos

### Módulo 1 — Prediction Logging

Guardar inputs, outputs, latencia y versión del modelo.

### Módulo 2 — Data Drift

Comparar distribuciones entre datos de entrenamiento y datos nuevos.

### Módulo 3 — Model Drift

Comparar rendimiento actual vs rendimiento anterior.

### Módulo 4 — Retraining

Crear un flujo básico de reentrenamiento.

### Módulo 5 — ML System Design

Diseñar cómo vive el modelo en producción.

---

## 🧪 Labs

* `tec-data-drift-detector-lab`
* `tec-retraining-pipeline-lab`
* `tec-model-performance-monitoring-lab`
* `cloud-vertex-ai-to-aws-sagemaker-lab`
* `cloud-cloud-logging-to-aws-cloudwatch-lab`
* `cloud-secret-manager-to-azure-key-vault-lab`

---

## 📊 Métricas / Evidencia

* Logs de predicciones.
* Métricas de rendimiento.
* Drift report.
* Script de retraining.
* Dashboard MLOps.
* Documento ML System Design.

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

* Diseñar esquema de logging.
* Guardar predicciones.
* Medir métricas.
* Comparar datos de entrenamiento vs datos nuevos.
* Simular data drift.
* Simular model drift.
* Crear dashboard.
* Crear retraining script.
* Documentar ML System Design.
* Grabar demo.
* Actualizar LinkedIn y CV.

