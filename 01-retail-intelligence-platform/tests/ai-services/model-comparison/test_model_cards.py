"""Tests for evidence-backed Model Card generation."""

from __future__ import annotations

from copy import deepcopy

import pytest

from model_comparison.model_cards import ModelCardError, build_model_cards


MODEL_IDS = (
    "training_mean",
    "linear_regression",
    "random_forest",
    "gradient_boosting",
)


def results() -> list[dict[str, object]]:
    return [
        {
            "model_id": model_id,
            "model_name": model_id.replace("_", " ").title(),
            "model_family": "controlled",
            "dataset_sha256": "3" * 64,
            "split_strategy": "chronological_holdout",
            "target": "units_sold",
            "target_unit": "units_per_sale_record",
            "train_rows": 12,
            "test_rows": 6,
            "configuration": (
                {"strategy": "mean"}
                if model_id == "training_mean"
                else {
                    "estimator_parameters": {"random_state": 42},
                    "preprocessing": {"fit_scope": "training_partition_only"},
                }
            ),
        }
        for model_id in MODEL_IDS
    ]


def comparison() -> dict[str, object]:
    return {
        "rows": [
            {
                "model_id": model_id,
                "mae_units": 3.0 + index,
                "mae_rank": index + 1,
                "rmse_units": 4.0 + index,
                "r2_contextual": 0.2,
                "mae_improvement_vs_baseline_percent": 20.0,
                "within_practical_equivalence": model_id
                in {"random_forest", "gradient_boosting"},
            }
            for index, model_id in enumerate(MODEL_IDS)
        ]
    }


def errors() -> dict[str, object]:
    return {
        "candidate_summaries": [
            {
                "model_id": model_id,
                "mean_signed_residual": 0.1,
                "under_prediction_count": 3,
                "over_prediction_count": 3,
                "largest_error": {
                    "absolute_error": 5.0,
                    "date": "2026-01-09",
                    "product_name": "Bread",
                },
            }
            for model_id in MODEL_IDS
        ]
    }


def decision() -> dict[str, object]:
    return {
        "decision_status": "selected_for_next_integration",
        "selected_candidate": {"model_id": "random_forest"},
        "measurement_leader": {"model_id": "gradient_boosting"},
    }


def test_model_cards_cover_every_candidate_and_role() -> None:
    cards = build_model_cards(results(), comparison(), errors(), decision())
    roles = {card["model_id"]: card["decision_role"] for card in cards}

    assert len(cards) == 4
    assert roles["training_mean"] == "comparison_baseline"
    assert roles["random_forest"] == "selected_for_next_integration"
    assert roles["gradient_boosting"] == "measurement_leader_not_selected"


def test_model_cards_keep_common_limitations_and_status() -> None:
    cards = build_model_cards(results(), comparison(), errors(), decision())

    assert all(card["production_status"] == "not_production_ready" for card in cards)
    assert all(
        any("18 synthetic" in limitation for limitation in card["limitations"])
        for card in cards
    )


def test_model_cards_reject_incomplete_comparison_evidence() -> None:
    incomplete = deepcopy(comparison())
    incomplete["rows"] = incomplete["rows"][:-1]

    with pytest.raises(ModelCardError, match="four candidates"):
        build_model_cards(results(), incomplete, errors(), decision())
