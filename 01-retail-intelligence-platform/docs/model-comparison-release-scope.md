# Model Comparison Release Scope

## Candidate release

`v0.2.0-sprint-02-model-comparison`

## Included

- one frozen chronological experiment with four comparable candidates;
- versioned comparison, error, decision, Model Card and Decision Card evidence;
- one strict backend read service and FastAPI endpoint;
- one isolated React comparison experience;
- cross-layer, HTTP smoke and compatibility checks;
- documentation and portfolio evidence produced through Day 84.

## Excluded

- model tuning or additional estimators;
- cross-validation or production validation;
- deployment and authentication;
- automated inventory decisions;
- real retail generalization claims;
- Sprint 3 implementation.

## Evidence limitations

The analytical result uses 18 synthetic rows and a six-row chronological holdout.
It is suitable for architecture and workflow learning, not for
production performance claims or real retail generalization.

## Release acceptance

1. Analytical artifacts regenerate deterministically.
2. Python and frontend automated suites pass.
3. Frontend compilation and local HTTP smoke pass.
4. All manual checks pass, including Sprint 1 compatibility.
5. Documentation, release notes and evidence paths are current.
6. Browser screenshots are either valid real-app artifacts or explicitly
   recorded as blocked; mockups are never substituted.
7. Release branch, `main`, annotated tag and `develop` synchronization are clean.
