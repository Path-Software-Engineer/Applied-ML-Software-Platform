"""Readable Day 64 documentation check for Week 6 exploration."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    """Validate the frozen Week 6 decision boundary."""
    sprint_root = (
        PROJECT_ROOT / "docs" / "sprints" / "sprint-02-model-comparison"
    )
    exploration = sprint_root / "week-06" / "exploration.md"
    plan = sprint_root / "week-06" / "plan.md"
    summary = (
        PROJECT_ROOT
        / "reports"
        / "summaries"
        / "model-comparison"
        / "day_64_week_06_exploration_summary.md"
    )
    required = [exploration, plan, summary]
    assert all(path.is_file() and path.stat().st_size > 0 for path in required)

    exploration_text = exploration.read_text(encoding="utf-8")
    plan_text = plan.read_text(encoding="utf-8")
    for phrase in (
        "MAE",
        "RMSE",
        "R²",
        "0.25",
        "10%",
        "practically equivalent",
        "selected_for_next_integration",
        "None beyond deterministic repetition",
    ):
        assert phrase in exploration_text
    for day in range(64, 71):
        assert f"| {day} |" in plan_text
    assert "production deployment" in plan_text

    print("OK - Sprint 2 Day 64 Week 6 exploration check passed")
    print("Primary metric: MAE")
    print("Practical-equivalence tolerance: 0.25 units")
    print("Minimum baseline improvement: 10%")
    print("Stability evidence: explicitly unavailable")


if __name__ == "__main__":
    main()
