"""Read and validate canonical Inventory Decision evidence."""

from __future__ import annotations

from copy import deepcopy
from datetime import date
import json
import logging
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[4]
REPORT_RELATIVE_PATH = Path(
    "reports/outputs/inventory-decision/inventory_decision_report.json"
)
STALE_AFTER_DAYS = 7
MAX_REPORT_BYTES = 2 * 1024 * 1024
LOGGER = logging.getLogger("retail_intelligence.inventory_decision")


class InventoryDecisionError(RuntimeError):
    """Raised when Inventory Decision evidence is missing or invalid."""


class InventoryDecisionService:
    """Return a stable read resource without importing policy production code."""

    def __init__(self, project_root: Path = PROJECT_ROOT) -> None:
        self.project_root = Path(project_root)

    @property
    def report_path(self) -> Path:
        return self.project_root / REPORT_RELATIVE_PATH

    def get_summary(self, *, today: date | None = None) -> dict[str, Any]:
        report = self._read_report()
        evidence_date = self._validate_report(report)
        current_date = today or date.today()
        age_days = max(0, (current_date - evidence_date).days)
        freshness_status = "stale" if age_days > STALE_AFTER_DAYS else "current"

        integration = self._record(report["integration"], "integration")
        resource = {
            "schema_version": report["schema_version"],
            "module": report["module"],
            "report_status": report["report_status"],
            "freshness": {
                "evidence_as_of_date": evidence_date.isoformat(),
                "age_days": age_days,
                "stale_after_days": STALE_AFTER_DAYS,
                "status": freshness_status,
            },
            "snapshot": deepcopy(report["snapshot"]),
            "demand_signal": deepcopy(report["demand_signal"]),
            "integration": {
                field: integration[field]
                for field in (
                    "join_key",
                    "join_strategy",
                    "joined_products",
                    "unmatched_products",
                )
            },
            "policy": deepcopy(report["policy"]),
            "summary": deepcopy(report["summary"]),
            "ranking": deepcopy(report["ranking"]),
            "recommendation_cards": deepcopy(report["recommendation_cards"]),
            "limitations": deepcopy(report["limitations"]),
        }
        LOGGER.info(
            "inventory_decision_summary_ready schema_version=%s products=%d "
            "review_queue=%d freshness_status=%s",
            resource["schema_version"],
            resource["summary"]["products"],
            resource["summary"]["products_requiring_replenishment_review"],
            freshness_status,
        )
        return resource

    def _read_report(self) -> dict[str, Any]:
        if not self.report_path.is_file():
            raise InventoryDecisionError("Inventory Decision report is missing.")
        try:
            if self.report_path.stat().st_size > MAX_REPORT_BYTES:
                raise InventoryDecisionError("Inventory Decision report exceeds the size boundary.")
            payload = json.loads(self.report_path.read_text(encoding="utf-8"))
        except InventoryDecisionError:
            raise
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise InventoryDecisionError(
                "Inventory Decision report cannot be read."
            ) from error
        return self._record(payload, "Inventory Decision report")

    def _validate_report(self, report: dict[str, Any]) -> date:
        expected_top = {
            "schema_version",
            "module",
            "report_status",
            "evidence_as_of_date",
            "snapshot",
            "demand_signal",
            "integration",
            "policy",
            "summary",
            "ranking",
            "recommendation_cards",
            "limitations",
        }
        if set(report) != expected_top:
            raise InventoryDecisionError("Inventory Decision report fields are invalid.")
        if (
            report.get("schema_version") != "1.0"
            or report.get("module") != "inventory_decision"
            or report.get("report_status") != "learning_evidence_only"
        ):
            raise InventoryDecisionError("Inventory Decision report identity is invalid.")
        try:
            evidence_date = date.fromisoformat(report["evidence_as_of_date"])
        except (TypeError, ValueError) as error:
            raise InventoryDecisionError("Inventory evidence date is invalid.") from error

        snapshot = self._record(report["snapshot"], "snapshot")
        demand = self._record(report["demand_signal"], "demand signal")
        integration = self._record(report["integration"], "integration")
        policy = self._record(report["policy"], "policy")
        summary = self._record(report["summary"], "summary")
        ranking = self._list(report["ranking"], "ranking")
        cards = self._list(report["recommendation_cards"], "Recommendation Cards")
        limitations = self._list(report["limitations"], "limitations")

        if snapshot.get("as_of_date") != evidence_date.isoformat():
            raise InventoryDecisionError("Snapshot and evidence dates conflict.")
        if demand.get("signal_type") != "observed_daily_average" or demand.get("signal_unit") != "units_per_day":
            raise InventoryDecisionError("Demand signal identity is invalid.")
        if (
            integration.get("join_key") != "product_id"
            or integration.get("join_strategy") != "strict_one_to_one"
            or integration.get("unmatched_products") != 0
        ):
            raise InventoryDecisionError("Inventory integration boundary is invalid.")
        for field in ("inventory_sha256", "demand_source_sha256"):
            checksum = integration.get(field)
            if not isinstance(checksum, str) or len(checksum) != 64 or any(
                char not in "0123456789abcdef" for char in checksum
            ):
                raise InventoryDecisionError("Inventory integration checksum is invalid.")
        if (
            policy.get("version") != "inventory-review-policy/1.0"
            or policy.get("risk_score_meaning") != "priority_index_not_probability"
        ):
            raise InventoryDecisionError("Inventory policy identity is invalid.")

        products = self._integer(summary, "products", "summary", minimum=1)
        if len(ranking) != products or len(cards) != products:
            raise InventoryDecisionError("Inventory product collections are inconsistent.")
        if integration.get("joined_products") != products or snapshot.get("products") != products:
            raise InventoryDecisionError("Inventory product coverage is inconsistent.")
        risk_total = sum(
            self._integer(summary, field, "summary", minimum=0)
            for field in (
                "critical_products",
                "high_risk_products",
                "watch_products",
                "healthy_products",
            )
        )
        if risk_total != products:
            raise InventoryDecisionError("Inventory risk counts are inconsistent.")

        ranking_ids: list[str] = []
        previous_score = float("inf")
        for expected_rank, value in enumerate(ranking, start=1):
            item = self._record(value, "ranking item")
            if self._integer(item, "priority_rank", "ranking item", minimum=1) != expected_rank:
                raise InventoryDecisionError("Inventory priority ranks are invalid.")
            product_id = self._text(item, "product_id", "ranking item")
            ranking_ids.append(product_id)
            score = self._number(item, "risk_score", "ranking item", minimum=0)
            if score > 100 or score > previous_score:
                raise InventoryDecisionError("Inventory risk ordering is invalid.")
            previous_score = score
            if item.get("risk_score_meaning") != "priority_index_not_probability":
                raise InventoryDecisionError("Inventory risk meaning is invalid.")
            for field in (
                "current_stock_units",
                "reorder_point_units",
                "target_stock_units",
                "suggested_quantity_units",
            ):
                self._integer(item, field, "ranking item", minimum=0)
            self._text(item, "reason", "ranking item")
            if item.get("policy_version") != policy["version"]:
                raise InventoryDecisionError("Inventory ranking policy is inconsistent.")
        if len(ranking_ids) != len(set(ranking_ids)):
            raise InventoryDecisionError("Inventory ranking identities are duplicated.")

        card_ids: list[str] = []
        card_product_ids: list[str] = []
        for value in cards:
            card = self._record(value, "Recommendation Card")
            card_ids.append(self._text(card, "card_id", "Recommendation Card"))
            product = self._record(card.get("product"), "Recommendation Card product")
            card_product_ids.append(self._text(product, "product_id", "Recommendation Card product"))
            risk = self._record(card.get("risk"), "Recommendation Card risk")
            if risk.get("meaning") != "priority_index_not_probability":
                raise InventoryDecisionError("Recommendation Card risk meaning is invalid.")
            action = self._record(card.get("action"), "Recommendation Card action")
            self._integer(action, "suggested_quantity_units", "Recommendation Card action", minimum=0)
            self._text(card, "reason", "Recommendation Card")
            self._text(card, "limitation", "Recommendation Card")
            if card.get("policy_version") != policy["version"]:
                raise InventoryDecisionError("Recommendation Card policy is inconsistent.")
        if len(card_ids) != len(set(card_ids)) or card_product_ids != ranking_ids:
            raise InventoryDecisionError("Recommendation Card identities are inconsistent.")
        if len(limitations) < 5 or not all(isinstance(item, str) and item.strip() for item in limitations):
            raise InventoryDecisionError("Inventory limitations are invalid.")
        return evidence_date

    @staticmethod
    def _record(value: Any, label: str) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise InventoryDecisionError(f"{label} must be an object.")
        return value

    @staticmethod
    def _list(value: Any, label: str) -> list[Any]:
        if not isinstance(value, list) or not value:
            raise InventoryDecisionError(f"{label} must be a non-empty list.")
        return value

    @staticmethod
    def _text(container: dict[str, Any], field: str, label: str) -> str:
        value = container.get(field)
        if not isinstance(value, str) or not value.strip():
            raise InventoryDecisionError(f"{label} field {field} is invalid.")
        return value

    @staticmethod
    def _integer(
        container: dict[str, Any], field: str, label: str, *, minimum: int
    ) -> int:
        value = container.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
            raise InventoryDecisionError(f"{label} field {field} is invalid.")
        return value

    @staticmethod
    def _number(
        container: dict[str, Any], field: str, label: str, *, minimum: float
    ) -> float:
        value = container.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < minimum:
            raise InventoryDecisionError(f"{label} field {field} is invalid.")
        return float(value)
