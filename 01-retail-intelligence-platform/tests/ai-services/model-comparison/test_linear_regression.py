"""Tests for common preprocessing and the Linear Regression candidate."""

from __future__ import annotations

import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression

from model_comparison.candidate import evaluate_candidate
from model_comparison.preprocessing import build_preprocessor


def controlled_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sale_id": range(1, 9),
            "date": pd.date_range("2026-01-01", periods=8).astype(str),
            "product_id": ["P1", "P2", "P1", "P2", "P1", "P2", "P1", "P3"],
            "category": ["A", "B", "A", "B", "A", "B", "A", "C"],
            "unit_price": [1, 2, 1, 2, 1, 2, 1, 3],
            "day_of_week": [0, 1, 2, 3, 4, 5, 6, 0],
            "is_weekend": [False, False, False, False, False, True, True, False],
            "units_sold": [5, 8, 7, 10, 9, 12, 11, 14],
        }
    )


def manifest() -> dict[str, object]:
    return {
        "dataset_sha256": "b" * 64,
        "target": "units_sold",
        "target_unit": "units_per_sale_record",
        "split": {"strategy": "chronological_holdout"},
    }


def test_preprocessor_ignores_unseen_test_categories() -> None:
    data = controlled_frame()
    preprocessor = build_preprocessor()
    preprocessor.fit(data.iloc[:7])

    transformed = preprocessor.transform(data.iloc[7:])

    assert transformed.shape[0] == 1
    assert transformed.shape[1] > 5


def test_linear_candidate_uses_common_result_contract() -> None:
    data = controlled_frame()
    result, predictions = evaluate_candidate(
        model_id="linear_regression",
        model_name="Linear Regression",
        model_family="linear_model",
        estimator=LinearRegression(),
        estimator_parameters={"fit_intercept": True},
        train=data.iloc[:6],
        test=data.iloc[6:],
        manifest=manifest(),
    )

    assert result.model_id == "linear_regression"
    assert result.dataset_sha256 == "b" * 64
    assert result.configuration["preprocessing"]["fit_scope"] == (
        "training_partition_only"
    )
    assert len(predictions) == 2
    assert predictions["absolute_error"].ge(0).all()
    assert result.metrics.mae >= 0


def test_candidate_rejects_empty_training_partition() -> None:
    data = controlled_frame()

    with pytest.raises(ValueError, match="requires train and test"):
        evaluate_candidate(
            model_id="linear_regression",
            model_name="Linear Regression",
            model_family="linear_model",
            estimator=LinearRegression(),
            estimator_parameters={},
            train=data.iloc[:0],
            test=data.iloc[6:],
            manifest=manifest(),
        )
