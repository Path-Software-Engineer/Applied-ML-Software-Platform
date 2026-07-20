import assert from "node:assert/strict";
import test from "node:test";

import { createDecisionCardView } from "../src/features/model-comparison/presentation/decisionCardViewModel.js";


function sampleCard(overrides = {}) {
  return {
    card_id: "integration-candidate",
    eyebrow: "Selected for next integration",
    title: "Random Forest",
    status: "selected_for_next_integration",
    model_id: "random_forest",
    primary_metric: {
      label: "MAE",
      value: 3.125795965608463,
      unit: "units",
      direction: "lower_is_better",
    },
    summary: "Selected by the frozen rule.",
    reasons: ["Practically equivalent.", "Lower recorded complexity."],
    limitation: "Not production ready.",
    ...overrides,
  };
}


test("preserves API identity and metric without recomputation", () => {
  const card = sampleCard();
  const view = createDecisionCardView(card);

  assert.equal(view.cardId, card.card_id);
  assert.equal(view.modelId, card.model_id);
  assert.equal(view.metricValue, card.primary_metric.value);
  assert.equal(view.metricDirection, card.primary_metric.direction);
  assert.equal(view.reasons, card.reasons);
});


test("maps the API status to presentation copy only", () => {
  const view = createDecisionCardView(sampleCard());

  assert.equal(view.status, "selected_for_next_integration");
  assert.equal(view.statusLabel, "Integration candidate");
});


test("preserves a null model on the evidence-boundary card", () => {
  const view = createDecisionCardView(sampleCard({
    card_id: "evidence-boundary",
    model_id: null,
    status: "not_production_ready",
  }));

  assert.equal(view.modelId, null);
  assert.equal(view.statusLabel, "Evidence boundary");
});
