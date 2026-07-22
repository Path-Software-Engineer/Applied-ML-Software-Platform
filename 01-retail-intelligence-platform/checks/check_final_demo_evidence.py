"""Validate the final demo package without accepting fabricated visual evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    evidence = PROJECT_ROOT / "reports" / "portfolio" / "retail-intelligence-platform"
    manifest = json.loads((evidence / "evidence_manifest.json").read_text(encoding="utf-8"))
    demo = (evidence / "demo-script.md").read_text(encoding="utf-8")
    readme = (evidence / "README.md").read_text(encoding="utf-8")

    assert manifest["schema_version"] == "1.0"
    assert manifest["release_candidate"] == "v1.0.0-retail-intelligence-platform"
    assert manifest["evidence_status"] == "runtime_verified_visual_capture_blocked"
    assert [stage["route"] for stage in manifest["stages"]] == [
        "#demand-insight",
        "#model-comparison",
        "#inventory-decision",
    ]
    for artifact in manifest["canonical_artifacts"]:
        path = PROJECT_ROOT / artifact["path"]
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == artifact["sha256"]

    expected_views = {
        ("desktop", 1440, 900),
        ("tablet", 768, 1024),
        ("mobile", 390, 844),
    }
    assert {
        (view["name"], view["width"], view["height"])
        for view in manifest["required_views"]
    } == expected_views
    for view in manifest["required_views"]:
        assert view["path"] is None
        assert view["status"] == "blocked_by_browser_policy"

    combined = f"{readme}\n{demo}\n{json.dumps(manifest)}".lower()
    for forbidden in ("password=", "secret=", "api_key=", "bearer "):
        assert forbidden not in combined
    assert "no screenshot, mockup or browser approval is claimed" in readme.lower()
    for stage in ("Demand Insight", "Model Comparison", "Inventory Decision"):
        assert stage in demo

    print("OK - Sprint 3 Day 145 final demo evidence check passed")
    print("Canonical artifact hashes: 3 confirmed")
    print("Demo stages: Demand Insight | Model Comparison | Inventory Decision")
    print("Visual capture status: blocked and honestly recorded")


if __name__ == "__main__":
    main()
