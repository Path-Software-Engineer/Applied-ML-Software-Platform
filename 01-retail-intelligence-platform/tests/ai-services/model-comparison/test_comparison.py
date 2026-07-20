"""Tests for initial result consolidation and comparability guards."""

from __future__ import annotations

from copy import deepcopy

import pytest

from model_comparison.comparison import (
    ComparisonError,
    build_initial_results,
    validate_comparability,
)


def candidate(model_id: str) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "model_id": model_id,
        "model_name": model_id.replace("_", " ").title(),
        "model_family": "controlled",
        "dataset_sha256": "e" * 64,
        "split_strategy": "chronological_holdout",
        "target": "units_sold",
        "target_unit": "units_per_sale_record",
        "train_rows": 12,
        "test_rows": 6,
        "metrics": {"mae": 2.0, "rmse": 3.0, "r2": 0.1},
        "production_status": "learning_evidence_only",
    }


def candidates() -> list[dict[str, object]]:
    return [
        candidate("training_mean"),
        candidate("linear_regression"),
        candidate("random_forest"),
        candidate("gradient_boosting"),
    ]


def test_initial_results_preserve_stable_candidate_order() -> None:
    table = build_initial_results(candidates())

    assert table["model_id"].tolist() == [
        "training_mean",
        "linear_regression",
        "random_forest",
        "gradient_boosting",
    ]
    assert "rank" not in table.columns


def test_comparison_rejects_different_dataset_checksum() -> None:
    evidence = deepcopy(candidates())
    evidence[2]["dataset_sha256"] = "f" * 64

    with pytest.raises(ComparisonError, match="dataset_sha256"):
        validate_comparability(evidence)


def test_comparison_requires_all_four_candidates() -> None:
    with pytest.raises(ComparisonError, match="Exactly four"):
        validate_comparability(candidates()[:3])
