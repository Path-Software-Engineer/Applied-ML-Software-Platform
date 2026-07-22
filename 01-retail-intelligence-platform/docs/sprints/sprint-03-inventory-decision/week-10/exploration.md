# Week 10 Exploration — Replenishment and Risk Policy

## Decision problem

Week 9 provides validated stock facts and an observed demand signal. Week 10
must turn those inputs into a transparent review priority without claiming to
optimize purchasing, predict demand or estimate a calibrated stockout probability.

## Formula alternatives

### Reorder point

1. `daily demand × lead time`. Simple but carries no explicit buffer.
2. `daily demand × (lead time + safety days)`. Selected because the safety
   assumption is visible and auditable.
3. Statistical safety stock. Rejected because demand variability, target service
   level and lead-time distribution are not validated.

### Target stock

1. Fill only to reorder point. Rejected because the product could immediately
   re-enter the review queue.
2. Add a fixed review-period horizon. Selected as a transparent learning rule.
3. Economic order quantity. Rejected because ordering and holding costs do not exist.

### Risk

1. A binary low-stock flag. Too coarse for ranking.
2. A weighted shortage and coverage pressure index. Selected with explicit
   weights and thresholds.
3. A probability of stockout. Rejected because no calibrated probabilistic model exists.

## Frozen policy 1.0

| Parameter | Value | Meaning |
|---|---:|---|
| default lead time | 2 days | policy assumption when source lead time is absent |
| safety horizon | 1 demand day | explicit simple buffer |
| review period | 3 days | target-stock horizon beyond reorder point |
| rounding | ceiling | whole non-negative units |
| reorder trigger | stock at or below reorder point | inclusive deterministic boundary |

```text
reorder_point = ceil(daily_demand × (lead_time_days + safety_days))
target_stock  = ceil(daily_demand × (lead_time_days + safety_days + review_period_days))
suggested_quantity = max(0, target_stock - stock) only when trigger is active
```

## Priority index

For positive demand:

```text
shortage_ratio = clamp((reorder_point - stock) / max(reorder_point, 1), 0, 1)
coverage_pressure = clamp((lead_time + safety_days - coverage_days)
                          / (lead_time + safety_days), 0, 1)
risk_score = round(100 × (0.7 × shortage_ratio + 0.3 × coverage_pressure), 1)
```

Zero stock with positive demand has score 100. Zero observed demand has score 0
and no finite coverage value. The score is a deterministic priority index, not
a probability.

## Labels and actions

| Score | Label | Review action |
|---:|---|---|
| 75–100 | critical | replenish now |
| 50–74.9 | high | replenish soon |
| 25–49.9 | watch | review |
| 0–24.9 | healthy | monitor |

Priority sorts score descending, then finite coverage ascending, then
`product_id` ascending.

## Nemesis scenarios

- stock exactly equals reorder point;
- stockout with positive demand;
- zero demand with positive or zero stock;
- missing source lead time;
- very large demand;
- rounding near an integer boundary;
- invalid negative inputs;
- two products with the same score.

## Day 120 boundary

The formulas, parameters, units, thresholds, language and limitations are frozen.
No policy function or Recommendation Card is implemented on this exploration day.

