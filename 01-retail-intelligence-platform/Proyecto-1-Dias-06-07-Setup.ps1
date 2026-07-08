param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("6", "7")]
    [string]$Day
)

$ErrorActionPreference = "Stop"

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-WarnSafe {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-Ok {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Assert-ProjectRoot {
    if (-not (Test-Path "README.md") -or -not (Test-Path "ai-services\demand-insight")) {
        throw "Ejecuta este script desde la raíz de 01-retail-intelligence-platform."
    }
}

function Assert-Branch {
    param([string]$ExpectedBranch)

    $currentBranch = git branch --show-current
    if ($currentBranch -ne $ExpectedBranch) {
        throw "Rama incorrecta. Estás en '$currentBranch'. Debes estar en '$ExpectedBranch'."
    }

    Write-Ok "Rama correcta: $currentBranch"
}

function Ensure-Directory {
    param([string]$Path)

    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Force -Path $Path | Out-Null
        Write-Ok "Directorio creado: $Path"
    }
    else {
        Write-Info "Directorio ya existe: $Path"
    }
}

function New-FileIfMissing {
    param(
        [string]$Path,
        [string]$Content
    )

    if (Test-Path $Path) {
        Write-WarnSafe "Archivo ya existe, no se sobreescribe: $Path"
        return
    }

    $parent = Split-Path -Path $Path -Parent
    if ($parent -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }

    Set-Content -Path $Path -Value $Content -Encoding UTF8
    Write-Ok "Archivo creado: $Path"
}

function Add-SectionIfMissing {
    param(
        [string]$Path,
        [string]$Marker,
        [string]$Section
    )

    if (-not (Test-Path $Path)) {
        $parent = Split-Path -Path $Path -Parent
        if ($parent -and -not (Test-Path $parent)) {
            New-Item -ItemType Directory -Force -Path $parent | Out-Null
        }
        Set-Content -Path $Path -Value "# $([System.IO.Path]::GetFileNameWithoutExtension($Path))`n" -Encoding UTF8
    }

    $current = Get-Content -Path $Path -Raw
    if ($current -like "*$Marker*") {
        Write-WarnSafe "Section already exists in ${Path}: $Marker"
        return
    }

    Add-Content -Path $Path -Value "`n$Section" -Encoding UTF8
    Write-Ok "Sección agregada a ${Path}: $Marker"
}

function Setup-Day6 {
    Assert-Branch -ExpectedBranch "feature/s1-d06-first-data-pipeline"

    Ensure-Directory "ai-services\demand-insight\src\pipelines"
    Ensure-Directory "ai-services\demand-insight\checks"
    Ensure-Directory "data\processed\demand-insight"
    Ensure-Directory "reports\summaries\demand-insight"
    Ensure-Directory "docs\sprints"

    $pipelinePy = @'
"""First data pipeline for the Demand Insight Module.

This module connects the previous work from Day 4 and Day 5:
raw sales data -> validation -> cleaning -> pipeline-ready dataset -> summary.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["date", "product_id", "product_name", "units_sold", "unit_price"]
RAW_DATA_CANDIDATES = ["sales.csv", "sales_raw.csv", "retail_sales.csv"]


def find_raw_sales_file(project_root: Path) -> Path:
    """Find the raw sales CSV inside data/raw/demand-insight."""
    raw_dir = project_root / "data" / "raw" / "demand-insight"

    for filename in RAW_DATA_CANDIDATES:
        candidate = raw_dir / filename
        if candidate.exists():
            return candidate

    csv_files = sorted(raw_dir.glob("*.csv"))
    if csv_files:
        return csv_files[0]

    raise FileNotFoundError(f"No CSV file found in {raw_dir}")


def load_raw_sales_data(raw_data_path: str | Path) -> pd.DataFrame:
    """Load raw sales data from CSV."""
    path = Path(raw_data_path)

    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found: {path}")

    return pd.read_csv(path)


def validate_required_columns(data: pd.DataFrame) -> None:
    """Validate that the dataset contains the required sales columns."""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in data.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def prepare_pipeline_dataset(data: pd.DataFrame) -> pd.DataFrame:
    """Create a clean, pipeline-ready dataset from raw sales data."""
    validate_required_columns(data)

    prepared = data.copy()
    prepared = prepared.drop_duplicates()
    prepared = prepared.dropna(subset=REQUIRED_COLUMNS)

    prepared["date"] = pd.to_datetime(prepared["date"], errors="coerce")
    prepared["units_sold"] = pd.to_numeric(prepared["units_sold"], errors="coerce")
    prepared["unit_price"] = pd.to_numeric(prepared["unit_price"], errors="coerce")

    prepared = prepared.dropna(subset=["date", "units_sold", "unit_price"])
    prepared = prepared[prepared["units_sold"] >= 0]
    prepared = prepared[prepared["unit_price"] >= 0]

    prepared = prepared.sort_values(["date", "product_id"]).reset_index(drop=True)
    prepared["date"] = prepared["date"].dt.strftime("%Y-%m-%d")

    return prepared


def write_pipeline_summary(
    data: pd.DataFrame,
    raw_data_path: str | Path,
    output_path: str | Path,
    summary_path: str | Path,
) -> None:
    """Write a markdown summary for the first data pipeline."""
    raw_path = Path(raw_data_path)
    output = Path(output_path)
    summary = Path(summary_path)
    summary.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# First Data Pipeline Summary

## Sprint

Sprint 1 — Demand Insight Module

## Day

Day 6 — First Data Pipeline

## Pipeline flow

```txt
raw sales data
→ load dataset
→ validate required columns
→ clean rows
→ export pipeline-ready dataset
→ write summary
```

## Inputs

```txt
{raw_path.as_posix()}
```

## Outputs

```txt
{output.as_posix()}
```

## Result

| Metric | Value |
| ------ | ----: |
| Rows | {len(data)} |
| Columns | {len(data.columns)} |

## Required columns

```txt
{', '.join(REQUIRED_COLUMNS)}
```

## Interpretation

The Demand Insight Module now has a repeatable first data pipeline.

This pipeline connects raw data loading, column validation, cleaning rules and a processed output that can be reused by later feature engineering, baseline and insight steps.

## Status

```txt
Completed
```
"""

    summary.write_text(content, encoding="utf-8")


def build_pipeline_ready_dataset(
    raw_data_path: str | Path,
    output_path: str | Path,
    summary_path: str | Path | None = None,
) -> pd.DataFrame:
    """Run the first data pipeline and return the pipeline-ready dataset."""
    raw_data = load_raw_sales_data(raw_data_path)
    pipeline_ready = prepare_pipeline_dataset(raw_data)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    pipeline_ready.to_csv(output, index=False)

    if summary_path is not None:
        write_pipeline_summary(
            data=pipeline_ready,
            raw_data_path=raw_data_path,
            output_path=output_path,
            summary_path=summary_path,
        )

    return pipeline_ready
'@

    $checkDay6Py = @'
"""Check Day 6 first data pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.pipelines.first_data_pipeline import (  # noqa: E402
    REQUIRED_COLUMNS,
    build_pipeline_ready_dataset,
    find_raw_sales_file,
)


def main() -> None:
    raw_data_path = find_raw_sales_file(PROJECT_ROOT)
    output_path = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_pipeline_ready.csv"
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "first_data_pipeline_summary.md"

    pipeline_ready = build_pipeline_ready_dataset(
        raw_data_path=raw_data_path,
        output_path=output_path,
        summary_path=summary_path,
    )

    if pipeline_ready.empty:
        raise AssertionError("Pipeline-ready dataset is empty.")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in pipeline_ready.columns]
    if missing_columns:
        raise AssertionError(f"Missing required columns in pipeline output: {missing_columns}")

    if not output_path.exists():
        raise AssertionError(f"Expected output file was not created: {output_path}")

    if not summary_path.exists():
        raise AssertionError(f"Expected summary file was not created: {summary_path}")

    print("OK - Day 6 first data pipeline check passed")
    print(f"Raw data: {raw_data_path}")
    print(f"Output: {output_path}")
    print(f"Summary: {summary_path}")
    print(f"Rows: {len(pipeline_ready)}")
    print(f"Columns: {len(pipeline_ready.columns)}")


if __name__ == "__main__":
    main()
'@

    New-FileIfMissing -Path "ai-services\demand-insight\src\pipelines\first_data_pipeline.py" -Content $pipelinePy
    New-FileIfMissing -Path "ai-services\demand-insight\checks\check_first_data_pipeline.py" -Content $checkDay6Py

    $decisionSection = @'
<!-- DAY-06-FIRST-DATA-PIPELINE -->

## Decision 006 — First data pipeline for Demand Insight

### Context

The Demand Insight Module already has data loading and data cleaning pieces.

The next step is to connect those pieces into a repeatable pipeline that creates a pipeline-ready dataset and a technical summary.

### Decision

Create a first data pipeline responsible for:

```txt
raw sales data
→ validation
→ cleaning
→ pipeline-ready output
→ summary report
```

### Why

A pipeline makes the data workflow repeatable and prevents manual steps from becoming hidden requirements.

Later work such as feature engineering, baseline calculation, MAE and insight cards should depend on a clear processed output.

### Consequences

The project now has a stronger base for Sprint 1.

Future modules can reuse the pipeline output instead of reading raw data directly.

### Status

Accepted.
'@

    $sprintSection = @'
<!-- DAY-06-FIRST-DATA-PIPELINE -->

## Day 6 — First Data Pipeline

### Goal

Connect data loading and data cleaning into a repeatable first pipeline.

### Flow

```txt
raw sales data
→ load dataset
→ validate columns
→ clean rows
→ export pipeline-ready dataset
→ generate summary
```

### Expected files

```txt
ai-services/demand-insight/src/pipelines/first_data_pipeline.py
ai-services/demand-insight/checks/check_first_data_pipeline.py
data/processed/demand-insight/sales_pipeline_ready.csv
reports/summaries/demand-insight/first_data_pipeline_summary.md
```

### Definition of Done

- The raw dataset can be loaded.
- Required columns are validated.
- Cleaning rules are applied inside the pipeline.
- A pipeline-ready dataset is generated.
- A technical summary is generated.
- The check script passes without errors.
'@

    Add-SectionIfMissing -Path "docs\decisions.md" -Marker "DAY-06-FIRST-DATA-PIPELINE" -Section $decisionSection
    Add-SectionIfMissing -Path "docs\sprints\sprint-01-demand-insight.md" -Marker "DAY-06-FIRST-DATA-PIPELINE" -Section $sprintSection

    Write-Ok "Setup Día 6 completado. Ejecuta el check con .\.venv\Scripts\python.exe ai-services\demand-insight\checks\check_first_data_pipeline.py"
}

function Setup-Day7 {
    Assert-Branch -ExpectedBranch "feature/s1-d07-week-01-close"

    Ensure-Directory "ai-services\demand-insight\checks"
    Ensure-Directory "docs\sprints"
    Ensure-Directory "reports\summaries\demand-insight"

    $checkDay7Py = @'
"""Check Day 7 week 1 close evidence."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

REQUIRED_PATHS = [
    "README.md",
    "project-structure.txt",
    "docs/architecture.md",
    "docs/decisions.md",
    "docs/user-stories.md",
    "docs/technical-stories.md",
    "docs/sprints/sprint-01-demand-insight.md",
    "ai-services/demand-insight/src/data/data_loader.py",
    "ai-services/demand-insight/checks/check_data_loading.py",
    "ai-services/demand-insight/src/data/data_cleaner.py",
    "ai-services/demand-insight/checks/check_data_cleaning.py",
    "ai-services/demand-insight/src/pipelines/first_data_pipeline.py",
    "ai-services/demand-insight/checks/check_first_data_pipeline.py",
    "data/processed/demand-insight/sales_pipeline_ready.csv",
    "reports/summaries/demand-insight/first_data_pipeline_summary.md",
]


def write_week_close_summary(missing_paths: list[str], raw_csv_count: int) -> None:
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "week_01_close_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    status = "Completed" if not missing_paths and raw_csv_count > 0 else "Needs review"
    missing_text = "None" if not missing_paths else "\n".join(f"- {path}" for path in missing_paths)

    content = f"""# Week 1 Close Summary — Demand Insight Module

## Sprint

Sprint 1 — Demand Insight Module

## Day

Day 7 — Week 1 Close

## Week 1 focus

```txt
project base
→ dataset setup
→ data loading
→ data cleaning
→ first data pipeline
→ documentation close
```

## Evidence status

| Evidence | Status |
| -------- | ------ |
| Raw CSV files found | {raw_csv_count} |
| Missing required paths | {len(missing_paths)} |
| Week close status | {status} |

## Missing paths

{missing_text}

## Interpretation

Week 1 closes the foundation of the Demand Insight Module.

The project is ready to move toward feature engineering, baseline, metrics and insight generation only after the missing path count is zero.

## Status

```txt
{status}
```
"""

    summary_path.write_text(content, encoding="utf-8")


def main() -> None:
    raw_dir = PROJECT_ROOT / "data" / "raw" / "demand-insight"
    raw_csv_count = len(list(raw_dir.glob("*.csv"))) if raw_dir.exists() else 0

    missing_paths = [path for path in REQUIRED_PATHS if not (PROJECT_ROOT / path).exists()]
    write_week_close_summary(missing_paths=missing_paths, raw_csv_count=raw_csv_count)

    if raw_csv_count == 0:
        raise AssertionError("No raw CSV files found in data/raw/demand-insight.")

    if missing_paths:
        raise AssertionError(f"Missing required Week 1 evidence: {missing_paths}")

    print("OK - Day 7 week 1 close check passed")
    print("Summary: reports/summaries/demand-insight/week_01_close_summary.md")


if __name__ == "__main__":
    main()
'@

    $weekReviewMd = @'
# Sprint 1 — Week 1 Review

## Sprint

Sprint 1 — Demand Insight Module

## Week

Week 1

## Days covered

```txt
Day 1 — Exploration
Day 2 — Base architecture
Day 3 — Initial dataset and data contract
Day 4 — Data loading
Day 5 — Data cleaning
Day 6 — First data pipeline
Day 7 — Week close
```

## Goal

Close the first foundation week of the Demand Insight Module.

## Evidence expected

```txt
project structure
architecture docs
decisions.md
raw dataset
data contract
data loader
data cleaner
first data pipeline
summary reports
```

## Review

Week 1 establishes the base that allows the project to move from raw data into repeatable data processing.

The next week should focus on feature engineering, revenue, baseline, MAE and the first technical report.

## Rule

Do not move to dashboard work until the data pipeline, features, baseline and metric evidence are clear.
'@

    New-FileIfMissing -Path "ai-services\demand-insight\checks\check_week_01_close.py" -Content $checkDay7Py
    New-FileIfMissing -Path "docs\sprints\sprint-01-week-01-review.md" -Content $weekReviewMd

    $decisionSection = @'
<!-- DAY-07-WEEK-01-CLOSE -->

## Decision 007 — Close Week 1 with evidence checklist

### Context

The first week created the base of the Demand Insight Module.

Before moving into features, baseline and metrics, the project needs a checkpoint that confirms evidence exists.

### Decision

Use a Week 1 close check that verifies core files, raw data, data loading, data cleaning, first pipeline and summaries.

### Why

A week close prevents silent gaps from moving forward into later work.

### Consequences

The project can start Week 2 with a clearer foundation.

### Status

Accepted.
'@

    $sprintSection = @'
<!-- DAY-07-WEEK-01-CLOSE -->

## Day 7 — Week 1 Close

### Goal

Close the first week of Sprint 1 with evidence, documentation and a clear checkpoint.

### Expected files

```txt
ai-services/demand-insight/checks/check_week_01_close.py
docs/sprints/sprint-01-week-01-review.md
reports/summaries/demand-insight/week_01_close_summary.md
```

### Definition of Done

- The week close check passes.
- Week 1 evidence is documented.
- Missing files are identified if something is incomplete.
- A Week 1 summary is generated.
- The project is ready for Week 2 only if the checklist is clean.
'@

    Add-SectionIfMissing -Path "docs\decisions.md" -Marker "DAY-07-WEEK-01-CLOSE" -Section $decisionSection
    Add-SectionIfMissing -Path "docs\sprints\sprint-01-demand-insight.md" -Marker "DAY-07-WEEK-01-CLOSE" -Section $sprintSection

    Write-Ok "Setup Día 7 completado. Ejecuta el check con .\.venv\Scripts\python.exe ai-services\demand-insight\checks\check_week_01_close.py"
}

Assert-ProjectRoot

if ($Day -eq "6") {
    Setup-Day6
}
elseif ($Day -eq "7") {
    Setup-Day7
}
