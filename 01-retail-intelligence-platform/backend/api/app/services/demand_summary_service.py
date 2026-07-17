"""Assemble the versioned Demand Insight summary from official artifacts."""

from __future__ import annotations

import csv
import json
from math import isclose
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "outputs"
    / "demand-insight"
    / "demand_summary.json"
)

ARTIFACT_PATHS = {
    "sales_summary": "data/processed/demand-insight/sales_summary.csv",
    "pipeline": (
        "data/processed/demand-insight/"
        "sales_feature_baseline_metric_pipeline.csv"
    ),
    "product_units": (
        "data/processed/demand-insight/product_ranking_by_units.csv"
    ),
    "product_revenue": (
        "data/processed/demand-insight/product_ranking_by_revenue.csv"
    ),
    "daily_sales": "data/processed/demand-insight/daily_sales_summary.csv",
    "insight_cards": "reports/insight-cards/demand_insight_cards.json",
}

EXPECTED_CARD_IDS = {
    "observed-demand",
    "top-product-units",
    "top-product-revenue",
    "top-day-units",
    "top-day-revenue",
}
CARD_FIELDS = {
    "card_id",
    "title",
    "metric",
    "insight",
    "recommendation",
    "limitation",
}


class DemandSummaryError(RuntimeError):
    """Raised when required Demand Insight evidence is unavailable or invalid."""


class DemandSummaryService:
    """Validate official artifacts and assemble the schema-versioned response."""

    def __init__(self, project_root: Path = PROJECT_ROOT) -> None:
        self.project_root = Path(project_root)

    def get_summary(self) -> dict[str, Any]:
        sales_summary = self._read_single_csv("sales_summary")
        pipeline = self._read_csv("pipeline")
        product_units = self._read_csv("product_units")
        product_revenue = self._read_csv("product_revenue")
        daily_sales = self._read_csv("daily_sales")
        insight_cards = self._read_cards()

        baseline_values = {
            self._float(row, "mean_baseline_prediction", "pipeline")
            for row in pipeline
        }
        if len(baseline_values) != 1:
            raise DemandSummaryError(
                "Pipeline evidence must contain one mean baseline prediction."
            )
        baseline_value = next(iter(baseline_values))
        baseline_mae = sum(
            self._float(row, "baseline_absolute_error", "pipeline")
            for row in pipeline
        ) / len(pipeline)

        units_product = self._first_ranked(
            product_units, "units_rank", "product units ranking"
        )
        revenue_product = self._first_ranked(
            product_revenue, "revenue_rank", "product revenue ranking"
        )
        units_date = self._maximum(
            daily_sales, "total_units_sold", "daily sales"
        )
        revenue_date = self._maximum(
            daily_sales, "total_revenue", "daily sales"
        )

        return {
            "schema_version": "1.0",
            "period": {
                "start_date": self._required(sales_summary, "start_date", "sales summary"),
                "end_date": self._required(sales_summary, "end_date", "sales summary"),
                "observed_days": len(daily_sales),
            },
            "sales_summary": {
                "total_units_sold": self._int(
                    sales_summary, "total_units_sold", "sales summary"
                ),
                "total_revenue": round(
                    self._float(sales_summary, "total_revenue", "sales summary"),
                    2,
                ),
                "sales_count": self._int(
                    sales_summary, "sales_count", "sales summary"
                ),
                "unique_products": self._int(
                    sales_summary, "unique_products", "sales summary"
                ),
                "unique_categories": self._int(
                    sales_summary, "unique_categories", "sales summary"
                ),
            },
            "baseline": {
                "mean_units_prediction": round(baseline_value, 2),
                "mae": round(baseline_mae, 2),
            },
            "leaders": {
                "product_by_units": self._leader(
                    units_product, "product_name", "total_units_sold", "units", integer=True
                ),
                "product_by_revenue": self._leader(
                    revenue_product, "product_name", "total_revenue", "revenue"
                ),
                "date_by_units": self._leader(
                    units_date, "date", "total_units_sold", "units", integer=True
                ),
                "date_by_revenue": self._leader(
                    revenue_date, "date", "total_revenue", "revenue"
                ),
            },
            "insight_cards": insight_cards,
            "limitations": [
                "The response describes observed sales and does not forecast future demand.",
                (
                    "The source covers "
                    f"{self._int(sales_summary, 'sales_count', 'sales summary')} records "
                    f"from {sales_summary['start_date']} through {sales_summary['end_date']}."
                ),
            ],
        }

    def save_summary(
        self,
        summary: dict[str, Any] | None = None,
        output_path: Path = DEFAULT_OUTPUT_PATH,
    ) -> Path:
        response = self.get_summary() if summary is None else summary
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(response, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return destination

    def _artifact_path(self, key: str) -> Path:
        return self.project_root / ARTIFACT_PATHS[key]

    def _read_csv(self, key: str) -> list[dict[str, str]]:
        path = self._artifact_path(key)
        if not path.is_file():
            raise DemandSummaryError(f"Required artifact is missing: {path}")
        try:
            with path.open(encoding="utf-8-sig", newline="") as source:
                rows = list(csv.DictReader(source))
        except (OSError, UnicodeError, csv.Error) as error:
            raise DemandSummaryError(f"Cannot read artifact: {path}") from error
        if not rows:
            raise DemandSummaryError(f"Required artifact is empty: {path}")
        return rows

    def _read_single_csv(self, key: str) -> dict[str, str]:
        rows = self._read_csv(key)
        if len(rows) != 1:
            raise DemandSummaryError(
                f"Artifact {self._artifact_path(key)} must contain exactly one row."
            )
        return rows[0]

    def _read_cards(self) -> list[dict[str, str]]:
        path = self._artifact_path("insight_cards")
        if not path.is_file():
            raise DemandSummaryError(f"Required artifact is missing: {path}")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise DemandSummaryError(f"Cannot read Insight Cards: {path}") from error
        if not isinstance(payload, list) or len(payload) != 5:
            raise DemandSummaryError("Insight Card evidence must contain five cards.")
        card_ids = set()
        for card in payload:
            if not isinstance(card, dict) or set(card) != CARD_FIELDS:
                raise DemandSummaryError("Insight Card field contract is invalid.")
            if not all(isinstance(value, str) and value.strip() for value in card.values()):
                raise DemandSummaryError("Insight Card values must be non-empty strings.")
            card_ids.add(card["card_id"])
        if card_ids != EXPECTED_CARD_IDS:
            raise DemandSummaryError(f"Unexpected Insight Card identifiers: {card_ids}")
        return payload

    def _first_ranked(
        self, rows: list[dict[str, str]], rank_field: str, label: str
    ) -> dict[str, str]:
        ranked = sorted(rows, key=lambda row: self._int(row, rank_field, label))
        if self._int(ranked[0], rank_field, label) != 1:
            raise DemandSummaryError(f"{label} does not start at rank 1.")
        return ranked[0]

    def _maximum(
        self, rows: list[dict[str, str]], field: str, label: str
    ) -> dict[str, str]:
        return max(rows, key=lambda row: self._float(row, field, label))

    def _leader(
        self,
        row: dict[str, str],
        name_field: str,
        value_field: str,
        unit: str,
        *,
        integer: bool = False,
    ) -> dict[str, Any]:
        label = f"{unit} leader"
        value: int | float
        if integer:
            value = self._int(row, value_field, label)
        else:
            value = round(self._float(row, value_field, label), 2)
        return {
            "name": self._required(row, name_field, label),
            "value": value,
            "unit": unit,
        }

    @staticmethod
    def _required(row: dict[str, str], field: str, label: str) -> str:
        value = row.get(field, "").strip()
        if not value:
            raise DemandSummaryError(f"Missing {field} in {label} evidence.")
        return value

    @classmethod
    def _float(cls, row: dict[str, str], field: str, label: str) -> float:
        raw_value = cls._required(row, field, label)
        try:
            return float(raw_value)
        except ValueError as error:
            raise DemandSummaryError(
                f"Invalid numeric value for {field} in {label}: {raw_value}"
            ) from error

    @classmethod
    def _int(cls, row: dict[str, str], field: str, label: str) -> int:
        value = cls._float(row, field, label)
        integer_value = int(value)
        if not isclose(value, integer_value):
            raise DemandSummaryError(
                f"Expected integer value for {field} in {label}: {value}"
            )
        return integer_value


def main() -> None:
    service = DemandSummaryService()
    summary = service.get_summary()
    output_path = service.save_summary(summary)
    print("Demand Summary generated")
    print(f"Schema version: {summary['schema_version']}")
    print(f"Insight Cards: {len(summary['insight_cards'])}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
