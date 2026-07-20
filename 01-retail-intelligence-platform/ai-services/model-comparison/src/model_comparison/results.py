"""Common result and prediction contracts for Model Comparison."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd

from .metrics import RegressionMetrics


RESULT_SCHEMA_VERSION = "1.0"
PREDICTION_COLUMNS = (
    "sale_id",
    "date",
    "actual_units",
    "predicted_units",
    "residual",
    "absolute_error",
)


@dataclass(frozen=True)
class CandidateResult:
    """Comparable metadata and metrics for one evaluated candidate."""

    schema_version: str
    model_id: str
    model_name: str
    model_family: str
    configuration: dict[str, Any]
    dataset_sha256: str
    split_strategy: str
    target: str
    target_unit: str
    train_rows: int
    test_rows: int
    metrics: RegressionMetrics
    production_status: str = "learning_evidence_only"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["metrics"] = self.metrics.to_dict()
        return payload


def build_prediction_table(
    test: pd.DataFrame,
    predictions: list[float],
) -> pd.DataFrame:
    """Build observation-level evidence under one stable column contract."""
    if len(test) != len(predictions):
        raise ValueError("Test rows and predictions must have the same length.")
    table = pd.DataFrame(
        {
            "sale_id": test["sale_id"].astype(int).to_numpy(),
            "date": pd.to_datetime(test["date"]).dt.strftime("%Y-%m-%d"),
            "actual_units": test["units_sold"].astype(float).to_numpy(),
            "predicted_units": predictions,
        }
    )
    table["residual"] = table["actual_units"] - table["predicted_units"]
    table["absolute_error"] = table["residual"].abs()
    return table.loc[:, list(PREDICTION_COLUMNS)]
