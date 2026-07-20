"""Isolated tests for the Model Comparison read service."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from backend.api.app.services.model_comparison_service import (
    ModelComparisonError,
    ModelComparisonService,
)


def make_report() -> dict[str, object]:
    model_specs = (
        ("gradient_boosting", "Gradient Boosting", "boosted_tree_ensemble"),
        ("random_forest", "Random Forest", "bagged_tree_ensemble"),
        ("linear_regression", "Linear Regression", "linear_model"),
        ("training_mean", "Training Mean Baseline", "constant_baseline"),
    )
    candidates = []
    for rank, (model_id, name, family) in enumerate(model_specs, start=1):
        candidates.append(
            {
                "model_id": model_id,
                "model_name": name,
                "model_family": family,
                "mae_units": 3.0 + rank / 10,
                "rmse_units": 3.5 + rank / 10,
                "r2_contextual": 0.5 - rank / 10,
                "test_rows": 6,
                "production_status": "learning_evidence_only",
                "mae_rank": rank,
                "mae_delta_vs_baseline_units": 1.0,
                "mae_improvement_vs_baseline_percent": 20.0,
                "within_practical_equivalence": rank <= 2,
                "meets_minimum_baseline_improvement": rank <= 3,
            }
        )
    cards = []
    for card_id, model_id, title in (
        ("metric-leader", "gradient_boosting", "Gradient Boosting"),
        ("integration-candidate", "random_forest", "Random Forest"),
        ("evidence-boundary", None, "Learning evidence only"),
    ):
        cards.append(
            {
                "card_id": card_id,
                "eyebrow": "Evidence",
                "title": title,
                "status": "not_production_ready",
                "model_id": model_id,
                "primary_metric": {
                    "label": "MAE",
                    "value": 3.2,
                    "unit": "units",
                    "direction": "lower_is_better",
                },
                "summary": "Controlled evidence.",
                "reasons": ["Controlled reason."],
                "limitation": "Controlled limitation.",
            }
        )
    return {
        "schema_version": "1.0",
        "module": "model_comparison",
        "report_status": "learning_evidence_only",
        "experiment": {
            "dataset_sha256": "a" * 64,
            "split_strategy": "chronological_holdout",
            "target": "units_sold",
            "target_unit": "units_per_sale_record",
            "train_rows": 12,
            "test_rows": 6,
        },
        "comparison": {
            "primary_metric": {},
            "diagnostic_metrics": {},
            "policy": {},
            "rows": candidates,
        },
        "error_review": {},
        "decision": {
            "dataset_sha256": "a" * 64,
            "decision_status": "selected_for_next_integration",
            "production_status": "not_production_ready",
            "measurement_leader": {
                "model_id": "gradient_boosting",
                "model_name": "Gradient Boosting",
                "mae_units": 3.1,
            },
            "selected_candidate": {
                "model_id": "random_forest",
                "model_name": "Random Forest",
                "mae_units": 3.2,
                "mae_improvement_vs_baseline_percent": 20.0,
                "largest_observed_error_units": 4.5,
            },
            "policy": {"practical_equivalence_units": 0.25},
            "stability_evidence": {"status": "not_assessed"},
            "rationale": ["Controlled rationale."],
        },
        "decision_cards": cards,
        "limitations": ["one", "two", "three", "four"],
    }


def write_report(project_root: Path, payload: dict[str, object]) -> None:
    path = (
        project_root
        / "reports"
        / "outputs"
        / "model-comparison"
        / "model_comparison_report.json"
    )
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_service_returns_stable_read_resource(tmp_path: Path) -> None:
    write_report(tmp_path, make_report())

    summary = ModelComparisonService(tmp_path).get_summary()

    assert summary["schema_version"] == "1.0"
    assert len(summary["candidates"]) == 4
    assert len(summary["decision_cards"]) == 3
    assert summary["decision"]["selected_candidate"]["model_id"] == "random_forest"
    assert "comparison" not in summary


def test_service_rejects_missing_report(tmp_path: Path) -> None:
    with pytest.raises(ModelComparisonError, match="missing"):
        ModelComparisonService(tmp_path).get_summary()


def test_service_rejects_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "reports/outputs/model-comparison/model_comparison_report.json"
    path.parent.mkdir(parents=True)
    path.write_text("{broken", encoding="utf-8")

    with pytest.raises(ModelComparisonError, match="cannot be read"):
        ModelComparisonService(tmp_path).get_summary()


def test_service_rejects_unsupported_version(tmp_path: Path) -> None:
    report = make_report()
    report["schema_version"] = "2.0"
    write_report(tmp_path, report)

    with pytest.raises(ModelComparisonError, match="identity"):
        ModelComparisonService(tmp_path).get_summary()


def test_service_rejects_inconsistent_selected_metric(tmp_path: Path) -> None:
    report = make_report()
    report["decision"]["selected_candidate"]["mae_units"] = 99.0
    write_report(tmp_path, report)

    with pytest.raises(ModelComparisonError, match="metric is inconsistent"):
        ModelComparisonService(tmp_path).get_summary()


def test_service_rejects_duplicate_decision_card(tmp_path: Path) -> None:
    report = make_report()
    duplicate = deepcopy(report["decision_cards"][0])
    report["decision_cards"][2] = duplicate
    write_report(tmp_path, report)

    with pytest.raises(ModelComparisonError, match="identifiers"):
        ModelComparisonService(tmp_path).get_summary()
