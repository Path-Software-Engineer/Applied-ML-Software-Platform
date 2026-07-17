"""Readable release-readiness check for the official Sprint 1 close."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RELEASE_ID = "v0.1.0-sprint-01-demand-insight"
EXPECTED_FILES = (
    "CHANGELOG.md",
    "docs/releases/v0.1.0-sprint-01-demand-insight.md",
    "docs/sprints/sprint-01-demand-insight/README.md",
    "docs/sprints/sprint-01-demand-insight/week-04/review.md",
    "docs/sprints/sprint-01-demand-insight/retrospective.md",
    "reports/summaries/demand-insight/sprint_01_close_summary.md",
)
VERSIONED_DOCUMENTS = (
    "docs/releases/v0.1.0-sprint-01-demand-insight.md",
    "docs/sprints/sprint-01-demand-insight/README.md",
    "docs/sprints/sprint-01-demand-insight/week-04/review.md",
    "reports/summaries/demand-insight/sprint_01_close_summary.md",
)
REQUIRED_EVIDENCE = (
    "293",
    "747.65",
    "Bread",
    "105",
    "Rice 1kg",
    "220.50",
    "2026-01-06",
    "45",
    "2026-01-08",
    "99.30",
    "16.28",
    "5.42",
)


def read(relative_path: str) -> str:
    path = PROJECT_ROOT / relative_path
    if not path.is_file():
        raise AssertionError(f"Missing Sprint 1 close evidence: {relative_path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    documents = {relative_path: read(relative_path) for relative_path in EXPECTED_FILES}
    release_notes = documents[
        "docs/releases/v0.1.0-sprint-01-demand-insight.md"
    ]
    close_summary = documents[
        "reports/summaries/demand-insight/sprint_01_close_summary.md"
    ]
    sprint_readme = documents[
        "docs/sprints/sprint-01-demand-insight/README.md"
    ]
    technical_stories = read("docs/technical-stories.md")
    decisions = read("docs/decisions.md")

    for relative_path in VERSIONED_DOCUMENTS:
        if RELEASE_ID not in documents[relative_path]:
            raise AssertionError(
                f"Release identifier missing from close evidence: {relative_path}"
            )

    missing_values = [
        value
        for value in REQUIRED_EVIDENCE
        if value not in release_notes or value not in close_summary
    ]
    if missing_values:
        raise AssertionError(f"Release evidence is incomplete: {missing_values}")

    if "TS-S1-016" not in technical_stories:
        raise AssertionError("Day 28 Technical Story is missing.")
    if "Decision 028" not in decisions:
        raise AssertionError("Day 28 architecture decision is missing.")
    if "Sprint 2 remains" not in sprint_readme:
        raise AssertionError("The inactive Sprint 2 boundary is not explicit.")

    print("OK - Sprint 1 Day 28 release-readiness check passed")
    print(f"Release identifier: {RELEASE_ID}")
    print(f"Closure evidence files: {len(EXPECTED_FILES)}")
    print("Technical Story and architecture decision: confirmed")
    print("Sprint 2 boundary: inactive")


if __name__ == "__main__":
    main()
