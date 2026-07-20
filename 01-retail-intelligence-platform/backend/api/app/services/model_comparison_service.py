"""Read and validate the canonical Model Comparison evidence artifact."""

from __future__ import annotations

from copy import deepcopy
import json
from math import isclose
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[4]
REPORT_RELATIVE_PATH = Path(
    "reports/outputs/model-comparison/model_comparison_report.json"
)
EXPECTED_MODEL_IDS = {
    "training_mean",
    "linear_regression",
    "random_forest",
    "gradient_boosting",
}
EXPECTED_CARD_IDS = {
    "metric-leader",
    "integration-candidate",
    "evidence-boundary",
}
TOP_LEVEL_FIELDS = {
    "schema_version",
    "module",
    "report_status",
    "experiment",
    "comparison",
    "error_review",
    "decision",
    "decision_cards",
    "limitations",
}
CANDIDATE_FIELDS = {
    "model_id",
    "model_name",
    "model_family",
    "mae_units",
    "rmse_units",
    "r2_contextual",
    "test_rows",
    "production_status",
    "mae_rank",
    "mae_delta_vs_baseline_units",
    "mae_improvement_vs_baseline_percent",
    "within_practical_equivalence",
    "meets_minimum_baseline_improvement",
}
PUBLIC_CANDIDATE_FIELDS = (
    "model_id",
    "model_name",
    "model_family",
    "mae_rank",
    "mae_units",
    "rmse_units",
    "r2_contextual",
    "mae_improvement_vs_baseline_percent",
    "within_practical_equivalence",
    "production_status",
)
CARD_FIELDS = {
    "card_id",
    "eyebrow",
    "title",
    "status",
    "model_id",
    "primary_metric",
    "summary",
    "reasons",
    "limitation",
}


class ModelComparisonError(RuntimeError):
    """Raised when Model Comparison evidence is missing or invalid."""


class ModelComparisonService:
    """Return a stable read resource without executing analytical code."""

    def __init__(self, project_root: Path = PROJECT_ROOT) -> None:
        self.project_root = Path(project_root)

    @property
    def report_path(self) -> Path:
        return self.project_root / REPORT_RELATIVE_PATH

    def get_summary(self) -> dict[str, Any]:
        report = self._read_report()
        self._validate_report(report)
        comparison = self._record(report["comparison"], "comparison")
        decision = self._record(report["decision"], "decision")
        selected = self._record(
            decision["selected_candidate"], "selected candidate"
        )
        leader = self._record(
            decision["measurement_leader"], "measurement leader"
        )
        policy = self._record(decision["policy"], "decision policy")
        stability = self._record(
            decision["stability_evidence"], "stability evidence"
        )

        return {
            "schema_version": report["schema_version"],
            "module": report["module"],
            "report_status": report["report_status"],
            "experiment": deepcopy(report["experiment"]),
            "candidates": [
                {field: candidate[field] for field in PUBLIC_CANDIDATE_FIELDS}
                for candidate in comparison["rows"]
            ],
            "decision": {
                "measurement_leader": {
                    "model_id": leader["model_id"],
                    "model_name": leader["model_name"],
                    "mae_units": leader["mae_units"],
                },
                "selected_candidate": {
                    "model_id": selected["model_id"],
                    "model_name": selected["model_name"],
                    "mae_units": selected["mae_units"],
                    "mae_improvement_vs_baseline_percent": selected[
                        "mae_improvement_vs_baseline_percent"
                    ],
                    "largest_observed_error_units": selected[
                        "largest_observed_error_units"
                    ],
                },
                "practical_equivalence_units": policy[
                    "practical_equivalence_units"
                ],
                "rationale": deepcopy(decision["rationale"]),
                "production_status": decision["production_status"],
                "stability_status": stability["status"],
            },
            "decision_cards": deepcopy(report["decision_cards"]),
            "limitations": deepcopy(report["limitations"]),
        }

    def _read_report(self) -> dict[str, Any]:
        path = self.report_path
        if not path.is_file():
            raise ModelComparisonError("Model Comparison report is missing.")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ModelComparisonError(
                "Model Comparison report cannot be read."
            ) from error
        return self._record(payload, "Model Comparison report")

    def _validate_report(self, report: dict[str, Any]) -> None:
        if set(report) != TOP_LEVEL_FIELDS:
            raise ModelComparisonError("Model Comparison report fields are invalid.")
        if (
            report.get("schema_version") != "1.0"
            or report.get("module") != "model_comparison"
            or report.get("report_status") != "learning_evidence_only"
        ):
            raise ModelComparisonError("Model Comparison report identity is invalid.")

        experiment = self._record(report["experiment"], "experiment")
        if set(experiment) != {
            "dataset_sha256",
            "split_strategy",
            "target",
            "target_unit",
            "train_rows",
            "test_rows",
        }:
            raise ModelComparisonError("Experiment fields are invalid.")
        checksum = self._text(experiment, "dataset_sha256", "experiment")
        if len(checksum) != 64 or any(character not in "0123456789abcdef" for character in checksum):
            raise ModelComparisonError("Experiment checksum is invalid.")
        if (
            experiment.get("split_strategy") != "chronological_holdout"
            or experiment.get("target") != "units_sold"
            or experiment.get("target_unit") != "units_per_sale_record"
            or self._integer(experiment, "train_rows", "experiment") != 12
            or self._integer(experiment, "test_rows", "experiment") != 6
        ):
            raise ModelComparisonError("Experiment boundary is invalid.")

        comparison = self._record(report["comparison"], "comparison")
        rows = self._list(comparison.get("rows"), "comparison rows", length=4)
        candidates: dict[str, dict[str, Any]] = {}
        ranks: set[int] = set()
        for value in rows:
            candidate = self._record(value, "candidate")
            if set(candidate) != CANDIDATE_FIELDS:
                raise ModelComparisonError("Candidate fields are invalid.")
            model_id = self._text(candidate, "model_id", "candidate")
            if model_id in candidates:
                raise ModelComparisonError("Candidate identifiers must be unique.")
            self._text(candidate, "model_name", "candidate")
            self._text(candidate, "model_family", "candidate")
            for field in (
                "mae_units",
                "rmse_units",
                "r2_contextual",
                "mae_improvement_vs_baseline_percent",
            ):
                self._number(candidate, field, "candidate")
            rank = self._integer(candidate, "mae_rank", "candidate")
            ranks.add(rank)
            if (
                candidate.get("test_rows") != experiment["test_rows"]
                or candidate.get("production_status") != "learning_evidence_only"
                or not isinstance(candidate.get("within_practical_equivalence"), bool)
            ):
                raise ModelComparisonError("Candidate evidence is inconsistent.")
            candidates[model_id] = candidate
        if set(candidates) != EXPECTED_MODEL_IDS or ranks != {1, 2, 3, 4}:
            raise ModelComparisonError("Candidate identity or ranking is invalid.")

        decision = self._record(report["decision"], "decision")
        if (
            decision.get("dataset_sha256") != checksum
            or decision.get("decision_status") != "selected_for_next_integration"
            or decision.get("production_status") != "not_production_ready"
        ):
            raise ModelComparisonError("Decision boundary is invalid.")
        leader = self._record(decision.get("measurement_leader"), "measurement leader")
        selected = self._record(decision.get("selected_candidate"), "selected candidate")
        self._validate_decision_model(leader, candidates, "measurement leader")
        self._validate_decision_model(selected, candidates, "selected candidate")
        if leader.get("model_id") != "gradient_boosting" or selected.get("model_id") != "random_forest":
            raise ModelComparisonError("Decision identities conflict with frozen evidence.")
        rationale = self._list(decision.get("rationale"), "decision rationale")
        if not all(isinstance(item, str) and item.strip() for item in rationale):
            raise ModelComparisonError("Decision rationale is invalid.")
        policy = self._record(decision.get("policy"), "decision policy")
        self._number(policy, "practical_equivalence_units", "decision policy")
        stability = self._record(decision.get("stability_evidence"), "stability evidence")
        if stability.get("status") != "not_assessed":
            raise ModelComparisonError("Stability status is invalid.")

        cards = self._list(report["decision_cards"], "decision cards", length=3)
        card_ids: set[str] = set()
        for value in cards:
            card = self._record(value, "Decision Card")
            if set(card) != CARD_FIELDS:
                raise ModelComparisonError("Decision Card fields are invalid.")
            card_id = self._text(card, "card_id", "Decision Card")
            card_ids.add(card_id)
            for field in ("eyebrow", "title", "status", "summary", "limitation"):
                self._text(card, field, "Decision Card")
            reasons = self._list(card.get("reasons"), "Decision Card reasons")
            if not reasons or not all(isinstance(item, str) and item.strip() for item in reasons):
                raise ModelComparisonError("Decision Card reasons are invalid.")
            metric = self._record(card.get("primary_metric"), "Decision Card metric")
            if set(metric) != {"label", "value", "unit", "direction"}:
                raise ModelComparisonError("Decision Card metric fields are invalid.")
            self._number(metric, "value", "Decision Card metric")
            model_id = card.get("model_id")
            if model_id is not None and model_id not in candidates:
                raise ModelComparisonError("Decision Card model is invalid.")
        if card_ids != EXPECTED_CARD_IDS:
            raise ModelComparisonError("Decision Card identifiers are invalid.")

        limitations = self._list(report["limitations"], "limitations")
        if len(limitations) < 4 or not all(
            isinstance(item, str) and item.strip() for item in limitations
        ):
            raise ModelComparisonError("Limitations are invalid.")

    def _validate_decision_model(
        self,
        decision_model: dict[str, Any],
        candidates: dict[str, dict[str, Any]],
        label: str,
    ) -> None:
        model_id = self._text(decision_model, "model_id", label)
        if model_id not in candidates:
            raise ModelComparisonError(f"{label.title()} is absent from candidates.")
        mae = self._number(decision_model, "mae_units", label)
        if not isclose(mae, candidates[model_id]["mae_units"], abs_tol=1e-12):
            raise ModelComparisonError(f"{label.title()} metric is inconsistent.")

    @staticmethod
    def _record(value: Any, label: str) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise ModelComparisonError(f"{label} must be an object.")
        return value

    @staticmethod
    def _list(value: Any, label: str, *, length: int | None = None) -> list[Any]:
        if not isinstance(value, list) or (length is not None and len(value) != length):
            raise ModelComparisonError(f"{label} has an invalid collection shape.")
        return value

    @staticmethod
    def _text(container: dict[str, Any], field: str, label: str) -> str:
        value = container.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ModelComparisonError(f"{label} field {field} is invalid.")
        return value

    @staticmethod
    def _number(container: dict[str, Any], field: str, label: str) -> float:
        value = container.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ModelComparisonError(f"{label} field {field} is invalid.")
        return float(value)

    @staticmethod
    def _integer(container: dict[str, Any], field: str, label: str) -> int:
        value = container.get(field)
        if isinstance(value, bool) or not isinstance(value, int):
            raise ModelComparisonError(f"{label} field {field} is invalid.")
        return value
