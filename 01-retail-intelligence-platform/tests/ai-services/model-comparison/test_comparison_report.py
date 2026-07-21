"""Tests for the composite comparison report and Decision Cards."""

from __future__ import annotations

from copy import deepcopy

import pytest

from model_comparison.comparison_report import (
    ComparisonReportError,
    build_comparison_report,
)


def comparison() -> dict[str, object]:
    model_ids = (
        "gradient_boosting",
        "random_forest",
        "linear_regression",
        "training_mean",
    )
    return {
        "schema_version": "1.0",
        "dataset_sha256": "4" * 64,
        "split_strategy": "chronological_holdout",
        "target": "units_sold",
        "target_unit": "units_per_sale_record",
        "primary_metric": {"id": "mae", "unit": "units"},
        "diagnostic_metrics": {"rmse": {}, "r2": {}},
        "policy": {"practical_equivalence_units": 0.25},
        "rows": [
            {
                "model_id": model_id,
                "model_name": model_id.replace("_", " ").title(),
                "mae_rank": index + 1,
                "mae_units": 3.0 + index * 0.2,
                "rmse_units": 3.5 + index * 0.2,
                "r2_contextual": 0.4 - index * 0.1,
                "mae_improvement_vs_baseline_percent": 25 - index * 5,
                "train_rows": 12,
                "test_rows": 6,
            }
            for index, model_id in enumerate(model_ids)
        ],
    }


def errors() -> dict[str, object]:
    return {
        "prediction_rows": 24,
        "residual_definition": "actual_units - predicted_units",
        "interpretation_boundary": "descriptive_no_causal_claims",
        "candidate_summaries": [
            {"model_id": model_id, "largest_error": {"absolute_error": 5.0}}
            for model_id in (
                "gradient_boosting",
                "random_forest",
                "linear_regression",
                "training_mean",
            )
        ],
    }


def decision() -> dict[str, object]:
    return {
        "decision_status": "selected_for_next_integration",
        "dataset_sha256": "4" * 64,
        "measurement_leader": {
            "model_id": "gradient_boosting",
            "model_name": "Gradient Boosting",
            "mae_units": 3.0,
        },
        "selected_candidate": {
            "model_id": "random_forest",
            "model_name": "Random Forest",
            "mae_units": 3.2,
        },
        "production_status": "not_production_ready",
    }


def split_manifest() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "dataset_sha256": "4" * 64,
        "split": {
            "strategy": "chronological_holdout",
            "train_rows": 12,
            "test_rows": 6,
        },
    }


def test_report_builds_stable_decision_cards() -> None:
    report = build_comparison_report(
        comparison(), errors(), decision(), split_manifest()
    )

    assert report["schema_version"] == "1.0"
    assert len(report["decision_cards"]) == 3
    assert report["decision_cards"][1]["model_id"] == "random_forest"
    assert report["decision_cards"][2]["status"] == "not_production_ready"


def test_report_rejects_different_decision_dataset() -> None:
    invalid = deepcopy(decision())
    invalid["dataset_sha256"] = "5" * 64

    with pytest.raises(ComparisonReportError, match="datasets differ"):
        build_comparison_report(comparison(), errors(), invalid, split_manifest())


def test_report_rejects_missing_candidate_error_summary() -> None:
    invalid = deepcopy(errors())
    invalid["candidate_summaries"] = invalid["candidate_summaries"][:3]

    with pytest.raises(ComparisonReportError, match="four candidates"):
        build_comparison_report(comparison(), invalid, decision(), split_manifest())


def test_report_rejects_inconsistent_split_evidence() -> None:
    invalid = deepcopy(split_manifest())
    invalid["split"]["test_rows"] = 5

    with pytest.raises(ComparisonReportError, match="Split evidence conflicts"):
        build_comparison_report(comparison(), errors(), decision(), invalid)
