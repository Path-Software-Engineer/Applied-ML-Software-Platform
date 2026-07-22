"""Generate and validate the Day 138 inventory visual report."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "ai-services/inventory-decision/src"))

from inventory_decision.reporting import run_inventory_visual_report  # noqa: E402


def main() -> None:
    figures = run_inventory_visual_report(PROJECT_ROOT)
    assert len(figures) == 3
    figure_root = PROJECT_ROOT / "reports/figures/inventory-decision"
    for figure in figures:
        assert (figure_root / figure["path"]).read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    report = (
        PROJECT_ROOT / "reports/outputs/inventory-decision/inventory_visual_report.md"
    ).read_text(encoding="utf-8")
    for phrase in ("Priority is not probability", "observed demand is not a forecast", "human review"):
        assert phrase in report

    print("OK - Sprint 3 Day 138 inventory visual report check passed")
    print("Figures: priority index | stock policy levels | coverage days")
    print("PNG signatures and interpretation boundary: confirmed")


if __name__ == "__main__":
    main()
