# Data Contract — Demand Insight Module

## Dataset

```txt
data/raw/demand-insight/sales.csv
```

## Purpose

This dataset represents a small retail sales sample used by the Demand Insight Module.

The dataset is intentionally small, controlled and easy to inspect.

It will be used to support:

```txt
data loading
→ validation
→ cleaning
→ feature engineering
→ baseline
→ MAE
→ demand insights
```

---

# Columns

| Column | Type | Required | Description |
| --- | --- | --- | --- |
| sale_id | integer | yes | Unique identifier for each sale record. |
| date | date | yes | Date of the sale. |
| product_id | string | yes | Product identifier. |
| product_name | string | yes | Human-readable product name. |
| category | string | yes | Product category. |
| units_sold | integer | yes | Number of units sold. |
| unit_price | float | yes | Price per unit. |
| stock_available | integer | yes | Available stock after or near the sale record. |

---

# Expected rules

## sale_id

Must be unique.

## date

Must be parseable as a date.

Expected format:

```txt
YYYY-MM-DD
```

## product_id

Must not be empty.

## product_name

Must not be empty.

## category

Must not be empty.

## units_sold

Must be numeric.

Expected:

```txt
units_sold >= 0
```

## unit_price

Must be numeric.

Expected:

```txt
unit_price > 0
```

## stock_available

Must be numeric.

Expected:

```txt
stock_available >= 0
```

---

# Initial dataset shape

Expected initial shape:

```txt
18 rows
8 columns
```

---

# Future processed dataset

The processed dataset will add derived columns.

Expected future columns may include:

```txt
day_of_week
month
year
is_weekend
revenue
```

Main derived rule:

```txt
revenue = units_sold * unit_price
```

---

# Limitations

This dataset is small and artificial.

It is useful for learning software structure, data contracts, validation, feature engineering and baseline evaluation.

It should not be treated as a real business dataset.

---

# Data ownership

This dataset is a local learning asset for the project:

```txt
01-retail-intelligence-platform
```
