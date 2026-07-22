import assert from "node:assert/strict";
import test from "node:test";

import {
  InventoryDecisionApiError,
  fetchInventoryDecision,
  validateInventoryDecision,
} from "../src/features/inventory-decision/api/inventoryDecisionApi.js";


const originalFetch = globalThis.fetch;
test.afterEach(() => { globalThis.fetch = originalFetch; });


function sampleResponse() {
  const ranking = Array.from({ length: 2 }, (_, index) => ({
    priority_rank: index + 1,
    product_id: `P00${index + 1}`,
    product_name: `Product ${index + 1}`,
    current_stock_units: index,
    observed_daily_demand: 2.5,
    coverage_days: index / 2,
    reorder_point_units: 8,
    target_stock_units: 16,
    suggested_quantity_units: 16 - index,
    risk_score: 100 - index * 50,
    risk_score_meaning: "priority_index_not_probability",
    risk_label: index === 0 ? "critical" : "high",
    recommended_action: index === 0 ? "replenish_now" : "replenish_soon",
    reason: "Controlled reason.",
    policy_version: "inventory-review-policy/1.0",
  }));
  return {
    schema_version: "1.0",
    module: "inventory_decision",
    report_status: "learning_evidence_only",
    freshness: { evidence_as_of_date: "2026-01-09", age_days: 2, stale_after_days: 7, status: "current" },
    snapshot: { products: 2, as_of_date: "2026-01-09" },
    demand_signal: { signal_type: "observed_daily_average" },
    integration: { join_key: "product_id", join_strategy: "strict_one_to_one", joined_products: 2, unmatched_products: 0 },
    policy: { version: "inventory-review-policy/1.0", risk_score_meaning: "priority_index_not_probability" },
    summary: { products: 2 },
    ranking,
    recommendation_cards: ranking.map((item) => ({
      card_id: `inventory-${item.product_id}`,
      product: { product_id: item.product_id, product_name: item.product_name },
      risk: { label: item.risk_label, score: item.risk_score, meaning: "priority_index_not_probability" },
      evidence: { current_stock_units: item.current_stock_units },
      action: { code: item.recommended_action, suggested_quantity_units: item.suggested_quantity_units },
      reason: item.reason,
      limitation: "Human review required.",
    })),
    limitations: ["one", "two", "three", "four", "five"],
  };
}


test("validates supported inventory decision evidence", () => {
  const payload = sampleResponse();
  assert.equal(validateInventoryDecision(payload), payload);
});


test("rejects probability semantics", () => {
  const payload = sampleResponse();
  payload.ranking[0].risk_score_meaning = "stockout_probability";
  assert.throws(() => validateInventoryDecision(payload), InventoryDecisionApiError);
});


test("rejects inconsistent product coverage", () => {
  const payload = sampleResponse();
  payload.recommendation_cards.pop();
  assert.throws(() => validateInventoryDecision(payload), /expected contract/);
});


test("fetches and validates inventory decision evidence", async () => {
  const payload = sampleResponse();
  globalThis.fetch = async () => new Response(JSON.stringify(payload), { status: 200 });
  assert.deepEqual(await fetchInventoryDecision(), payload);
});


test("maps 503 without inventing stock evidence", async () => {
  globalThis.fetch = async () => new Response("", { status: 503 });
  await assert.rejects(
    fetchInventoryDecision(),
    (error) => error.status === 503 && error.message.includes("temporarily unavailable"),
  );
});
