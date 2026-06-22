# 01-product-demand-insight-lite

## 🧠 Descripción

Microproducto de IA aplicada para analizar ventas de productos y generar insights básicos de demanda.

Este proyecto pertenece al Plan 1 — IA Aplicada / Microproductos ML de Building Projects.

La idea no es construir una plataforma grande, sino una herramienta pequeña, visible y terminable que convierta datos simples de ventas en análisis, baseline, gráficos, tarjetas de insight y conclusiones claras.

---

## 🎯 Objetivo

Crear una herramienta ligera que analice ventas de productos y genere insights básicos de demanda:

```txt
CSV local → limpieza → features → baseline → métricas simples → análisis → insight cards → gráficos → dashboard ligero
```

---

## 👤 Usuario objetivo

* Dueño de una tienda pequeña.
* Analista de ventas.
* Equipo comercial.
* Persona que necesita entender qué productos se venden mejor.
* Reclutador técnico que quiere ver evidencia aplicada de análisis con datos.

---

## 🧱 Arquitectura esperada

```txt
CSV local
      ↓
Pandas / Limpieza básica
      ↓
Feature Engineering simple
      ↓
Baseline promedio
      ↓
Análisis de ventas
      ↓
Insight Cards
      ↓
Gráficos
      ↓
Dashboard ligero / README visual
```

---

## 🧩 Módulos

### Módulo 1 — Data Loading

Cargar dataset y revisar columnas.

### Módulo 2 — Basic Sales Analysis

Calcular ventas por producto, categoría y fecha.

### Módulo 3 — Simple Baseline

Crear una predicción simple para comparar.

### Módulo 4 — Insight Cards

Convertir resultados en frases claras.

### Módulo 5 — Visual Report

Crear gráficos simples y evidencia visual.

---

## 🧪 Labs

### tec-sales-eda-lab

Explorar columnas, productos, fechas, ventas y estructura inicial del dataset.

### tec-product-ranking-lab

Calcular ranking de productos por unidades vendidas y revenue.

### tec-basic-demand-insight-lab

Convertir análisis y baseline en insights de demanda entendibles.

### cloud-local-csv-to-gcp-cloud-storage-lab

Traducir conceptualmente el CSV local hacia GCP Cloud Storage.

### cloud-local-csv-to-aws-s3-lab

Traducir conceptualmente el CSV local hacia AWS S3.

### cloud-local-csv-to-azure-blob-lab

Traducir conceptualmente el CSV local hacia Azure Blob Storage.

---

## 📊 Métricas / Evidencia

* Total de unidades vendidas.
* Revenue total.
* Producto más vendido.
* Producto con mayor revenue.
* Mejor día de ventas.
* Baseline promedio.
* MAE del baseline.
* Insight cards.
* Gráficos exportados.
* Dashboard ligero o README visual.

---

## 🚀 Estado actual

Pendiente / por iniciar desde cero.

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

* Crear estructura base del proyecto.
* Crear dataset inicial en `data/raw`.
* Crear carga de datos con Pandas.
* Crear limpieza básica.
* Crear features simples.
* Calcular revenue.
* Crear baseline promedio.
* Calcular MAE.
* Analizar productos más vendidos.
* Crear insight cards.
* Crear gráficos.
* Documentar labs.
* Preparar README final.
* Agregar capturas o evidencia visual.
* Publicar repo.
