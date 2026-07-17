"""Readable cross-layer check for Sprint 1 Day 27 hardening."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FILES = (
    "backend/api/app/services/demand_figure_service.py",
    "frontend/dashboard-app/tests/demandSummaryApi.test.js",
    "docs/sprints/sprint-01-demand-insight/week-04/review.md",
    "docs/sprints/sprint-01-demand-insight/retrospective.md",
    "reports/summaries/demand-insight/sprint_01_hardening_summary.md",
)


def main() -> None:
    missing = [
        relative_path
        for relative_path in EXPECTED_FILES
        if not (PROJECT_ROOT / relative_path).is_file()
    ]
    if missing:
        raise AssertionError(f"Missing hardening evidence: {missing}")

    package = json.loads(
        (PROJECT_ROOT / "frontend/dashboard-app/package.json").read_text(
            encoding="utf-8"
        )
    )
    scripts = package.get("scripts", {})
    if "test" not in scripts or "check" not in scripts:
        raise AssertionError("Frontend test and check scripts must be declared.")

    figure_service = (
        PROJECT_ROOT / "backend/api/app/services/demand_figure_service.py"
    ).read_text(encoding="utf-8")
    if "MAX_FIGURE_BYTES" not in figure_service or "PNG_SIGNATURE" not in figure_service:
        raise AssertionError("Figure size and signature boundaries are missing.")

    route = (
        PROJECT_ROOT / "backend/api/app/routes/demand_summary.py"
    ).read_text(encoding="utf-8")
    if "X-Content-Type-Options" not in route or "nosniff" not in route:
        raise AssertionError("Figure response hardening header is missing.")

    technical_stories = (
        PROJECT_ROOT / "docs/technical-stories.md"
    ).read_text(encoding="utf-8")
    if "TS-S1-015" not in technical_stories:
        raise AssertionError("Day 27 Technical Story is missing.")

    print("OK - Sprint 1 Day 27 hardening check passed")
    print(f"Cross-layer evidence files: {len(EXPECTED_FILES)}")
    print("Frontend contract tests: configured")
    print("Figure security boundaries: confirmed")
    print("Week 4 review and Sprint retrospective: confirmed")


if __name__ == "__main__":
    main()
