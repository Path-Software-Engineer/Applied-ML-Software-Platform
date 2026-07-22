"""Generate decision-support figures from canonical Inventory Decision evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


INK = "#16201c"
MUTED = "#66736d"
GRID = "#dce4df"
AMBER = "#e8963b"
RED = "#d45f50"
GREEN = "#61a879"
BLUE = "#5e9cb5"


def _style(axis: Any, *, title: str, subtitle: str) -> None:
    axis.set_title(title, loc="left", color=INK, fontsize=15, fontweight="bold", pad=20)
    axis.text(0, 1.02, subtitle, transform=axis.transAxes, color=MUTED, fontsize=8)
    axis.grid(axis="x", color=GRID, linewidth=0.7)
    axis.set_axisbelow(True)
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.tick_params(axis="both", colors=MUTED, labelsize=8, length=0)


def _save(figure: Any, path: Path) -> None:
    figure.savefig(
        path,
        dpi=160,
        bbox_inches="tight",
        facecolor="#f7faf8",
        metadata={"Software": "Retail Intelligence Platform"},
    )
    plt.close(figure)


def generate_inventory_figures(report: dict[str, Any], output_root: Path) -> list[dict[str, str]]:
    ranking = report.get("ranking")
    if not isinstance(ranking, list) or not ranking:
        raise ValueError("Inventory visual report requires ranked evidence.")
    output_root.mkdir(parents=True, exist_ok=True)
    products = [item["product_name"] for item in ranking]
    positions = list(range(len(products)))

    figure, axis = plt.subplots(figsize=(10, 5.2), layout="constrained")
    colors = [RED if item["risk_label"] == "critical" else AMBER if item["risk_label"] in {"high", "watch"} else GREEN for item in ranking]
    axis.barh(positions, [item["risk_score"] for item in ranking], color=colors, height=0.56)
    axis.set_yticks(positions, products)
    axis.invert_yaxis()
    axis.set_xlim(0, 100)
    axis.set_xlabel("Priority index (0–100; not probability)", color=MUTED, fontsize=8)
    _style(axis, title="Inventory review priority", subtitle=f"Policy {report['policy']['version']} · evidence {report['evidence_as_of_date']}")
    risk_path = output_root / "inventory_priority_index.png"
    _save(figure, risk_path)

    figure, axis = plt.subplots(figsize=(10, 5.2), layout="constrained")
    width = 0.25
    axis.barh([value - width for value in positions], [item["current_stock_units"] for item in ranking], height=width, color=BLUE, label="Current stock")
    axis.barh(positions, [item["reorder_point_units"] for item in ranking], height=width, color=AMBER, label="Reorder point")
    axis.barh([value + width for value in positions], [item["target_stock_units"] for item in ranking], height=width, color=GREEN, label="Target stock")
    axis.set_yticks(positions, products)
    axis.invert_yaxis()
    axis.set_xlabel("Whole units", color=MUTED, fontsize=8)
    axis.legend(frameon=False, fontsize=8, ncols=3, loc="lower right")
    _style(axis, title="Stock against policy levels", subtitle="Observed stock compared with versioned reorder and target quantities")
    levels_path = output_root / "inventory_stock_policy_levels.png"
    _save(figure, levels_path)

    finite = [item for item in ranking if item["coverage_days"] is not None]
    figure, axis = plt.subplots(figsize=(10, 4.8), layout="constrained")
    coverage_products = [item["product_name"] for item in finite]
    coverage = [item["coverage_days"] for item in finite]
    axis.barh(range(len(finite)), coverage, color=[RED if value < 3 else GREEN for value in coverage], height=0.56)
    axis.axvline(3, color=AMBER, linestyle="--", linewidth=1.2, label="Protected horizon: 3 days")
    axis.set_yticks(range(len(finite)), coverage_products)
    axis.invert_yaxis()
    axis.set_xlabel("Observed coverage days", color=MUTED, fontsize=8)
    axis.legend(frameon=False, fontsize=8, loc="lower right")
    _style(axis, title="Observed stock coverage", subtitle="Descriptive period-average demand; no forecast claim")
    coverage_path = output_root / "inventory_coverage_days.png"
    _save(figure, coverage_path)

    return [
        {"id": "priority-index", "path": risk_path.name, "caption": "Bread and Milk 1L lead the human review queue."},
        {"id": "stock-policy-levels", "path": levels_path.name, "caption": "Current stock is shown separately from reorder and target policy levels."},
        {"id": "coverage-days", "path": coverage_path.name, "caption": "Observed coverage uses descriptive demand and the three-day protected horizon."},
    ]


def render_visual_report(report: dict[str, Any], figures: list[dict[str, str]]) -> str:
    lines = [
        "# Inventory Decision Visual Report",
        "",
        f"Evidence date: `{report['evidence_as_of_date']}`  ",
        f"Policy: `{report['policy']['version']}`",
        "",
    ]
    for figure in figures:
        lines.extend(
            [
                f"## {figure['id'].replace('-', ' ').title()}",
                "",
                f"![{figure['caption']}](../../figures/inventory-decision/{figure['path']})",
                "",
                figure["caption"],
                "",
            ]
        )
    lines.extend(
        [
            "## Interpretation boundary",
            "",
            "Figures visualize the canonical report. Priority is not probability, observed demand is not a forecast, and suggested quantities require human review.",
            "",
        ]
    )
    return "\n".join(lines)


def run_inventory_visual_report(project_root: Path) -> list[dict[str, str]]:
    report_path = project_root / "reports/outputs/inventory-decision/inventory_decision_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    figures = generate_inventory_figures(
        report, project_root / "reports/figures/inventory-decision"
    )
    (project_root / "reports/outputs/inventory-decision/inventory_visual_report.md").write_text(
        render_visual_report(report, figures), encoding="utf-8", newline="\n"
    )
    return figures
