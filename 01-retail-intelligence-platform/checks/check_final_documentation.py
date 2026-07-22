"""Validate Day 144 final documentation and story traceability."""

from __future__ import annotations

from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    users = (PROJECT_ROOT / "docs/user-stories.md").read_text(encoding="utf-8")
    technical = (PROJECT_ROOT / "docs/technical-stories.md").read_text(encoding="utf-8")
    architecture = (PROJECT_ROOT / "docs/architecture.md").read_text(encoding="utf-8")
    release = (PROJECT_ROOT / "docs/releases/v1.0.0-retail-intelligence-platform.md").read_text(encoding="utf-8")
    runbook = (PROJECT_ROOT / "docs/runbook.md").read_text(encoding="utf-8")
    changelog = (PROJECT_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    user_ids = set(re.findall(r"US-S3-\d{3}", users))
    referenced = set(re.findall(r"US-S3-\d{3}", technical))
    assert user_ids == {f"US-S3-{number:03d}" for number in range(1, 7)}
    assert referenced <= user_ids
    assert "Planned for global Days 127" not in technical
    assert "Planned for global Days 130" not in technical
    assert "Planned for global Days 128" not in users
    assert "Planned for global Days 130" not in users

    evidence_paths = re.findall(r"`([^`]+(?:\.py|\.json|\.md|/))`", technical)
    repository_roots = (
        "ai-services/",
        "backend/",
        "checks/",
        "data/",
        "docs/",
        "frontend/",
        "reports/",
        "scripts/",
        "tests/",
    )
    for relative in (path for path in evidence_paths if path.startswith(repository_roots)):
        assert (PROJECT_ROOT / relative).exists(), f"Missing technical-story evidence: {relative}"
    for phrase in ("Final Inventory Decision flow", "Final platform integration"):
        assert phrase in architecture
    for phrase in ("Clean setup", "Regenerate evidence", "Start locally", "Validate", "Shutdown"):
        assert phrase in runbook
    assert "release candidate" in release
    assert "v1.0.0-retail-intelligence-platform" in changelog

    print("OK - Sprint 3 Day 144 final documentation check passed")
    print("Sprint 3 User Stories / Technical Stories: 6 / 8")
    print("Architecture, runbook, changelog and release draft: traceable")


if __name__ == "__main__":
    main()
