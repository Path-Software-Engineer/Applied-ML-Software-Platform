# Sprint 2 — Model Comparison Retrospective

## What worked well

- one immutable experiment contract made every candidate comparable;
- selection policy was frozen before the final model decision;
- analytical, transport and presentation responsibilities stayed separate;
- one canonical report prevented request-time artifact joins;
- cross-layer validation detected drift across Python and JavaScript;
- daily branches and non-fast-forward merges preserved implementation history.

## Challenges

- the intentionally small synthetic dataset limits model conclusions;
- local scikit-learn availability required a controlled runtime path;
- Vite process creation was restricted in the engineering runner;
- the in-app browser policy rejected the local URL and blocked real screenshots.

## Improvements adopted

- a direct esbuild path makes frontend compilation deterministic;
- a live HTTP smoke starts and stops its own API and static services;
- the shared platform shell removed duplicate frontend structure;
- safe service logs expose only low-cardinality release metadata;
- the portfolio manifest records blocked captures instead of fabricating them.

## Carry-forward

- unblock and capture the three real responsive views before releasing Sprint 2;
- keep the API schema and analytical evidence frozen during release mechanics;
- begin Sprint 3 only in a new planning and exploration boundary;
- preserve `not_production_ready` until real data and validation justify change.
