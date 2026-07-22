"""Validate Sprint 3 review, deployment and release-readiness boundaries."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (PROJECT_ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    deployment = read("docs/deployment-readiness.md")
    review = read("docs/sprints/sprint-03-inventory-decision/sprint-review.md")
    retrospective = read("docs/sprints/sprint-03-inventory-decision/retrospective.md")
    week = read("docs/sprints/sprint-03-inventory-decision/week-13/review.md")

    for phrase in (
        "not a production deployment approval",
        "empty placeholders",
        "No credentials",
        "Production gaps",
    ):
        assert phrase in deployment
    for phrase in (
        "181 Python",
        "31 frontend",
        "84 manual",
        "accepted limitation",
        "97 units",
    ):
        assert phrase in review
    for phrase in (
        "What worked well",
        "Challenges",
        "Improvements adopted",
        "Carry-forward",
    ):
        assert phrase in retrospective
    assert "No new feature is authorized" in week
    assert "Day 147" in week

    assert (PROJECT_ROOT / "docker-compose.yml").stat().st_size == 0
    assert not list((PROJECT_ROOT / "deployment").rglob("Dockerfile"))

    print("OK - Sprint 3 Day 146 release readiness check passed")
    print("Review and retrospective: complete")
    print("Deployment status: reproducible local release | production excluded")
    print("Accepted visual limitation: explicit")


if __name__ == "__main__":
    main()
