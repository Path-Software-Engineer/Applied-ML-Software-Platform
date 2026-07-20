"""Consolidate comparable candidate results without selecting a model."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


CANDIDATE_IDS = (
    "training_mean",
    "linear_regression",
    "random_forest",
    "gradient_boosting",
)
COMPARABILITY_FIELDS = (
    "schema_version",
    "dataset_sha256",
    "split_strategy",
    "target",
    "target_unit",
    "train_rows",
    "test_rows",
    "production_status",
)


class ComparisonError(ValueError):
    """Raised when candidate evidence cannot be compared fairly."""


def load_candidate_results(results_root: Path) -> list[dict[str, Any]]:
    """Load the four planned result artifacts in stable experiment order."""
    results: list[dict[str, Any]] = []
    for model_id in CANDIDATE_IDS:
        path = results_root / f"{model_id}.json"
        if not path.is_file():
            raise FileNotFoundError(f"Candidate result not found: {path}")
        result = json.loads(path.read_text(encoding="utf-8"))
        if result.get("model_id") != model_id:
            raise ComparisonError(f"Result identity mismatch: {path}")
        results.append(result)
    return results


def validate_comparability(results: list[dict[str, Any]]) -> None:
    """Require every candidate to share the frozen experiment boundary."""
    if len(results) != len(CANDIDATE_IDS):
        raise ComparisonError("Exactly four candidate results are required.")
    reference = results[0]
    for candidate in results[1:]:
        mismatches = [
            field
            for field in COMPARABILITY_FIELDS
            if candidate.get(field) != reference.get(field)
        ]
        if mismatches:
            raise ComparisonError(
                f"{candidate.get('model_id')} differs on {mismatches}."
            )


def build_initial_results(results: list[dict[str, Any]]) -> pd.DataFrame:
    """Create a compact metrics table without ranking or recommendation."""
    validate_comparability(results)
    rows = []
    for result in results:
        metrics = result["metrics"]
        rows.append(
            {
                "model_id": result["model_id"],
                "model_name": result["model_name"],
                "model_family": result["model_family"],
                "mae_units": float(metrics["mae"]),
                "rmse_units": float(metrics["rmse"]),
                "r2_contextual": metrics["r2"],
                "test_rows": int(result["test_rows"]),
                "production_status": result["production_status"],
            }
        )
    return pd.DataFrame(rows)


def _markdown_summary(table: pd.DataFrame, reference: dict[str, Any]) -> str:
    rows = [
        "# Sprint 2 Week 5 Initial Model Results",
        "",
        "All rows use the same 18-observation synthetic dataset, 12/6",
        "chronological split, target, feature contract and metric registry.",
        "",
        "| Candidate | MAE (units) | RMSE (units) | R² (contextual) |",
        "|---|---:|---:|---:|",
    ]
    for record in table.to_dict(orient="records"):
        rows.append(
            "| {name} | {mae:.4f} | {rmse:.4f} | {r2:.4f} |".format(
                name=record["model_name"],
                mae=record["mae_units"],
                rmse=record["rmse_units"],
                r2=record["r2_contextual"],
            )
        )
    rows.extend(
        [
            "",
            f"Dataset SHA-256: `{reference['dataset_sha256']}`.",
            "",
            "These are initial observed metrics, not a final recommendation.",
            "Formal comparison criteria, error review and model selection belong",
            "to Week 6. No row is evidence of production readiness or",
            "generalization beyond the controlled snapshot.",
            "",
        ]
    )
    return "\n".join(rows)


def run_initial_comparison(project_root: Path) -> pd.DataFrame:
    """Generate the official Week 5 consolidated result artifacts."""
    output_root = project_root / "reports" / "outputs" / "model-comparison"
    results = load_candidate_results(output_root / "results")
    table = build_initial_results(results)

    csv_path = output_root / "initial_results.csv"
    json_path = output_root / "initial_results.json"
    markdown_path = output_root / "initial_results.md"
    table.to_csv(csv_path, index=False)
    json_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "comparison_status": "observed_metrics_not_selection",
                "dataset_sha256": results[0]["dataset_sha256"],
                "split_strategy": results[0]["split_strategy"],
                "target": results[0]["target"],
                "target_unit": results[0]["target_unit"],
                "candidates": table.to_dict(orient="records"),
                "limitations": [
                    "18 synthetic observations",
                    "6 test observations",
                    "single chronological holdout",
                    "no production-readiness claim",
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    markdown_path.write_text(
        _markdown_summary(table, results[0]),
        encoding="utf-8",
        newline="\n",
    )
    return table


def main() -> None:
    """Generate official Day 63 consolidation."""
    project_root = Path(__file__).resolve().parents[4]
    table = run_initial_comparison(project_root)
    print("Week 5 initial results consolidated")
    print(table.loc[:, ["model_name", "mae_units", "rmse_units"]].to_string(index=False))
    print("Selection status: deferred to Week 6")


if __name__ == "__main__":
    main()
