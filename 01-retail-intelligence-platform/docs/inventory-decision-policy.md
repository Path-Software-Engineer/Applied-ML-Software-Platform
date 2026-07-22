# Inventory Decision Policy

Status: policy `inventory-review-policy/1.0` frozen on global Day 120.

## Candidate policy

- observed demand, stock and reorder quantities use compatible units;
- missing source lead time may use a declared policy default;
- safety stock is expressed as a documented number of demand days;
- target stock adds a review-period horizon;
- all integer quantities round upward;
- suggested quantity is never negative;
- risk score ranks attention and is not a probability.

## Frozen parameters and formulas

- default lead time: `2` days when the source value is missing;
- safety horizon: `1` demand day;
- review period: `3` days;
- rounding: mathematical ceiling to whole units;
- reorder trigger: stock at or below reorder point;
- reorder point: `ceil(daily_demand × (lead_time + safety_days))`;
- target stock: `ceil(daily_demand × (lead_time + safety_days + review_period))`;
- suggested quantity: `max(0, target_stock - stock)` only when triggered.

Risk score weights shortage ratio at 70% and coverage pressure at 30%. Labels
are `critical` from 75, `high` from 50, `watch` from 25 and `healthy` below 25.
The index is not a calibrated probability.

## Recommendation language

Every card must state the product, risk label, review action, suggested quantity,
reason, policy version and limitation. The words “order”, “purchase” or
“guarantee” cannot imply that the system executed an operational transaction.

