"""Assemble the reusable Sprint 2 comparison report and Decision Cards."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPORT_SCHEMA_VERSION = "1.0"


class ComparisonReportError(ValueError):
    """Raised when report inputs do not share the completed decision boundary."""


def build_decision_cards(
    comparison: dict[str, Any],
    decision: dict[str, Any],
) -> list[dict[str, Any]]:
    """Create three stable, presentation-ready decision cards."""
    rows = {row["model_id"]: row for row in comparison.get("rows", [])}
    leader = decision.get("measurement_leader", {})
    selected = decision.get("selected_candidate", {})
    if leader.get("model_id") not in rows or selected.get("model_id") not in rows:
        raise ComparisonReportError("Decision models are absent from comparison rows.")
    test_rows = int(rows[selected["model_id"]]["test_rows"])
    return [
        {
            "card_id": "metric-leader",
            "eyebrow": "Observed metric leader",
            "title": leader["model_name"],
            "status": "measurement_leader_not_selected",
            "model_id": leader["model_id"],
            "primary_metric": {
                "label": "MAE",
                "value": leader["mae_units"],
                "unit": "units",
                "direction": "lower_is_better",
            },
            "summary": "Lowest observed MAE on the fixed chronological holdout.",
            "reasons": [
                "Ranks first by the frozen primary metric.",
                "Remains practically equivalent to Random Forest.",
            ],
            "limitation": (
                "Metric leadership on six test rows does not establish stability "
                "or production readiness."
            ),
        },
        {
            "card_id": "integration-candidate",
            "eyebrow": "Selected for next integration",
            "title": selected["model_name"],
            "status": "selected_for_next_integration",
            "model_id": selected["model_id"],
            "primary_metric": {
                "label": "MAE",
                "value": selected["mae_units"],
                "unit": "units",
                "direction": "lower_is_better",
            },
            "summary": (
                "Chosen by the frozen practical-equivalence and lower-complexity "
                "rule."
            ),
            "reasons": [
                "Falls within 0.25 MAE units of the observed leader.",
                "Improves baseline MAE by more than the required 10%.",
                "Has lower recorded complexity than the equivalent leader.",
            ],
            "limitation": (
                "Selection authorizes a later read-only platform integration, "
                "not deployment or inventory action."
            ),
        },
        {
            "card_id": "evidence-boundary",
            "eyebrow": "Evidence boundary",
            "title": "Learning evidence only",
            "status": "not_production_ready",
            "model_id": None,
            "primary_metric": {
                "label": "Test observations",
                "value": test_rows,
                "unit": "rows",
                "direction": "context_only",
            },
            "summary": (
                "Every comparison result comes from one small synthetic snapshot."
            ),
            "reasons": [
                "The experiment contains 18 observations in total.",
                "Only one chronological 12/6 split was evaluated.",
                "Repeatability is not stability or external validation.",
            ],
            "limitation": (
                "No production, generalization, forecasting or inventory claim "
                "is supported."
            ),
        },
    ]


def build_comparison_report(
    comparison: dict[str, Any],
    errors: dict[str, Any],
    decision: dict[str, Any],
    split_manifest: dict[str, Any],
) -> dict[str, Any]:
    """Combine versioned evidence without recalculating model decisions."""
    if comparison.get("schema_version") != REPORT_SCHEMA_VERSION:
        raise ComparisonReportError("Unsupported comparison schema version.")
    if decision.get("decision_status") != "selected_for_next_integration":
        raise ComparisonReportError("A completed model decision is required.")
    if errors.get("interpretation_boundary") != "descriptive_no_causal_claims":
        raise ComparisonReportError("Error evidence boundary is invalid.")
    rows = comparison.get("rows", [])
    summaries = errors.get("candidate_summaries", [])
    if len(rows) != 4 or len(summaries) != 4:
        raise ComparisonReportError("Report inputs must cover four candidates.")
    if comparison.get("dataset_sha256") != decision.get("dataset_sha256"):
        raise ComparisonReportError("Decision and comparison datasets differ.")
    if comparison.get("dataset_sha256") != split_manifest.get("dataset_sha256"):
        raise ComparisonReportError("Split and comparison datasets differ.")
    split = split_manifest.get("split", {})
    if (
        split.get("strategy") != comparison.get("split_strategy")
        or int(split.get("test_rows", -1)) != int(rows[0].get("test_rows", -2))
    ):
        raise ComparisonReportError("Split evidence conflicts with comparison rows.")

    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "module": "model_comparison",
        "report_status": "learning_evidence_only",
        "experiment": {
            "dataset_sha256": comparison["dataset_sha256"],
            "split_strategy": comparison["split_strategy"],
            "target": comparison["target"],
            "target_unit": comparison["target_unit"],
            "train_rows": int(split["train_rows"]),
            "test_rows": int(split["test_rows"]),
        },
        "comparison": {
            "primary_metric": comparison["primary_metric"],
            "diagnostic_metrics": comparison["diagnostic_metrics"],
            "policy": comparison["policy"],
            "rows": rows,
        },
        "error_review": {
            "prediction_rows": errors["prediction_rows"],
            "residual_definition": errors["residual_definition"],
            "interpretation_boundary": errors["interpretation_boundary"],
            "candidate_summaries": summaries,
        },
        "decision": decision,
        "decision_cards": build_decision_cards(comparison, decision),
        "limitations": [
            "The source contains 18 synthetic observations.",
            "Only one six-row chronological holdout was evaluated.",
            "No cross-validation or external validation was performed.",
            "The selected candidate is not production ready.",
        ],
    }


def _markdown_report(report: dict[str, Any]) -> str:
    rows = [
        "# Sprint 2 Model Comparison Report",
        "",
        "## Decision summary",
        "",
        (
            f"- Metric leader: **{report['decision']['measurement_leader']['model_name']}**."
        ),
        (
            "- Selected for next integration: "
            f"**{report['decision']['selected_candidate']['model_name']}**."
        ),
        "- Production status: **not production ready**.",
        "",
        "## Comparable metrics",
        "",
        "| Rank | Candidate | MAE | RMSE | R² | Improvement vs baseline |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    for candidate in report["comparison"]["rows"]:
        rows.append(
            "| {rank} | {name} | {mae:.4f} | {rmse:.4f} | {r2:.4f} | "
            "{improvement:+.2f}% |".format(
                rank=candidate["mae_rank"],
                name=candidate["model_name"],
                mae=candidate["mae_units"],
                rmse=candidate["rmse_units"],
                r2=candidate["r2_contextual"],
                improvement=candidate["mae_improvement_vs_baseline_percent"],
            )
        )
    rows.extend(["", "## Decision Cards", ""])
    for card in report["decision_cards"]:
        rows.extend(
            [
                f"### {card['eyebrow']} — {card['title']}",
                "",
                f"**{card['primary_metric']['label']}:** "
                f"{card['primary_metric']['value']:.4f} "
                f"{card['primary_metric']['unit']}",
                "",
                card["summary"],
                "",
                *[f"- {reason}" for reason in card["reasons"]],
                "",
                f"Limitation: {card['limitation']}",
                "",
            ]
        )
    rows.extend(
        [
            "## Reuse boundary",
            "",
            "Backend may read the JSON report as validated evidence. It must not",
            "train models, recompute metrics or alter the decision during a request.",
            "",
            "## Limitations",
            "",
            *[f"- {item}" for item in report["limitations"]],
            "",
        ]
    )
    return "\n".join(rows)


def run_comparison_report(project_root: Path) -> dict[str, Any]:
    """Generate official Day 69 JSON, Markdown and Decision Card artifacts."""
    output_root = project_root / "reports" / "outputs" / "model-comparison"
    comparison = json.loads(
        (output_root / "comparison_table.json").read_text(encoding="utf-8")
    )
    errors = json.loads(
        (output_root / "error_analysis.json").read_text(encoding="utf-8")
    )
    decision = json.loads(
        (output_root / "model_decision.json").read_text(encoding="utf-8")
    )
    split_manifest = json.loads(
        (output_root / "split_manifest.json").read_text(encoding="utf-8")
    )
    report = build_comparison_report(
        comparison,
        errors,
        decision,
        split_manifest,
    )
    (output_root / "model_comparison_report.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output_root / "model_comparison_report.md").write_text(
        _markdown_report(report),
        encoding="utf-8",
        newline="\n",
    )
    card_root = project_root / "reports" / "decision-cards" / "model-comparison"
    card_root.mkdir(parents=True, exist_ok=True)
    (card_root / "decision_cards.json").write_text(
        json.dumps(
            {
                "schema_version": REPORT_SCHEMA_VERSION,
                "card_count": len(report["decision_cards"]),
                "cards": report["decision_cards"],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return report


def main() -> None:
    """Generate the reusable comparison report."""
    project_root = Path(__file__).resolve().parents[4]
    report = run_comparison_report(project_root)
    print("Model Comparison report generated")
    print(f"Decision Cards: {len(report['decision_cards'])}")
    print(
        "Selected for next integration: "
        f"{report['decision']['selected_candidate']['model_name']}"
    )
    print("Production status: not production ready")


if __name__ == "__main__":
    main()
