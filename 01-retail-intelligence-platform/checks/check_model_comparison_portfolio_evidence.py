"""Validate Day 82 portfolio evidence without accepting fabricated images."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    portfolio = PROJECT_ROOT / "reports" / "portfolio" / "model-comparison"
    manifest = json.loads(
        (portfolio / "evidence_manifest.json").read_text(encoding="utf-8")
    )
    readme = (portfolio / "README.md").read_text(encoding="utf-8")

    assert manifest["schema_version"] == "1.0"
    assert manifest["release_candidate"] == (
        "v0.2.0-sprint-02-model-comparison"
    )
    assert manifest["evidence_status"] == "blocked_visual_capture"
    for artifact in manifest["canonical_artifacts"]:
        path = PROJECT_ROOT / artifact["path"]
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == artifact["sha256"]
    expected_views = {
        ("desktop", 1440, 900),
        ("tablet", 768, 1024),
        ("mobile", 390, 844),
    }
    actual_views = {
        (view["name"], view["width"], view["height"])
        for view in manifest["required_views"]
    }
    assert actual_views == expected_views
    for view in manifest["required_views"]:
        assert view["path"] is None
        assert view["status"] == "blocked_by_browser_policy"
    assert "No screenshot, mockup or browser approval is claimed" in readme
    assert "known release limitation" in readme

    print("OK - Sprint 2 Day 82 portfolio evidence check passed")
    print("Canonical artifact hashes: 4 confirmed")
    print("Required viewports: desktop | tablet | mobile")
    print("Visual capture status: unavailable and honestly recorded")


if __name__ == "__main__":
    main()
