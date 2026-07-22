# Inventory Decision Trace

Policy: `inventory-review-policy/1.0`  
Evidence date: `2026-01-09`  
Risk score meaning: priority index, not probability.

## 01 — Bread

- Inputs: stock 0 units; observed demand 11.666667 units/day; lead time 2 days (policy_default).
- Policy: reorder point 35 units; target 70 units; priority index 100.0.
- Review outcome: `replenish_now`; suggested 70 units.
- Reason: Observed stock is zero while observed demand is positive.
- Limitation: Learning evidence from a small synthetic period; review current stock, supplier lead time and recent demand before acting.

## 02 — Milk 1L

- Inputs: stock 9 units; observed demand 6.0 units/day; lead time 2 days (policy_default).
- Policy: reorder point 18 units; target 36 units; priority index 50.0.
- Review outcome: `replenish_soon`; suggested 27 units.
- Reason: Observed stock covers 1.50 days, below the 3-day protected horizon.
- Limitation: Learning evidence from a small synthetic period; review current stock, supplier lead time and recent demand before acting.

## 03 — Coffee 250g

- Inputs: stock 10 units; observed demand 2.555556 units/day; lead time 2 days (policy_default).
- Policy: reorder point 8 units; target 16 units; priority index 0.0.
- Review outcome: `monitor`; suggested 0 units.
- Reason: Observed stock remains above the policy reorder point.
- Limitation: Learning evidence from a small synthetic period; review current stock, supplier lead time and recent demand before acting.

## 04 — Rice 1kg

- Inputs: stock 29 units; observed demand 7.0 units/day; lead time 2 days (policy_default).
- Policy: reorder point 21 units; target 42 units; priority index 0.0.
- Review outcome: `monitor`; suggested 0 units.
- Reason: Observed stock remains above the policy reorder point.
- Limitation: Learning evidence from a small synthetic period; review current stock, supplier lead time and recent demand before acting.

## 05 — Eggs 12 pack

- Inputs: stock 24 units; observed demand 2.777778 units/day; lead time 2 days (policy_default).
- Policy: reorder point 9 units; target 17 units; priority index 0.0.
- Review outcome: `monitor`; suggested 0 units.
- Reason: Observed stock remains above the policy reorder point.
- Limitation: Learning evidence from a small synthetic period; review current stock, supplier lead time and recent demand before acting.

## 06 — Orange Juice

- Inputs: stock 27 units; observed demand 2.555556 units/day; lead time 2 days (policy_default).
- Policy: reorder point 8 units; target 16 units; priority index 0.0.
- Review outcome: `monitor`; suggested 0 units.
- Reason: Observed stock remains above the policy reorder point.
- Limitation: Learning evidence from a small synthetic period; review current stock, supplier lead time and recent demand before acting.
