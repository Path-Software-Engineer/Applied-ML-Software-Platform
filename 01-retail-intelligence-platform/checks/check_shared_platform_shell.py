"""Validate Day 79 frontend responsibility cleanup."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND = PROJECT_ROOT / "frontend" / "dashboard-app" / "src"


def main() -> None:
    shared_path = FRONTEND / "shared" / "components" / "PlatformShell.jsx"
    demand_path = (
        FRONTEND / "features" / "demand-summary" / "components" / "DemandDashboard.jsx"
    )
    comparison_path = (
        FRONTEND
        / "features"
        / "model-comparison"
        / "components"
        / "ModelComparisonDashboard.jsx"
    )
    shared = shared_path.read_text(encoding="utf-8")
    demand = demand_path.read_text(encoding="utf-8")
    comparison = comparison_path.read_text(encoding="utf-8")

    for phrase in (
        "export function LogoMark",
        "export function PlatformShell",
        "function PlatformHeader",
        'aria-label="Primary navigation"',
        'role="status"',
    ):
        assert phrase in shared
    for feature in (demand, comparison):
        assert "<PlatformShell" in feature
        assert '<aside className="sidebar' not in feature
        assert "function LogoMark" not in feature
        assert "function PlatformHeader" not in feature
    assert 'homeHref="#top"' in demand
    assert 'homeHref="#demand-insight"' in comparison

    print("OK - Sprint 2 Day 79 shared platform shell check passed")
    print("Shared responsibilities: brand, navigation, header and API status")
    print("Feature-owned responsibilities: navigation configuration and content")
    print("Duplicate structural shells: removed")


if __name__ == "__main__":
    main()
