"""Apply the frozen Day 64 policy to select the next integration candidate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


COMPLEXITY_ORDER = {
    "training_mean": 1,
    "linear_regression": 2,
    "random_forest": 3,
    "gradient_boosting": 4,
}
PRACTICAL_EQUIVALENCE_UNITS = 0.25
MINIMUM_BASELINE_IMPROVEMENT_PERCENT = 10.0


class DecisionError(ValueError):
    """Raised when decision evidence is incomplete or inconsistent."""


def select_candidate(
    comparison: dict[str, Any],
    error_analysis: dict[str, Any],
) -> dict[str, Any]:
    """Return a reproducible decision from formal metric and error evidence."""
    rows = comparison.get("rows")
    summaries = error_analysis.get("candidate_summaries")
    if not isinstance(rows, list) or len(rows) != 4:
        raise DecisionError("Comparison evidence must contain four rows.")
    if not isinstance(summaries, list) or len(summaries) != 4:
        raise DecisionError("Error evidence must contain four summaries.")
    if comparison.get("selection_status") != "not_selected":
        raise DecisionError("Comparison input must precede formal selection.")
    if error_analysis.get("interpretation_boundary") != (
        "descriptive_no_causal_claims"
    ):
        raise DecisionError("Error evidence has an invalid interpretation boundary.")

    row_ids = {row["model_id"] for row in rows}
    summary_by_id = {summary["model_id"]: summary for summary in summaries}
    if row_ids != set(COMPLEXITY_ORDER) or row_ids != set(summary_by_id):
        raise DecisionError("Candidate identities differ across decision inputs.")

    measurement_leader = min(rows, key=lambda row: float(row["mae_units"]))
    eligible = [
        row
        for row in rows
        if row["model_id"] != "training_mean"
        and float(row["mae_improvement_vs_baseline_percent"])
        >= MINIMUM_BASELINE_IMPROVEMENT_PERCENT
    ]
    if not eligible:
        raise DecisionError("No learned candidate meets the baseline threshold.")
    best_eligible_mae = min(float(row["mae_units"]) for row in eligible)
    practically_equivalent = [
        row
        for row in eligible
        if float(row["mae_units"])
        <= best_eligible_mae + PRACTICAL_EQUIVALENCE_UNITS
    ]
    selected = min(
        practically_equivalent,
        key=lambda row: COMPLEXITY_ORDER[row["model_id"]],
    )
    selected_error = summary_by_id[selected["model_id"]]
    leader_error = summary_by_id[measurement_leader["model_id"]]

    return {
        "schema_version": "1.0",
        "decision_status": "selected_for_next_integration",
        "dataset_sha256": comparison["dataset_sha256"],
        "split_strategy": comparison["split_strategy"],
        "target": comparison["target"],
        "target_unit": comparison["target_unit"],
        "measurement_leader": {
            "model_id": measurement_leader["model_id"],
            "model_name": measurement_leader["model_name"],
            "mae_units": measurement_leader["mae_units"],
            "rmse_units": measurement_leader["rmse_units"],
            "largest_observed_error_units": leader_error["largest_error"][
                "absolute_error"
            ],
        },
        "selected_candidate": {
            "model_id": selected["model_id"],
            "model_name": selected["model_name"],
            "mae_units": selected["mae_units"],
            "rmse_units": selected["rmse_units"],
            "r2_contextual": selected["r2_contextual"],
            "mae_improvement_vs_baseline_percent": selected[
                "mae_improvement_vs_baseline_percent"
            ],
            "complexity_order": COMPLEXITY_ORDER[selected["model_id"]],
            "largest_observed_error_units": selected_error["largest_error"][
                "absolute_error"
            ],
        },
        "measurement_leader_is_selected_candidate": (
            measurement_leader["model_id"] == selected["model_id"]
        ),
        "practically_equivalent_candidates": [
            {
                "model_id": row["model_id"],
                "model_name": row["model_name"],
                "mae_units": row["mae_units"],
                "complexity_order": COMPLEXITY_ORDER[row["model_id"]],
            }
            for row in sorted(
                practically_equivalent,
                key=lambda item: COMPLEXITY_ORDER[item["model_id"]],
            )
        ],
        "policy": {
            "primary_metric": "mae",
            "primary_metric_direction": "lower_is_better",
            "minimum_baseline_improvement_percent": (
                MINIMUM_BASELINE_IMPROVEMENT_PERCENT
            ),
            "practical_equivalence_units": PRACTICAL_EQUIVALENCE_UNITS,
            "tie_breaker": "lower_operational_and_explanation_complexity",
            "complexity_order": COMPLEXITY_ORDER,
        },
        "error_review": {
            "status": "reviewed",
            "role": "descriptive_diagnostic_not_causal_override",
            "selected_candidate_largest_error": selected_error["largest_error"],
            "measurement_leader_largest_error": leader_error["largest_error"],
        },
        "stability_evidence": {
            "status": "not_assessed",
            "reason": "single_fixed_chronological_holdout",
            "repeatability_is_not_stability": True,
        },
        "rationale": [
            "Gradient Boosting has the lowest observed MAE.",
            (
                "Random Forest and Gradient Boosting are within the frozen "
                "0.25-unit practical-equivalence tolerance."
            ),
            (
                "Random Forest has lower recorded complexity and is selected "
                "for the next integration step."
            ),
            (
                "Largest-error evidence was reviewed descriptively and does "
                "not replace the frozen selection rule."
            ),
        ],
        "production_status": "not_production_ready",
        "authorized_next_step": "week_7_platform_integration_after_week_6_close",
        "prohibited_claims": [
            "production readiness",
            "stability",
            "generalization to real retail operations",
            "inventory action",
        ],
    }


def _markdown_decision(decision: dict[str, Any]) -> str:
    leader = decision["measurement_leader"]
    selected = decision["selected_candidate"]
    equivalent = ", ".join(
        item["model_name"]
        for item in decision["practically_equivalent_candidates"]
    )
    rows = [
        "# Sprint 2 Model Selection Decision",
        "",
        "## Outcome",
        "",
        f"- Measurement leader: **{leader['model_name']}** "
        f"(MAE {leader['mae_units']:.4f} units).",
        f"- Candidate selected for next integration: "
        f"**{selected['model_name']}** "
        f"(MAE {selected['mae_units']:.4f} units).",
        f"- Practically equivalent candidates: {equivalent}.",
        "- Production status: **not production ready**.",
        "",
        "## Why the two outcomes differ",
        "",
        "Gradient Boosting has the lowest observed MAE. Random Forest is only",
        f"{selected['mae_units'] - leader['mae_units']:.4f} MAE units higher,",
        "inside the frozen 0.25-unit tolerance, and has lower recorded",
        "operational and explanation complexity. The Day 64 rule therefore",
        "selects Random Forest for the next integration step.",
        "",
        "## Error review",
        "",
        f"Random Forest's largest observed absolute error is "
        f"{selected['largest_observed_error_units']:.4f} units. Gradient",
        f"Boosting's is {leader['largest_observed_error_units']:.4f} units.",
        "These six-row observations are descriptive and do not establish",
        "causality or stability.",
        "",
        "## Limits",
        "",
        "- 18 synthetic observations and one six-row chronological holdout;",
        "- no cross-validation, external validation or hyperparameter search;",
        "- repeatability does not demonstrate stability;",
        "- selection authorizes only later platform integration, not deployment",
        "  or inventory action.",
        "",
    ]
    return "\n".join(rows)


def run_model_decision(project_root: Path) -> dict[str, Any]:
    """Generate official Day 67 JSON and Markdown decision artifacts."""
    output_root = project_root / "reports" / "outputs" / "model-comparison"
    comparison = json.loads(
        (output_root / "comparison_table.json").read_text(encoding="utf-8")
    )
    error_analysis = json.loads(
        (output_root / "error_analysis.json").read_text(encoding="utf-8")
    )
    decision = select_candidate(comparison, error_analysis)
    (output_root / "model_decision.json").write_text(
        json.dumps(decision, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output_root / "model_decision.md").write_text(
        _markdown_decision(decision),
        encoding="utf-8",
        newline="\n",
    )
    return decision


def main() -> None:
    """Generate official model selection evidence."""
    project_root = Path(__file__).resolve().parents[4]
    decision = run_model_decision(project_root)
    print(
        "Measurement leader: "
        f"{decision['measurement_leader']['model_name']}"
    )
    print(
        "Selected for next integration: "
        f"{decision['selected_candidate']['model_name']}"
    )
    print(f"Production status: {decision['production_status']}")


if __name__ == "__main__":
    main()
