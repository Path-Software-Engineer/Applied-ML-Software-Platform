"""Controlled MAE-versus-RMSE sensitivity experiment."""

from __future__ import annotations

from pathlib import Path

from model_comparison.metrics import calculate_regression_metrics


def main() -> None:
    """Write a metric sensitivity comparison outside production outputs."""
    actual = [10, 10, 10, 10]
    spread_errors = [8, 12, 8, 12]
    concentrated_error = [10, 10, 10, 16]
    spread = calculate_regression_metrics(actual, spread_errors)
    concentrated = calculate_regression_metrics(actual, concentrated_error)
    output = Path(__file__).resolve().parents[1] / "outputs" / (
        "mae_rmse_comparison.md"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "\n".join(
            [
                "# MAE and RMSE Controlled Comparison",
                "",
                "| Error shape | MAE | RMSE |",
                "|---|---:|---:|",
                f"| Four spread misses | {spread.mae:.2f} | {spread.rmse:.2f} |",
                (
                    "| One concentrated miss | "
                    f"{concentrated.mae:.2f} | {concentrated.rmse:.2f} |"
                ),
                "",
                "RMSE reacts more strongly to the concentrated large error.",
                "MAE remains the primary Sprint 2 metric because it is directly",
                "readable in units; RMSE keeps large misses visible.",
                "",
                "These values are controlled lab evidence, not official model",
                "results.",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Model-metrics lab generated: {output}")


if __name__ == "__main__":
    main()
