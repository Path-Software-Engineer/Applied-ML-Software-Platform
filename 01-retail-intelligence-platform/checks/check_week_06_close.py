"""Readable Day 70 check for the completed Model Comparison decision week."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    """Validate Week 6 evidence, traceability and honest closure language."""
    sprint_root = (
        PROJECT_ROOT / "docs" / "sprints" / "sprint-02-model-comparison"
    )
    report = json.loads(
        (
            PROJECT_ROOT
            / "reports"
            / "outputs"
            / "model-comparison"
            / "model_comparison_report.json"
        ).read_text(encoding="utf-8")
    )
    cards = json.loads(
        (
            PROJECT_ROOT
            / "reports"
            / "decision-cards"
            / "model-comparison"
            / "decision_cards.json"
        ).read_text(encoding="utf-8")
    )
    review = (sprint_root / "week-06" / "review.md").read_text(encoding="utf-8")
    summary = (
        PROJECT_ROOT
        / "reports"
        / "summaries"
        / "model-comparison"
        / "day_70_week_06_close_summary.md"
    ).read_text(encoding="utf-8")
    decisions = (PROJECT_ROOT / "docs" / "decisions.md").read_text(
        encoding="utf-8"
    )
    user_stories = (PROJECT_ROOT / "docs" / "user-stories.md").read_text(
        encoding="utf-8"
    )
    technical_stories = (
        PROJECT_ROOT / "docs" / "technical-stories.md"
    ).read_text(encoding="utf-8")

    assert report["schema_version"] == "1.0"
    assert len(report["comparison"]["rows"]) == 4
    assert len(report["decision_cards"]) == 3
    assert cards["card_count"] == 3
    assert report["decision"]["selected_candidate"]["model_id"] == "random_forest"
    assert report["decision"]["production_status"] == "not_production_ready"
    for phrase in (
        "83 Python tests",
        "7 frontend contract tests",
        "37 manual checks",
        "Week 6 is complete",
        "read-only integration",
    ):
        assert phrase in review
    assert "learning-only" in summary
    assert "Decision 042" in decisions
    for story_id in ("US-S2-001", "US-S2-002", "US-S2-003", "US-S2-004"):
        assert story_id in user_stories
    for story_id in ("TS-S2-001", "TS-S2-002", "TS-S2-003", "TS-S2-004"):
        assert story_id in technical_stories

    print("OK - Sprint 2 Day 70 Week 6 close check passed")
    print("Comparable candidates: 4")
    print("Decision Cards: 3")
    print("Selected for next integration: Random Forest")
    print("Week 6 status: closed")


if __name__ == "__main__":
    main()
