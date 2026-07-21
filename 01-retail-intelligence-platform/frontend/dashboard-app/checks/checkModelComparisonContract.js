import fs from "node:fs";

import { validateModelComparison } from "../src/features/model-comparison/api/modelComparisonApi.js";


const payloadPath = process.argv[2];
if (!payloadPath) {
  throw new Error("A Model Comparison response path is required.");
}

const payload = JSON.parse(fs.readFileSync(payloadPath, "utf8"));
const validated = validateModelComparison(payload);

if (validated.decision.selected_candidate.model_id !== "random_forest") {
  throw new Error("Unexpected selected integration candidate.");
}

console.log("OK - frontend accepted the real Model Comparison API contract");
console.log(`Candidates / Decision Cards: ${validated.candidates.length} / ${validated.decision_cards.length}`);
