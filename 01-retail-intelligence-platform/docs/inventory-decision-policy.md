# Inventory Decision Policy

Status: preliminary on global Day 113; alternatives and final version are
frozen during Week 10.

## Candidate policy

- observed demand, stock and reorder quantities use compatible units;
- missing source lead time may use a declared policy default;
- safety stock is expressed as a documented number of demand days;
- target stock adds a review-period horizon;
- all integer quantities round upward;
- suggested quantity is never negative;
- risk score ranks attention and is not a probability.

## Recommendation language

Every card must state the product, risk label, review action, suggested quantity,
reason, policy version and limitation. The words “order”, “purchase” or
“guarantee” cannot imply that the system executed an operational transaction.

