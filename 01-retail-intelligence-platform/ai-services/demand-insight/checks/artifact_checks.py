"""Reusable manual validations for existing Demand Insight artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.analysis.product_ranking import (  # noqa: E402
    PRODUCT_SUMMARY_PATH,
    REVENUE_RANKING_PATH,
    UNITS_RANKING_PATH,
    build_product_summary,
    build_revenue_ranking,
    build_units_ranking,
    load_sales_data as load_ranking_data,
)
from src.baselines.baseline import (  # noqa: E402
    calculate_mae,
    calculate_mean_baseline,
    create_mean_baseline_predictions,
)
from src.data.data_cleaner import (  # noqa: E402
    REQUIRED_COLUMNS,
    run_data_cleaning_pipeline,
)
from src.data.data_loader import load_sales_data, validate_required_columns  # noqa: E402
from src.features.feature_engineering import (  # noqa: E402
    add_date_features,
    add_revenue_column,
    build_sales_features,
)

RAW = PROJECT_ROOT / "data/raw/demand-insight/sales.csv"
PROCESSED = PROJECT_ROOT / "data/processed/demand-insight"
REPORTS = PROJECT_ROOT / "reports/summaries/demand-insight"


def require_files(*paths: Path) -> None:
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise AssertionError(f"Missing expected evidence: {missing}")


def check_data_loading() -> None:
    data = load_sales_data(RAW)
    missing = validate_required_columns(data, REQUIRED_COLUMNS)
    if missing:
        raise AssertionError(f"Missing required columns: {missing}")
    require_files(REPORTS / "data_loading_summary.md")
    print(f"OK - data loading: {len(data)} rows, {len(data.columns)} columns")


def check_data_cleaning() -> None:
    output = PROCESSED / "sales_clean.csv"
    report = REPORTS / "data_cleaning_summary.md"
    expected = run_data_cleaning_pipeline(RAW, output, report)
    require_files(output, report)
    actual = pd.read_csv(output)
    if len(actual) != len(expected) or actual[REQUIRED_COLUMNS].isna().any().any():
        raise AssertionError("Clean artifact does not match the production cleaning contract.")
    if actual.duplicated().any() or (actual[["units_sold", "unit_price"]] < 0).any().any():
        raise AssertionError("Clean artifact contains invalid rows.")
    print(f"OK - data cleaning: {len(actual)} valid rows")


def _input() -> tuple[Path, pd.DataFrame]:
    for name in ("sales_pipeline_ready.csv", "sales_clean.csv"):
        path = PROCESSED / name
        if path.exists():
            return path, pd.read_csv(path)
    raise FileNotFoundError("No processed input dataset found.")


def check_temporal_features() -> None:
    _, data = _input()
    expected = add_date_features(data)
    output = PROCESSED / "sales_temporal_features.csv"
    require_files(output, REPORTS / "temporal_features_summary.md")
    actual = pd.read_csv(output)
    required = {"day_of_week", "month", "year", "is_weekend"}
    if len(actual) != len(expected) or not required.issubset(actual.columns):
        raise AssertionError("Temporal feature artifact violates its contract.")
    print(f"OK - temporal features: {len(actual)} rows")


def check_revenue() -> None:
    source = PROCESSED / "sales_temporal_features.csv"
    data = pd.read_csv(source) if source.exists() else _input()[1]
    expected = add_revenue_column(data)
    output = PROCESSED / "sales_revenue.csv"
    require_files(output, REPORTS / "revenue_processed_dataset_summary.md")
    actual = pd.read_csv(output)
    calculated = actual["units_sold"] * actual["unit_price"]
    if len(actual) != len(expected) or not (
        (actual["revenue"] - calculated).abs() < 1e-9
    ).all():
        raise AssertionError("Revenue artifact violates its production formula.")
    print(f"OK - revenue: {actual['revenue'].sum():.2f}")


def check_features() -> None:
    _, data = _input()
    expected = build_sales_features(data)
    output = PROCESSED / "sales_features.csv"
    require_files(output, REPORTS / "feature_engineering_summary.md")
    actual = pd.read_csv(output)
    required = {"day_of_week", "month", "year", "is_weekend", "revenue"}
    if len(actual) != len(expected) or not required.issubset(actual.columns):
        raise AssertionError("Feature artifact violates its contract.")
    print(f"OK - feature engineering: {len(actual)} rows")


def check_baseline(include_mae: bool = False) -> None:
    data = pd.read_csv(PROCESSED / "sales_features.csv")
    target = data["units_sold"]
    baseline = calculate_mean_baseline(target)
    predictions = create_mean_baseline_predictions(target)
    require_files(REPORTS / ("baseline_mae_summary.md" if include_mae else "mean_baseline_summary.md"))
    if len(predictions) != len(target):
        raise AssertionError("Baseline prediction length mismatch.")
    if include_mae:
        mae = calculate_mae(target, predictions)
        if mae < 0:
            raise AssertionError("MAE cannot be negative.")
        print(f"OK - baseline MAE: {mae:.2f}")
    else:
        print(f"OK - mean baseline: {baseline:.2f}")


def check_product_ranking() -> None:
    source = load_ranking_data()
    summary = build_product_summary(source)
    units = build_units_ranking(summary)
    revenue = build_revenue_ranking(summary)
    require_files(
        PRODUCT_SUMMARY_PATH,
        UNITS_RANKING_PATH,
        REVENUE_RANKING_PATH,
        REPORTS / "product_ranking_summary.md",
    )
    if summary["total_units_sold"].sum() != source["units_sold"].sum():
        raise AssertionError("Product summary does not preserve units.")
    if round(summary["total_revenue"].sum(), 2) != round(source["revenue"].sum(), 2):
        raise AssertionError("Product summary does not preserve revenue.")
    if not units["total_units_sold"].is_monotonic_decreasing:
        raise AssertionError("Units ranking is not descending.")
    if not revenue["total_revenue"].is_monotonic_decreasing:
        raise AssertionError("Revenue ranking is not descending.")
    print(f"OK - product ranking: {len(summary)} products")
