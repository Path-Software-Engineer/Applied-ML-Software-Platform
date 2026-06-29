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

## DÍA 4 — EJECUCIÓN 3 — DOCUMENTACIÓN BASE Y CIERRE DEL BLOQUE 1

Proyecto:
01-product-demand-insight-lite

Ruta:
Building Projects / Applied AI / Microproducto ML

### 1. Qué entendí hoy

Entendí que la documentación base no existe solo para llenar archivos Markdown. Existe para que el proyecto tenga dirección, sea entendible y pueda crecer sin convertirse en una carpeta desordenada.

También entendí que cada documento cumple una responsabilidad distinta. El README principal presenta el proyecto. `data/README.md` explica los datos. `reports/README.md` explica la evidencia generada. `dashboard/README.md` explica la presentación ligera. `docs/data-dictionary.md` define las columnas. `docs/insight-methodology.md` explica cómo se transforman datos en conclusiones. `docs/decisions.md` registra la ruta mental del proyecto.

### 2. Decisión sobre el README principal

El README principal será la puerta de entrada del proyecto.

Debe permitir que alguien externo entienda qué hace el microproducto, para quién sirve, qué problema resuelve, qué datos usa, cómo está organizado y qué resultado espera mostrar.

No debe ser solo una lista de carpetas. Debe explicar el sentido del proyecto.

### 3. Decisión sobre reports y dashboard

`reports/` será la carpeta donde se guardará evidencia generada por el proyecto, como resúmenes, gráficos e insight cards.

`dashboard/` será una presentación ligera de los resultados. En esta primera versión no construiremos una app real, sino una vista documental o visual que reúna los resultados importantes de forma entendible.

La regla será:

`reports/ guarda evidencia; dashboard/ presenta evidencia.`

### 4. Decisión sobre data dictionary

`docs/data-dictionary.md` explicará las columnas del dataset.

Debe indicar qué significa cada campo, si pertenece al dataset raw o si será una columna calculada en processed.

Esto ayuda a no confundir datos originales con datos derivados.

### 5. Decisión sobre insight methodology

`docs/insight-methodology.md` explicará cómo el proyecto transforma datos en conclusiones útiles.

Aquí se documentará cómo se usarán columnas como `units_sold`, `unit_price`, `date` y futuras columnas calculadas como `revenue`, `day_of_week`, `month`, `year` e `is_weekend`.

Este documento debe conectar cálculos con valor para el usuario.

### 6. Fuera de alcance del día

Hoy no construiremos carga de datos con Pandas, limpieza, feature engineering, baseline, MAE, análisis, gráficos ni dashboard real.

El foco del día es cerrar la base documental antes de avanzar al Bloque 2.

### 7. Evidencia del día

La evidencia del día será:

* README principal revisado;
* `data/README.md` actualizado;
* `reports/README.md` creado o revisado;
* `dashboard/README.md` creado o revisado;
* `docs/data-dictionary.md` creado o revisado;
* `docs/insight-methodology.md` creado o revisado;
* `docs/decisions.md` actualizado;
* Bloque 1 cerrado con dirección clara.

### 8. Conclusión del día

El Bloque 1 deja preparado el terreno del proyecto.

Ya existe una estructura, un dataset inicial, una configuración mínima y una base documental. A partir del Bloque 2, el proyecto puede empezar a trabajar con datos sin perder orden ni mezclar responsabilidades.


## DÍA 5 — EXPLORACIÓN — DATASET INICIAL Y SIGNIFICADO DE COLUMNAS

Proyecto:
01-product-demand-insight-lite

Ruta:
Building Projects / Applied AI / Microproducto ML

### 1. Qué entendí hoy

Entendí que antes de crear funciones oficiales de carga, limpieza o transformación, primero debo inspeccionar el dataset y comprender qué representa cada columna.

El objetivo del Día 5 no fue programar lógica definitiva, sino observar el archivo `data/raw/sales_raw.csv`, revisar sus columnas, verificar sus tipos de datos y detectar posibles problemas iniciales.

### 2. Archivo explorado

El archivo revisado fue:

`data/raw/sales_raw.csv`

Columnas encontradas:

* `date`
* `product`
* `category`
* `units_sold`
* `unit_price`

Cada fila representa ventas agregadas de un producto en una fecha específica.

### 3. Resultado de la inspección

La lectura inicial con Pandas funcionó correctamente.

Los tipos detectados fueron:

* `date`: texto
* `product`: texto
* `category`: texto
* `units_sold`: entero
* `unit_price`: decimal

No se encontraron valores nulos en las columnas iniciales.

### 4. Decisión sobre date

La columna `date` aparece como texto en la lectura inicial.

Esto no se considera un error en el dataset raw. La conversión de `date` a tipo fecha se realizará más adelante dentro del flujo de limpieza o transformación.

La decisión es no modificar directamente `data/raw/sales_raw.csv`.

### 5. Decisión sobre demanda observada

La columna principal para analizar demanda observada será `units_sold`.

Esta columna indica cuántas unidades se vendieron de un producto en una fecha específica.

No representa necesariamente toda la demanda real del mercado, pero sí representa la demanda observada en las ventas registradas.

### 6. Problemas iniciales revisados

En esta exploración se revisaron:

* columnas existentes;
* primeras filas del dataset;
* tipos de datos;
* valores nulos;
* significado general de cada columna.

No se detectaron valores nulos en esta versión inicial del dataset.

### 7. Fuera de alcance del día

Hoy no se creó `load_data.py`, no se creó `clean_data.py`, no se crearon features, no se calculó `revenue`, no se generó dataset processed y no se construyó baseline.

El foco del día fue entender el dataset antes de construir lógica oficial.

### 8. Evidencia del día

La evidencia del día fue la salida de inspección con Pandas, donde se verificó que:

* el CSV se puede leer;
* las columnas están presentes;
* los tipos son razonables para esta etapa;
* no hay valores nulos;
* `date` deberá convertirse más adelante;
* `units_sold` será la señal principal de demanda observada.

### 9. Conclusión del día

El dataset inicial está suficientemente sano para continuar.

El siguiente paso será crear una función oficial de carga de datos en `src/data/load_data.py`, manteniendo una responsabilidad clara: cargar datos, no limpiarlos, no crear features y no analizarlos.


## DÍA 6 — EJECUCIÓN 1 — LOAD_DATA.PY PROFESIONAL

Proyecto:
01-product-demand-insight-lite

Ruta:
Building Projects / Applied AI / Microproducto ML

### 1. Qué entendí hoy

Entendí que cargar datos no es lo mismo que limpiar, transformar, analizar o crear features.

La función de carga debe tener una responsabilidad pequeña y clara: recibir una ruta, verificar que el archivo exista, leer el CSV y devolver un DataFrame.

Esto ayuda a que el proyecto sea más ordenado, porque cada archivo cumple una función específica dentro del microproducto.

### 2. Archivo creado

Se trabajó el archivo:

`src/data/load_data.py`

Este archivo contiene la función:

`load_sales_data`

Su responsabilidad es cargar el dataset de ventas desde un archivo CSV.

### 3. Check manual

Se trabajó el archivo:

`checks/check_load_data.py`

Este check permite verificar manualmente que la función de carga funciona correctamente.

La ejecución correcta desde la raíz del proyecto es:

`python -m checks.check_load_data`

### 4. Resultado de la prueba

La carga fue exitosa.

El dataset cargado tiene:

* 18 filas;
* 5 columnas.

Columnas cargadas:

* `date`
* `product`
* `category`
* `units_sold`
* `unit_price`

### 5. Decisión sobre responsabilidad

La función `load_sales_data` no debe convertir `date` a `datetime`, no debe limpiar nulos, no debe crear `revenue`, no debe crear features y no debe analizar datos.

La decisión es mantener esta función enfocada únicamente en carga de datos.

### 6. Error aprendido

Apareció el error:

`ModuleNotFoundError: No module named 'src'`

Este error ocurrió porque el check fue ejecutado de una forma en la que Python no encontraba correctamente la carpeta `src`.

La decisión es ejecutar los checks desde la raíz del proyecto usando el modo módulo:

`python -m checks.check_load_data`

### 7. Fuera de alcance del día

Hoy no se creó `clean_data.py`, no se convirtió `date`, no se revisaron reglas de limpieza, no se crearon features, no se calculó `revenue` y no se generó dataset processed.

Eso pertenece a los próximos días.

### 8. Conclusión del día

El proyecto ya tiene una función oficial para cargar datos desde `data/raw/sales_raw.csv`.

La carga está separada de la limpieza y de la transformación, lo cual mantiene el proyecto más claro, reutilizable y fácil de probar.


## DÍA 7 — EJECUCIÓN 2 — CLEAN_DATA.PY PROFESIONAL

Proyecto:
01-product-demand-insight-lite

Ruta:
Building Projects / Applied AI / Microproducto ML

### 1. Qué entendí hoy

Entendí que limpiar datos no significa crear nuevas columnas analíticas, sino dejar el dataset en un estado confiable para poder trabajar con él después.

La limpieza se encarga de validar columnas requeridas, revisar valores nulos, convertir tipos importantes y detectar valores imposibles.

También entendí que `clean_data.py` debe mantenerse separado de `feature_engineering.py`.

### 2. Archivo trabajado

Se trabajó el archivo:

`src/data/clean_data.py`

Este archivo contiene la función:

`clean_sales_data`

Su responsabilidad es limpiar y validar el dataset de ventas después de cargarlo.

### 3. Check manual

Se trabajó el archivo:

`checks/check_clean_data.py`

Este check permite verificar que la carga y limpieza funcionan juntas.

La ejecución correcta desde la raíz del proyecto es:

`python -m checks.check_clean_data`

### 4. Resultado de la prueba

La limpieza fue exitosa.

El dataset limpio tiene:

* 18 filas;
* 5 columnas.

La columna `date` fue convertida correctamente desde texto a tipo fecha.

Los tipos principales quedaron así:

* `date`: datetime
* `product`: texto
* `category`: texto
* `units_sold`: entero
* `unit_price`: decimal

### 5. Decisión sobre date

La conversión de `date` a tipo fecha pertenece a limpieza porque permite validar que las fechas sean utilizables.

Si una fecha está mal escrita, debe detectarse en esta etapa antes de crear features temporales.

### 6. Decisión sobre features

`clean_sales_data` no debe crear `day_of_week`, `month`, `year`, `is_weekend` ni `revenue`.

Estas columnas son derivadas y pertenecen a `feature_engineering.py`, no a `clean_data.py`.

La regla será:

`clean_data.py limpia; feature_engineering.py crea columnas nuevas.`

### 7. Fuera de alcance del día

Hoy no se creó `revenue`, no se crearon features temporales, no se generó `sales_features.csv`, no se calculó baseline y no se hicieron gráficos.

Eso pertenece a los próximos bloques.

### 8. Evidencia del día

La evidencia del día fue:

* `src/data/clean_data.py` funcionando;
* `checks/check_clean_data.py` funcionando;
* dataset cargado y limpiado correctamente;
* `date` convertido a datetime;
* número de filas conservado;
* número de columnas conservado;
* separación clara entre limpieza y feature engineering.

### 9. Conclusión del día

El proyecto ya puede cargar y limpiar datos de forma separada.

Esto permite avanzar hacia un pipeline inicial con responsabilidades claras: primero cargar, luego limpiar, después crear features y finalmente analizar.

## DÍA 8 — EJECUCIÓN 3 — PIPELINE INICIAL DE DATOS

Proyecto:
01-product-demand-insight-lite

Ruta:
Building Projects / Applied AI / Microproducto ML

### 1. Qué entendí hoy

Entendí que `pipeline.py` no debe contener toda la lógica interna del proyecto.

Su responsabilidad es coordinar piezas ya separadas. En este caso, llama a `load_sales_data` para cargar datos y luego a `clean_sales_data` para limpiar el dataset.

La regla principal es:

`pipeline.py orquesta; los módulos ejecutan su responsabilidad.`

### 2. Archivos trabajados

Se trabajaron estos archivos:

* `src/pipeline.py`
* `checks/check_pipeline.py`
* `scripts/run_pipeline.ps1`

### 3. Flujo construido

El flujo inicial del pipeline quedó así:

`data/raw/sales_raw.csv → load_sales_data → clean_sales_data → clean_data`

Este flujo todavía no crea features, no calcula revenue, no genera baseline y no guarda `data/processed`.

### 4. Resultado de la prueba

El pipeline se ejecutó correctamente.

Resultado principal:

* raw data: 18 filas y 5 columnas;
* clean data: 18 filas y 5 columnas;
* `date` fue convertido a tipo datetime;
* `units_sold` se mantuvo presente;
* las columnas limpias fueron preservadas.

### 5. Decisión sobre responsabilidades

La decisión principal es mantener separadas las responsabilidades:

* `load_data.py` carga datos;
* `clean_data.py` limpia datos;
* `pipeline.py` conecta los pasos en orden;
* `check_pipeline.py` verifica manualmente que el flujo funcione;
* `run_pipeline.ps1` permite ejecutar el flujo de forma repetible desde PowerShell.

### 6. Fuera de alcance del día

Hoy no se crearon features temporales, no se calculó revenue, no se generó `sales_features.csv`, no se calculó baseline, no se creó MAE y no se hizo análisis de ventas.

Eso pertenece a los siguientes bloques.

### 7. Evidencia del día

La evidencia del día fue:

* `python -m src.pipeline` ejecutado correctamente;
* `python -m checks.check_pipeline` ejecutado correctamente;
* `.\scripts\run_pipeline.ps1` ejecutado correctamente;
* carga y limpieza conectadas;
* `date` convertido a datetime;
* `units_sold` preservado;
* pipeline reproducible desde script.

### 8. Conclusión del día

El Bloque 2 queda cerrado.

El proyecto ya puede cargar y limpiar datos desde `data/raw` de forma reproducible. La base de datos del microproducto está lista para avanzar al Bloque 3, donde se trabajará el primer lab cloud y luego feature engineering.
