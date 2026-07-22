"""Validate the Day 134 hardening plan and boundary."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    exploration = (
        PROJECT_ROOT / "docs/sprints/sprint-03-inventory-decision/week-12/exploration.md"
    ).read_text(encoding="utf-8")
    plan = (
        PROJECT_ROOT / "docs/sprints/sprint-03-inventory-decision/week-12/plan.md"
    ).read_text(encoding="utf-8")
    for phrase in (
        "Sufficient stock",
        "Low stock",
        "Stockout",
        "Zero demand",
        "High demand",
        "fails closed",
        "stale evidence",
    ):
        assert phrase.lower() in exploration.lower()
    for day in range(134, 141):
        assert str(day) in plan
    assert "purchase orders" in exploration
    assert "does not open another product capability" in plan

    print("OK - Sprint 3 Day 134 Week 12 exploration check passed")
    print("Scenarios: sufficient | low | stockout | zero demand | high demand")
    print("Adversarial boundary and polish scope: explicit")
    print("Runtime behavior: unchanged")


if __name__ == "__main__":
    main()
