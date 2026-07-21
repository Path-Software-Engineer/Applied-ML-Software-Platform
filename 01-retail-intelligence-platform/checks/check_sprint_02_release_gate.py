"""Validate the Day 84 release gate and declared visual limitation."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    gate = (
        PROJECT_ROOT
        / "reports/quality/model-comparison/day_84_release_gate.md"
    ).read_text(encoding="utf-8")
    summary = (
        PROJECT_ROOT
        / "reports/summaries/model-comparison/day_84_release_gate_summary.md"
    ).read_text(encoding="utf-8")
    release = (
        PROJECT_ROOT / "docs/releases/v0.2.0-sprint-02-model-comparison.md"
    ).read_text(encoding="utf-8")
    manifest = json.loads(
        (
            PROJECT_ROOT
            / "reports/portfolio/model-comparison/evidence_manifest.json"
        ).read_text(encoding="utf-8")
    )

    for phrase in (
        "PASSED — release authorized with a known visual limitation",
        "96 Python",
        "18 frontend",
        "51 manual repository checks",
        "release sequence uses",
        "Sprint 2 closes at Day 84",
    ):
        assert phrase in gate
    assert "RELEASED — visual capture remains a documented limitation" in release
    assert manifest["evidence_status"] == "blocked_visual_capture"
    assert len(manifest["required_views"]) == 3
    assert all(view["path"] is None for view in manifest["required_views"])
    assert "Sprint 3 remains unstarted" in summary

    print("OK - Sprint 2 Day 84 release gate passed")
    print("Software gate: passed")
    print("Visual capture: accepted documented limitation")
    print("Release branch / main merge / tag: authorized")
    print("Sprint 3: not started")


if __name__ == "__main__":
    main()
