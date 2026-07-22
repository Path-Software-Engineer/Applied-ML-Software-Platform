import fs from "node:fs";

import { validateInventoryDecision } from "../src/features/inventory-decision/api/inventoryDecisionApi.js";

const payloadPath = process.argv[2];
if (!payloadPath) throw new Error("An Inventory Decision response path is required.");

const payload = JSON.parse(fs.readFileSync(payloadPath, "utf8"));
const validated = validateInventoryDecision(payload);
if (validated.ranking[0].product_id !== "P003") {
  throw new Error("Unexpected first inventory review priority.");
}
if (validated.summary.suggested_review_quantity_units !== 97) {
  throw new Error("Unexpected suggested review quantity.");
}

console.log("OK - frontend accepted the real Inventory Decision API contract");
console.log(`Products / Recommendation Cards: ${validated.ranking.length} / ${validated.recommendation_cards.length}`);
