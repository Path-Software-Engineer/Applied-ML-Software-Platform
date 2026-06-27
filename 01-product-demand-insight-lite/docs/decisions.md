## DÍA 1 — EXPLORACIÓN — MAPA DEL PRODUCTO, USUARIO Y ALCANCE

Proyecto:
01-product-demand-insight-lite

Ruta:
Building Projects / Applied AI / Microproducto ML

### 1. Qué entendí hoy

Entendí que antes de construir un proyecto relacionado con análisis de ventas, demanda o Machine Learning, primero debo preparar el problema de negocio, el contexto analítico y la dirección del producto.

Aunque un caso pequeño podría resolverse rápidamente en un notebook, esta base documental me servirá para construir proyectos cada vez más ordenados, claros y grandes relacionados con análisis de datos, Machine Learning y productos aplicados.

También entendí que este proyecto no debe empezar creando archivos Python sin dirección. Primero necesito saber qué problema resuelve, quién lo usaría, qué valor entrega, qué datos necesita y qué partes no deben construirse todavía.

### 2. Decisión principal del día

La decisión principal del día es que este proyecto tendrá documentación viva desde el inicio.

Usaremos archivos como `README.md`, `docs/product-brief.md`, `docs/data-dictionary.md`, `docs/insight-methodology.md` y `docs/decisions.md` para explicar qué función cumple cada parte del proyecto.

Esto me ayudará a aprender la estructura del proyecto, separar responsabilidades de forma clara y evitar construir archivos sueltos sin propósito.

### 3. Fuera de alcance

En este primer bloque todavía no haremos carga de datos, limpieza, feature engineering, baseline, métricas, análisis, gráficos ni código de Machine Learning.

Primero estamos preparando la base del proyecto para que luego la construcción sea ordenada, limpia y entendible.

Tampoco construiremos una API, backend pesado, modelo complejo, MLOps ni deploy. Eso pertenece al enfoque más profundo de AI Engineer, no a esta primera versión de Building Projects.

### 4. Evidencia del día

La evidencia del día es haber definido el sentido inicial del proyecto:

* qué problema busca ordenar;
* qué tipo de usuario lo usaría;
* qué valor debe entregar;
* qué documentación necesita;
* qué cosas no deben construirse todavía;
* por qué primero se diseña el terreno antes de programar.

### 5. Conclusión del día

Este proyecto debe empezar como un microproducto aplicado y documentado.

La meta no es programar rápido, sino construir con dirección. Primero se diseña el camino, luego se crean los datos, después se construye la lógica y finalmente se genera evidencia visual entendible.


## DÍA 2 — EJECUCIÓN 1 — AUDITORÍA DE ESTRUCTURA Y RESPONSABILIDADES

Proyecto:
01-product-demand-insight-lite

Ruta:
Building Projects / Applied AI / Microproducto ML

### 1. Qué entendí hoy

Entendí que no basta con tener carpetas creadas. Cada carpeta debe tener una responsabilidad clara dentro del proyecto.

La estructura no debe existir solo por verse profesional. Debe ayudarme a separar datos, lógica, documentación, evidencias, labs, scripts y presentación visual.

También entendí que este Día 2 no necesita enfocarse en crear carpetas desde cero, porque la mayoría de carpetas ya existen. Por eso el objetivo cambia a auditar la estructura, revisar responsabilidades y evitar ambigüedad.

### 2. Decisión sobre `src/`

`src/` será la fuente oficial del código del producto.

Aquí vivirá la lógica limpia y reutilizable del microproducto: carga de datos, limpieza, features, baseline, análisis, insights, visualización y pipeline.

La regla será:

`src/ formaliza la lógica del producto.`

### 3. Decisión sobre `notebooks/`

`notebooks/` será usado solo como espacio de exploración.

Puede servir para probar ideas, inspeccionar datos, experimentar con Pandas o revisar resultados rápidamente, pero no será la fuente oficial del proyecto.

Si algo probado en un notebook se vuelve importante para el producto, debe pasar después a un archivo limpio dentro de `src/`.

La regla será:

`notebooks/ descubre; src/ formaliza.`

### 4. Decisión sobre `app/` y `dashboard/`

En este primer proyecto no construiremos una app real todavía.

Para evitar ambigüedad, `dashboard/` se usará como presentación ligera o documentación visual del resultado. No debe duplicar lógica de `src/`.

La carpeta `app/` no será usada en esta primera versión, salvo que más adelante se tome una decisión explícita.

La regla será:

`src/ calcula; dashboard/ presenta.`

### 5. Decisión sobre archivos generados

`.venv/`, `__pycache__/`, archivos `.pyc`, `.env` y checkpoints de notebooks no deben subirse a GitHub.

Estos archivos no son fuente del proyecto. Son generados por el entorno, por Python o por herramientas locales. Pueden ocupar espacio, ensuciar el repositorio y crear cambios innecesarios.

La decisión es mantenerlos fuera del repositorio mediante `.gitignore`.

### 6. Fuera de alcance del día

Hoy no construiremos carga de datos, limpieza, features, baseline, análisis, gráficos ni dashboard real.

El foco del día es entender y dejar clara la estructura del proyecto antes de avanzar hacia datos y código.

### 7. Evidencia del día

La evidencia del día será:

* estructura revisada;
* responsabilidades de carpetas entendidas;
* decisión sobre `src/`, `notebooks/`, `dashboard/` y `app/`;
* `.gitignore` revisado;
* `project-structure.txt` generado sin `.venv`, `.git` ni `__pycache__`;
* entrada registrada en `docs/decisions.md`.

### 8. Conclusión del día

El proyecto no debe crecer como una carpeta desordenada.

Cada parte debe tener una responsabilidad clara:

`data/` guarda datos.
`src/` contiene lógica oficial.
`checks/` verifica manualmente.
`reports/` guarda evidencia.
`docs/` explica decisiones.
`labs/` guarda experimentos.
`scripts/` automatiza comandos.
`dashboard/` presenta resultados.

La estructura correcta no es tener muchas carpetas, sino saber por qué existe cada una.


## DÍA 3 — EJECUCIÓN 2 — DATASET INICIAL Y CONFIGURACIÓN MÍNIMA

Proyecto:
01-product-demand-insight-lite

Ruta:
Building Projects / Applied AI / Microproducto ML

### 1. Qué entendí hoy

Entendí que antes de cargar datos con Pandas o crear lógica en `src/`, primero debo definir correctamente la materia prima del proyecto.

El archivo `data/raw/sales_raw.csv` representa los datos originales del microproducto. Estos datos deben mantenerse simples y no deben mezclarse con columnas calculadas.

También entendí que el dataset raw no debe incluir todo lo que quiero analizar, sino solo lo que viene como base inicial. Las columnas derivadas se crearán después en `data/processed`.

### 2. Dataset inicial

El dataset inicial será:

`data/raw/sales_raw.csv`

Columnas iniciales:

* `date`
* `product`
* `category`
* `units_sold`
* `unit_price`

Cada fila representa ventas agregadas de un producto en una fecha específica.

### 3. Decisión sobre raw y processed

La decisión principal es separar claramente los datos originales de los datos calculados.

`data/raw` guardará la fuente original.

`data/processed` guardará los datos generados después de limpiar, transformar o enriquecer el dataset.

La columna `date` pertenece al raw porque viene como parte del registro original. Pero desde `date` se crearán nuevas columnas calculadas como:

* `day_of_week`
* `month`
* `year`
* `is_weekend`

Estas columnas pertenecerán al dataset procesado.

### 4. Decisión sobre revenue

`revenue` no estará en `sales_raw.csv`.

Aunque es una métrica importante para el análisis, no viene directamente como dato original. Será calculada después usando:

`revenue = units_sold * unit_price`

Por eso `revenue` debe aparecer en `data/processed/sales_features.csv`, no en `data/raw/sales_raw.csv`.

### 5. Decisión sobre requirements.txt

Se creó `requirements.txt` para registrar las dependencias externas del proyecto.

Por ahora la dependencia principal será:

`pandas`

La decisión es subir `requirements.txt` a GitHub, pero no subir `.venv/`, porque el entorno virtual puede reconstruirse instalando las dependencias desde `requirements.txt`.

### 6. Fuera de alcance del día

Hoy no se construirá carga de datos con Pandas, limpieza, feature engineering, baseline, análisis, gráficos ni dashboard.

El objetivo del día es dejar lista la materia prima del proyecto y entender qué representa cada columna.

### 7. Evidencia del día

La evidencia del día será:

* `requirements.txt` creado;
* `data/raw/sales_raw.csv` creado;
* `data/README.md` actualizado;
* columnas raw definidas;
* diferencia entre raw y processed entendida;
* `project-structure.txt` actualizado;
* decisión registrada en `docs/decisions.md`.

### 8. Conclusión del día

El proyecto ya tiene una fuente inicial de datos.

La regla principal es no contaminar `raw` con columnas calculadas. Primero recibo datos simples, luego los transformo y recién después genero un dataset procesado más útil para análisis, baseline, insights y gráficos.
