"""Generate the formal candidate metrics table for decision review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from .comparison import build_initial_results, load_candidate_results


PRACTICAL_EQUIVALENCE_UNITS = 0.25
MINIMUM_BASELINE_IMPROVEMENT_PERCENT = 10.0


def build_comparison_table(results: list[dict[str, Any]]) -> pd.DataFrame:
    """Rank common metrics and calculate baseline-relative evidence."""
    initial = build_initial_results(results)
    baseline_rows = initial.loc[initial["model_id"] == "training_mean"]
    if len(baseline_rows) != 1:
        raise ValueError("Exactly one training-mean baseline is required.")
    baseline_mae = float(baseline_rows.iloc[0]["mae_units"])
    learned_mae = initial.loc[
        initial["model_id"] != "training_mean", "mae_units"
    ]
    if learned_mae.empty:
        raise ValueError("At least one learned candidate is required.")
    best_learned_mae = float(learned_mae.min())

    table = initial.copy()
    table["mae_rank"] = table["mae_units"].rank(method="min").astype(int)
    table["mae_delta_vs_baseline_units"] = baseline_mae - table["mae_units"]
    table["mae_improvement_vs_baseline_percent"] = (
        table["mae_delta_vs_baseline_units"] / baseline_mae * 100
    )
    table["within_practical_equivalence"] = (
        table["model_id"].ne("training_mean")
        & table["mae_units"].le(
            best_learned_mae + PRACTICAL_EQUIVALENCE_UNITS
        )
    )
    table["meets_minimum_baseline_improvement"] = (
        table["model_id"].ne("training_mean")
        & table["mae_improvement_vs_baseline_percent"].ge(
            MINIMUM_BASELINE_IMPROVEMENT_PERCENT
        )
    )
    return table.sort_values(
        ["mae_rank", "model_id"], kind="stable"
    ).reset_index(drop=True)


def _markdown_table(table: pd.DataFrame) -> str:
    rows = [
        "# Sprint 2 Formal Model Comparison Table",
        "",
        "| Rank | Candidate | MAE | RMSE | R² | Δ MAE vs baseline | Improvement | Equivalent |",
        "|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in table.to_dict(orient="records"):
        rows.append(
            "| {rank} | {name} | {mae:.4f} | {rmse:.4f} | {r2:.4f} | "
            "{delta:+.4f} | {improvement:+.2f}% | {equivalent} |".format(
                rank=row["mae_rank"],
                name=row["model_name"],
                mae=row["mae_units"],
                rmse=row["rmse_units"],
                r2=row["r2_contextual"],
                delta=row["mae_delta_vs_baseline_units"],
                improvement=row["mae_improvement_vs_baseline_percent"],
                equivalent="yes" if row["within_practical_equivalence"] else "no",
            )
        )
    rows.extend(
        [
            "",
            "MAE is the primary metric; lower is better. RMSE is a large-error",
            "diagnostic; lower is better. R² is contextual on six test rows.",
            "",
            "Practical equivalence means a learned candidate is within 0.25 MAE",
            "units of the best learned result. The table does not select a model.",
            "Error review and the frozen complexity tie-break belong to Days 66–67.",
            "",
        ]
    )
    return "\n".join(rows)


def run_comparison_table(project_root: Path) -> pd.DataFrame:
    """Generate deterministic CSV, JSON and Markdown comparison artifacts."""
    output_root = project_root / "reports" / "outputs" / "model-comparison"
    results = load_candidate_results(output_root / "results")
    table = build_comparison_table(results)

    table.to_csv(output_root / "comparison_table.csv", index=False)
    (output_root / "comparison_table.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "dataset_sha256": results[0]["dataset_sha256"],
                "split_strategy": results[0]["split_strategy"],
                "target": results[0]["target"],
                "target_unit": results[0]["target_unit"],
                "primary_metric": {
                    "id": "mae",
                    "unit": "units",
                    "direction": "lower_is_better",
                },
                "diagnostic_metrics": {
                    "rmse": {
                        "unit": "units",
                        "direction": "lower_is_better",
                    },
                    "r2": {
                        "unit": "unitless",
                        "direction": "higher_is_better",
                        "role": "contextual_only",
                    },
                },
                "policy": {
                    "practical_equivalence_units": (
                        PRACTICAL_EQUIVALENCE_UNITS
                    ),
                    "minimum_baseline_improvement_percent": (
                        MINIMUM_BASELINE_IMPROVEMENT_PERCENT
                    ),
                },
                "selection_status": "not_selected",
                "rows": table.to_dict(orient="records"),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output_root / "comparison_table.md").write_text(
        _markdown_table(table),
        encoding="utf-8",
        newline="\n",
    )
    return table


def main() -> None:
    """Generate official Day 65 artifacts."""
    project_root = Path(__file__).resolve().parents[4]
    table = run_comparison_table(project_root)
    print("Formal Model Comparison table generated")
    print(
        table.loc[
            :,
            [
                "mae_rank",
                "model_name",
                "mae_units",
                "mae_improvement_vs_baseline_percent",
            ],
        ].to_string(index=False)
    )
    print("Selection status: not selected")


if __name__ == "__main__":
    main()
