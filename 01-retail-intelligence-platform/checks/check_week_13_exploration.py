"""Validate the final closure inventory and no-feature boundary."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    exploration = (
        PROJECT_ROOT / "docs/sprints/sprint-03-inventory-decision/week-13/exploration.md"
    ).read_text(encoding="utf-8")
    plan = (
        PROJECT_ROOT / "docs/sprints/sprint-03-inventory-decision/week-13/plan.md"
    ).read_text(encoding="utf-8")
    for module in ("Demand Insight", "Model Comparison", "Inventory Decision"):
        assert module in exploration
    for phrase in ("Prioritized gaps and risks", "Final acceptance criteria", "Demo and release plan", "No new feature"):
        assert phrase in exploration
    for day in range(141, 148):
        assert str(day) in plan
    assert "does not create Sprint 4" in plan

    print("OK - Sprint 3 Day 141 final closure exploration check passed")
    print("Product stages inventoried: 3")
    print("Acceptance, demo, release and no-feature boundaries: explicit")


if __name__ == "__main__":
    main()
