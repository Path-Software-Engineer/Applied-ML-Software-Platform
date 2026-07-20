"""Readable Day 67 check for the frozen model decision."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "model-comparison" / "src"
sys.path.insert(0, str(MODULE_SRC))

from model_comparison.decision import run_model_decision  # noqa: E402


def main() -> None:
    """Regenerate and validate official selection evidence."""
    decision = run_model_decision(PROJECT_ROOT)
    lab_output = (
        PROJECT_ROOT
        / "labs"
        / "tec-labs"
        / "tec-model-decision-lab"
        / "outputs"
        / "metric_leader_vs_selected_candidate.md"
    )

    assert decision["measurement_leader"]["model_id"] == "gradient_boosting"
    assert decision["selected_candidate"]["model_id"] == "random_forest"
    assert not decision["measurement_leader_is_selected_candidate"]
    assert len(decision["practically_equivalent_candidates"]) == 2
    assert decision["decision_status"] == "selected_for_next_integration"
    assert decision["production_status"] == "not_production_ready"
    assert decision["stability_evidence"]["status"] == "not_assessed"
    assert decision["error_review"]["status"] == "reviewed"
    assert lab_output.is_file() and lab_output.stat().st_size > 0

    print("OK - Sprint 2 Day 67 model decision check passed")
    print("Measurement leader: Gradient Boosting")
    print("Selected for next integration: Random Forest")
    print("Decision rule: practical equivalence plus lower complexity")
    print("Production status: not production ready")


if __name__ == "__main__":
    main()
