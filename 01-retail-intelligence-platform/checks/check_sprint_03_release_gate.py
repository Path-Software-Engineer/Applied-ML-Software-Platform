"""Authorize the final release mechanics from versioned, validated evidence."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    package = json.loads(
        (PROJECT_ROOT / "frontend/dashboard-app/package.json").read_text(encoding="utf-8")
    )
    lock = json.loads(
        (PROJECT_ROOT / "frontend/dashboard-app/package-lock.json").read_text(encoding="utf-8")
    )
    sprint = (PROJECT_ROOT / "docs/sprints/sprint-03-inventory-decision/README.md").read_text(encoding="utf-8")
    release = (PROJECT_ROOT / "docs/releases/v1.0.0-retail-intelligence-platform.md").read_text(encoding="utf-8")
    changelog = (PROJECT_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    manifest = json.loads(
        (PROJECT_ROOT / "reports/portfolio/retail-intelligence-platform/evidence_manifest.json").read_text(encoding="utf-8")
    )

    assert package["version"] == "1.0.0"
    assert lock["version"] == "1.0.0"
    assert lock["packages"][""]["version"] == "1.0.0"
    assert "Week 13 | 141–147 | final integration, evidence and release | completed" in sprint
    assert any(
        status in release
        for status in (
            "release-ready — Gitflow mechanics authorized",
            "Status: **released**",
        )
    )
    assert "85 manual checks passed" in release
    assert "85 manual checks passed at the final release gate" in changelog
    assert manifest["release_candidate"] == "v1.0.0-retail-intelligence-platform"
    assert manifest["evidence_status"] == "runtime_verified_visual_capture_blocked"
    assert not list(PROJECT_ROOT.rglob("*.env"))

    print("OK - Sprint 3 Day 147 final release gate passed")
    print("Version: 1.0.0 | Sprint 3 Week 13: completed")
    print("Release branch, main merge, annotated tag and develop sync: authorized")
    print("Production and screenshot claims: not authorized")


if __name__ == "__main__":
    main()
