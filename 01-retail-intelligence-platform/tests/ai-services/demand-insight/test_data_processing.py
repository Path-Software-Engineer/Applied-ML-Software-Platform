from pathlib import Path

import pandas as pd
import pytest

from src.data.data_cleaner import clean_sales_data, validate_required_columns
from src.data.data_loader import load_sales_data


def valid_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": ["2026-01-02", "2026-01-01"],
            "product_id": [" P2 ", "P1"],
            "product_name": [" Bread ", "Rice"],
            "units_sold": [2, 3],
            "unit_price": [1.5, 2.0],
        }
    )


def test_loader_reads_existing_csv(tmp_path: Path) -> None:
    path = tmp_path / "sales.csv"
    valid_data().to_csv(path, index=False)
    assert len(load_sales_data(path)) == 2


def test_loader_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_sales_data(tmp_path / "missing.csv")


def test_loader_rejects_empty_csv(tmp_path: Path) -> None:
    path = tmp_path / "empty.csv"
    path.write_text("date,product_id\n", encoding="utf-8")
    with pytest.raises(ValueError, match="empty"):
        load_sales_data(path)


def test_cleaner_rejects_missing_columns() -> None:
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_required_columns(pd.DataFrame({"date": ["2026-01-01"]}))


def test_cleaner_removes_null_invalid_negative_and_duplicate_rows() -> None:
    data = pd.concat(
        [
            valid_data(),
            valid_data().iloc[[0]],
            pd.DataFrame(
                {
                    "date": ["bad", "2026-01-03", None],
                    "product_id": ["P3", "P4", "P5"],
                    "product_name": ["A", "B", "C"],
                    "units_sold": [1, -1, 2],
                    "unit_price": [1, 2, 3],
                }
            ),
        ],
        ignore_index=True,
    )
    cleaned = clean_sales_data(data)
    assert len(cleaned) == 2
    assert cleaned.isna().sum().sum() == 0
    assert pd.api.types.is_datetime64_any_dtype(cleaned["date"])
    assert cleaned["product_id"].tolist() == ["P1", "P2"]
