"""Validate Day 78 scope freeze and Week 8 plan."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    week = (
        PROJECT_ROOT
        / "docs"
        / "sprints"
        / "sprint-02-model-comparison"
        / "week-08"
    )
    exploration = (week / "exploration.md").read_text(encoding="utf-8")
    plan = (week / "plan.md").read_text(encoding="utf-8")
    release_scope = (
        PROJECT_ROOT / "docs" / "model-comparison-release-scope.md"
    ).read_text(encoding="utf-8")

    for module in (
        "ai-services/model-comparison",
        "backend/api",
        "frontend/dashboard-app",
        "checks",
        "reports",
    ):
        assert module in exploration
    for day in range(78, 85):
        assert f"| {day} |" in plan
    for phrase in (
        "18 synthetic rows",
        "six-row chronological holdout",
        "Sprint 3 implementation",
        "mockups are never substituted",
    ):
        assert phrase in release_scope

    print("OK - Sprint 2 Day 78 Week 8 exploration check passed")
    print("Real modules inventoried: 5")
    print("Release scope: frozen through Day 84")
    print("Sprint 3 status: not started")


if __name__ == "__main__":
    main()
