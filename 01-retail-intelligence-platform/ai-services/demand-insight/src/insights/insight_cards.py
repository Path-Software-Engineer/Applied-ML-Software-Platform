"""Build structured insight cards from validated Demand Insight artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import TypedDict

import pandas as pd

import json

PROJECT_ROOT = Path(__file__).resolve().parents[4]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "demand-insight"
OUTPUT_DIR = PROJECT_ROOT / "reports" / "insight-cards"

JSON_OUTPUT_PATH = OUTPUT_DIR / "demand_insight_cards.json"
MARKDOWN_OUTPUT_PATH = OUTPUT_DIR / "demand_insight_cards.md"

ARTIFACT_CONTRACTS: dict[Path, set[str]] = {
    PROCESSED_DIR / "sales_summary.csv": {
        "total_units_sold",
        "total_revenue",
        "start_date",
        "end_date",
    },
    PROCESSED_DIR / "product_ranking_by_units.csv": {
        "units_rank",
        "product_name",
        "total_units_sold",
    },
    PROCESSED_DIR / "product_ranking_by_revenue.csv": {
        "revenue_rank",
        "product_name",
        "total_revenue",
    },
    PROCESSED_DIR / "daily_sales_summary.csv": {
        "date",
        "total_units_sold",
        "total_revenue",
    },
}

EXPECTED_CARD_IDS = {
    "observed-demand",
    "top-product-units",
    "top-product-revenue",
    "top-day-units",
    "top-day-revenue",
}

DATASET_LIMITATION = (
    "Describe únicamente las ventas observadas entre 2026-01-01 y "
    "2026-01-09; no predice demanda futura."
)

class InsightCard(TypedDict):
    card_id: str
    title: str
    metric: str
    insight: str
    recommendation: str
    limitation: str

def load_artifacts(
    contracts: dict[Path, set[str]] | None = None,
) -> dict[str, pd.DataFrame]:
    selected_contracts = ARTIFACT_CONTRACTS if contracts is None else contracts
    artifacts: dict[str, pd.DataFrame] = {}

    for path, required_columns in selected_contracts.items():
        if not path.exists():
            raise FileNotFoundError(f"Required insight artifact not found: {path}")

        data = pd.read_csv(path)

        if data.empty:
            raise ValueError(f"Insight artifact is empty: {path}")

        missing_columns = required_columns - set(data.columns)
        if missing_columns:
            raise ValueError(
                f"Insight artifact {path.name} is missing columns: "
                f"{sorted(missing_columns)}"
            )

        artifacts[path.stem] = data

    return artifacts

def build_insight_cards(
    artifacts: dict[str, pd.DataFrame],
) -> list[InsightCard]:
    summary = artifacts["sales_summary"].iloc[0]

    units_leader = (
        artifacts["product_ranking_by_units"]
        .sort_values("units_rank")
        .iloc[0]
    )
    revenue_leader = (
        artifacts["product_ranking_by_revenue"]
        .sort_values("revenue_rank")
        .iloc[0]
    )

    daily_summary = artifacts["daily_sales_summary"]
    top_units_day = daily_summary.loc[
        daily_summary["total_units_sold"].idxmax()
    ]
    top_revenue_day = daily_summary.loc[
        daily_summary["total_revenue"].idxmax()
    ]

    cards: list[InsightCard] = [
        {
            "card_id": "observed-demand",
            "title": "Demanda observada",
            "metric": (
                f"{int(summary['total_units_sold'])} unidades | "
                f"{float(summary['total_revenue']):.2f} de revenue"
            ),
            "insight": (
                f"El periodo analizado va de {summary['start_date']} "
                f"a {summary['end_date']}."
            ),
            "recommendation": (
                "Usar estos totales como contexto general para interpretar "
                "las demás señales del dashboard."
            ),
            "limitation": DATASET_LIMITATION,
        },
        {
            "card_id": "top-product-units",
            "title": "Producto con mayor demanda",
            "metric": (
                f"{units_leader['product_name']} — "
                f"{int(units_leader['total_units_sold'])} unidades"
            ),
            "insight": (
                "Este producto concentró el mayor volumen de unidades "
                "vendidas en el periodo observado."
            ),
            "recommendation": (
                "Vigilar su disponibilidad y comparar su comportamiento "
                "cuando exista un periodo histórico mayor."
            ),
            "limitation": DATASET_LIMITATION,
        },
        {
            "card_id": "top-product-revenue",
            "title": "Producto con mayor revenue",
            "metric": (
                f"{revenue_leader['product_name']} — "
                f"{float(revenue_leader['total_revenue']):.2f}"
            ),
            "insight": (
                "Este producto generó el mayor valor económico observado, "
                "aunque no lideró en unidades."
            ),
            "recommendation": (
                "Mostrar esta señal junto al volumen vendido para evitar "
                "decisiones basadas en una sola métrica."
            ),
            "limitation": DATASET_LIMITATION,
        },
        {
            "card_id": "top-day-units",
            "title": "Día con mayor movimiento",
            "metric": (
                f"{top_units_day['date']} — "
                f"{int(top_units_day['total_units_sold'])} unidades"
            ),
            "insight": (
                "Esta fecha presentó el mayor volumen diario de unidades "
                "vendidas dentro del periodo."
            ),
            "recommendation": (
                "Comparar esta fecha con periodos futuros antes de asumir "
                "que representa un patrón recurrente."
            ),
            "limitation": DATASET_LIMITATION,
        },
        {
            "card_id": "top-day-revenue",
            "title": "Día con mayor revenue",
            "metric": (
                f"{top_revenue_day['date']} — "
                f"{float(top_revenue_day['total_revenue']):.2f}"
            ),
            "insight": (
                "Esta fecha generó el mayor revenue diario observado y no "
                "coincidió con el día de mayor volumen."
            ),
            "recommendation": (
                "Revisar conjuntamente revenue y unidades para comprender "
                "mejor el desempeño diario."
            ),
            "limitation": DATASET_LIMITATION,
        },
    ]

    card_ids = {card["card_id"] for card in cards}
    if card_ids != EXPECTED_CARD_IDS:
        raise AssertionError("Generated Insight Card IDs do not match the contract.")

    return cards

def render_cards_markdown(cards: list[InsightCard]) -> str:
    sections = ["# Demand Insight Cards", ""]

    for card in cards:
        sections.extend(
            [
                f"## {card['title']}",
                "",
                f"**Metric:** {card['metric']}",
                "",
                f"**Insight:** {card['insight']}",
                "",
                f"**Recommendation:** {card['recommendation']}",
                "",
                f"**Limitation:** {card['limitation']}",
                "",
            ]
        )

    return "\n".join(sections)


def save_insight_cards(
    cards: list[InsightCard],
    json_path: Path = JSON_OUTPUT_PATH,
    markdown_path: Path = MARKDOWN_OUTPUT_PATH,
) -> tuple[Path, Path]:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)

    json_path.write_text(
        json.dumps(cards, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_cards_markdown(cards),
        encoding="utf-8",
    )

    return json_path, markdown_path


def main() -> None:
    artifacts = load_artifacts()
    cards = build_insight_cards(artifacts)
    json_path, markdown_path = save_insight_cards(cards)

    print("Demand Insight Cards generated")
    print(f"Cards: {len(cards)}")
    print(f"JSON: {json_path}")
    print(f"Markdown: {markdown_path}")


if __name__ == "__main__":
    main()