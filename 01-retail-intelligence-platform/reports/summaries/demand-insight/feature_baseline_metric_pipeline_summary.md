# Feature + Baseline + Metric Pipeline Summary

## Official map alignment

This output closes the official Week 2 Day 6 requirement:

```txt
Pipeline with features, baseline and metric.
```

## Input

```txt
C:/JeanLoa/Path-Software-Engineer/Applied-AI-Software-Platform/01-retail-intelligence-platform/data/processed/demand-insight/sales_pipeline_ready.csv
```

## Output

```txt
C:/JeanLoa/Path-Software-Engineer/Applied-AI-Software-Platform/01-retail-intelligence-platform/data/processed/demand-insight/sales_feature_baseline_metric_pipeline.csv
```

## Pipeline flow

```txt
processed dataset
â†’ feature engineering
â†’ mean baseline
â†’ baseline predictions
â†’ MAE
â†’ technical summary
```

## Results

| Metric | Value |
| ------ | ----: |
| Rows | 18 |
| Columns | 15 |
| Baseline | 16.28 |
| Baseline MAE | 5.42 |

## Interpretation

The baseline gives the reference prediction.

MAE shows the average error in units sold.

This pipeline makes the Week 2 technical flow repeatable before moving into analysis and insights.

## Status

```txt
Completed
```
