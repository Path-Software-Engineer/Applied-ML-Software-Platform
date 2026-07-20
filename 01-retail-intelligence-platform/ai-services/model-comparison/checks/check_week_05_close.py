"""Readable Day 63 check for the Sprint 2 Week 5 close."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "model-comparison" / "src"
sys.path.insert(0, str(MODULE_SRC))

from model_comparison.comparison import run_initial_comparison  # noqa: E402


def main() -> None:
    """Regenerate and validate Week 5 closure evidence."""
    table = run_initial_comparison(PROJECT_ROOT)
    output_root = PROJECT_ROOT / "reports" / "outputs" / "model-comparison"
    payload = json.loads(
        (output_root / "initial_results.json").read_text(encoding="utf-8")
    )
    required = [
        PROJECT_ROOT
        / "docs"
        / "sprints"
        / "sprint-02-model-comparison"
        / "week-05"
        / "review.md",
        PROJECT_ROOT
        / "labs"
        / "tec-labs"
        / "tec-baseline-vs-model-lab"
        / "README.md",
        PROJECT_ROOT
        / "labs"
        / "tec-labs"
        / "tec-baseline-vs-model-lab"
        / "outputs"
        / "baseline_vs_model_lab.md",
        PROJECT_ROOT
        / "reports"
        / "summaries"
        / "model-comparison"
        / "day_63_week_05_close_summary.md",
    ]

    assert len(table) == 4
    assert table["model_id"].nunique() == 4
    assert table["test_rows"].eq(6).all()
    assert table["production_status"].eq("learning_evidence_only").all()
    assert payload["comparison_status"] == "observed_metrics_not_selection"
    assert len(payload["limitations"]) == 4
    assert all(path.is_file() and path.stat().st_size > 0 for path in required)

    print("OK - Sprint 2 Day 63 Week 5 close check passed")
    print("Comparable candidates: 4")
    print("Official test rows per candidate: 6")
    print("Selection status: deferred to Week 6")
    print("Week 5 laboratory: separated from production module")


if __name__ == "__main__":
    main()
