"""Shared training, evaluation and persistence boundary for model candidates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.base import RegressorMixin
from sklearn.pipeline import Pipeline

from .contract import EXPERIMENT_CONTRACT
from .metrics import calculate_regression_metrics
from .preprocessing import build_preprocessor, preprocessing_metadata
from .results import RESULT_SCHEMA_VERSION, CandidateResult, build_prediction_table


def evaluate_candidate(
    *,
    model_id: str,
    model_name: str,
    model_family: str,
    estimator: RegressorMixin,
    estimator_parameters: dict[str, Any],
    train: pd.DataFrame,
    test: pd.DataFrame,
    manifest: dict[str, Any],
) -> tuple[CandidateResult, pd.DataFrame]:
    """Fit one candidate on the official training partition and evaluate it."""
    if train.empty or test.empty:
        raise ValueError("Candidate evaluation requires train and test rows.")

    pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("estimator", estimator),
        ]
    )
    features = list(EXPERIMENT_CONTRACT.feature_columns)
    target = EXPERIMENT_CONTRACT.target_column
    pipeline.fit(train[features], train[target])
    predicted = pipeline.predict(test[features]).astype(float).tolist()
    metrics = calculate_regression_metrics(test[target], predicted)

    split = manifest.get("split")
    if not isinstance(split, dict):
        raise ValueError("Split manifest has an invalid split section.")
    result = CandidateResult(
        schema_version=RESULT_SCHEMA_VERSION,
        model_id=model_id,
        model_name=model_name,
        model_family=model_family,
        configuration={
            "estimator_parameters": estimator_parameters,
            "preprocessing": preprocessing_metadata(),
        },
        dataset_sha256=str(manifest["dataset_sha256"]),
        split_strategy=str(split["strategy"]),
        target=str(manifest["target"]),
        target_unit=str(manifest["target_unit"]),
        train_rows=len(train),
        test_rows=len(test),
        metrics=metrics,
    )
    return result, build_prediction_table(test, predicted)


def run_candidate(
    project_root: Path,
    *,
    model_id: str,
    model_name: str,
    model_family: str,
    estimator: RegressorMixin,
    estimator_parameters: dict[str, Any],
) -> tuple[CandidateResult, pd.DataFrame]:
    """Evaluate and persist one candidate under the common result contract."""
    data_root = project_root / "data" / "processed" / "model-comparison"
    output_root = project_root / "reports" / "outputs" / "model-comparison"
    train = pd.read_csv(data_root / "train.csv")
    test = pd.read_csv(data_root / "test.csv")
    manifest = json.loads(
        (output_root / "split_manifest.json").read_text(encoding="utf-8")
    )
    result, predictions = evaluate_candidate(
        model_id=model_id,
        model_name=model_name,
        model_family=model_family,
        estimator=estimator,
        estimator_parameters=estimator_parameters,
        train=train,
        test=test,
        manifest=manifest,
    )

    prediction_path = output_root / "predictions" / f"{model_id}.csv"
    result_path = output_root / "results" / f"{model_id}.json"
    prediction_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(prediction_path, index=False)
    result_path.write_text(
        json.dumps(result.to_dict(), indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return result, predictions
