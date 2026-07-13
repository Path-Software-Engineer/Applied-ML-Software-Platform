from pathlib import Path

import pandas as pd

from src.pipelines.feature_baseline_metric_pipeline import (
    ERROR_COLUMN,
    PREDICTION_COLUMN,
    build_feature_baseline_metric_table,
    run_feature_baseline_metric_pipeline,
)
from src.pipelines.first_data_pipeline import (
    REQUIRED_COLUMNS,
    build_pipeline_ready_dataset,
)


def sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": ["2026-01-02", "2026-01-01"],
            "product_id": ["P2", "P1"],
            "product_name": ["Bread", "Rice"],
            "category": ["Bakery", "Grocery"],
            "units_sold": [2, 4],
            "unit_price": [3.0, 2.0],
        }
    )


def test_first_pipeline_writes_only_requested_tmp_paths(tmp_path: Path) -> None:
    raw = tmp_path / "raw.csv"
    output = tmp_path / "processed" / "ready.csv"
    summary = tmp_path / "reports" / "summary.md"
    sample_data().to_csv(raw, index=False)

    result = build_pipeline_ready_dataset(raw, output, summary)

    assert output.exists() and summary.exists()
    assert all(column in result.columns for column in REQUIRED_COLUMNS)
    assert result["date"].is_monotonic_increasing


def test_feature_baseline_metric_table_contract() -> None:
    output, baseline, mae = build_feature_baseline_metric_table(sample_data())
    expected = {"day_of_week", "month", "year", "is_weekend", "revenue", PREDICTION_COLUMN, ERROR_COLUMN}
    assert expected.issubset(output.columns)
    assert baseline == 3.0
    assert mae == 1.0


def test_integrated_pipeline_uses_isolated_project_root(tmp_path: Path) -> None:
    input_dir = tmp_path / "data" / "processed" / "demand-insight"
    input_dir.mkdir(parents=True)
    sample_data().to_csv(input_dir / "sales_pipeline_ready.csv", index=False)

    result = run_feature_baseline_metric_pipeline(tmp_path)

    assert Path(result["output_path"]).exists()
    assert Path(result["summary_path"]).exists()
    assert result["rows"] == 2
