# 06-ai-cost-latency-optimizer

## 🧠 Descripción

Herramienta para medir costos y latencia de servicios de IA.

Este proyecto ayuda a pensar como AI Engineer en producción: no solo importa que un modelo responda, también importa cuánto tarda, cuánto cuesta y qué estrategia conviene.

---

## 🎯 Objetivo

Medir tiempos de respuesta, percentiles de latencia, costos estimados, batch vs online y caching para generar recomendaciones técnicas.

---

## 👤 Usuario objetivo

* AI Engineer.
* Backend Engineer.
* Equipo de producto.
* Empresa que usa APIs de IA.
* Reclutador técnico interesado en optimización de sistemas IA.

---

## 🧱 Arquitectura esperada

```txt
Test Requests
     ↓
Latency Logger
     ↓
Cost Estimator
     ↓
Batch vs Online Comparison
     ↓
Caching Strategy
     ↓
Benchmark Table
     ↓
Dashboard
     ↓
Recommendation Report
```

---

## 🧩 Módulos

### Módulo 1 — Latency Benchmarking

Medir tiempos de respuesta.

### Módulo 2 — Cost Estimation

Estimar costos por request.

### Módulo 3 — Batch vs Online

Comparar modos de inferencia.

### Módulo 4 — Caching

Reducir llamadas repetidas.

---

## 🧪 Labs

* `tec-latency-benchmark-lab`
* `tec-batch-vs-online-lab`
* `tec-caching-strategy-lab`
* `cloud-render-vs-cloud-run-cost-lab`
* `cloud-cloud-run-to-aws-app-runner-cost-lab`
* `cloud-vertex-ai-to-sagemaker-endpoint-cost-lab`

---

## 📊 Métricas

* Latencia promedio.
* p50.
* p95.
* p99.
* Costo estimado por request.
* Costo estimado por lote.
* Comparación batch vs online.
* Reducción por caching.

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

* Definir endpoints a medir.
* Medir latencia promedio.
* Medir p50, p95 y p99.
* Comparar batch vs online.
* Probar caching.
* Estimar costos.
* Crear dashboard.
* Generar recomendaciones.
* Grabar demo.
* Actualizar LinkedIn y CV.
