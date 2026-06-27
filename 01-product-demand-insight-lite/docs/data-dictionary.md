# Data Dictionary — 01-product-demand-insight-lite

Este documento explica el significado de las columnas usadas en el dataset inicial del proyecto.

El objetivo es entender qué representa cada campo antes de crear funciones de carga, limpieza, features, baseline, análisis o gráficos.

## Dataset inicial

Archivo:

`data/raw/sales_raw.csv`

Cada fila representa ventas agregadas de un producto en una fecha específica.

## Columnas raw

### date

Fecha en la que se registró la venta.

Ejemplo:

`2026-06-01`

Esta columna pertenece al dataset raw porque viene directamente como parte del registro original.

Más adelante se usará para crear columnas calculadas como:

* `day_of_week`
* `month`
* `year`
* `is_weekend`

### product

Nombre del producto vendido.

Ejemplo:

`Classic Glazed Donut`

Esta columna permite identificar qué producto tuvo ventas en una fecha específica.

### category

Categoría o grupo al que pertenece el producto.

Ejemplo:

`Classic`

La categoría ayuda a analizar productos por grupos más generales.

Un producto es específico.
Una categoría agrupa varios productos.

### units_sold

Cantidad de unidades vendidas de un producto en una fecha específica.

Ejemplo:

`18`

Esta es la columna principal para analizar demanda observada en este proyecto.

No representa necesariamente toda la demanda real del mercado, sino la cantidad registrada como vendida.

### unit_price

Precio unitario del producto vendido.

Ejemplo:

`4.00`

Esta columna permitirá calcular después el revenue:

`revenue = units_sold * unit_price`

## Columnas calculadas futuras

Estas columnas no pertenecen al dataset raw. Serán generadas más adelante en `data/processed`.

### revenue

Dinero generado por las ventas de un producto en una fecha específica.

Se calculará usando:

`units_sold * unit_price`

### day_of_week

Día de la semana derivado desde `date`.

Puede ayudar a detectar qué días tienen mejor rendimiento.

### month

Mes derivado desde `date`.

Puede ayudar a analizar patrones por mes.

### year

Año derivado desde `date`.

Puede servir si el dataset contiene registros de varios años.

### is_weekend

Columna calculada para indicar si la fecha corresponde a fin de semana.

Puede ayudar a comparar ventas entre días de semana y fines de semana.

## Posibles problemas iniciales a revisar

Antes de limpiar o transformar los datos, se deben revisar posibles problemas como:

* valores nulos;
* fechas mal formateadas;
* tipos de datos incorrectos;
* unidades vendidas negativas;
* precios negativos;
* productos duplicados por error;
* categorías inconsistentes;
* registros repetidos.

## Conclusión

Este dataset inicial es suficiente para comenzar el microproducto porque permite analizar ventas por fecha, producto, categoría, unidades vendidas y precio unitario.

La columna más importante para demanda observada es `units_sold`.
