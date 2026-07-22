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
    navigation_path = (
        FRONTEND / "shared" / "navigation" / "platformNavigation.js"
    )
    shared = shared_path.read_text(encoding="utf-8")
    demand = demand_path.read_text(encoding="utf-8")
    comparison = comparison_path.read_text(encoding="utf-8")
    navigation = navigation_path.read_text(encoding="utf-8")

    for phrase in (
        "export function LogoMark",
        "export function PlatformShell",
        "function PlatformHeader",
        'aria-label="Primary navigation"',
        'aria-label="Platform stages"',
        'aria-current={active ? "page" : undefined}',
        "aria-expanded={expanded}",
        "window.location.hash = stage.href",
        'className="nav-stage-panel"',
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
    assert 'activeStageId="demand-insight"' in demand
    assert 'activeStageId="model-comparison"' in comparison
    for label in (
        "Demand insight",
        "Model comparison",
        "Insight cards",
        "Candidates",
        "Decision rationale",
        "Evidence boundary",
    ):
        assert label in navigation

    print("OK - Sprint 2 Day 79 shared platform shell check passed")
    print("Shared responsibilities: brand, staged navigation, header and API status")
    print("Stage sections: centralized and feature-specific")
    print("Duplicate structural shells: removed")


if __name__ == "__main__":
    main()
