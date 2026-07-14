# Sprint 1 — Week 3 Review

## Review status

In progress through Day 20. This is a checkpoint, not a weekly closure.

## Completed work

- Day 15: analysis and insight exploration.
- Day 16: general Sales Summary.
- Day 17: Product Summary and rankings.
- Day 18: Temporal Sales Analysis.
- Day 19: structured Insight Cards.
- Day 20: basic sales figures and reusable visual report.

## Evidence

- `data/processed/demand-insight/sales_summary.csv`
- `data/processed/demand-insight/product_summary.csv`
- `data/processed/demand-insight/product_ranking_by_units.csv`
- `data/processed/demand-insight/product_ranking_by_revenue.csv`
- `data/processed/demand-insight/daily_sales_summary.csv`
- `reports/summaries/demand-insight/sales_summary.md`
- `reports/summaries/demand-insight/product_ranking_summary.md`
- `reports/summaries/demand-insight/temporal_sales_analysis_summary.md`
- `reports/insight-cards/demand_insight_cards.json`
- `reports/insight-cards/demand_insight_cards.md`
- `reports/figures/demand-insight/daily_sales.png`
- `reports/figures/demand-insight/product_units_ranking.png`
- `reports/figures/demand-insight/product_revenue_ranking.png`
- `reports/outputs/demand-insight/sales_visual_report.md`

## Validated results

- Total observed demand: 293 units.
- Total observed revenue: 747.65.
- Bread leads units with 105.
- Rice 1kg leads revenue with 220.50.
- 2026-01-06 leads daily units with 45.
- 2026-01-08 leads daily revenue with 99.30.

## Validation

The accumulated suite reports 30 passing tests.

The Day 20 isolated suite contains seven passing cases covering input contracts, date parsing, PNG generation, Insight Card validation and visual report rendering.

## Decisions

Demand volume and economic value remain separate analytical signals. All
interpretations must state the short observed period and avoid predictive or
inventory claims.

Visual artifacts consume validated processed datasets and the interpretations already defined by the Insight Cards. They remain independent from React so their analytical meaning and generated evidence can be verified before a user interface consumes them.

## Day 19 checkpoint — Insight Cards

Day 19 converted validated sales artifacts into five structured Insight Cards:

- observed demand;
- top product by units;
- top product by revenue;
- top date by units;
- top date by revenue.

The cards are available as JSON for future software integration and Markdown for human review.

The implementation keeps metric calculation separate from user-facing interpretation and explicitly states that the observed period does not predict future demand.

## Day 20 checkpoint — Visual report

Day 20 converted the validated sales signals into three reusable figures:

- daily sales, with units and revenue shown in separate panels;
- product ranking by units sold;
- product ranking by revenue.

Units sold represent demand volume, while revenue represents observed economic value. They use separate figures or axes because they are different magnitudes and must not be interpreted as equivalent measurements.

The Markdown visual report embeds the generated PNG files and reuses the validated interpretations from the Insight Cards. This avoids duplicating analytical conclusions inside the visualization layer.

The figures and report are production artifacts generated without requiring a browser or React. A future frontend may consume the same validated information without becoming responsible for its analytical meaning.

Week 3 remains open. Day 21 is still pending.
