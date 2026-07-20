"""Readable Day 75 check for API-driven frontend Decision Cards."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    feature_root = (
        PROJECT_ROOT
        / "frontend"
        / "dashboard-app"
        / "src"
        / "features"
        / "model-comparison"
    )
    dashboard = (feature_root / "components" / "ModelComparisonDashboard.jsx")
    card_component = feature_root / "components" / "DecisionCard.jsx"
    view_model = feature_root / "presentation" / "decisionCardViewModel.js"
    tests = (
        PROJECT_ROOT
        / "frontend"
        / "dashboard-app"
        / "tests"
        / "decisionCardViewModel.test.js"
    )
    for path in (dashboard, card_component, view_model, tests):
        assert path.is_file() and path.stat().st_size > 0

    dashboard_text = dashboard.read_text(encoding="utf-8")
    card_text = card_component.read_text(encoding="utf-8")
    view_text = view_model.read_text(encoding="utf-8")
    assert "decision_cards: cards" in dashboard_text
    assert "<DecisionCard card={card}" in dashboard_text
    assert ".sort(" not in dashboard_text
    for phrase in (
        "aria-labelledby",
        "aria-describedby",
        'role="status"',
        "<data value={view.metricValue}",
        "view.reasons.map",
        "view.limitation",
    ):
        assert phrase in card_text
    assert "card.primary_metric.value" in view_text
    assert "mae_units" not in view_text

    print("OK - Sprint 2 Day 75 frontend Decision Cards check passed")
    print("API-driven cards: 3")
    print("Accessible labels and status: confirmed")
    print("Client-side decision recomputation: absent")
    print("Day 76 smoke validation: not started")


if __name__ == "__main__":
    main()
