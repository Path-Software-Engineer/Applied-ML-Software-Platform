"""Generate evidence-backed Model Cards for every Sprint 2 candidate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .comparison import CANDIDATE_IDS, load_candidate_results


MODEL_CONTEXT = {
    "training_mean": {
        "purpose": (
            "Provide a transparent reference that predicts the mean training "
            "target for every test observation."
        ),
        "observed_strengths": [
            "Creates a minimum comparison reference with no learned feature use.",
            "Configuration and prediction behavior are directly explainable.",
        ],
        "model_specific_limitations": [
            "Cannot represent product, category, price or temporal differences.",
            "Uses one constant prediction for every observation.",
        ],
        "risks": [
            "May underfit structured demand variation.",
            "A simple reference must not be presented as a deployment candidate.",
        ],
    },
    "linear_regression": {
        "purpose": (
            "Test whether one transparent linear relationship over the shared "
            "encoded features improves the training-mean reference."
        ),
        "observed_strengths": [
            "Improves observed MAE over the baseline on the fixed holdout.",
            "Has the lowest recorded complexity among learned candidates.",
        ],
        "model_specific_limitations": [
            "Represents additive linear relationships after preprocessing.",
            "Was evaluated with one fixed configuration and no tuning.",
        ],
        "risks": [
            "Linear assumptions may miss interactions in future data.",
            "Coefficients are not stable or generalizable from 12 training rows.",
        ],
    },
    "random_forest": {
        "purpose": (
            "Test a bounded bagged-tree ensemble that can represent nonlinear "
            "feature interactions under a reproducible seed."
        ),
        "observed_strengths": [
            "Falls inside the best candidate's practical-equivalence tolerance.",
            "Improves observed MAE over the baseline by more than 10%.",
            "Has lower recorded complexity than the equivalent boosted ensemble.",
        ],
        "model_specific_limitations": [
            "Uses a fixed, untuned 200-tree configuration.",
            "Feature effects are less direct than in Linear Regression.",
        ],
        "risks": [
            "A tree ensemble can still overfit a 12-row training partition.",
            "Selection for integration does not establish production readiness.",
        ],
    },
    "gradient_boosting": {
        "purpose": (
            "Test a bounded sequential tree ensemble as the third learned "
            "candidate under the common comparison contract."
        ),
        "observed_strengths": [
            "Has the lowest observed MAE and RMSE in the fixed holdout.",
            "Improves observed MAE over the baseline by more than 10%.",
        ],
        "model_specific_limitations": [
            "Uses a fixed configuration without hyperparameter search.",
            "Sequential boosting has higher recorded explanation complexity.",
        ],
        "risks": [
            "Small-sample metric leadership may not persist on new data.",
            "The lowest observed metric is not evidence of production readiness.",
        ],
    },
}

COMMON_LIMITATIONS = [
    "18 synthetic observations with 12 training and 6 test rows.",
    "One chronological holdout and no cross-validation or external validation.",
    "No stability, confidence interval or real-retail generalization evidence.",
    "No model authorizes forecasting, inventory action or production deployment.",
]


class ModelCardError(ValueError):
    """Raised when card evidence is incomplete or inconsistent."""


def build_model_cards(
    results: list[dict[str, Any]],
    comparison: dict[str, Any],
    error_analysis: dict[str, Any],
    decision: dict[str, Any],
) -> list[dict[str, Any]]:
    """Combine metrics, errors and decision roles into four Model Cards."""
    result_by_id = {result["model_id"]: result for result in results}
    comparison_rows = {
        row["model_id"]: row for row in comparison.get("rows", [])
    }
    error_summaries = {
        summary["model_id"]: summary
        for summary in error_analysis.get("candidate_summaries", [])
    }
    expected = set(CANDIDATE_IDS)
    if (
        set(result_by_id) != expected
        or set(comparison_rows) != expected
        or set(error_summaries) != expected
    ):
        raise ModelCardError("Model Card evidence must cover four candidates.")
    if decision.get("decision_status") != "selected_for_next_integration":
        raise ModelCardError("A completed model decision is required.")

    selected_id = decision["selected_candidate"]["model_id"]
    leader_id = decision["measurement_leader"]["model_id"]
    cards = []
    for model_id in CANDIDATE_IDS:
        result = result_by_id[model_id]
        comparison_row = comparison_rows[model_id]
        error_summary = error_summaries[model_id]
        context = MODEL_CONTEXT[model_id]
        if model_id == selected_id:
            decision_role = "selected_for_next_integration"
        elif model_id == leader_id:
            decision_role = "measurement_leader_not_selected"
        elif model_id == "training_mean":
            decision_role = "comparison_baseline"
        else:
            decision_role = "evaluated_candidate"

        cards.append(
            {
                "schema_version": "1.0",
                "model_id": model_id,
                "model_name": result["model_name"],
                "model_family": result["model_family"],
                "purpose": context["purpose"],
                "experiment": {
                    "dataset_sha256": result["dataset_sha256"],
                    "split_strategy": result["split_strategy"],
                    "target": result["target"],
                    "target_unit": result["target_unit"],
                    "train_rows": result["train_rows"],
                    "test_rows": result["test_rows"],
                },
                "configuration": result["configuration"],
                "observed_performance": {
                    "mae_units": comparison_row["mae_units"],
                    "mae_rank": comparison_row["mae_rank"],
                    "rmse_units": comparison_row["rmse_units"],
                    "r2_contextual": comparison_row["r2_contextual"],
                    "mae_improvement_vs_baseline_percent": comparison_row[
                        "mae_improvement_vs_baseline_percent"
                    ],
                    "within_practical_equivalence": comparison_row[
                        "within_practical_equivalence"
                    ],
                },
                "observed_error_profile": {
                    "mean_signed_residual": error_summary[
                        "mean_signed_residual"
                    ],
                    "under_prediction_count": error_summary[
                        "under_prediction_count"
                    ],
                    "over_prediction_count": error_summary[
                        "over_prediction_count"
                    ],
                    "largest_error": error_summary["largest_error"],
                    "interpretation_boundary": (
                        "observed_six_row_holdout_no_causal_claims"
                    ),
                },
                "decision_role": decision_role,
                "observed_strengths": context["observed_strengths"],
                "limitations": [
                    *context["model_specific_limitations"],
                    *COMMON_LIMITATIONS,
                ],
                "risks": context["risks"],
                "production_status": "not_production_ready",
                "evidence": [
                    (
                        "reports/outputs/model-comparison/results/"
                        f"{model_id}.json"
                    ),
                    (
                        "reports/outputs/model-comparison/predictions/"
                        f"{model_id}.csv"
                    ),
                    "reports/outputs/model-comparison/comparison_table.json",
                    "reports/outputs/model-comparison/error_analysis.json",
                    "reports/outputs/model-comparison/model_decision.json",
                ],
            }
        )
    return cards


def _configuration_lines(configuration: dict[str, Any]) -> list[str]:
    if "strategy" in configuration:
        return [f"- Strategy: `{configuration['strategy']}`."]
    parameters = configuration.get("estimator_parameters", {})
    lines = [
        f"- `{name}`: `{value}`."
        for name, value in parameters.items()
    ]
    preprocessing = configuration.get("preprocessing")
    if isinstance(preprocessing, dict):
        lines.extend(
            [
                "- Categorical preprocessing: one-hot encoding.",
                "- Numeric preprocessing: standard scaling.",
                "- Preprocessing fit scope: training partition only.",
            ]
        )
    return lines


def _markdown_card(card: dict[str, Any]) -> str:
    performance = card["observed_performance"]
    errors = card["observed_error_profile"]
    largest = errors["largest_error"]
    rows = [
        f"# Model Card — {card['model_name']}",
        "",
        f"- **Model ID:** `{card['model_id']}`",
        f"- **Family:** `{card['model_family']}`",
        f"- **Decision role:** `{card['decision_role']}`",
        f"- **Production status:** `{card['production_status']}`",
        "",
        "## Purpose",
        "",
        card["purpose"],
        "",
        "## Experiment boundary",
        "",
        f"- Target: `{card['experiment']['target']}` "
        f"({card['experiment']['target_unit']}).",
        f"- Split: `{card['experiment']['split_strategy']}` with "
        f"{card['experiment']['train_rows']} train and "
        f"{card['experiment']['test_rows']} test rows.",
        f"- Dataset SHA-256: `{card['experiment']['dataset_sha256']}`.",
        "",
        "## Configuration",
        "",
        *_configuration_lines(card["configuration"]),
        "",
        "## Observed performance",
        "",
        f"- MAE: {performance['mae_units']:.4f} units "
        f"(rank {performance['mae_rank']}).",
        f"- RMSE: {performance['rmse_units']:.4f} units.",
        f"- R²: {performance['r2_contextual']:.4f}, contextual only.",
        f"- MAE improvement versus baseline: "
        f"{performance['mae_improvement_vs_baseline_percent']:.2f}%.",
        f"- Inside practical-equivalence tolerance: "
        f"{'yes' if performance['within_practical_equivalence'] else 'no'}.",
        "",
        "## Observed error profile",
        "",
        f"- Mean signed residual: {errors['mean_signed_residual']:+.4f}.",
        f"- Under-/over-predictions: {errors['under_prediction_count']}/"
        f"{errors['over_prediction_count']}.",
        f"- Largest absolute error: {largest['absolute_error']:.4f} units on "
        f"{largest['date']} for {largest['product_name']}.",
        "- Interpretation: six-row descriptive evidence, no causal claim.",
        "",
        "## Observed strengths",
        "",
        *[f"- {item}" for item in card["observed_strengths"]],
        "",
        "## Limitations",
        "",
        *[f"- {item}" for item in card["limitations"]],
        "",
        "## Risks",
        "",
        *[f"- {item}" for item in card["risks"]],
        "",
        "## Evidence",
        "",
        *[f"- `{item}`" for item in card["evidence"]],
        "",
    ]
    return "\n".join(rows)


def _index_markdown(cards: list[dict[str, Any]]) -> str:
    rows = [
        "# Sprint 2 Model Cards",
        "",
        "| Candidate | MAE rank | Decision role | Production status |",
        "|---|---:|---|---|",
    ]
    for card in cards:
        rows.append(
            f"| [{card['model_name']}](./{card['model_id']}.md) | "
            f"{card['observed_performance']['mae_rank']} | "
            f"`{card['decision_role']}` | "
            f"`{card['production_status']}` |"
        )
    rows.extend(
        [
            "",
            "These cards describe evidence from 18 synthetic observations and",
            "one six-row holdout. They do not establish stability,",
            "generalization or production readiness.",
            "",
            "Random Forest is selected only for the next integration step.",
            "The Week 6 technical report and Decision Cards are not part of Day 68.",
            "",
        ]
    )
    return "\n".join(rows)


def run_model_cards(project_root: Path) -> list[dict[str, Any]]:
    """Generate official Day 68 JSON and per-candidate Markdown cards."""
    output_root = project_root / "reports" / "outputs" / "model-comparison"
    card_root = project_root / "reports" / "model-cards" / "model-comparison"
    results = load_candidate_results(output_root / "results")
    comparison = json.loads(
        (output_root / "comparison_table.json").read_text(encoding="utf-8")
    )
    errors = json.loads(
        (output_root / "error_analysis.json").read_text(encoding="utf-8")
    )
    decision = json.loads(
        (output_root / "model_decision.json").read_text(encoding="utf-8")
    )
    cards = build_model_cards(results, comparison, errors, decision)
    card_root.mkdir(parents=True, exist_ok=True)
    (card_root / "model_cards.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "card_count": len(cards),
                "production_status": "not_production_ready",
                "cards": cards,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    for card in cards:
        (card_root / f"{card['model_id']}.md").write_text(
            _markdown_card(card),
            encoding="utf-8",
            newline="\n",
        )
    (card_root / "README.md").write_text(
        _index_markdown(cards),
        encoding="utf-8",
        newline="\n",
    )
    return cards


def main() -> None:
    """Generate official Model Cards."""
    project_root = Path(__file__).resolve().parents[4]
    cards = run_model_cards(project_root)
    print(f"Model Cards generated: {len(cards)}")
    for card in cards:
        print(f"{card['model_name']}: {card['decision_role']}")
    print("Production status: not_production_ready")


if __name__ == "__main__":
    main()
