# 02-classical-model-comparison-visual-report

## 🧠 Descripción

Reporte visual de comparación de modelos clásicos de Machine Learning.

Este proyecto pertenece a la ruta:

```txt
Building Projects
```

y acompaña directamente al proyecto:

```txt
AI Engineer Proyecto 03 — classical-model-comparison-suite
```

La idea central es convertir la comparación técnica de modelos en una herramienta visual, clara y entendible.

Mientras el proyecto de AI Engineer profundiza en entrenamiento, evaluación, estructura, métricas, tests y decisión técnica, este Building Project se enfoca en mostrar los resultados de forma visible:

```txt
baseline
→ modelos clásicos
→ métricas
→ comparación
→ análisis de error
→ tarjetas de decisión
→ reporte visual
```

Este proyecto no busca construir un sistema pesado ni una API grande.

Busca crear evidencia clara de que puedo comparar modelos, interpretar métricas y explicar una decisión técnica.

---

## 🎯 Objetivo

Crear un reporte visual que compare modelos clásicos usando métricas, tablas, gráficos, notas de error y tarjetas de decisión.

El objetivo es responder:

```txt
¿Qué modelo funcionó mejor?
¿Qué modelo fue más simple?
¿Qué modelo fue más riesgoso?
¿Qué modelo elegiría para esta versión?
¿Qué limitaciones tiene la comparación?
```

---

## 👤 Usuario objetivo

* AI Engineer en formación.
* Analista de datos.
* Reclutador técnico.
* Persona que quiere entender model comparison sin leer todo el código.
* Usuario que necesita una recomendación clara de modelo.
* Yo mismo como constructor de portafolio aplicado.

---

## 🧱 Arquitectura esperada

```txt
Dataset pequeño
      ↓
Preparación de datos
      ↓
Baseline
      ↓
Modelo clásico 1
      ↓
Modelo clásico 2
      ↓
Modelo clásico 3
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

```txt
data
→ load / prepare
→ train test split
→ baseline
→ train classical models
→ calculate metrics
→ compare results
→ analyze errors
→ generate decision cards
→ export visual report
```

---

## 🧩 Módulos

### Módulo 1 — Dataset Setup

Preparar un dataset pequeño para comparación.

Incluye:

* Cargar datos.
* Revisar columnas.
* Separar features y target.
* Crear train/test split.
* Documentar limitaciones del dataset.

---

### Módulo 2 — Baseline Summary

Crear una referencia mínima antes de comparar modelos.

Incluye:

* Baseline simple.
* Métrica base.
* Interpretación.
* Explicación de por qué el baseline importa.

---

### Módulo 3 — Classical Models

Entrenar o registrar modelos clásicos.

Puede incluir:

* Linear Regression.
* Decision Tree.
* Random Forest.
* Logistic Regression.
* SVM si aplica.

La selección depende del tipo de problema:

```txt
regresión
o
clasificación
```

---

### Módulo 4 — Metrics Table

Crear tabla comparativa de resultados.

Para regresión puede incluir:

* MAE.
* RMSE.
* R².
* Error promedio.
* Error máximo.

Para clasificación puede incluir:

* Accuracy.
* Precision.
* Recall.
* F1-score.
* Confusion matrix.

---

### Módulo 5 — Error Notes

Documentar dónde fallan los modelos.

Incluye:

* Casos con mayor error.
* Casos donde el modelo mejora.
* Casos donde el modelo empeora.
* Riesgo de overfitting.
* Limitaciones por dataset pequeño.
* Advertencias técnicas.

---

### Módulo 6 — Decision Cards

Crear tarjetas de decisión.

Cada tarjeta debe convertir resultados técnicos en una conclusión clara.

Ejemplos:

```txt
Modelo con mejor métrica
Modelo más simple
Modelo más interpretable
Modelo con mayor riesgo
Modelo recomendado
```

Cada tarjeta debe tener:

* título;
* modelo;
* métrica principal;
* explicación;
* recomendación;
* limitación.

---

### Módulo 7 — Visual Report

Crear el reporte final.

Puede ser:

* Markdown report;
* dashboard ligero;
* notebook visual;
* HTML simple;
* carpeta `reports/`;
* `dashboard/README.md`.

Debe mostrar:

* tabla de métricas;
* gráficos;
* decision cards;
* error notes;
* conclusión técnica;
* siguiente paso.

---

## 🧪 Labs

### tec-labs

#### `tec-baseline-vs-model-lab`

Comparar baseline contra un modelo clásico.

Debe responder:

```txt
¿El modelo realmente supera la referencia mínima?
```

---

#### `tec-metrics-comparison-lab`

Comparar métricas entre varios modelos.

Debe responder:

```txt
¿Qué métrica estoy usando y qué significa?
```

---

#### `tec-error-analysis-card-lab`

Convertir errores en notas entendibles.

Debe responder:

```txt
¿Dónde falla el modelo y qué puedo aprender de esos fallos?
```

---

#### `tec-model-decision-card-lab`

Crear tarjetas de decisión técnica.

Debe responder:

```txt
¿Qué modelo elegiría y por qué?
```

---

### docs-labs

#### `docs-model-comparison-report-template-lab`

Crear plantilla de reporte reutilizable para model comparison.

---

#### `docs-technical-storytelling-lab`

Practicar cómo explicar resultados técnicos en lenguaje claro.

---

### cloud-labs

#### `cloud-model-report-to-gcp-storage-lab`

Traducir conceptualmente el reporte hacia GCP Cloud Storage.

---

#### `cloud-model-report-to-aws-s3-lab`

Traducir conceptualmente el reporte hacia AWS S3.

---

#### `cloud-model-report-to-azure-blob-lab`

Traducir conceptualmente el reporte hacia Azure Blob Storage.

---

## 📊 Métricas / Evidencia

Según el tipo de problema, el proyecto puede generar:

### Regresión

* MAE.
* RMSE.
* R².
* Error promedio.
* Error máximo.
* Tabla real vs predicho.
* Gráfico de errores.

### Clasificación

* Accuracy.
* Precision.
* Recall.
* F1-score.
* Confusion matrix.
* Tabla de predicciones.
* Gráfico de resultados.

### Evidencia visual

* Tabla comparativa.
* Decision cards.
* Error notes.
* Reporte Markdown.
* Dashboard ligero.
* Capturas.
* README profesional.

---

## 🚀 Estado actual

Pendiente / por iniciar.

---

## 🧭 Ciclo de trabajo

```txt
Semana 1 → Problema, dataset, baseline y primera métrica
Semana 2 → Modelos clásicos y tabla comparativa
Semana 3 → Error analysis, decision cards y visual report
Semana 4 → Labs, README, capturas y cierre del proyecto
```

---

## 📌 Próximos pasos

* Elegir dataset pequeño.
* Definir si el problema será regresión o clasificación.
* Preparar datos.
* Crear baseline.
* Calcular métrica base.
* Entrenar modelos clásicos.
* Comparar métricas.
* Crear tabla visual.
* Analizar errores.
* Crear decision cards.
* Crear visual report.
* Documentar labs.
* Preparar capturas.
* Publicar repo.

---

## ✅ Entregable final

Al terminar este proyecto debe existir:

* Dataset pequeño preparado.
* Baseline documentado.
* Modelos clásicos comparados.
* Tabla de métricas.
* Error notes.
* Decision cards.
* Visual report.
* README profesional.
* Labs documentados.
* Capturas o outputs visibles.
* Conexión clara con `classical-model-comparison-suite`.

---

## 🧭 Regla final

```txt
Comparar modelos no es mirar quién gana una métrica.
Es entender rendimiento, simplicidad, riesgo, limitaciones y decisión técnica.

Un reporte claro vale más que una tabla sin explicación.
```

Este proyecto debe demostrar que puedo convertir model comparison en evidencia visual, no solo en código ejecutado.
