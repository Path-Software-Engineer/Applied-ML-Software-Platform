import assert from "node:assert/strict";
import test from "node:test";

import {
  PLATFORM_STAGES,
  resolvePlatformView,
} from "../src/shared/navigation/platformNavigation.js";


test("keeps product stages separate and ordered", () => {
  assert.deepEqual(
    PLATFORM_STAGES.map(({ id, label }) => ({ id, label })),
    [
      { id: "demand-insight", label: "Demand insight" },
      { id: "model-comparison", label: "Model comparison" },
    ],
  );
});


test("assigns only Demand Insight sections to the first stage", () => {
  assert.deepEqual(
    PLATFORM_STAGES[0].sections.map(({ label }) => label),
    ["Overview", "Leaders", "Insight cards", "Visual report"],
  );
});


test("assigns comparison-specific sections to the second stage", () => {
  assert.deepEqual(
    PLATFORM_STAGES[1].sections.map(({ label }) => label),
    [
      "Overview",
      "Candidates",
      "Decision rationale",
      "Decision cards",
      "Evidence boundary",
    ],
  );
});


test("keeps every Model Comparison section in the comparison view", () => {
  for (const section of PLATFORM_STAGES[1].sections) {
    assert.equal(resolvePlatformView(section.href), "model-comparison");
  }
  assert.equal(resolvePlatformView("#leaders"), "demand-insight");
  assert.equal(resolvePlatformView(""), "demand-insight");
});
