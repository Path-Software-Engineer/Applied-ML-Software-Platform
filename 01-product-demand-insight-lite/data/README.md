# Data — 01-product-demand-insight-lite

Esta carpeta contiene los datos usados por el microproducto.

El objetivo es separar claramente los datos originales de los datos procesados para evitar confusión durante el análisis.

## Estructura

```txt
data/
├── raw/
│   └── sales_raw.csv
├── processed/
└── README.md
```

## data/raw

La carpeta `data/raw` contiene los datos originales del proyecto.

Estos datos representan la fuente inicial y no deben modificarse directamente durante el proceso de análisis.

Archivo inicial:

```txt
data/raw/sales_raw.csv
```

Columnas iniciales:

```txt
date
product
category
units_sold
unit_price
```

Cada fila representa ventas agregadas de un producto en una fecha específica.

Ejemplo:

```txt
2026-06-01,Classic Glazed Donut,Classic,18,4.00
```

Esto significa que el día 2026-06-01 se vendieron 18 unidades de Classic Glazed Donut con un precio unitario de 4.00.

## data/processed

La carpeta `data/processed` contendrá datos generados por el proyecto después de limpiar, transformar o enriquecer el dataset original.

Aquí podrán aparecer columnas calculadas como:

```txt
revenue
day_of_week
month
year
is_weekend
```

Estas columnas no pertenecen al archivo raw porque no vienen directamente de la fuente inicial. Son generadas por el proyecto.

## Diferencia entre raw y processed

`raw` es lo que recibimos como fuente original.

`processed` es lo que construimos después de aplicar limpieza, transformaciones o creación de features.

## Regla del proyecto

No modificar directamente los archivos de `data/raw`.

Si necesito limpiar o enriquecer datos, debo generar un nuevo archivo dentro de `data/processed`.
