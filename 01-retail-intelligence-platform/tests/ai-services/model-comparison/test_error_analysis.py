"""Tests for residual validation and descriptive error summaries."""

from __future__ import annotations

import pandas as pd
import pytest

from model_comparison.error_analysis import (
    ErrorAnalysisError,
    build_error_analysis,
    summarize_errors,
)


def controlled_test_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sale_id": [1, 2],
            "date": ["2026-01-07", "2026-01-08"],
            "product_id": ["P1", "P2"],
            "product_name": ["Bread", "Milk"],
            "category": ["Food", "Dairy"],
            "units_sold": [10.0, 14.0],
        }
    )


def predictions() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sale_id": [1, 2],
            "date": ["2026-01-07", "2026-01-08"],
            "actual_units": [10.0, 14.0],
            "predicted_units": [8.0, 16.0],
            "residual": [2.0, -2.0],
            "absolute_error": [2.0, 2.0],
        }
    )


def test_error_analysis_enriches_residual_direction() -> None:
    analysis = build_error_analysis(
        {"model": predictions()},
        controlled_test_data(),
        {"model": "Controlled Model"},
    )

    assert analysis["error_direction"].tolist() == [
        "under_prediction",
        "over_prediction",
    ]
    assert analysis["product_name"].tolist() == ["Bread", "Milk"]
    assert analysis["squared_error"].tolist() == [4.0, 4.0]


def test_error_summary_records_largest_observation() -> None:
    analysis = build_error_analysis(
        {"model": predictions()},
        controlled_test_data(),
        {"model": "Controlled Model"},
    )
    summary = summarize_errors(analysis)[0]

    assert summary["under_prediction_count"] == 1
    assert summary["over_prediction_count"] == 1
    assert summary["largest_error"]["sale_id"] == 1
    assert "no causal" in summary["interpretation"]


def test_error_analysis_rejects_invalid_residual() -> None:
    invalid = predictions()
    invalid.loc[0, "residual"] = 99

    with pytest.raises(ErrorAnalysisError, match="residual"):
        build_error_analysis(
            {"model": invalid},
            controlled_test_data(),
            {"model": "Controlled Model"},
        )
