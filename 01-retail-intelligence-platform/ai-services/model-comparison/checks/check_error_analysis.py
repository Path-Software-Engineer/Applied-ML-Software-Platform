"""Readable Day 66 check for prediction-level error evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "model-comparison" / "src"
sys.path.insert(0, str(MODULE_SRC))

from model_comparison.error_analysis import run_error_analysis  # noqa: E402


def main() -> None:
    """Regenerate and validate official residual evidence."""
    analysis, summaries = run_error_analysis(PROJECT_ROOT)
    output_root = PROJECT_ROOT / "reports" / "outputs" / "model-comparison"
    payload = json.loads(
        (output_root / "error_analysis.json").read_text(encoding="utf-8")
    )
    lab_output = (
        PROJECT_ROOT
        / "labs"
        / "tec-labs"
        / "tec-model-error-analysis-lab"
        / "outputs"
        / "residual_direction_lab.md"
    )

    assert len(analysis) == 24
    assert analysis.groupby("model_id").size().eq(6).all()
    assert len(summaries) == 4
    assert all(item["largest_error"]["absolute_error"] >= 0 for item in summaries)
    assert payload["residual_definition"] == "actual_units - predicted_units"
    assert payload["interpretation_boundary"] == "descriptive_no_causal_claims"
    assert lab_output.is_file() and lab_output.stat().st_size > 0

    largest = analysis.sort_values("absolute_error", ascending=False).iloc[0]
    print("OK - Sprint 2 Day 66 error analysis check passed")
    print("Validated prediction rows: 24")
    print(
        f"Largest observed error: {largest['model_name']} / "
        f"{largest['product_name']} / {largest['absolute_error']:.4f} units"
    )
    print("Interpretation boundary: descriptive, no causal claims")


if __name__ == "__main__":
    main()
