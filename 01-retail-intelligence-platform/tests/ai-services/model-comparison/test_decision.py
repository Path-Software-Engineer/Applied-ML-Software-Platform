"""Tests for the frozen metric-to-decision policy."""

from __future__ import annotations

from copy import deepcopy

import pytest

from model_comparison.decision import DecisionError, select_candidate


def comparison() -> dict[str, object]:
    rows = [
        ("gradient_boosting", "Gradient Boosting", 3.0, 3.5, 30.0),
        ("random_forest", "Random Forest", 3.1, 3.6, 28.0),
        ("linear_regression", "Linear Regression", 3.6, 4.0, 16.0),
        ("training_mean", "Training Mean Baseline", 4.3, 4.9, 0.0),
    ]
    return {
        "selection_status": "not_selected",
        "dataset_sha256": "2" * 64,
        "split_strategy": "chronological_holdout",
        "target": "units_sold",
        "target_unit": "units_per_sale_record",
        "rows": [
            {
                "model_id": model_id,
                "model_name": name,
                "mae_units": mae,
                "rmse_units": rmse,
                "r2_contextual": 0.3,
                "mae_improvement_vs_baseline_percent": improvement,
            }
            for model_id, name, mae, rmse, improvement in rows
        ],
    }


def errors() -> dict[str, object]:
    return {
        "interpretation_boundary": "descriptive_no_causal_claims",
        "candidate_summaries": [
            {
                "model_id": model_id,
                "largest_error": {
                    "sale_id": index,
                    "absolute_error": float(index + 1),
                },
            }
            for index, model_id in enumerate(
                [
                    "training_mean",
                    "linear_regression",
                    "random_forest",
                    "gradient_boosting",
                ],
                start=1,
            )
        ],
    }


def test_decision_separates_metric_leader_from_selected_candidate() -> None:
    decision = select_candidate(comparison(), errors())

    assert decision["measurement_leader"]["model_id"] == "gradient_boosting"
    assert decision["selected_candidate"]["model_id"] == "random_forest"
    assert not decision["measurement_leader_is_selected_candidate"]


def test_decision_rejects_candidates_below_baseline_threshold() -> None:
    evidence = comparison()
    for row in evidence["rows"]:
        if row["model_id"] != "training_mean":
            row["mae_improvement_vs_baseline_percent"] = 5.0

    with pytest.raises(DecisionError, match="threshold"):
        select_candidate(evidence, errors())


def test_decision_requires_preselection_table() -> None:
    evidence = deepcopy(comparison())
    evidence["selection_status"] = "selected"

    with pytest.raises(DecisionError, match="precede formal selection"):
        select_candidate(evidence, errors())
