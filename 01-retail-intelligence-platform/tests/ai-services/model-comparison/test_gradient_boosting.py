"""Tests for the reproducible Gradient Boosting candidate."""

from __future__ import annotations

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

from model_comparison.candidate import evaluate_candidate
from model_comparison.gradient_boosting import MODEL_PARAMETERS


def controlled_frame() -> pd.DataFrame:
    rows = 14
    return pd.DataFrame(
        {
            "sale_id": range(1, rows + 1),
            "date": pd.date_range("2026-01-01", periods=rows).astype(str),
            "product_id": ["P1", "P2"] * 7,
            "category": ["A", "B"] * 7,
            "unit_price": [1.0, 2.0] * 7,
            "day_of_week": [index % 7 for index in range(rows)],
            "is_weekend": [index % 7 in (5, 6) for index in range(rows)],
            "units_sold": [6 + index + (index % 3) for index in range(rows)],
        }
    )


def manifest() -> dict[str, object]:
    return {
        "dataset_sha256": "d" * 64,
        "target": "units_sold",
        "target_unit": "units_per_sale_record",
        "split": {"strategy": "chronological_holdout"},
    }


def evaluate_once() -> tuple[object, pd.DataFrame]:
    data = controlled_frame()
    return evaluate_candidate(
        model_id="gradient_boosting",
        model_name="Gradient Boosting",
        model_family="boosted_tree_ensemble",
        estimator=GradientBoostingRegressor(**MODEL_PARAMETERS),
        estimator_parameters=MODEL_PARAMETERS,
        train=data.iloc[:10],
        test=data.iloc[10:],
        manifest=manifest(),
    )


def test_gradient_boosting_records_bounded_configuration() -> None:
    result, predictions = evaluate_once()

    parameters = result.configuration["estimator_parameters"]
    assert parameters["random_state"] == 42
    assert parameters["learning_rate"] == 0.05
    assert parameters["max_depth"] == 2
    assert len(predictions) == 4


def test_gradient_boosting_is_reproducible() -> None:
    first_result, first_predictions = evaluate_once()
    second_result, second_predictions = evaluate_once()

    assert first_result.metrics == second_result.metrics
    assert first_predictions["predicted_units"].tolist() == (
        second_predictions["predicted_units"].tolist()
    )
