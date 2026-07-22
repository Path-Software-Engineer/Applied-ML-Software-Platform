import assert from "node:assert/strict";
import test from "node:test";

import {
  formatAction,
  formatCoverage,
  toRecommendationCardViewModel,
} from "../src/features/inventory-decision/presentation/inventoryDecisionViewModel.js";

test("formats null coverage without inventing a number", () => {
  assert.equal(formatCoverage(null), "No observed coverage");
});

test("maps action codes to review-oriented language", () => {
  assert.equal(formatAction("replenish_now"), "Replenish now");
  assert.equal(formatAction("monitor"), "Monitor");
});

test("keeps API evidence unchanged in the recommendation view model", () => {
  const view = toRecommendationCardViewModel({
    card_id: "inventory-P003",
    priority_rank: 1,
    product: { product_id: "P003", product_name: "Bread" },
    risk: { label: "critical", score: 100 },
    evidence: { current_stock_units: 0, coverage_days: 0 },
    action: { code: "replenish_now", suggested_quantity_units: 70 },
    reason: "Observed stock is zero.",
    limitation: "Human review required.",
  });
  assert.equal(view.productName, "Bread");
  assert.equal(view.quantityLabel, "70 units");
  assert.equal(view.riskScore, "100.0");
});
