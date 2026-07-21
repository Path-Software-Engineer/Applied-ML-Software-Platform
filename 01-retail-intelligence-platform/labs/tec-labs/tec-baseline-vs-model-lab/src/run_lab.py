"""Controlled baseline-versus-model learning experiment."""

from __future__ import annotations

from pathlib import Path

from model_comparison.metrics import calculate_regression_metrics


def main() -> None:
    """Generate a small lab note without touching official model evidence."""
    actual = [10, 12, 14, 16]
    baseline = [11, 11, 11, 11]
    candidate = [11, 13, 13, 15]
    baseline_metrics = calculate_regression_metrics(actual, baseline)
    candidate_metrics = calculate_regression_metrics(actual, candidate)
    output = Path(__file__).resolve().parents[1] / "outputs" / (
        "baseline_vs_model_lab.md"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "\n".join(
            [
                "# Baseline versus Model Lab Output",
                "",
                "| Controlled candidate | MAE | RMSE |",
                "|---|---:|---:|",
                (
                    "| Mean-style reference | "
                    f"{baseline_metrics.mae:.2f} | {baseline_metrics.rmse:.2f} |"
                ),
                (
                    "| Hypothetical model | "
                    f"{candidate_metrics.mae:.2f} | {candidate_metrics.rmse:.2f} |"
                ),
                "",
                "A learned candidate adds value only when it improves a relevant",
                "baseline under the same observations and metric definitions.",
                "These controlled values are not official Sprint 2 results.",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Baseline-versus-model lab generated: {output}")


if __name__ == "__main__":
    main()
