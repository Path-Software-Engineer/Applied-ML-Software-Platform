# First Data Pipeline Summary

## Sprint

Sprint 1 â€” Demand Insight Module

## Day

Day 6 â€” First Data Pipeline

## Pipeline flow

```txt
raw sales data
â†’ load dataset
â†’ validate required columns
â†’ clean rows
â†’ export pipeline-ready dataset
â†’ write summary
```

## Inputs

```txt
C:/JeanLoa/Path-Software-Engineer/Applied-AI-Software-Platform/01-retail-intelligence-platform/data/raw/demand-insight/sales.csv
```

## Outputs

```txt
C:/JeanLoa/Path-Software-Engineer/Applied-AI-Software-Platform/01-retail-intelligence-platform/data/processed/demand-insight/sales_pipeline_ready.csv
```

## Result

| Metric | Value |
| ------ | ----: |
| Rows | 18 |
| Columns | 8 |

## Required columns

```txt
date, product_id, product_name, units_sold, unit_price
```

## Interpretation

The Demand Insight Module now has a repeatable first data pipeline.

This pipeline connects raw data loading, column validation, cleaning rules and a processed output that can be reused by later feature engineering, baseline and insight steps.

## Status

```txt
Completed
```
