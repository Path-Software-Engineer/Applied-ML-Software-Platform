import assert from "node:assert/strict";
import test from "node:test";

import {
  DemandSummaryApiError,
  fetchDemandSummary,
  getDemandFigureUrl,
  validateDemandSummary,
} from "../src/features/demand-summary/api/demandSummaryApi.js";


const originalFetch = globalThis.fetch;

test.afterEach(() => {
  globalThis.fetch = originalFetch;
});


function sampleResponse() {
  const cards = Array.from({ length: 5 }, (_, index) => ({
    card_id: `card-${index + 1}`,
    title: `Card ${index + 1}`,
    metric: `${index + 1}`,
  }));
  return {
    schema_version: "1.0",
    period: {
      start_date: "2026-01-01",
      end_date: "2026-01-09",
      observed_days: 9,
    },
    sales_summary: {
      total_units_sold: 293,
      total_revenue: 747.65,
    },
    baseline: {
      mean_units_prediction: 16.28,
      mae: 5.42,
    },
    leaders: {
      product_by_units: { name: "Bread", value: 105, unit: "units" },
      product_by_revenue: { name: "Rice 1kg", value: 220.5, unit: "revenue" },
      date_by_units: { name: "2026-01-06", value: 45, unit: "units" },
      date_by_revenue: { name: "2026-01-08", value: 99.3, unit: "revenue" },
    },
    insight_cards: cards,
    limitations: ["Observed sales only."],
  };
}


test("validates the supported summary contract", () => {
  const payload = sampleResponse();

  assert.equal(validateDemandSummary(payload), payload);
});


test("rejects an unsupported schema version", () => {
  const payload = { ...sampleResponse(), schema_version: "2.0" };

  assert.throws(
    () => validateDemandSummary(payload),
    DemandSummaryApiError,
  );
});


test("rejects incomplete Insight Card evidence", () => {
  const payload = { ...sampleResponse(), insight_cards: [] };

  assert.throws(
    () => validateDemandSummary(payload),
    /expected contract/,
  );
});


test("fetches and validates the Demand Summary", async () => {
  const payload = sampleResponse();
  globalThis.fetch = async () => new Response(JSON.stringify(payload), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });

  assert.deepEqual(await fetchDemandSummary(), payload);
});


test("maps a 503 response to an explicit client error", async () => {
  globalThis.fetch = async () => new Response("", { status: 503 });

  await assert.rejects(
    fetchDemandSummary(),
    (error) => (
      error instanceof DemandSummaryApiError
      && error.status === 503
      && error.message.includes("temporarily unavailable")
    ),
  );
});


test("maps network failure without inventing evidence", async () => {
  globalThis.fetch = async () => {
    throw new TypeError("controlled network failure");
  };

  await assert.rejects(
    fetchDemandSummary(),
    /could not be reached/,
  );
});


test("encodes public figure identifiers", () => {
  assert.equal(
    getDemandFigureUrl("daily sales"),
    "/api/v1/demand-insights/figures/daily%20sales",
  );
});
