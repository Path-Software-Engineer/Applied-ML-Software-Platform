# Final Demo Script

## Preparation

1. Run the platform evidence generator and root quality gate.
2. Start the API and frontend with `docs/runbook.md`.
3. Open `http://127.0.0.1:5173/#demand-insight`.
4. Keep the browser console and network panel available for verification.

## Demand Insight

1. Expand **Demand Insight** and select **Overview**.
2. Explain the nine-day evidence period, 293 observed units and 747.65 revenue.
3. Open **Leaders** and contrast Bread by units with Rice 1kg by revenue.
4. Show **Insight cards** and **Visual report** while stating that they describe
   observed history and do not forecast future demand.

## Model Comparison

1. Expand **Model Comparison** and select **Experiment**.
2. Compare the four candidates on the chronological six-row holdout.
3. Open **Decision** and explain why Gradient Boosting leads measured MAE while
   Random Forest is selected under the frozen practical-equivalence policy.
4. Open **Evidence** and state the 18-row synthetic-data boundary.

## Inventory Decision

1. Expand **Inventory Decision** and select **Priority queue**.
2. Show Bread as the critical zero-stock item and Milk 1L as high risk.
3. Open **Recommendations** and review the six product-level cards.
4. Open **Policy trace** to show the deterministic rule, inputs and rationale.
5. Close on the 97-unit suggested review quantity and clarify that it is not an
   executed purchase order.

## Acceptance close

Confirm that all three endpoints return HTTP 200, the UI exposes explicit
loading/error/evidence states, no browser calculation replaces analytical
artifacts, and no production-readiness claim is made.
