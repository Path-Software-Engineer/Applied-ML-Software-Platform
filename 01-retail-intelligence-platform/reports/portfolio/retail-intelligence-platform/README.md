# Retail Intelligence Platform — Demo Evidence

## Demonstrable product flow

The local application exposes three expandable product stages backed by three
read-only API resources. Demand Insight explains observed sales, Model
Comparison separates metric leadership from the selected candidate, and
Inventory Decision turns the evidence into review priorities under a versioned
policy.

Run the API and frontend with the commands in `docs/runbook.md`, then open
`http://127.0.0.1:5173/#demand-insight`. The complete walkthrough is in
`demo-script.md`.

## Reproducible runtime evidence

`checks/check_final_platform_smoke.py` starts a real Uvicorn process and the
compiled React smoke shell, requests all three resources through the same-origin
proxy, validates their canonical outcomes, and stops both processes. The
manifest binds the three official JSON reports to SHA-256 hashes.

## Visual capture boundary

Desktop 1440×900, tablet 768×1024 and mobile 390×844 remain required. The
in-app browser policy rejects the local application URL, so their paths are
intentionally null. No screenshot, mockup or browser approval is claimed. The
runtime and source-level checks do not replace responsive visual approval.

## Public evidence limits

- The source contains 18 synthetic sales observations.
- Model comparison uses one six-row chronological holdout.
- Inventory recommendations are deterministic review suggestions, not orders.
- No external validation, production deployment or autonomous action is claimed.
