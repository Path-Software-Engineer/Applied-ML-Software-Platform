"""Controlled residual-direction experiment."""

from __future__ import annotations

from pathlib import Path


def main() -> None:
    """Write a residual sign demonstration outside official outputs."""
    observations = [
        {"actual": 12, "predicted": 9},
        {"actual": 12, "predicted": 15},
    ]
    rows = []
    for observation in observations:
        residual = observation["actual"] - observation["predicted"]
        direction = "under-prediction" if residual > 0 else "over-prediction"
        rows.append(
            "| {actual} | {predicted} | {residual:+d} | {absolute} | {direction} |".format(
                actual=observation["actual"],
                predicted=observation["predicted"],
                residual=residual,
                absolute=abs(residual),
                direction=direction,
            )
        )
    output = Path(__file__).resolve().parents[1] / "outputs" / (
        "residual_direction_lab.md"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "\n".join(
            [
                "# Residual Direction Lab",
                "",
                "| Actual | Predicted | Residual | Absolute error | Direction |",
                "|---:|---:|---:|---:|---|",
                *rows,
                "",
                "Equal absolute errors can describe opposite prediction",
                "directions. The sign is descriptive and does not explain why",
                "the error occurred.",
                "",
                "These are controlled lab values, not official model results.",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Model-error-analysis lab generated: {output}")


if __name__ == "__main__":
    main()
