# Temporal Sales Analysis Summary

## Day

Sprint 1 - Week 3 - Day 18

## Objective

Analyze observed sales by date to identify temporal concentration in units sold and revenue.

## Input

`data/processed/demand-insight/sales_feature_baseline_metric_pipeline.csv`

## Output

`data/processed/demand-insight/daily_sales_summary.csv`

## Main results

| Metric | Result |
|---|---:|
| Observed dates | 9 |
| Total units preserved | 293 |
| Total revenue preserved | 747.65 |
| Top date by units sold | 2026-01-06 |
| Units sold on top date | 45 |
| Share of total units | 15.36% |
| Top date by revenue | 2026-01-08 |
| Revenue on top date | 99.30 |
| Share of total revenue | 13.28% |

## Daily summary

| Date | Total units sold | Total revenue | Sales records |
|---|---:|---:|---:|
| 2026-01-01 | 30 | 74.40 | 2 |
| 2026-01-02 | 33 | 77.20 | 2 |
| 2026-01-03 | 35 | 88.50 | 2 |
| 2026-01-04 | 40 | 63.50 | 2 |
| 2026-01-05 | 20 | 94.20 | 2 |
| 2026-01-06 | 45 | 93.10 | 2 |
| 2026-01-07 | 29 | 64.55 | 2 |
| 2026-01-08 | 20 | 99.30 | 2 |
| 2026-01-09 | 41 | 92.90 | 2 |

## Interpretation

The highest observed demand occurred on 2026-01-06 with 45 units sold, representing 15.36% of all units in the available period.

The highest observed revenue occurred on 2026-01-08 with 99.30, representing 13.28% of total revenue.

Units sold and revenue peaked on different dates. This confirms that demand volume and economic value do not necessarily tell the same temporal story.

## Limitations

This analysis describes only the period from 2026-01-01 to 2026-01-09.

It does not demonstrate a recurring weekday pattern, trend or seasonality.

It does not predict future demand.

It does not justify replenishment, production or promotional decisions without additional historical, inventory and cost information.