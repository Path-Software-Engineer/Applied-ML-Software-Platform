"""Validate Day 83 review, retrospective and blocked release notes."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SPRINT = PROJECT_ROOT / "docs/sprints/sprint-02-model-comparison"


def main() -> None:
    review = (SPRINT / "sprint-review.md").read_text(encoding="utf-8")
    retrospective = (SPRINT / "retrospective.md").read_text(encoding="utf-8")
    week_review = (SPRINT / "week-08/review.md").read_text(encoding="utf-8")
    release = (
        PROJECT_ROOT / "docs/releases/v0.2.0-sprint-02-model-comparison.md"
    ).read_text(encoding="utf-8")
    summary = (
        PROJECT_ROOT
        / "reports/summaries/model-comparison/day_83_sprint_review_summary.md"
    ).read_text(encoding="utf-8")

    for phrase in (
        "96 Python",
        "18 frontend",
        "50 manual checks",
        "real desktop, tablet and mobile captures",
        "Sprint 3 is registered",
    ):
        assert phrase in review
    assert "portfolio manifest" in retrospective
    assert "Week 8 remains open at Day 83" in week_review
    assert "BLOCKED — visual acceptance incomplete" in release
    assert "Do not merge a release branch" in release
    assert "must not merge to `main`" in summary

    print("OK - Sprint 2 Day 83 review and release-readiness check passed")
    print("Software acceptance: passed")
    print("Visual acceptance: blocked")
    print("Release notes: prepared | Sprint 3: not started")


if __name__ == "__main__":
    main()
