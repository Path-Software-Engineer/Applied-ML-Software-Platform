"""Generate reproducible sales figures and a visual report."""

from __future__ import annotations

from pathlib import Path

import json

import matplotlib
import pandas as pd

matplotlib.use("Agg")

from matplotlib import pyplot as plt  # noqa: E402


PROJECT_ROOT = Path(__file__).resolve().parents[4]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "demand-insight"

INSIGHT_CARDS_PATH = (
    PROJECT_ROOT
    / "reports"
    / "insight-cards"
    / "demand_insight_cards.json"
)

FIGURES_DIR = PROJECT_ROOT / "reports" / "figures" / "demand-insight"
OUTPUTS_DIR = PROJECT_ROOT / "reports" / "outputs" / "demand-insight"

DAILY_SALES_FIGURE_PATH = FIGURES_DIR / "daily_sales.png"
UNITS_RANKING_FIGURE_PATH = FIGURES_DIR / "product_units_ranking.png"
REVENUE_RANKING_FIGURE_PATH = FIGURES_DIR / "product_revenue_ranking.png"
VISUAL_REPORT_PATH = OUTPUTS_DIR / "sales_visual_report.md"

EXPECTED_OUTPUTS = (
    DAILY_SALES_FIGURE_PATH,
    UNITS_RANKING_FIGURE_PATH,
    REVENUE_RANKING_FIGURE_PATH,
    VISUAL_REPORT_PATH,
)

DAILY_SALES_PATH = PROCESSED_DIR / "daily_sales_summary.csv"
UNITS_RANKING_PATH = PROCESSED_DIR / "product_ranking_by_units.csv"
REVENUE_RANKING_PATH = PROCESSED_DIR / "product_ranking_by_revenue.csv"

INPUT_CONTRACTS: dict[Path, set[str]] = {
    DAILY_SALES_PATH: {
        "date",
        "total_units_sold",
        "total_revenue",
    },
    UNITS_RANKING_PATH: {
        "units_rank",
        "product_name",
        "total_units_sold",
    },
    REVENUE_RANKING_PATH: {
        "revenue_rank",
        "product_name",
        "total_revenue",
    },
}

def load_visual_data(
    contracts: dict[Path, set[str]] | None = None,
) -> dict[str, pd.DataFrame]:
    selected_contracts = INPUT_CONTRACTS if contracts is None else contracts
    datasets: dict[str, pd.DataFrame] = {}

    for path, required_columns in selected_contracts.items():
        if not path.exists():
            raise FileNotFoundError(f"Required visual artifact not found: {path}")

        data = pd.read_csv(path)

        if data.empty:
            raise ValueError(f"Visual artifact is empty: {path}")

        missing_columns = required_columns - set(data.columns)
        if missing_columns:
            raise ValueError(
                f"Visual artifact {path.name} is missing columns: "
                f"{sorted(missing_columns)}"
            )

        if "date" in data.columns:
            data["date"] = pd.to_datetime(data["date"], errors="raise")

        datasets[path.stem] = data

    return datasets

def build_daily_sales_figure(
    daily_sales: pd.DataFrame,
    output_path: Path = DAILY_SALES_FIGURE_PATH,
) -> Path:
    ordered = daily_sales.sort_values("date").copy()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    figure, axes = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(10, 7),
        sharex=True,
    )

    axes[0].plot(
        ordered["date"],
        ordered["total_units_sold"],
        color="#2563EB",
        marker="o",
        linewidth=2,
    )
    axes[0].set_title("Daily units sold")
    axes[0].set_ylabel("Units")
    axes[0].grid(alpha=0.25)

    axes[1].plot(
        ordered["date"],
        ordered["total_revenue"],
        color="#D97706",
        marker="o",
        linewidth=2,
    )
    axes[1].set_title("Daily revenue")
    axes[1].set_xlabel("Date")
    axes[1].set_ylabel("Revenue")
    axes[1].grid(alpha=0.25)

    figure.suptitle("Demand Insight — Daily Sales", fontsize=14)
    figure.autofmt_xdate()
    figure.tight_layout()
    figure.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(figure)

    return output_path

def build_ranking_figure(
    ranking: pd.DataFrame,
    value_column: str,
    title: str,
    x_label: str,
    color: str,
    output_path: Path,
    value_format: str,
) -> Path:
    ordered = ranking.sort_values(value_column, ascending=True).copy()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    figure, axis = plt.subplots(figsize=(9, 5))
    bars = axis.barh(
        ordered["product_name"],
        ordered[value_column],
        color=color,
    )

    axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel("Product")
    axis.grid(axis="x", alpha=0.25)

    for bar, value in zip(bars, ordered[value_column], strict=True):
        axis.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f" {format(float(value), value_format)}",
            va="center",
        )

    figure.tight_layout()
    figure.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(figure)

    return output_path

def load_insight_cards(
    path: Path = INSIGHT_CARDS_PATH,
) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Insight Cards artifact not found: {path}")

    cards = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(cards, list) or not cards:
        raise ValueError("Insight Cards artifact must contain a non-empty list.")

    required_fields = {
        "card_id",
        "title",
        "metric",
        "insight",
        "recommendation",
        "limitation",
    }
    for card in cards:
        if set(card) != required_fields:
            raise ValueError(
                f"Insight Card {card.get('card_id')} violates its contract."
            )

    return cards


def render_visual_report(cards: list[dict[str, str]]) -> str:
    cards_by_id = {card["card_id"]: card for card in cards}

    return f"""# Demand Insight Visual Report

## Objective

Present validated sales signals through reusable visual artifacts.

## Daily sales

![Daily sales](../../figures/demand-insight/daily_sales.png)

- Units leader: {cards_by_id["top-day-units"]["metric"]}.
- Revenue leader: {cards_by_id["top-day-revenue"]["metric"]}.
- Interpretation: {cards_by_id["top-day-revenue"]["insight"]}

## Product ranking by units

![Product ranking by units](../../figures/demand-insight/product_units_ranking.png)

- Leader: {cards_by_id["top-product-units"]["metric"]}.
- Interpretation: {cards_by_id["top-product-units"]["insight"]}

## Product ranking by revenue

![Product ranking by revenue](../../figures/demand-insight/product_revenue_ranking.png)

- Leader: {cards_by_id["top-product-revenue"]["metric"]}.
- Interpretation: {cards_by_id["top-product-revenue"]["insight"]}

## Reading rule

Units sold represent demand volume.

Revenue represents observed economic value.

They must not be interpreted as the same magnitude.

## Limitation

{cards_by_id["observed-demand"]["limitation"]}

These figures describe observed data and do not demonstrate trend, seasonality or future demand.
"""


def generate_visual_report(
    report_path: Path = VISUAL_REPORT_PATH,
) -> tuple[Path, ...]:
    datasets = load_visual_data()
    cards = load_insight_cards()

    build_daily_sales_figure(
        datasets["daily_sales_summary"],
        DAILY_SALES_FIGURE_PATH,
    )
    build_ranking_figure(
        datasets["product_ranking_by_units"],
        "total_units_sold",
        "Product ranking by units sold",
        "Units sold",
        "#2563EB",
        UNITS_RANKING_FIGURE_PATH,
        ".0f",
    )
    build_ranking_figure(
        datasets["product_ranking_by_revenue"],
        "total_revenue",
        "Product ranking by revenue",
        "Revenue",
        "#D97706",
        REVENUE_RANKING_FIGURE_PATH,
        ".2f",
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        render_visual_report(cards),
        encoding="utf-8",
    )

    return (
        DAILY_SALES_FIGURE_PATH,
        UNITS_RANKING_FIGURE_PATH,
        REVENUE_RANKING_FIGURE_PATH,
        report_path,
    )


def main() -> None:
    outputs = generate_visual_report()

    print("Demand Insight visual report generated")
    for output in outputs:
        print(f"Output: {output}")


if __name__ == "__main__":
    main()