const API_BASE_URL = import.meta.env?.VITE_API_BASE_URL ?? "";
const DEMAND_SUMMARY_PATH = "/api/v1/demand-insights/summary";

export const DEMAND_FIGURES = [
  {
    figureId: "daily-sales",
    title: "Daily performance",
    description: "Observed units and revenue by trading day.",
  },
  {
    figureId: "product-units-ranking",
    title: "Demand ranking",
    description: "Products ordered by observed unit volume.",
  },
  {
    figureId: "product-revenue-ranking",
    title: "Revenue ranking",
    description: "Products ordered by observed economic value.",
  },
];


export function getDemandFigureUrl(figureId) {
  return `${API_BASE_URL}/api/v1/demand-insights/figures/${encodeURIComponent(figureId)}`;
}


export class DemandSummaryApiError extends Error {
  constructor(message, status = null) {
    super(message);
    this.name = "DemandSummaryApiError";
    this.status = status;
  }
}


function isRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}


export function validateDemandSummary(payload) {
  if (!isRecord(payload) || payload.schema_version !== "1.0") {
    throw new DemandSummaryApiError(
      "The Demand Insight response uses an unsupported contract version.",
    );
  }

  const summary = payload.sales_summary;
  const leaders = payload.leaders;
  const cards = payload.insight_cards;
  if (
    !isRecord(payload.period)
    || !isRecord(summary)
    || !isRecord(payload.baseline)
    || !isRecord(leaders)
    || !Array.isArray(cards)
    || cards.length !== 5
  ) {
    throw new DemandSummaryApiError(
      "The Demand Insight response does not match the expected contract.",
    );
  }

  const numericMeasures = [
    summary.total_units_sold,
    summary.total_revenue,
    payload.baseline.mean_units_prediction,
    payload.baseline.mae,
  ];
  const leaderKeys = [
    "product_by_units",
    "product_by_revenue",
    "date_by_units",
    "date_by_revenue",
  ];
  const cardIds = new Set(cards.map((card) => card?.card_id));
  if (
    numericMeasures.some((value) => typeof value !== "number" || value < 0)
    || leaderKeys.some((key) => !isRecord(leaders[key]))
    || cardIds.size !== 5
    || cards.some((card) => !isRecord(card) || !card.title || !card.metric)
  ) {
    throw new DemandSummaryApiError(
      "The Demand Insight response contains invalid evidence.",
    );
  }
  return payload;
}


export async function fetchDemandSummary({ signal } = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${DEMAND_SUMMARY_PATH}`, {
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
    throw new DemandSummaryApiError(
      "The Demand Insight service could not be reached.",
    );
  }

  if (!response.ok) {
    throw new DemandSummaryApiError(
      response.status === 503
        ? "Validated demand evidence is temporarily unavailable."
        : "The Demand Insight request could not be completed.",
      response.status,
    );
  }

  return validateDemandSummary(await response.json());
}
