"""Versioned Model Comparison experiment contract."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentContract:
    """Immutable configuration shared by every Sprint 2 candidate."""

    schema_version: str
    target_column: str
    target_unit: str
    categorical_features: tuple[str, ...]
    numeric_features: tuple[str, ...]
    split_strategy: str
    cutoff_date: str
    random_seed: int

    @property
    def feature_columns(self) -> tuple[str, ...]:
        return self.categorical_features + self.numeric_features


EXPERIMENT_CONTRACT = ExperimentContract(
    schema_version="1.0",
    target_column="units_sold",
    target_unit="units_per_sale_record",
    categorical_features=("product_id", "category"),
    numeric_features=("unit_price", "day_of_week", "is_weekend"),
    split_strategy="chronological_holdout",
    cutoff_date="2026-01-06",
    random_seed=42,
)

REQUIRED_COLUMNS = (
    "sale_id",
    "date",
    EXPERIMENT_CONTRACT.target_column,
    *EXPERIMENT_CONTRACT.feature_columns,
)

EXCLUDED_COLUMNS = {
    "sale_id": "row_identifier",
    "date": "split_key",
    "product_name": "duplicate_product_identity",
    "month": "constant_in_snapshot",
    "year": "constant_in_snapshot",
    "revenue": "target_derived_leakage",
    "stock_available": "ambiguous_measurement_timing",
    "mean_baseline_prediction": "target_derived",
    "baseline_absolute_error": "target_derived",
}
