# 03-inventory-decision-dashboard-lite

## 🧠 Descripción

Dashboard ligero de decisiones de inventario usando demanda observada, stock, reglas simples de reposición y tarjetas de riesgo.

Este proyecto pertenece a la ruta:

```txt id="bp03-route"
Building Projects
```

y acompaña directamente al proyecto:

```txt id="bp03-match"
AI Engineer Proyecto 05 — inventory-optimization-ml-service
```

La idea central es convertir conceptos de demanda, inventario y optimización básica en una herramienta visual, pequeña y terminable.

Mientras el proyecto de AI Engineer construye un servicio ML más completo para optimización de inventario, este Building Project se enfoca en mostrar decisiones prácticas de forma clara:

```txt id="bp03-core"
ventas
→ demanda observada
→ stock actual
→ regla de reorder
→ riesgo de falta
→ recomendación visual
→ dashboard ligero
```

Este proyecto no busca crear un sistema avanzado de optimización.

Busca demostrar que puedo traducir datos de ventas e inventario en recomendaciones simples, visuales y explicables.

---

## 🎯 Objetivo

Crear un dashboard ligero que ayude a responder:

```txt id="bp03-questions"
¿Qué productos parecen tener más demanda?
¿Qué productos tienen stock bajo?
¿Qué productos podrían necesitar reposición?
¿Qué riesgo tiene cada producto?
Qué recomendación simple puedo mostrar?
Qué limitaciones tiene esa recomendación?
```

El flujo principal será:

```txt id="bp03-flow-main"
Dataset de ventas / inventario
→ preparación de datos
→ resumen de demanda
→ resumen de stock
→ regla de reorder
→ risk score simple
→ recommendation cards
→ gráficos
→ dashboard ligero
```

---

## 👤 Usuario objetivo

* Dueño de tienda pequeña.
* Analista de inventario.
* Equipo de operaciones.
* Persona que necesita priorizar reposición.
* Reclutador técnico que quiere ver un microproducto aplicado.
* Yo mismo como constructor de evidencia visible.

---

## 🧱 Arquitectura esperada

```txt id="bp03-architecture"
Dataset de ventas / inventario
      ↓
Carga de datos
      ↓
Limpieza
      ↓
Demand Summary
      ↓
Stock Summary
      ↓
Reorder Rule
      ↓
Risk Scoring
      ↓
Recommendation Cards
      ↓
Visual Dashboard
      ↓
README / Capturas
```

---

## 🔁 Flujo técnico

```txt id="bp03-flow"
data/raw
→ load_data
→ clean_data
→ demand_summary
→ stock_summary
→ reorder_rule
→ risk_cards
→ recommendation_cards
→ charts
→ dashboard
→ README
```

---

## 🧩 Módulos

### Módulo 1 — Inventory Dataset Setup

Preparar un dataset pequeño de ventas e inventario.

Incluye:

* Producto.
* Categoría.
* Fecha.
* Unidades vendidas.
* Precio.
* Stock actual.
* Stock mínimo opcional.
* Lead time conceptual si aplica.

Pregunta central:

```txt id="bp03-q1"
¿Qué datos mínimos necesito para tomar decisiones simples de inventario?
```

---

### Módulo 2 — Demand Summary

Calcular demanda observada.

Incluye:

* Unidades vendidas por producto.
* Promedio de unidades vendidas.
* Producto con mayor demanda.
* Demanda por categoría si aplica.
* Tendencia simple si hay fechas suficientes.

Pregunta central:

```txt id="bp03-q2"
¿Qué productos parecen moverse más según las ventas observadas?
```

---

### Módulo 3 — Stock Summary

Analizar el estado del stock.

Incluye:

* Stock actual por producto.
* Productos con stock bajo.
* Productos con stock suficiente.
* Productos con stock crítico.
* Comparación demanda vs stock.

Pregunta central:

```txt id="bp03-q3"
¿Qué productos podrían quedarse sin inventario pronto?
```

---

### Módulo 4 — Reorder Rule

Crear una regla simple de reposición.

Ejemplo:

```txt id="bp03-reorder-rule"
Si stock actual < demanda promedio × factor de seguridad
→ sugerir reposición
```

Incluye:

* Reorder point.
* Safety factor.
* Umbral.
* Recomendación.
* Explicación de la regla.

Pregunta central:

```txt id="bp03-q4"
¿Qué regla simple puedo usar para sugerir reposición sin venderla como verdad absoluta?
```

---

### Módulo 5 — Risk Score

Crear un score simple de riesgo.

Puede clasificar productos como:

```txt id="bp03-risk-levels"
riesgo bajo
riesgo medio
riesgo alto
```

Incluye:

* Stock actual.
* Demanda observada.
* Diferencia entre stock y demanda.
* Nivel de prioridad.
* Explicación breve.

Pregunta central:

```txt id="bp03-q5"
¿Qué producto necesita atención primero y por qué?
```

---

### Módulo 6 — Recommendation Cards

Convertir resultados técnicos en tarjetas claras.

Cada tarjeta debe incluir:

* producto;
* nivel de riesgo;
* stock actual;
* demanda observada;
* recomendación;
* explicación;
* limitación.

Ejemplo:

```txt id="bp03-card-example"
Producto: Café Premium
Riesgo: Alto
Motivo: El stock actual está por debajo de la demanda promedio estimada.
Recomendación: Revisar reposición esta semana.
Limitación: La regla no considera proveedores ni lead time real.
```

Pregunta central:

```txt id="bp03-q6"
¿Cómo convierto una regla técnica en una recomendación entendible?
```

---

### Módulo 7 — Visual Dashboard

Crear una vista ligera del producto.

Puede ser:

* `dashboard/README.md`;
* Streamlit simple;
* notebook visual;
* HTML ligero.

Debe mostrar:

* productos;
* stock;
* demanda;
* riesgo;
* recomendaciones;
* gráficos;
* limitaciones.

Pregunta central:

```txt id="bp03-q7"
¿Puede alguien entender el estado del inventario sin abrir el código?
```

---

## 🧪 Labs

### tec-labs

#### `tec-demand-vs-stock-lab`

Comparar demanda observada contra stock actual.

Debe responder:

```txt id="bp03-lab1"
¿Qué productos tienen demanda alta pero stock bajo?
```

---

#### `tec-reorder-point-lab`

Probar una regla simple de punto de reposición.

Debe responder:

```txt id="bp03-lab2"
¿Cómo cambia la recomendación si cambio el factor de seguridad?
```

---

#### `tec-stock-risk-card-lab`

Crear tarjetas de riesgo de inventario.

Debe responder:

```txt id="bp03-lab3"
¿Cómo explico el riesgo sin hacerlo sonar como una predicción perfecta?
```

---

#### `tec-inventory-recommendation-lab`

Comparar salida técnica cruda contra recomendación entendible.

Debe responder:

```txt id="bp03-lab4"
¿Qué diferencia hay entre mostrar números y recomendar una acción?
```

---

### product-labs

#### `product-inventory-user-card-lab`

Definir el usuario objetivo del dashboard.

---

#### `product-recommendation-language-lab`

Practicar lenguaje responsable para recomendaciones de inventario.

---

### cloud-labs

#### `cloud-inventory-report-to-gcp-storage-lab`

Traducir conceptualmente reportes de inventario hacia GCP Cloud Storage.

---

#### `cloud-inventory-report-to-aws-s3-lab`

Traducir conceptualmente reportes de inventario hacia AWS S3.

---

#### `cloud-inventory-report-to-azure-blob-lab`

Traducir conceptualmente reportes de inventario hacia Azure Blob Storage.

---

## 📊 Métricas / Evidencia

El proyecto puede generar:

* unidades vendidas por producto;
* demanda promedio por producto;
* stock actual;
* diferencia entre demanda y stock;
* reorder point;
* safety factor;
* nivel de riesgo;
* productos en riesgo alto;
* productos en riesgo medio;
* productos en riesgo bajo;
* número de recomendaciones generadas;
* gráficos de demanda vs stock;
* tarjetas de recomendación;
* dashboard ligero;
* capturas;
* README profesional.

---

## 🚀 Estado actual

Pendiente / por iniciar.

---

## 🧭 Ciclo de trabajo

```txt id="bp03-cycle"
Semana 1 → Problema, usuario, dataset e inventario base
Semana 2 → Demand summary, stock summary y comparación demanda vs stock
Semana 3 → Reorder rule, risk score y recommendation cards
Semana 4 → Dashboard, gráficos, labs técnicos y lenguaje de producto
Semana 5 → Cloud-labs, README final, capturas y cierre del proyecto
```

---

## 📌 Próximos pasos

* Definir dataset pequeño de ventas e inventario.
* Agregar columnas mínimas de stock.
* Cargar y limpiar datos.
* Calcular demanda observada.
* Calcular stock actual.
* Comparar demanda vs stock.
* Crear regla simple de reorder.
* Crear risk score.
* Crear recommendation cards.
* Crear gráficos.
* Crear dashboard ligero.
* Documentar labs.
* Preparar capturas.
* Publicar repo.

---

## ✅ Entregable final

Al terminar este proyecto debe existir:

* Dashboard ligero de inventario.
* Dataset pequeño de ventas e inventario.
* Demand summary.
* Stock summary.
* Reorder rule.
* Risk score simple.
* Recommendation cards.
* Gráficos.
* Labs documentados.
* README profesional.
* Capturas o outputs visibles.
* Conexión clara con `inventory-optimization-ml-service`.

---

## 🧭 Regla final

```txt id="bp03-rule"
Una recomendación de inventario no debe sonar como verdad absoluta.
Debe explicar la regla, el riesgo y la limitación.

Building Projects convierte la optimización en una decisión visible.
```

Este proyecto debe demostrar que puedo tomar datos simples de ventas e inventario y convertirlos en una herramienta entendible para decidir mejor.
