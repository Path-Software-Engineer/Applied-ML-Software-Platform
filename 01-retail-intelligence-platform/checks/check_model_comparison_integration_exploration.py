"""Readable Day 71 check for the planned Model Comparison read flow."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    sprint_root = (
        PROJECT_ROOT / "docs" / "sprints" / "sprint-02-model-comparison"
    )
    exploration = (sprint_root / "week-07" / "exploration.md").read_text(
        encoding="utf-8"
    )
    plan = (sprint_root / "week-07" / "plan.md").read_text(encoding="utf-8")
    contract = (
        PROJECT_ROOT / "docs" / "model-comparison-read-contract.md"
    ).read_text(encoding="utf-8")
    user_stories = (PROJECT_ROOT / "docs" / "user-stories.md").read_text(
        encoding="utf-8"
    )
    technical_stories = (
        PROJECT_ROOT / "docs" / "technical-stories.md"
    ).read_text(encoding="utf-8")

    for phrase in (
        "loading",
        "connected",
        "unavailable",
        "backend/api/app/services",
        "frontend/dashboard-app",
        "must never train models",
    ):
        assert phrase in exploration
    for day in range(71, 78):
        assert f"| {day} |" in plan
    for phrase in (
        "GET /api/v1/model-comparisons/summary",
        '"schema_version": "1.0"',
        '"module": "model_comparison"',
        "exactly four unique candidates",
        "503 Service Unavailable",
    ):
        assert phrase in contract
    for story_id in ("US-S2-005", "US-S2-006"):
        assert story_id in user_stories
    for story_id in ("TS-S2-005", "TS-S2-006"):
        assert story_id in technical_stories

    print("OK - Sprint 2 Day 71 integration exploration check passed")
    print("Proposed endpoint: GET /api/v1/model-comparisons/summary")
    print("Frontend states: loading / connected / unavailable")
    print("Runtime implementation: deferred to Days 72-75")


if __name__ == "__main__":
    main()
