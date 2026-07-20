import assert from "node:assert/strict";
import test from "node:test";

import {
  ModelComparisonApiError,
  fetchModelComparison,
  validateModelComparison,
} from "../src/features/model-comparison/api/modelComparisonApi.js";


const originalFetch = globalThis.fetch;

test.afterEach(() => {
  globalThis.fetch = originalFetch;
});


function sampleResponse() {
  const modelSpecs = [
    ["gradient_boosting", "Gradient Boosting"],
    ["random_forest", "Random Forest"],
    ["linear_regression", "Linear Regression"],
    ["training_mean", "Training Mean Baseline"],
  ];
  const candidates = modelSpecs.map(([modelId, modelName], index) => ({
    model_id: modelId,
    model_name: modelName,
    model_family: "controlled_family",
    mae_rank: index + 1,
    mae_units: 3 + index / 10,
    rmse_units: 3.5 + index / 10,
    r2_contextual: 0.4 - index / 10,
    mae_improvement_vs_baseline_percent: 20 - index,
    within_practical_equivalence: index < 2,
    production_status: "learning_evidence_only",
  }));
  const cards = [
    ["metric-leader", "gradient_boosting"],
    ["integration-candidate", "random_forest"],
    ["evidence-boundary", null],
  ].map(([cardId, modelId]) => ({
    card_id: cardId,
    title: cardId,
    summary: "Controlled summary.",
    limitation: "Controlled limitation.",
    reasons: ["Controlled reason."],
    primary_metric: { value: modelId ? 3.1 : 6 },
  }));
  return {
    schema_version: "1.0",
    module: "model_comparison",
    report_status: "learning_evidence_only",
    experiment: { train_rows: 12, test_rows: 6, target: "units_sold" },
    candidates,
    decision: {
      measurement_leader: {
        model_id: "gradient_boosting",
        model_name: "Gradient Boosting",
        mae_units: 3.1,
      },
      selected_candidate: {
        model_id: "random_forest",
        model_name: "Random Forest",
        mae_units: 3.2,
      },
      rationale: ["Controlled rationale."],
      production_status: "not_production_ready",
      stability_status: "not_assessed",
      practical_equivalence_units: 0.25,
    },
    decision_cards: cards,
    limitations: ["one", "two", "three", "four"],
  };
}


test("validates the supported Model Comparison contract", () => {
  const payload = sampleResponse();

  assert.equal(validateModelComparison(payload), payload);
});


test("rejects an unsupported Model Comparison version", () => {
  const payload = { ...sampleResponse(), schema_version: "2.0" };

  assert.throws(() => validateModelComparison(payload), ModelComparisonApiError);
});


test("rejects missing candidates", () => {
  const payload = { ...sampleResponse(), candidates: [] };

  assert.throws(() => validateModelComparison(payload), /expected contract/);
});


test("rejects duplicate candidate identities", () => {
  const payload = sampleResponse();
  payload.candidates[3].model_id = "random_forest";

  assert.throws(() => validateModelComparison(payload), /candidates/);
});


test("rejects incomplete Decision Cards", () => {
  const payload = sampleResponse();
  payload.decision_cards[2].reasons = [];

  assert.throws(() => validateModelComparison(payload), /Decision Cards/);
});


test("fetches and validates Model Comparison evidence", async () => {
  const payload = sampleResponse();
  globalThis.fetch = async () => new Response(JSON.stringify(payload), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });

  assert.deepEqual(await fetchModelComparison(), payload);
});


test("maps a 503 without inventing model evidence", async () => {
  globalThis.fetch = async () => new Response("", { status: 503 });

  await assert.rejects(
    fetchModelComparison(),
    (error) => (
      error instanceof ModelComparisonApiError
      && error.status === 503
      && error.message.includes("temporarily unavailable")
    ),
  );
});


test("maps network failure to an unavailable client error", async () => {
  globalThis.fetch = async () => {
    throw new TypeError("controlled network failure");
  };

  await assert.rejects(fetchModelComparison(), /could not be reached/);
});
