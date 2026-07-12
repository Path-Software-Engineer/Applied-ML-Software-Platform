from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = PROJECT_ROOT / "ai-services" / "demand-insight"
sys.path.insert(0, str(MODULE_ROOT))

from src.analysis.temporal_sales_analysis import (  # noqa: E402
    build_daily_sales_summary,
    build_temporal_results,
    load_sales_data,
    save_daily_sales_summary,
)


@pytest.fixture
def sales_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2026-01-02", "2026-01-01", "2026-01-02", "2026-01-03"]
            ),
            "units_sold": [10, 20, 35, 5],
            "revenue": [30.00, 50.00, 69.30, 10.70],
        }
    )


def test_load_sales_data_validates_required_columns(tmp_path: Path) -> None:
    input_path = tmp_path / "invalid.csv"
    pd.DataFrame({"date": ["2026-01-01"]}).to_csv(input_path, index=False)

    with pytest.raises(ValueError, match="Missing required columns"):
        load_sales_data(input_path)


def test_load_sales_data_converts_date_to_datetime(tmp_path: Path) -> None:
    input_path = tmp_path / "sales.csv"
    pd.DataFrame(
        {"date": ["2026-01-01"], "units_sold": [2], "revenue": [9.50]}
    ).to_csv(input_path, index=False)

    loaded = load_sales_data(input_path)

    assert pd.api.types.is_datetime64_any_dtype(loaded["date"])


def test_daily_summary_is_unique_ordered_and_preserves_totals(
    sales_data: pd.DataFrame,
) -> None:
    summary = build_daily_sales_summary(sales_data)

    assert len(summary) == sales_data["date"].nunique()
    assert not summary["date"].duplicated().any()
    assert summary["date"].is_monotonic_increasing
    assert int(summary["total_units_sold"].sum()) == 70
    assert float(summary["total_revenue"].sum()) == pytest.approx(160.00)


def test_temporal_results_identify_leaders_and_shares(
    sales_data: pd.DataFrame,
) -> None:
    summary = build_daily_sales_summary(sales_data)
    results = build_temporal_results(summary)

    assert results["top_units_date"] == "2026-01-02"
    assert results["top_units_sold"] == 45
    assert results["top_revenue_date"] == "2026-01-02"
    assert results["top_revenue"] == pytest.approx(99.30)
    assert results["top_units_share"] == pytest.approx(64.29)
    assert results["top_revenue_share"] == pytest.approx(62.06)


def test_save_daily_sales_summary_uses_requested_path(
    sales_data: pd.DataFrame,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "daily_sales_summary.csv"
    summary = build_daily_sales_summary(sales_data)

    saved_path = save_daily_sales_summary(summary, output_path)

    assert saved_path == output_path
    assert output_path.exists()
    saved_data = pd.read_csv(output_path)
    assert saved_data["date"].tolist() == [
        "2026-01-01",
        "2026-01-02",
        "2026-01-03",
    ]
