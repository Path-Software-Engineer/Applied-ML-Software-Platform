"""Validate the documentation-only Week 11 integration exploration."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    files = (
        "docs/sprints/sprint-03-inventory-decision/week-11/exploration.md",
        "docs/sprints/sprint-03-inventory-decision/week-11/plan.md",
        "docs/inventory-decision-read-contract.md",
    )
    content = "\n".join(
        (PROJECT_ROOT / relative).read_text(encoding="utf-8") for relative in files
    )
    for value in (
        "GET /api/v1/inventory-decisions/summary",
        "loading",
        "connected",
        "stale",
        "unavailable",
        "does not run the inventory pipeline",
        "No backend",
    ):
        assert value in content

    print("OK - Sprint 3 Day 127 integration exploration check passed")
    print("Proposed endpoint: GET /api/v1/inventory-decisions/summary")
    print("States: loading / connected / stale / unavailable")
    print("Runtime implementation: deferred to Days 128-131")


if __name__ == "__main__":
    main()
