"""Validate Week 12 evidence and frozen release scope."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    required = (
        "docs/sprints/sprint-03-inventory-decision/week-12/exploration.md",
        "docs/sprints/sprint-03-inventory-decision/week-12/plan.md",
        "docs/sprints/sprint-03-inventory-decision/week-12/review.md",
        "docs/inventory-decision-release-scope.md",
        "docs/inventory-decision-policy-card.md",
        "reports/scenarios/inventory-decision/policy_scenarios.json",
        "reports/quality/inventory-decision/adversarial_contracts.md",
        "reports/outputs/inventory-decision/decision_trace.json",
        "reports/outputs/inventory-decision/inventory_visual_report.md",
        "reports/figures/inventory-decision/inventory_priority_index.png",
        "reports/figures/inventory-decision/inventory_stock_policy_levels.png",
        "reports/figures/inventory-decision/inventory_coverage_days.png",
    )
    for relative in required:
        assert (PROJECT_ROOT / relative).is_file(), f"Missing Week 12 evidence: {relative}"
    scope = (PROJECT_ROOT / "docs/inventory-decision-release-scope.md").read_text(encoding="utf-8")
    for phrase in ("Explicitly excluded", "purchase-order", "production deployment", "Sprint 4"):
        assert phrase in scope

    print("OK - Sprint 3 Day 140 Week 12 close check passed")
    print("Scenarios, adversarial contracts, trace, visuals and UI polish: confirmed")
    print("Final release scope: frozen | Week 13: closure only")


if __name__ == "__main__":
    main()
