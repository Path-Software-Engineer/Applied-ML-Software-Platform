# tec-sales-eda-lab

## Objetivo

Explorar el dataset inicial de ventas antes de crear funciones oficiales de carga, limpieza o transformación.

Este lab sirve para entender qué columnas existen, qué representa cada fila y qué posibles problemas deberían revisarse antes de avanzar.

## Archivo explorado

`data/raw/sales_raw.csv`

## Preguntas del lab

### 1. ¿Qué representa cada fila?

Cada fila representa ventas agregadas de un producto en una fecha específica.

### 2. ¿Qué columnas existen?

Columnas iniciales:

* `date`
* `product`
* `category`
* `units_sold`
* `unit_price`

### 3. ¿Cuál es la columna principal para demanda observada?

La columna principal es `units_sold`, porque indica cuántas unidades se vendieron.

### 4. ¿Qué significa date?

`date` representa la fecha en la que se registró la venta.

Más adelante se usará para crear features temporales como `day_of_week`, `month`, `year` e `is_weekend`.

### 5. ¿Qué diferencia hay entre product y category?

`product` representa el producto específico vendido.

`category` representa el grupo o familia del producto.

### 6. ¿Qué significa unit_price?

`unit_price` representa el precio unitario del producto vendido.

Más adelante se usará para calcular `revenue`.

## Revisión inicial de calidad

En esta exploración se deben revisar posibles problemas como:

* valores nulos;
* fechas mal formateadas;
* tipos de datos incorrectos;
* unidades negativas;
* precios negativos;
* registros duplicados;
* categorías inconsistentes.

## Aprendizaje del lab

Antes de limpiar, transformar o analizar datos, primero debo entender qué representa cada columna.

El objetivo de este lab no es crear lógica definitiva, sino observar el dataset y preparar criterios para los próximos días.
