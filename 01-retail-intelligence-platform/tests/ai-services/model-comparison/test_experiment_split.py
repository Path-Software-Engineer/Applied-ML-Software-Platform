"""Tests for the Model Comparison data and split contract."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from model_comparison.contract import EXPERIMENT_CONTRACT
from model_comparison.data import (
    ExperimentDataError,
    load_experiment_dataset,
    split_experiment_dataset,
    write_experiment_split,
)


def controlled_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sale_id": [1, 2, 3, 4],
            "date": [
                "2026-01-05",
                "2026-01-06",
                "2026-01-07",
                "2026-01-08",
            ],
            "product_id": ["P1", "P2", "P1", "P2"],
            "category": ["Food", "Dairy", "Food", "Dairy"],
            "units_sold": [10, 20, 12, 18],
            "unit_price": [2.0, 3.0, 2.0, 3.0],
            "day_of_week": [0, 1, 2, 3],
            "is_weekend": [False, False, False, False],
        }
    )


def test_loader_validates_and_orders_the_dataset(tmp_path: Path) -> None:
    path = tmp_path / "sales.csv"
    controlled_dataset().iloc[[3, 0, 2, 1]].to_csv(path, index=False)

    loaded = load_experiment_dataset(path)

    assert loaded["sale_id"].tolist() == [1, 2, 3, 4]
    assert str(loaded["date"].dtype) == "datetime64[ns]"
    assert loaded["is_weekend"].dtype == bool


def test_loader_rejects_missing_columns(tmp_path: Path) -> None:
    path = tmp_path / "invalid.csv"
    controlled_dataset().drop(columns=["category"]).to_csv(path, index=False)

    with pytest.raises(ExperimentDataError, match="Missing experiment columns"):
        load_experiment_dataset(path)


def test_loader_rejects_duplicate_identifiers(tmp_path: Path) -> None:
    path = tmp_path / "duplicate.csv"
    data = controlled_dataset()
    data.loc[1, "sale_id"] = 1
    data.to_csv(path, index=False)

    with pytest.raises(ExperimentDataError, match="sale_id must be unique"):
        load_experiment_dataset(path)


def test_chronological_split_uses_the_fixed_boundary(tmp_path: Path) -> None:
    path = tmp_path / "sales.csv"
    controlled_dataset().to_csv(path, index=False)
    loaded = load_experiment_dataset(path)

    split = split_experiment_dataset(loaded, source_path=path)

    assert split.train["sale_id"].tolist() == [1, 2]
    assert split.test["sale_id"].tolist() == [3, 4]
    assert split.manifest["split"]["random_seed"] == 42
    assert split.manifest["target"] == "units_sold"
    assert split.manifest["numeric_features"] == [
        "unit_price",
        "day_of_week",
        "is_weekend",
    ]


def test_split_artifacts_are_written_without_mutating_inputs(
    tmp_path: Path,
) -> None:
    source = tmp_path / "sales.csv"
    controlled_dataset().to_csv(source, index=False)
    split = split_experiment_dataset(
        load_experiment_dataset(source),
        source_path=source,
    )
    train_path = tmp_path / "train.csv"
    test_path = tmp_path / "test.csv"
    manifest_path = tmp_path / "split_manifest.json"

    write_experiment_split(
        split,
        train_path=train_path,
        test_path=test_path,
        manifest_path=manifest_path,
    )

    assert len(pd.read_csv(train_path)) == 2
    assert len(pd.read_csv(test_path)) == 2
    assert '"schema_version": "1.0"' in manifest_path.read_text(encoding="utf-8")
    assert EXPERIMENT_CONTRACT.target_column in split.train.columns
