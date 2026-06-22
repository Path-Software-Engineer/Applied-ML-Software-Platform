# 02-mini-sales-forecast-dashboard

## 🧠 Descripción

Dashboard ligero de forecasting de ventas usando métodos simples.

Este proyecto continúa la línea aplicada de Building Projects, pero se enfoca en datos temporales y predicción básica de ventas futuras.

La idea no es construir un sistema MLOps pesado, sino una herramienta visual que compare métodos simples como naive forecast y moving average, mostrando resultados de forma clara.

---

## 🎯 Objetivo

Crear un dashboard pequeño que proyecte ventas futuras usando métodos simples:

```txt
Dataset temporal → preparación de serie → naive forecast → moving average → error básico → gráfico real vs predicho → dashboard
```

---

## 👤 Usuario objetivo

* Analista de ventas.
* Dueño de tienda pequeña.
* Equipo comercial.
* Persona que necesita estimar ventas futuras de forma simple.
* Reclutador técnico que quiere ver forecasting aplicado en un microproducto.

---

## 🧱 Arquitectura esperada

```txt
Dataset temporal
      ↓
Preparación por fecha
      ↓
Naive Forecast
      ↓
Moving Average Forecast
      ↓
Comparación de error
      ↓
Gráfico real vs predicho
      ↓
Dashboard ligero
```

---

## 🧩 Módulos

### Módulo 1 — Time Series Preparation

Ordenar y preparar datos temporales.

### Módulo 2 — Naive Forecast

Usar el último valor como predicción base.

### Módulo 3 — Moving Average Forecast

Crear predicción usando promedio móvil.

### Módulo 4 — Forecast Dashboard

Mostrar comparación visual entre valores reales y predichos.

---

## 🧪 Labs

### tec-naive-forecast-lab

Crear una predicción simple usando el último valor conocido.

### tec-moving-average-lab

Crear una predicción usando promedio móvil.

### tec-forecast-error-lab

Calcular error básico y comparar métodos.

### cloud-dashboard-to-gcp-cloud-run-concept-lab

Traducir conceptualmente el dashboard hacia GCP Cloud Run.

### cloud-dashboard-to-aws-app-runner-concept-lab

Traducir conceptualmente el dashboard hacia AWS App Runner.

### cloud-dashboard-to-azure-container-apps-concept-lab

Traducir conceptualmente el dashboard hacia Azure Container Apps.

---

## 📊 Métricas / Evidencia

* MAE.
* Comparación real vs predicción.
* Tabla de forecast.
* Gráfico de serie temporal.
* Gráfico real vs predicho.
* Conclusión de método.
* Dashboard ligero.
* Capturas.

---

## 🚀 Estado actual

Pendiente / por iniciar.

---

## 🧭 Ciclo de trabajo

```txt
Día 1 → Exploración
Día 2 → Ejecución 1
Día 3 → Ejecución 2
Día 4 → Ejecución 3
```

---

## 📌 Próximos pasos

* Elegir dataset temporal pequeño.
* Ordenar ventas por fecha.
* Crear baseline naive.
* Crear media móvil.
* Calcular error básico.
* Comparar métodos.
* Crear gráfico real vs predicho.
* Crear dashboard ligero.
* Documentar labs.
* Preparar capturas.
* Publicar repo.
