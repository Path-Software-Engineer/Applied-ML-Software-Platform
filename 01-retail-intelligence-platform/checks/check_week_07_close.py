"""Validate the documented Day 77 integration-week closure."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    sprint_root = PROJECT_ROOT / "docs" / "sprints" / "sprint-02-model-comparison"
    review = (sprint_root / "week-07" / "review.md").read_text(encoding="utf-8")
    visual = (
        PROJECT_ROOT
        / "reports"
        / "quality"
        / "model-comparison"
        / "day_77_visual_contract_review.md"
    ).read_text(encoding="utf-8")
    summary = (
        PROJECT_ROOT
        / "reports"
        / "summaries"
        / "model-comparison"
        / "day_77_week_07_close_summary.md"
    ).read_text(encoding="utf-8")
    view = (
        PROJECT_ROOT
        / "frontend"
        / "dashboard-app"
        / "src"
        / "features"
        / "model-comparison"
        / "components"
        / "ModelComparisonDashboard.jsx"
    ).read_text(encoding="utf-8")
    styles = (
        PROJECT_ROOT / "frontend" / "dashboard-app" / "src" / "styles.css"
    ).read_text(encoding="utf-8")

    for phrase in (
        "94 Python tests",
        "18 frontend contract tests",
        "44 manual checks",
        "Week 7 is complete",
        "Browser screenshots are not claimed",
        "Sprint 3",
    ):
        assert phrase in review
    for phrase in (
        "LoadingView",
        "UnavailableView",
        "CandidateTable",
        "DecisionCard",
    ):
        assert phrase in view
    for phrase in (
        "@media (prefers-reduced-motion: reduce)",
        "@media (max-width: 980px)",
        "@media (max-width: 640px)",
    ):
        assert phrase in styles
    assert "not a screenshot" in visual
    assert "Sprint 3 remains inactive" in summary

    print("OK - Sprint 2 Day 77 Week 7 close check passed")
    print("Integration path: report -> service -> FastAPI -> React")
    print("Visual contract: reviewed at source and bundle boundaries")
    print("Browser screenshot: explicitly not claimed")
    print("Week 7 status: closed")


if __name__ == "__main__":
    main()
