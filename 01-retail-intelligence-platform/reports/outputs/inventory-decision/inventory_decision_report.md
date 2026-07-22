# Inventory Decision Report

Status: **learning evidence only**

## Review summary

- Products: 6.
- Observed stock: 99 units.
- Replenishment review: 2 products.
- Critical / high / watch / healthy: 1 / 1 / 0 / 4.
- Suggested review quantity: 97 units.

## Priority ranking

| Rank | Product | Stock | Coverage | Reorder point | Suggested | Risk | Action |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | Bread | 0 | 0.00 days | 35 | 70 | critical (100.0) | replenish_now |
| 2 | Milk 1L | 9 | 1.50 days | 18 | 27 | high (50.0) | replenish_soon |
| 3 | Coffee 250g | 10 | 3.91 days | 8 | 0 | healthy (0.0) | monitor |
| 4 | Rice 1kg | 29 | 4.14 days | 21 | 0 | healthy (0.0) | monitor |
| 5 | Eggs 12 pack | 24 | 8.64 days | 9 | 0 | healthy (0.0) | monitor |
| 6 | Orange Juice | 27 | 10.57 days | 8 | 0 | healthy (0.0) | monitor |

## Limitations

- The inventory snapshot and sales period are small synthetic learning evidence.
- Observed daily average is descriptive and is not a validated demand forecast.
- Lead time is a versioned two-day policy default, not supplier evidence.
- Risk score is a prioritization index and is not a stockout probability.
- Suggested quantities require human review and do not create purchase orders.

The risk score is not a probability and no order was created.
