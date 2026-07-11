# Product Ranking Summary

## Day

Sprint 1 - Week 3 - Day 17

## Objective

Build a product-level summary and rank observed products by units sold and revenue.

## Input

`data/processed/demand-insight/sales_feature_baseline_metric_pipeline.csv`

## Outputs

- `data/processed/demand-insight/product_summary.csv`
- `data/processed/demand-insight/product_ranking_by_units.csv`
- `data/processed/demand-insight/product_ranking_by_revenue.csv`

## Main results

| Metric | Result |
|---|---|
| Unique products | 6 |
| Top product by units sold | Bread |
| Top units sold | 105 |
| Top product by revenue | Rice 1kg |
| Top revenue | 220.50 |

## Ranking by units sold

| units_rank | product_id | product_name | total_units_sold |
| --- | --- | --- | --- |
| 1 | P003 | Bread | 105 |
| 2 | P001 | Rice 1kg | 63 |
| 3 | P002 | Milk 1L | 54 |
| 4 | P006 | Eggs 12 pack | 25 |
| 5 | P004 | Coffee 250g | 23 |
| 6 | P005 | Orange Juice | 23 |

## Ranking by revenue

| revenue_rank | product_id | product_name | total_revenue |
| --- | --- | --- | --- |
| 1 | P001 | Rice 1kg | 220.5 |
| 2 | P004 | Coffee 250g | 135.7 |
| 3 | P003 | Bread | 126.0 |
| 4 | P006 | Eggs 12 pack | 105.0 |
| 5 | P002 | Milk 1L | 97.2 |
| 6 | P005 | Orange Juice | 63.25 |

## Interpretation

The units ranking measures accumulated observed demand per product.

The revenue ranking measures accumulated observed economic value per product.

The leading product can differ between rankings because revenue depends on both units sold and unit price.

## Limitations

These rankings describe only the current observed dataset.

They do not predict future demand and do not measure profit because product costs are unavailable.
