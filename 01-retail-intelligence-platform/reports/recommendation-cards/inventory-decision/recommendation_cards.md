# Inventory Recommendation Cards

## 01 — Bread

- Risk: **critical** (100.0/100 priority index).
- Stock / reorder point: 0 / 35 units.
- Action: `replenish_now`; suggested review quantity 70 units.
- Reason: Observed stock is zero while observed demand is positive.
- Policy: `inventory-review-policy/1.0`.
- Limitation: Learning evidence from a small synthetic period; review current stock, supplier lead time and recent demand before acting.

## 02 — Milk 1L

- Risk: **high** (50.0/100 priority index).
- Stock / reorder point: 9 / 18 units.
- Action: `replenish_soon`; suggested review quantity 27 units.
- Reason: Observed stock covers 1.50 days, below the 3-day protected horizon.
- Policy: `inventory-review-policy/1.0`.
- Limitation: Learning evidence from a small synthetic period; review current stock, supplier lead time and recent demand before acting.

## 03 — Coffee 250g

- Risk: **healthy** (0.0/100 priority index).
- Stock / reorder point: 10 / 8 units.
- Action: `monitor`; suggested review quantity 0 units.
- Reason: Observed stock remains above the policy reorder point.
- Policy: `inventory-review-policy/1.0`.
- Limitation: Learning evidence from a small synthetic period; review current stock, supplier lead time and recent demand before acting.

## 04 — Rice 1kg

- Risk: **healthy** (0.0/100 priority index).
- Stock / reorder point: 29 / 21 units.
- Action: `monitor`; suggested review quantity 0 units.
- Reason: Observed stock remains above the policy reorder point.
- Policy: `inventory-review-policy/1.0`.
- Limitation: Learning evidence from a small synthetic period; review current stock, supplier lead time and recent demand before acting.

## 05 — Eggs 12 pack

- Risk: **healthy** (0.0/100 priority index).
- Stock / reorder point: 24 / 9 units.
- Action: `monitor`; suggested review quantity 0 units.
- Reason: Observed stock remains above the policy reorder point.
- Policy: `inventory-review-policy/1.0`.
- Limitation: Learning evidence from a small synthetic period; review current stock, supplier lead time and recent demand before acting.

## 06 — Orange Juice

- Risk: **healthy** (0.0/100 priority index).
- Stock / reorder point: 27 / 8 units.
- Action: `monitor`; suggested review quantity 0 units.
- Reason: Observed stock remains above the policy reorder point.
- Policy: `inventory-review-policy/1.0`.
- Limitation: Learning evidence from a small synthetic period; review current stock, supplier lead time and recent demand before acting.
