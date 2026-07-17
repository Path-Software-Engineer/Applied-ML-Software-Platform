"""Manual end-to-end check for the Day 20 Demand Insight visual report."""

from __future__ import annotations

import sys
from pathlib import Path

MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.visualization.sales_visual_report import (  # noqa: E402
    DAILY_SALES_FIGURE_PATH,
    REVENUE_RANKING_FIGURE_PATH,
    UNITS_RANKING_FIGURE_PATH,
    VISUAL_REPORT_PATH,
    generate_visual_report,
    load_insight_cards,
    load_visual_data,
    render_visual_report,
)


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

EXPECTED_FIGURES = (
    DAILY_SALES_FIGURE_PATH,
    UNITS_RANKING_FIGURE_PATH,
    REVENUE_RANKING_FIGURE_PATH,
)


def check_png(path: Path) -> None:
    if not path.exists():
        raise AssertionError(f"Missing visual artifact: {path}")

    if path.stat().st_size <= len(PNG_SIGNATURE):
        raise AssertionError(f"Visual artifact is empty: {path}")

    if not path.read_bytes().startswith(PNG_SIGNATURE):
        raise AssertionError(f"Artifact is not a valid PNG file: {path}")


def main() -> None:
    generate_visual_report()

    for figure_path in EXPECTED_FIGURES:
        check_png(figure_path)

    if not VISUAL_REPORT_PATH.exists():
        raise AssertionError(
            f"Missing visual report: {VISUAL_REPORT_PATH}"
        )

    data = load_visual_data()
    cards = load_insight_cards()

    stored_report = VISUAL_REPORT_PATH.read_text(encoding="utf-8")
    expected_report = render_visual_report(cards)

    if stored_report != expected_report:
        raise AssertionError(
            "Stored visual report does not match the validated "
            "Insight Card interpretation."
        )

    required_references = (
        "../../figures/demand-insight/daily_sales.png",
        "../../figures/demand-insight/product_units_ranking.png",
        "../../figures/demand-insight/product_revenue_ranking.png",
    )

    missing_references = [
        reference
        for reference in required_references
        if reference not in stored_report
    ]

    if missing_references:
        raise AssertionError(
            f"Missing figure references: {missing_references}"
        )

    daily_sales = data["daily_sales_summary"]
    units_ranking = data["product_ranking_by_units"]
    revenue_ranking = data["product_ranking_by_revenue"]

    units_day = daily_sales.loc[
        daily_sales["total_units_sold"].idxmax()
    ]
    revenue_day = daily_sales.loc[
        daily_sales["total_revenue"].idxmax()
    ]

    if (
        units_day["date"].strftime("%Y-%m-%d"),
        int(units_day["total_units_sold"]),
    ) != ("2026-01-06", 45):
        raise AssertionError("Unexpected daily units leader.")

    if (
        revenue_day["date"].strftime("%Y-%m-%d"),
        round(float(revenue_day["total_revenue"]), 2),
    ) != ("2026-01-08", 99.30):
        raise AssertionError("Unexpected daily revenue leader.")

    units_product = units_ranking.loc[
        units_ranking["total_units_sold"].idxmax()
    ]
    revenue_product = revenue_ranking.loc[
        revenue_ranking["total_revenue"].idxmax()
    ]

    if (
        units_product["product_name"],
        int(units_product["total_units_sold"]),
    ) != ("Bread", 105):
        raise AssertionError("Unexpected product leader by units.")

    if (
        revenue_product["product_name"],
        round(float(revenue_product["total_revenue"]), 2),
    ) != ("Rice 1kg", 220.50):
        raise AssertionError("Unexpected product leader by revenue.")

    if "Units sold represent demand volume." not in stored_report:
        raise AssertionError("Missing units interpretation rule.")

    if "Revenue represents observed economic value." not in stored_report:
        raise AssertionError("Missing revenue interpretation rule.")

    if "no predice demanda futura" not in stored_report:
        raise AssertionError("Missing temporal limitation.")

    print("OK - Day 20 Demand Insight visual report check passed")
    print(f"Figures: {len(EXPECTED_FIGURES)}")
    print("PNG signatures: confirmed")
    print("Insight Card interpretation: confirmed")
    print("Units and revenue separation: confirmed")
    print("Daily units leader: 2026-01-06 — 45 units")
    print("Daily revenue leader: 2026-01-08 — 99.30")
    print("Product units leader: Bread — 105 units")
    print("Product revenue leader: Rice 1kg — 220.50")
    print(f"Report: {VISUAL_REPORT_PATH}")


if __name__ == "__main__":
    main()