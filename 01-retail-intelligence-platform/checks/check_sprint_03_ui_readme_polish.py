"""Validate Day 139 executable docs and accessible UI boundaries."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    frontend_readme = (PROJECT_ROOT / "frontend/dashboard-app/README.md").read_text(encoding="utf-8")
    shell = (PROJECT_ROOT / "frontend/dashboard-app/src/shared/components/PlatformShell.jsx").read_text(encoding="utf-8")
    styles = (PROJECT_ROOT / "frontend/dashboard-app/src/styles.css").read_text(encoding="utf-8")
    navigation = (PROJECT_ROOT / "frontend/dashboard-app/src/shared/navigation/platformNavigation.js").read_text(encoding="utf-8")

    for phrase in ("Setup from a clean checkout", "run-backend.ps1", "run-frontend.ps1", "run-quality-gate.ps1", "18 synthetic", "not production ready"):
        assert phrase in readme
    for phrase in ("Demand Insight", "Model Comparison", "Inventory Decision"):
        assert phrase in frontend_readme
        assert phrase.lower().replace(" ", "-") in navigation.lower() or phrase in navigation
    assert "VITE_API_BASE_URL" in frontend_readme
    assert 'className="skip-link"' in shell
    assert 'tabIndex="-1"' in shell
    assert "prefers-reduced-motion" in styles
    assert "a:focus-visible" in styles
    assert "@media (max-width: 980px)" in styles and "@media (max-width: 640px)" in styles

    print("OK - Sprint 3 Day 139 UI and README polish check passed")
    print("Navigation: three stages | keyboard and skip-link support")
    print("Responsive/reduced-motion states and clean-checkout commands: documented")


if __name__ == "__main__":
    main()
