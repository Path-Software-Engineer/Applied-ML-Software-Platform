"""Tests for shared metrics and the training-mean baseline."""

from __future__ import annotations

import pandas as pd
import pytest

from model_comparison.baseline import evaluate_training_mean_baseline
from model_comparison.metrics import MetricError, calculate_regression_metrics


def manifest() -> dict[str, object]:
    return {
        "dataset_sha256": "a" * 64,
        "target": "units_sold",
        "target_unit": "units_per_sale_record",
        "split": {"strategy": "chronological_holdout"},
    }


def test_regression_metrics_match_known_values() -> None:
    metrics = calculate_regression_metrics([1, 3], [2, 5])

    assert metrics.mae == pytest.approx(1.5)
    assert metrics.rmse == pytest.approx((5 / 2) ** 0.5)
    assert metrics.r2 == pytest.approx(-1.5)


def test_r2_is_none_for_constant_actual_values() -> None:
    metrics = calculate_regression_metrics([2, 2], [2, 3])

    assert metrics.r2 is None
    assert metrics.mae == pytest.approx(0.5)


def test_metrics_reject_incompatible_shapes() -> None:
    with pytest.raises(MetricError, match="same shape"):
        calculate_regression_metrics([1, 2], [1])


def test_baseline_uses_only_training_targets() -> None:
    train = pd.DataFrame({"units_sold": [10, 20]})
    test = pd.DataFrame(
        {
            "sale_id": [3, 4],
            "date": ["2026-01-07", "2026-01-08"],
            "units_sold": [100, 200],
        }
    )

    result, predictions = evaluate_training_mean_baseline(train, test, manifest())

    assert predictions["predicted_units"].tolist() == [15.0, 15.0]
    assert result.configuration["strategy"] == "mean_of_training_target"
    assert result.test_rows == 2


def test_prediction_evidence_contains_residual_and_absolute_error() -> None:
    train = pd.DataFrame({"units_sold": [10, 20]})
    test = pd.DataFrame(
        {
            "sale_id": [3],
            "date": ["2026-01-07"],
            "units_sold": [18],
        }
    )

    _, predictions = evaluate_training_mean_baseline(train, test, manifest())

    assert predictions.loc[0, "residual"] == pytest.approx(3.0)
    assert predictions.loc[0, "absolute_error"] == pytest.approx(3.0)
