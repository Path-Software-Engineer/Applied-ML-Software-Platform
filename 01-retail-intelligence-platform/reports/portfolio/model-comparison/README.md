# Model Comparison Portfolio Evidence

## Product story

The module compares a training-mean baseline, Linear Regression, Random Forest
and Gradient Boosting under one chronological holdout. Gradient Boosting leads
the observed MAE ranking; Random Forest moves to the next integration step under
the frozen practical-equivalence and lower-complexity policy.

## Reproducible demo

From the project root, start the API and frontend in separate PowerShell
terminals:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-backend.ps1
```

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-frontend.ps1
```

Open `http://127.0.0.1:5173/#model-comparison`. The expected connected view
shows four candidates, the leader-versus-selection strip, the rationale, three
Decision Cards and the evidence boundary.

## Canonical evidence

`evidence_manifest.json` records SHA-256 hashes for the final comparison report,
Decision Cards, Model Cards and comparison table. The quality gate regenerates
and validates those sources before release.

## Visual capture status

Desktop 1440×900, tablet 768×1024 and mobile 390×844 captures are required.
They are currently blocked because the in-app browser policy rejected the local
URL. No screenshot, mockup or browser approval is claimed. This is a release
blocker, not a reason to fabricate evidence.

## Limitations

- 18 synthetic observations;
- six-row chronological holdout;
- no stability or real-retail validation;
- no production-readiness or inventory-action claim.
