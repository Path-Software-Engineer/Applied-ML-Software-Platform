"""Tests for baseline-relative metric comparison."""

from __future__ import annotations

import pytest

from model_comparison.comparison_table import build_comparison_table


def candidate(model_id: str, mae: float, rmse: float) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "model_id": model_id,
        "model_name": model_id.replace("_", " ").title(),
        "model_family": "controlled",
        "dataset_sha256": "1" * 64,
        "split_strategy": "chronological_holdout",
        "target": "units_sold",
        "target_unit": "units_per_sale_record",
        "train_rows": 12,
        "test_rows": 6,
        "metrics": {"mae": mae, "rmse": rmse, "r2": 0.2},
        "production_status": "learning_evidence_only",
    }


def evidence() -> list[dict[str, object]]:
    return [
        candidate("training_mean", 5.0, 6.0),
        candidate("linear_regression", 4.0, 5.0),
        candidate("random_forest", 3.1, 4.0),
        candidate("gradient_boosting", 3.0, 3.8),
    ]


def test_comparison_table_ranks_mae_and_calculates_improvement() -> None:
    table = build_comparison_table(evidence())

    assert table.iloc[0]["model_id"] == "gradient_boosting"
    assert table.iloc[0]["mae_rank"] == 1
    assert table.iloc[0]["mae_improvement_vs_baseline_percent"] == pytest.approx(
        40.0
    )
    assert table.iloc[-1]["model_id"] == "training_mean"


def test_comparison_table_marks_practical_equivalence() -> None:
    table = build_comparison_table(evidence())
    equivalent = set(
        table.loc[table["within_practical_equivalence"], "model_id"].tolist()
    )

    assert equivalent == {"random_forest", "gradient_boosting"}


def test_comparison_table_requires_baseline() -> None:
    without_baseline = [
        candidate("extra_model", 4.5, 5.5),
        *evidence()[1:],
    ]

    with pytest.raises(ValueError, match="baseline"):
        build_comparison_table(without_baseline)
