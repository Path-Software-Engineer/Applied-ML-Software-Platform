const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";
const DEMAND_SUMMARY_PATH = "/api/v1/demand-insights/summary";


export class DemandSummaryApiError extends Error {
  constructor(message, status = null) {
    super(message);
    this.name = "DemandSummaryApiError";
    this.status = status;
  }
}


export async function fetchDemandSummary({ signal } = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${DEMAND_SUMMARY_PATH}`, {
      headers: { Accept: "application/json" },
      signal,
    });
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
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

  const payload = await response.json();
  if (payload.schema_version !== "1.0") {
    throw new DemandSummaryApiError(
      "The Demand Insight response uses an unsupported contract version.",
    );
  }
  return payload;
}
