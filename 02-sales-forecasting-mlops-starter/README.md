# 02-sales-forecasting-mlops-starter

## 🧠 Descripción

Sistema inicial de forecasting de ventas con dashboard, Docker y CI/CD.

Este proyecto continúa la base del Proyecto 01, pero se enfoca en series temporales y predicción de ventas futuras.

---

## 🎯 Objetivo

Crear un sistema de forecasting de ventas que compare métodos simples, entrene un modelo y lo presente en un dashboard reproducible.

---

## 👤 Usuario objetivo

* Analista de ventas.
* Equipo comercial.
* Operaciones retail.
* Reclutador técnico interesado en forecasting y MLOps básico.

---

## 🧱 Arquitectura esperada

```txt
Dataset temporal
      ↓
Time Series Features
      ↓
Baseline naive / moving average
      ↓
Modelo forecasting
      ↓
Dashboard
      ↓
Docker
      ↓
CI/CD
      ↓
Render
```

---

## 🧩 Módulos

### Módulo 1 — Forecasting Baselines

Comparar naive forecast vs moving average.

### Módulo 2 — Time Features

Crear lags, rolling mean y estacionalidad.

### Módulo 3 — Model Comparison

Comparar baseline contra modelo ML.

### Módulo 4 — Docker + CI/CD

Convertir el proyecto en contenedor y automatizar tests.

---

## 🧪 Labs

* `tec-forecasting-baseline-lab`
* `tec-time-series-features-lab`
* `tec-docker-ci-lab`
* `cloud-render-to-gcp-cloud-run-concept-lab`
* `cloud-docker-api-to-aws-app-runner-lab`
* `cloud-docker-api-to-azure-container-apps-lab`

---

## 📊 Métricas

* MAE.
* RMSE.
* MAPE.

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

* Preparar dataset temporal.
* Crear baseline naive.
* Crear media móvil.
* Crear lags.
* Crear rolling windows.
* Entrenar modelo de forecasting.
* Hacer backtesting.
* Comparar modelos.
* Dockerizar.
* Crear GitHub Actions.
* Desplegar demo.
* Grabar demo.
* Actualizar LinkedIn y CV.
