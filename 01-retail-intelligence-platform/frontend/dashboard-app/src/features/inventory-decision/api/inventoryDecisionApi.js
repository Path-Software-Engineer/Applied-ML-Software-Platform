const API_BASE_URL = import.meta.env?.VITE_API_BASE_URL ?? "";
const INVENTORY_DECISION_PATH = "/api/v1/inventory-decisions/summary";

const RISK_LABELS = new Set(["critical", "high", "watch", "healthy"]);
const ACTIONS = new Set(["replenish_now", "replenish_soon", "review", "monitor"]);


export class InventoryDecisionApiError extends Error {
  constructor(message, status = null) {
    super(message);
    this.name = "InventoryDecisionApiError";
    this.status = status;
  }
}


function isRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}


function isNumber(value) {
  return typeof value === "number" && Number.isFinite(value);
}


function invalidRankingItem(item) {
  return !isRecord(item)
    || !Number.isInteger(item.priority_rank)
    || item.priority_rank < 1
    || typeof item.product_id !== "string"
    || typeof item.product_name !== "string"
    || !Number.isInteger(item.current_stock_units)
    || item.current_stock_units < 0
    || !isNumber(item.observed_daily_demand)
    || item.observed_daily_demand < 0
    || !(item.coverage_days === null || (isNumber(item.coverage_days) && item.coverage_days >= 0))
    || !Number.isInteger(item.reorder_point_units)
    || !Number.isInteger(item.suggested_quantity_units)
    || !isNumber(item.risk_score)
    || item.risk_score < 0
    || item.risk_score > 100
    || item.risk_score_meaning !== "priority_index_not_probability"
    || !RISK_LABELS.has(item.risk_label)
    || !ACTIONS.has(item.recommended_action)
    || item.policy_version !== "inventory-review-policy/1.0";
}


function invalidCard(card) {
  return !isRecord(card)
    || !card.card_id?.startsWith("inventory-")
    || !isRecord(card.product)
    || !isRecord(card.risk)
    || !isRecord(card.evidence)
    || !isRecord(card.action)
    || !RISK_LABELS.has(card.risk.label)
    || card.risk.meaning !== "priority_index_not_probability"
    || !ACTIONS.has(card.action.code)
    || !Number.isInteger(card.action.suggested_quantity_units)
    || typeof card.reason !== "string"
    || typeof card.limitation !== "string";
}


export function validateInventoryDecision(payload) {
  if (
    !isRecord(payload)
    || payload.schema_version !== "1.0"
    || payload.module !== "inventory_decision"
    || payload.report_status !== "learning_evidence_only"
  ) {
    throw new InventoryDecisionApiError(
      "The Inventory Decision response uses an unsupported contract.",
    );
  }

  const { freshness, snapshot, demand_signal: demandSignal, integration, policy, summary } = payload;
  const ranking = payload.ranking;
  const cards = payload.recommendation_cards;
  if (
    !isRecord(freshness)
    || !["current", "stale"].includes(freshness.status)
    || !Number.isInteger(freshness.age_days)
    || !isRecord(snapshot)
    || !isRecord(demandSignal)
    || demandSignal.signal_type !== "observed_daily_average"
    || !isRecord(integration)
    || integration.join_key !== "product_id"
    || integration.join_strategy !== "strict_one_to_one"
    || integration.unmatched_products !== 0
    || !isRecord(policy)
    || policy.version !== "inventory-review-policy/1.0"
    || policy.risk_score_meaning !== "priority_index_not_probability"
    || !isRecord(summary)
    || !Number.isInteger(summary.products)
    || summary.products < 1
    || !Array.isArray(ranking)
    || ranking.length !== summary.products
    || !Array.isArray(cards)
    || cards.length !== summary.products
    || !Array.isArray(payload.limitations)
    || payload.limitations.length < 5
  ) {
    throw new InventoryDecisionApiError(
      "The Inventory Decision response does not match the expected contract.",
    );
  }

  const ranks = new Set(ranking.map((item) => item?.priority_rank));
  const productIds = new Set(ranking.map((item) => item?.product_id));
  const cardProductIds = new Set(cards.map((card) => card?.product?.product_id));
  if (
    ranking.some(invalidRankingItem)
    || cards.some(invalidCard)
    || ranks.size !== ranking.length
    || productIds.size !== ranking.length
    || cardProductIds.size !== cards.length
    || [...productIds].some((id) => !cardProductIds.has(id))
    || integration.joined_products !== summary.products
    || snapshot.products !== summary.products
  ) {
    throw new InventoryDecisionApiError(
      "The Inventory Decision evidence contains inconsistent products.",
    );
  }
  return payload;
}


export async function fetchInventoryDecision({ signal } = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${INVENTORY_DECISION_PATH}`, {
      headers: { Accept: "application/json" },
      signal,
    });
  } catch (error) {
    if (error?.name === "AbortError") throw error;
    throw new InventoryDecisionApiError(
      "The Inventory Decision service could not be reached.",
    );
  }

  if (!response.ok) {
    throw new InventoryDecisionApiError(
      response.status === 503
        ? "Validated inventory evidence is temporarily unavailable."
        : "The Inventory Decision request could not be completed.",
      response.status,
    );
  }
  return validateInventoryDecision(await response.json());
}
