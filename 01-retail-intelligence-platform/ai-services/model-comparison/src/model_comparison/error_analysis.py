"""Prediction-level residual and largest-error analysis."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .comparison import CANDIDATE_IDS, load_candidate_results


PREDICTION_COLUMNS = {
    "sale_id",
    "date",
    "actual_units",
    "predicted_units",
    "residual",
    "absolute_error",
}


class ErrorAnalysisError(ValueError):
    """Raised when prediction evidence does not match the test partition."""


def build_error_analysis(
    predictions_by_model: dict[str, pd.DataFrame],
    test: pd.DataFrame,
    model_names: dict[str, str],
) -> pd.DataFrame:
    """Validate and enrich prediction artifacts with test-row context."""
    required_test = {
        "sale_id",
        "date",
        "product_id",
        "product_name",
        "category",
        "units_sold",
    }
    if not required_test.issubset(test.columns):
        raise ErrorAnalysisError("Test data lacks required context columns.")
    official = test.loc[
        :,
        [
            "sale_id",
            "date",
            "product_id",
            "product_name",
            "category",
            "units_sold",
        ],
    ].copy()
    official["sale_id"] = official["sale_id"].astype(int)
    official["date"] = pd.to_datetime(official["date"]).dt.strftime("%Y-%m-%d")
    official_ids = set(official["sale_id"])

    frames: list[pd.DataFrame] = []
    for model_id, predictions in predictions_by_model.items():
        if not PREDICTION_COLUMNS.issubset(predictions.columns):
            raise ErrorAnalysisError(
                f"{model_id} prediction columns are incomplete."
            )
        candidate = predictions.copy()
        candidate["sale_id"] = candidate["sale_id"].astype(int)
        candidate["date"] = pd.to_datetime(candidate["date"]).dt.strftime(
            "%Y-%m-%d"
        )
        if candidate["sale_id"].duplicated().any():
            raise ErrorAnalysisError(f"{model_id} has duplicated sale IDs.")
        if set(candidate["sale_id"]) != official_ids:
            raise ErrorAnalysisError(
                f"{model_id} prediction rows differ from the test partition."
            )
        expected_residual = (
            candidate["actual_units"] - candidate["predicted_units"]
        )
        if not np.allclose(candidate["residual"], expected_residual):
            raise ErrorAnalysisError(f"{model_id} residual values are invalid.")
        if not np.allclose(
            candidate["absolute_error"], expected_residual.abs()
        ):
            raise ErrorAnalysisError(
                f"{model_id} absolute-error values are invalid."
            )

        enriched = candidate.merge(
            official,
            on=["sale_id", "date"],
            how="inner",
            validate="one_to_one",
        )
        if not np.allclose(enriched["actual_units"], enriched["units_sold"]):
            raise ErrorAnalysisError(
                f"{model_id} actual values differ from official targets."
            )
        enriched.insert(0, "model_id", model_id)
        enriched.insert(1, "model_name", model_names[model_id])
        enriched["squared_error"] = enriched["residual"].pow(2)
        enriched["error_direction"] = np.select(
            [
                enriched["residual"].gt(0),
                enriched["residual"].lt(0),
            ],
            ["under_prediction", "over_prediction"],
            default="exact",
        )
        frames.append(enriched)

    analysis = pd.concat(frames, ignore_index=True)
    return analysis.loc[
        :,
        [
            "model_id",
            "model_name",
            "sale_id",
            "date",
            "product_id",
            "product_name",
            "category",
            "actual_units",
            "predicted_units",
            "residual",
            "absolute_error",
            "squared_error",
            "error_direction",
        ],
    ]


def summarize_errors(analysis: pd.DataFrame) -> list[dict[str, Any]]:
    """Create descriptive per-candidate notes from validated residuals."""
    summaries: list[dict[str, Any]] = []
    for model_id, group in analysis.groupby("model_id", sort=False):
        largest = group.sort_values(
            ["absolute_error", "sale_id"],
            ascending=[False, True],
            kind="stable",
        ).iloc[0]
        summaries.append(
            {
                "model_id": model_id,
                "model_name": largest["model_name"],
                "mean_signed_residual": float(group["residual"].mean()),
                "under_prediction_count": int(
                    group["error_direction"].eq("under_prediction").sum()
                ),
                "over_prediction_count": int(
                    group["error_direction"].eq("over_prediction").sum()
                ),
                "exact_count": int(
                    group["error_direction"].eq("exact").sum()
                ),
                "largest_error": {
                    "sale_id": int(largest["sale_id"]),
                    "date": largest["date"],
                    "product_id": largest["product_id"],
                    "product_name": largest["product_name"],
                    "category": largest["category"],
                    "actual_units": float(largest["actual_units"]),
                    "predicted_units": float(largest["predicted_units"]),
                    "residual": float(largest["residual"]),
                    "absolute_error": float(largest["absolute_error"]),
                    "direction": largest["error_direction"],
                },
                "interpretation": (
                    "Observed residual pattern on six test rows; no causal "
                    "explanation or stability claim."
                ),
            }
        )
    return summaries


def _markdown_analysis(
    summaries: list[dict[str, Any]],
    analysis: pd.DataFrame,
) -> str:
    rows = [
        "# Sprint 2 Model Error Analysis",
        "",
        "| Candidate | Mean signed residual | Under | Over | Largest absolute error | Observation |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for summary in summaries:
        largest = summary["largest_error"]
        rows.append(
            "| {name} | {mean:+.4f} | {under} | {over} | {error:.4f} | "
            "{date}, {product} |".format(
                name=summary["model_name"],
                mean=summary["mean_signed_residual"],
                under=summary["under_prediction_count"],
                over=summary["over_prediction_count"],
                error=largest["absolute_error"],
                date=largest["date"],
                product=largest["product_name"],
            )
        )

    largest_rows = analysis.sort_values(
        ["absolute_error", "model_id", "sale_id"],
        ascending=[False, True, True],
        kind="stable",
    ).head(8)
    rows.extend(
        [
            "",
            "## Largest observed candidate-row errors",
            "",
            "| Candidate | Date | Product | Actual | Predicted | Residual | Absolute error |",
            "|---|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in largest_rows.to_dict(orient="records"):
        rows.append(
            "| {name} | {date} | {product} | {actual:.2f} | {predicted:.2f} | "
            "{residual:+.2f} | {absolute:.2f} |".format(
                name=row["model_name"],
                date=row["date"],
                product=row["product_name"],
                actual=row["actual_units"],
                predicted=row["predicted_units"],
                residual=row["residual"],
                absolute=row["absolute_error"],
            )
        )
    rows.extend(
        [
            "",
            "Residual is `actual - predicted`: positive values are",
            "under-predictions and negative values are over-predictions.",
            "",
            "This analysis describes 24 observed candidate-row predictions from",
            "one six-row holdout. It does not establish causes, stability or",
            "generalization.",
            "",
        ]
    )
    return "\n".join(rows)


def run_error_analysis(project_root: Path) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    """Generate official Day 66 CSV, JSON and Markdown error evidence."""
    output_root = project_root / "reports" / "outputs" / "model-comparison"
    results = load_candidate_results(output_root / "results")
    names = {result["model_id"]: result["model_name"] for result in results}
    predictions = {
        model_id: pd.read_csv(output_root / "predictions" / f"{model_id}.csv")
        for model_id in CANDIDATE_IDS
    }
    test = pd.read_csv(
        project_root / "data" / "processed" / "model-comparison" / "test.csv"
    )
    analysis = build_error_analysis(predictions, test, names)
    summaries = summarize_errors(analysis)

    analysis.to_csv(output_root / "error_analysis.csv", index=False)
    (output_root / "error_analysis.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "dataset_sha256": results[0]["dataset_sha256"],
                "split_strategy": results[0]["split_strategy"],
                "target": results[0]["target"],
                "target_unit": results[0]["target_unit"],
                "prediction_rows": len(analysis),
                "residual_definition": "actual_units - predicted_units",
                "interpretation_boundary": "descriptive_no_causal_claims",
                "candidate_summaries": summaries,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output_root / "error_analysis.md").write_text(
        _markdown_analysis(summaries, analysis),
        encoding="utf-8",
        newline="\n",
    )
    return analysis, summaries


def main() -> None:
    """Generate official error-analysis artifacts."""
    project_root = Path(__file__).resolve().parents[4]
    analysis, summaries = run_error_analysis(project_root)
    print(f"Model error analysis generated: {len(analysis)} prediction rows")
    for summary in summaries:
        largest = summary["largest_error"]
        print(
            f"{summary['model_name']}: largest error "
            f"{largest['absolute_error']:.4f} units on sale {largest['sale_id']}"
        )
    print("Interpretation boundary: descriptive, no causal claims")


if __name__ == "__main__":
    main()
