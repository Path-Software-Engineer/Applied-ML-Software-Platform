const API_BASE_URL = import.meta.env?.VITE_API_BASE_URL ?? "";
const MODEL_COMPARISON_PATH = "/api/v1/model-comparisons/summary";

const EXPECTED_MODEL_IDS = new Set([
  "training_mean",
  "linear_regression",
  "random_forest",
  "gradient_boosting",
]);
const EXPECTED_CARD_IDS = new Set([
  "metric-leader",
  "integration-candidate",
  "evidence-boundary",
]);


export class ModelComparisonApiError extends Error {
  constructor(message, status = null) {
    super(message);
    this.name = "ModelComparisonApiError";
    this.status = status;
  }
}


function isRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}


function isNumber(value) {
  return typeof value === "number" && Number.isFinite(value);
}


function sameMembers(values, expected) {
  return values.size === expected.size
    && [...values].every((value) => expected.has(value));
}


export function validateModelComparison(payload) {
  if (
    !isRecord(payload)
    || payload.schema_version !== "1.0"
    || payload.module !== "model_comparison"
    || payload.report_status !== "learning_evidence_only"
  ) {
    throw new ModelComparisonApiError(
      "The Model Comparison response uses an unsupported contract.",
    );
  }

  const experiment = payload.experiment;
  const candidates = payload.candidates;
  const decision = payload.decision;
  const cards = payload.decision_cards;
  if (
    !isRecord(experiment)
    || experiment.train_rows !== 12
    || experiment.test_rows !== 6
    || !Array.isArray(candidates)
    || candidates.length !== 4
    || !isRecord(decision)
    || !Array.isArray(cards)
    || cards.length !== 3
    || !Array.isArray(payload.limitations)
    || payload.limitations.length < 4
  ) {
    throw new ModelComparisonApiError(
      "The Model Comparison response does not match the expected contract.",
    );
  }

  const modelIds = new Set(candidates.map((candidate) => candidate?.model_id));
  const ranks = new Set(candidates.map((candidate) => candidate?.mae_rank));
  const invalidCandidate = candidates.some((candidate) => (
    !isRecord(candidate)
    || !candidate.model_name
    || !candidate.model_family
    || !isNumber(candidate.mae_units)
    || candidate.mae_units < 0
    || !isNumber(candidate.rmse_units)
    || candidate.rmse_units < 0
    || !isNumber(candidate.r2_contextual)
    || !isNumber(candidate.mae_improvement_vs_baseline_percent)
    || typeof candidate.within_practical_equivalence !== "boolean"
    || candidate.production_status !== "learning_evidence_only"
  ));
  if (
    invalidCandidate
    || !sameMembers(modelIds, EXPECTED_MODEL_IDS)
    || !sameMembers(ranks, new Set([1, 2, 3, 4]))
  ) {
    throw new ModelComparisonApiError(
      "The Model Comparison candidates contain invalid evidence.",
    );
  }

  const leader = decision.measurement_leader;
  const selected = decision.selected_candidate;
  if (
    !isRecord(leader)
    || !isRecord(selected)
    || !modelIds.has(leader.model_id)
    || !modelIds.has(selected.model_id)
    || !isNumber(leader.mae_units)
    || !isNumber(selected.mae_units)
    || decision.production_status !== "not_production_ready"
    || decision.stability_status !== "not_assessed"
    || !Array.isArray(decision.rationale)
    || decision.rationale.length === 0
  ) {
    throw new ModelComparisonApiError(
      "The Model Comparison decision contains invalid evidence.",
    );
  }

  const cardIds = new Set(cards.map((card) => card?.card_id));
  if (
    !sameMembers(cardIds, EXPECTED_CARD_IDS)
    || cards.some((card) => (
      !isRecord(card)
      || !card.title
      || !card.summary
      || !card.limitation
      || !isRecord(card.primary_metric)
      || !isNumber(card.primary_metric.value)
      || !Array.isArray(card.reasons)
      || card.reasons.length === 0
    ))
  ) {
    throw new ModelComparisonApiError(
      "The Model Comparison Decision Cards are incomplete.",
    );
  }

  return payload;
}


export async function fetchModelComparison({ signal } = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${MODEL_COMPARISON_PATH}`, {
      headers: { Accept: "application/json" },
      signal,
    });
  } catch (error) {
    if (
      typeof DOMException !== "undefined"
      && error instanceof DOMException
      && error.name === "AbortError"
    ) {
      throw error;
    }
    throw new ModelComparisonApiError(
      "The Model Comparison service could not be reached.",
    );
  }

  if (!response.ok) {
    throw new ModelComparisonApiError(
      response.status === 503
        ? "Validated comparison evidence is temporarily unavailable."
        : "The Model Comparison request could not be completed.",
      response.status,
    );
  }

  return validateModelComparison(await response.json());
}
