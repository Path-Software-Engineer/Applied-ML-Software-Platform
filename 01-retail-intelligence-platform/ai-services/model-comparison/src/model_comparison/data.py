"""Load, validate and split the official Model Comparison dataset."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from .contract import (
    EXCLUDED_COLUMNS,
    EXPERIMENT_CONTRACT,
    REQUIRED_COLUMNS,
    ExperimentContract,
)


class ExperimentDataError(ValueError):
    """Raised when experiment data violates the shared contract."""


@dataclass
class ExperimentSplit:
    """Chronological training and test partitions with auditable metadata."""

    train: pd.DataFrame
    test: pd.DataFrame
    manifest: dict[str, Any]


def file_sha256(path: Path) -> str:
    """Return a streaming SHA-256 checksum for a source artifact."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_experiment_dataset(path: Path) -> pd.DataFrame:
    """Load the prepared Sprint 1 dataset and enforce the Sprint 2 contract."""
    if not path.is_file():
        raise FileNotFoundError(f"Experiment dataset not found: {path}")
    if path.stat().st_size == 0:
        raise ExperimentDataError("Experiment dataset is empty.")

    data = pd.read_csv(path)
    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        raise ExperimentDataError(f"Missing experiment columns: {missing}")
    if data.empty:
        raise ExperimentDataError("Experiment dataset has no rows.")
    if data["sale_id"].duplicated().any():
        raise ExperimentDataError("sale_id must be unique.")

    validated = data.copy()
    validated["date"] = pd.to_datetime(validated["date"], errors="coerce")
    numeric_columns = (
        "sale_id",
        EXPERIMENT_CONTRACT.target_column,
        "unit_price",
        "day_of_week",
    )
    for column in numeric_columns:
        validated[column] = pd.to_numeric(validated[column], errors="coerce")

    weekend_values = (
        validated["is_weekend"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({"true": True, "false": False, "1": True, "0": False})
    )
    validated["is_weekend"] = weekend_values

    required = list(REQUIRED_COLUMNS)
    if validated[required].isna().any().any():
        raise ExperimentDataError("Required experiment values contain nulls.")
    if (validated[EXPERIMENT_CONTRACT.target_column] < 0).any():
        raise ExperimentDataError("Target values must be non-negative.")
    if (validated["unit_price"] <= 0).any():
        raise ExperimentDataError("unit_price must be positive.")
    if not validated["day_of_week"].between(0, 6).all():
        raise ExperimentDataError("day_of_week must be between 0 and 6.")

    return validated.sort_values(["date", "sale_id"], kind="stable").reset_index(
        drop=True
    )


def split_experiment_dataset(
    data: pd.DataFrame,
    *,
    contract: ExperimentContract = EXPERIMENT_CONTRACT,
    source_path: Path | None = None,
) -> ExperimentSplit:
    """Create the fixed chronological holdout without row or date overlap."""
    cutoff = pd.Timestamp(contract.cutoff_date)
    train = data.loc[data["date"] <= cutoff].copy()
    test = data.loc[data["date"] > cutoff].copy()

    if train.empty or test.empty:
        raise ExperimentDataError("Chronological split requires train and test rows.")
    if set(train["sale_id"]) & set(test["sale_id"]):
        raise ExperimentDataError("Train and test sale identifiers overlap.")
    if train["date"].max() >= test["date"].min():
        raise ExperimentDataError("Chronological split boundary is invalid.")

    manifest: dict[str, Any] = {
        "schema_version": contract.schema_version,
        "dataset": (
            source_path.as_posix() if source_path is not None else "controlled_input"
        ),
        "dataset_sha256": file_sha256(source_path) if source_path else None,
        "target": contract.target_column,
        "target_unit": contract.target_unit,
        "categorical_features": list(contract.categorical_features),
        "numeric_features": list(contract.numeric_features),
        "excluded_columns": EXCLUDED_COLUMNS,
        "split": {
            "strategy": contract.split_strategy,
            "cutoff_date": contract.cutoff_date,
            "random_seed": contract.random_seed,
            "train_rows": len(train),
            "test_rows": len(test),
            "train_start": train["date"].min().date().isoformat(),
            "train_end": train["date"].max().date().isoformat(),
            "test_start": test["date"].min().date().isoformat(),
            "test_end": test["date"].max().date().isoformat(),
            "train_sale_ids": train["sale_id"].astype(int).tolist(),
            "test_sale_ids": test["sale_id"].astype(int).tolist(),
        },
        "fairness_rule": (
            "Every candidate uses this dataset, feature contract, split and metrics."
        ),
        "production_status": "learning_evidence_only",
    }
    return ExperimentSplit(train=train, test=test, manifest=manifest)


def write_experiment_split(
    split: ExperimentSplit,
    *,
    train_path: Path,
    test_path: Path,
    manifest_path: Path,
) -> None:
    """Persist official split evidence from one production boundary."""
    for path in (train_path, test_path, manifest_path):
        path.parent.mkdir(parents=True, exist_ok=True)

    train_output = split.train.copy()
    test_output = split.test.copy()
    for output in (train_output, test_output):
        output["date"] = output["date"].dt.strftime("%Y-%m-%d")
    train_output.to_csv(train_path, index=False)
    test_output.to_csv(test_path, index=False)
    manifest_path.write_text(
        json.dumps(split.manifest, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def run_experiment_preparation(project_root: Path) -> ExperimentSplit:
    """Generate the official Day 58 partitions and split manifest."""
    source_path = (
        project_root / "data" / "processed" / "demand-insight" / "sales_features.csv"
    )
    train_path = (
        project_root / "data" / "processed" / "model-comparison" / "train.csv"
    )
    test_path = (
        project_root / "data" / "processed" / "model-comparison" / "test.csv"
    )
    manifest_path = (
        project_root
        / "reports"
        / "outputs"
        / "model-comparison"
        / "split_manifest.json"
    )

    data = load_experiment_dataset(source_path)
    relative_source = source_path.relative_to(project_root)
    split = split_experiment_dataset(
        data,
        source_path=project_root / relative_source,
    )
    split.manifest["dataset"] = relative_source.as_posix()
    write_experiment_split(
        split,
        train_path=train_path,
        test_path=test_path,
        manifest_path=manifest_path,
    )
    return split


def main() -> None:
    """Generate the official split from the repository root."""
    project_root = Path(__file__).resolve().parents[4]
    split = run_experiment_preparation(project_root)
    print(
        "Model Comparison split generated: "
        f"{len(split.train)} train / {len(split.test)} test"
    )
    print("Manifest: reports/outputs/model-comparison/split_manifest.json")


if __name__ == "__main__":
    main()
