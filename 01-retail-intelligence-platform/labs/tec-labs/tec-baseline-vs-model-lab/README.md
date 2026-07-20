# TEC Lab — Baseline versus Model

## Question

Why must a learned model be compared with a simple baseline under the same
observations and metric formula?

## Controlled experiment

The lab uses four invented observations unrelated to the official retail
dataset. It compares a fixed mean-style reference with a hypothetical learned
candidate and calculates MAE/RMSE through the production metric registry.

## Boundary

- The lab is not imported by production code.
- Its values are not Sprint 2 model results.
- It teaches comparison mechanics and does not select the official candidate.

Run:

```powershell
$env:PYTHONPATH = "ai-services/model-comparison/src"
python labs/tec-labs/tec-baseline-vs-model-lab/src/run_lab.py
```
