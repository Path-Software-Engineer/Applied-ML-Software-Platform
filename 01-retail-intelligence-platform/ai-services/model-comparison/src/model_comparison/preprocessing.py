"""Shared feature preprocessing for every classical regression candidate."""

from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .contract import EXPERIMENT_CONTRACT


def build_preprocessor() -> ColumnTransformer:
    """Create an unfitted, leakage-safe preprocessing contract."""
    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                list(EXPERIMENT_CONTRACT.categorical_features),
            ),
            (
                "numeric",
                StandardScaler(),
                list(EXPERIMENT_CONTRACT.numeric_features),
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def preprocessing_metadata() -> dict[str, object]:
    """Return the stable preprocessing description stored with results."""
    return {
        "categorical": {
            "columns": list(EXPERIMENT_CONTRACT.categorical_features),
            "strategy": "one_hot_encode",
            "unknown_values": "ignore",
        },
        "numeric": {
            "columns": list(EXPERIMENT_CONTRACT.numeric_features),
            "strategy": "standard_scale",
        },
        "fit_scope": "training_partition_only",
    }
