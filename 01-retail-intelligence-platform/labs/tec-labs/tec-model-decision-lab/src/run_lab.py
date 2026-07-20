"""Controlled metric-leader versus engineering-choice experiment."""

from __future__ import annotations

from pathlib import Path

from model_comparison.decision import select_candidate


def main() -> None:
    """Generate a controlled decision-card lesson."""
    comparison = {
        "selection_status": "not_selected",
        "dataset_sha256": "controlled",
        "split_strategy": "controlled_holdout",
        "target": "controlled_target",
        "target_unit": "units",
        "rows": [
            {
                "model_id": "gradient_boosting",
                "model_name": "Gradient Boosting",
                "mae_units": 3.0,
                "rmse_units": 3.5,
                "r2_contextual": 0.4,
                "mae_improvement_vs_baseline_percent": 30.0,
            },
            {
                "model_id": "random_forest",
                "model_name": "Random Forest",
                "mae_units": 3.1,
                "rmse_units": 3.6,
                "r2_contextual": 0.3,
                "mae_improvement_vs_baseline_percent": 28.0,
            },
            {
                "model_id": "linear_regression",
                "model_name": "Linear Regression",
                "mae_units": 3.6,
                "rmse_units": 4.0,
                "r2_contextual": 0.2,
                "mae_improvement_vs_baseline_percent": 16.0,
            },
            {
                "model_id": "training_mean",
                "model_name": "Training Mean Baseline",
                "mae_units": 4.3,
                "rmse_units": 4.9,
                "r2_contextual": -0.1,
                "mae_improvement_vs_baseline_percent": 0.0,
            },
        ],
    }
    errors = {
        "interpretation_boundary": "descriptive_no_causal_claims",
        "candidate_summaries": [
            {
                "model_id": model_id,
                "largest_error": {"sale_id": 1, "absolute_error": 5.0},
            }
            for model_id in (
                "training_mean",
                "linear_regression",
                "random_forest",
                "gradient_boosting",
            )
        ],
    }
    decision = select_candidate(comparison, errors)
    output = Path(__file__).resolve().parents[1] / "outputs" / (
        "metric_leader_vs_selected_candidate.md"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "\n".join(
            [
                "# Metric Leader versus Selected Candidate",
                "",
                f"- Metric leader: {decision['measurement_leader']['model_name']}.",
                (
                    "- Selected candidate: "
                    f"{decision['selected_candidate']['model_name']}."
                ),
                "- Difference: 0.10 MAE units, inside the 0.25 tolerance.",
                "- Tie-breaker: lower recorded complexity.",
                "",
                "The lowest metric and engineering choice can differ when a",
                "decision policy defines practical equivalence before selection.",
                "",
                "These are controlled lab values, not official model results.",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Model-decision lab generated: {output}")


if __name__ == "__main__":
    main()
