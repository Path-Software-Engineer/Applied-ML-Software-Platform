import pandas as pd
import pytest

from src.baselines.baseline import (
    calculate_mae,
    calculate_mean_baseline,
    create_mean_baseline_predictions,
)
from src.features.feature_engineering import build_sales_features


def test_feature_engineering_preserves_rows_and_builds_expected_types() -> None:
    data = pd.DataFrame(
        {
            "date": ["2026-01-03", "2026-01-05"],
            "units_sold": [2, 3],
            "unit_price": [4.0, 5.0],
        }
    )
    featured = build_sales_features(data)
    assert len(featured) == len(data)
    assert featured["day_of_week"].tolist() == [5, 0]
    assert featured["is_weekend"].tolist() == [True, False]
    assert featured["revenue"].tolist() == [8.0, 15.0]
    assert pd.api.types.is_integer_dtype(featured["year"])


def test_mean_baseline_and_predictions() -> None:
    target = pd.Series([1, 2, 6])
    assert calculate_mean_baseline(target) == pytest.approx(3.0)
    assert create_mean_baseline_predictions(target).tolist() == [3.0] * 3


def test_mae_is_correct_and_non_negative() -> None:
    mae = calculate_mae(pd.Series([1, 3]), pd.Series([2, 5]))
    assert mae == pytest.approx(1.5)
    assert mae >= 0


def test_mae_rejects_incompatible_lengths() -> None:
    with pytest.raises(ValueError, match="same length"):
        calculate_mae(pd.Series([1]), pd.Series([1, 2]))
