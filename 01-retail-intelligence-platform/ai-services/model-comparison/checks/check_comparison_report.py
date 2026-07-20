"""Readable Day 69 check for the reusable comparison report."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "model-comparison" / "src"
sys.path.insert(0, str(MODULE_SRC))

from model_comparison.comparison_report import run_comparison_report  # noqa: E402


def main() -> None:
    report = run_comparison_report(PROJECT_ROOT)
    output_root = PROJECT_ROOT / "reports" / "outputs" / "model-comparison"
    cards_path = (
        PROJECT_ROOT
        / "reports"
        / "decision-cards"
        / "model-comparison"
        / "decision_cards.json"
    )
    cards = json.loads(cards_path.read_text(encoding="utf-8"))
    lab = (
        PROJECT_ROOT
        / "labs"
        / "docs-labs"
        / "docs-model-comparison-report-template-lab"
        / "outputs"
        / "template_evaluation.md"
    )

    assert report["schema_version"] == "1.0"
    assert report["module"] == "model_comparison"
    assert len(report["comparison"]["rows"]) == 4
    assert len(report["error_review"]["candidate_summaries"]) == 4
    assert len(report["decision_cards"]) == 3
    assert cards["card_count"] == 3
    assert report["decision"]["selected_candidate"]["model_id"] == "random_forest"
    assert report["report_status"] == "learning_evidence_only"
    assert (output_root / "model_comparison_report.md").is_file()
    assert lab.is_file() and lab.stat().st_size > 0

    print("OK - Sprint 2 Day 69 comparison report check passed")
    print("Comparable candidates: 4")
    print("Decision Cards: 3")
    print("Backend-ready report schema: 1.0")
    print("Production status: not production ready")


if __name__ == "__main__":
    main()
