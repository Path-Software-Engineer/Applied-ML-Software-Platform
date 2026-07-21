"""Shared regression metrics for every Model Comparison candidate."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import sqrt
from typing import Any, Iterable

import numpy as np


class MetricError(ValueError):
    """Raised when regression metrics cannot be computed safely."""


@dataclass(frozen=True)
class RegressionMetrics:
    """Versioned metric values with explicit direction and units."""

    mae: float
    rmse: float
    r2: float | None

    def to_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "metadata": {
                "mae": {"direction": "lower_is_better", "unit": "units"},
                "rmse": {"direction": "lower_is_better", "unit": "units"},
                "r2": {"direction": "higher_is_better", "unit": "unitless"},
            },
        }


def _numeric_vector(values: Iterable[float], name: str) -> np.ndarray:
    vector = np.asarray(list(values), dtype=float)
    if vector.ndim != 1 or vector.size == 0:
        raise MetricError(f"{name} must be a non-empty one-dimensional vector.")
    if not np.isfinite(vector).all():
        raise MetricError(f"{name} contains non-finite values.")
    return vector


def calculate_regression_metrics(
    y_true: Iterable[float],
    y_pred: Iterable[float],
) -> RegressionMetrics:
    """Calculate MAE, RMSE and contextual R² from one prediction vector."""
    actual = _numeric_vector(y_true, "y_true")
    predicted = _numeric_vector(y_pred, "y_pred")
    if actual.shape != predicted.shape:
        raise MetricError("y_true and y_pred must have the same shape.")

    residuals = actual - predicted
    mae = float(np.mean(np.abs(residuals)))
    rmse = float(sqrt(np.mean(np.square(residuals))))
    centered = actual - float(np.mean(actual))
    total_variance = float(np.sum(np.square(centered)))
    r2 = (
        None
        if total_variance == 0.0
        else float(1.0 - np.sum(np.square(residuals)) / total_variance)
    )
    return RegressionMetrics(mae=mae, rmse=rmse, r2=r2)
