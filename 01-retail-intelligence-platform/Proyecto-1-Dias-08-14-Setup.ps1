param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("8", "9", "10", "11", "12", "13", "14")]
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
        Write-WarnSafe "Sección ya existe en ${Path}: $Marker"
        return
    }

    Add-Content -Path $Path -Value "`n$Section" -Encoding UTF8
    Write-Ok "Sección agregada a ${Path}: $Marker"
}

function Add-PythonBlockIfMissing {
    param(
        [string]$Path,
        [string]$Marker,
        [string]$Block
    )

    if (-not (Test-Path $Path)) {
        $parent = Split-Path -Path $Path -Parent
        if ($parent -and -not (Test-Path $parent)) {
            New-Item -ItemType Directory -Force -Path $parent | Out-Null
        }
        Set-Content -Path $Path -Value '"""Demand Insight Python module."""' -Encoding UTF8
        Write-Ok "Archivo base creado: $Path"
    }

    $current = Get-Content -Path $Path -Raw
    if ($current -like "*$Marker*") {
        Write-WarnSafe "Bloque Python ya existe en ${Path}: $Marker"
        return
    }

    Add-Content -Path $Path -Value "`n$Block" -Encoding UTF8
    Write-Ok "Bloque Python agregado a ${Path}: $Marker"
}

function Ensure-CommonDirectories {
    Ensure-Directory "ai-services\demand-insight\checks"
    Ensure-Directory "ai-services\demand-insight\src\features"
    Ensure-Directory "ai-services\demand-insight\src\baselines"
    Ensure-Directory "data\processed\demand-insight"
    Ensure-Directory "reports\summaries\demand-insight"
    Ensure-Directory "docs\sprints"
}

function Add-DaySection {
    param(
        [string]$Marker,
        [string]$DecisionSection,
        [string]$SprintSection
    )

    Add-SectionIfMissing -Path "docs\decisions.md" -Marker $Marker -Section $DecisionSection
    Add-SectionIfMissing -Path "docs\sprints\sprint-01-demand-insight.md" -Marker $Marker -Section $SprintSection
}

function Setup-Day8 {
    Assert-Branch -ExpectedBranch "feature/s1-d08-feature-baseline-exploration"
    Ensure-CommonDirectories

    $explorationMd = @'
# Sprint 1 — Week 2 Exploration

## Day

Day 8 — Feature, Baseline and Metric Exploration

## Goal

Prepare the technical map for the next execution days of the Demand Insight Module.

## Concepts to connect

```txt
processed data
→ temporal features
→ revenue
→ baseline
→ MAE
→ technical summary
```

## Central questions

- What signal can be extracted from the date column?
- Why does revenue matter for retail analysis?
- What does a mean baseline represent?
- Why do we need MAE before building better models?
- What is the difference between data, signal and insight?

## Execution map

```txt
Day 9  → temporal features
Day 10 → revenue and processed dataset
Day 11 → feature engineering integration
Day 12 → EDA flow lab
Day 13 → mean baseline
Day 14 → baseline MAE
```

## Rule

Week 2 does not start with dashboard work.

Week 2 starts by making the data more informative and measurable.
'@

    $checkPy = @'
"""Check Day 8 Week 2 exploration evidence."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

REQUIRED_FILES = [
    "docs/sprints/sprint-01-week-02-exploration.md",
    "docs/decisions.md",
    "docs/sprints/sprint-01-demand-insight.md",
]


def write_summary() -> None:
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "week_02_exploration_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        """# Week 2 Exploration Summary — Demand Insight Module

## Day

Day 8 — Feature, Baseline and Metric Exploration

## Exploration map

```txt
processed data
→ temporal features
→ revenue
→ baseline
→ MAE
→ technical summary
```

## Execution days prepared

```txt
Day 9  → temporal features
Day 10 → revenue and processed dataset
Day 11 → feature engineering integration
Day 12 → EDA flow lab
Day 13 → mean baseline
Day 14 → baseline MAE
```

## Status

```txt
Completed
```
""",
        encoding="utf-8",
    )


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (PROJECT_ROOT / path).exists()]
    write_summary()

    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "week_02_exploration_summary.md"
    if not summary_path.exists():
        raise AssertionError("Week 2 exploration summary was not created.")

    if missing:
        raise AssertionError(f"Missing Day 8 evidence: {missing}")

    print("OK - Day 8 Week 2 exploration check passed")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
'@

    New-FileIfMissing -Path "docs\sprints\sprint-01-week-02-exploration.md" -Content $explorationMd
    New-FileIfMissing -Path "ai-services\demand-insight\checks\check_week_02_exploration.py" -Content $checkPy

    $decisionSection = @'
<!-- DAY-08-FEATURE-BASELINE-EXPLORATION -->

## Decision 008 — Explore features, baseline and MAE before building reports

### Context

Week 1 created the data foundation for the Demand Insight Module.

Week 2 needs a clear technical map before execution continues.

### Decision

Use Day 8 to define the next execution flow:

```txt
processed data
→ temporal features
→ revenue
→ baseline
→ MAE
→ technical summary
```

### Why

Feature engineering and baseline metrics should be connected by intent, not added as isolated files.

### Status

Accepted.
'@

    $sprintSection = @'
<!-- DAY-08-FEATURE-BASELINE-EXPLORATION -->

## Day 8 — Feature, Baseline and Metric Exploration

### Goal

Prepare Week 2 execution around temporal features, revenue, baseline and MAE.

### Definition of Done

- Week 2 exploration document exists.
- Execution map for Days 9–14 is documented.
- The day check generates a summary.
'@

    Add-DaySection -Marker "DAY-08-FEATURE-BASELINE-EXPLORATION" -DecisionSection $decisionSection -SprintSection $sprintSection

    Write-Ok "Setup Día 8 completado. Ejecuta: .\.venv\Scripts\python.exe ai-services\demand-insight\checks\check_week_02_exploration.py"
}

function Ensure-FeatureEngineeringTemporalFunction {
    $block = @'
# DAY-09-TEMPORAL-FEATURES
import pandas as pd


def add_date_features(data: pd.DataFrame, date_column: str = "date") -> pd.DataFrame:
    """Add temporal features from a date column.

    Created for Sprint 1 Day 9 of the Demand Insight Module.
    """
    if date_column not in data.columns:
        raise ValueError(f"Missing required date column: {date_column}")

    enriched = data.copy()
    parsed_dates = pd.to_datetime(enriched[date_column], errors="coerce")

    if parsed_dates.isna().any():
        raise ValueError("Date column contains invalid dates.")

    enriched[date_column] = parsed_dates.dt.strftime("%Y-%m-%d")
    enriched["day_of_week"] = parsed_dates.dt.dayofweek
    enriched["month"] = parsed_dates.dt.month
    enriched["year"] = parsed_dates.dt.year
    enriched["is_weekend"] = enriched["day_of_week"].isin([5, 6])

    return enriched
'@

    Add-PythonBlockIfMissing -Path "ai-services\demand-insight\src\features\feature_engineering.py" -Marker "def add_date_features" -Block $block
}

function Ensure-FeatureEngineeringRevenueFunction {
    $block = @'
# DAY-10-REVENUE-PROCESSED-DATASET
import pandas as pd


def add_revenue_column(
    data: pd.DataFrame,
    units_column: str = "units_sold",
    price_column: str = "unit_price",
    revenue_column: str = "revenue",
) -> pd.DataFrame:
    """Add revenue as units sold multiplied by unit price.

    Created for Sprint 1 Day 10 of the Demand Insight Module.
    """
    required_columns = [units_column, price_column]
    missing_columns = [column for column in required_columns if column not in data.columns]

    if missing_columns:
        raise ValueError(f"Missing required revenue columns: {missing_columns}")

    enriched = data.copy()
    enriched[units_column] = pd.to_numeric(enriched[units_column], errors="coerce")
    enriched[price_column] = pd.to_numeric(enriched[price_column], errors="coerce")

    if enriched[[units_column, price_column]].isna().any().any():
        raise ValueError("Units or price columns contain invalid numeric values.")

    enriched[revenue_column] = enriched[units_column] * enriched[price_column]

    return enriched
'@

    Add-PythonBlockIfMissing -Path "ai-services\demand-insight\src\features\feature_engineering.py" -Marker "def add_revenue_column" -Block $block
}

function Ensure-FeatureEngineeringBuildFunction {
    $block = @'
# DAY-11-FEATURE-ENGINEERING-INTEGRATION
import pandas as pd


def build_sales_features(data: pd.DataFrame) -> pd.DataFrame:
    """Build the final sales feature dataset for the Demand Insight Module."""
    featured = add_date_features(data)
    featured = add_revenue_column(featured)
    return featured
'@

    Add-PythonBlockIfMissing -Path "ai-services\demand-insight\src\features\feature_engineering.py" -Marker "def build_sales_features" -Block $block
}

function Setup-Day9 {
    Assert-Branch -ExpectedBranch "feature/s1-d09-temporal-features"
    Ensure-CommonDirectories
    Ensure-FeatureEngineeringTemporalFunction

    $checkPy = @'
"""Check Day 9 temporal features."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.features.feature_engineering import add_date_features  # noqa: E402

INPUT_CANDIDATES = [
    "data/processed/demand-insight/sales_pipeline_ready.csv",
    "data/processed/demand-insight/sales_clean.csv",
]

REQUIRED_FEATURES = ["day_of_week", "month", "year", "is_weekend"]


def find_input_dataset() -> Path:
    for relative_path in INPUT_CANDIDATES:
        candidate = PROJECT_ROOT / relative_path
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No clean or pipeline-ready dataset found for temporal features.")


def write_summary(data: pd.DataFrame, input_path: Path, output_path: Path) -> None:
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "temporal_features_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        f"""# Temporal Features Summary

## Day

Day 9 — Temporal Features

## Input

```txt
{input_path.as_posix()}
```

## Output

```txt
{output_path.as_posix()}
```

## Features created

```txt
{', '.join(REQUIRED_FEATURES)}
```

## Result

| Metric | Value |
| ------ | ----: |
| Rows | {len(data)} |
| Columns | {len(data.columns)} |

## Status

```txt
Completed
```
""",
        encoding="utf-8",
    )


def main() -> None:
    input_path = find_input_dataset()
    data = pd.read_csv(input_path)
    featured = add_date_features(data)

    missing = [column for column in REQUIRED_FEATURES if column not in featured.columns]
    if missing:
        raise AssertionError(f"Missing temporal features: {missing}")

    output_path = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_temporal_features.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    featured.to_csv(output_path, index=False)
    write_summary(featured, input_path, output_path)

    print("OK - Day 9 temporal features check passed")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Rows: {len(featured)}")
    print(f"Columns: {len(featured.columns)}")


if __name__ == "__main__":
    main()
'@

    New-FileIfMissing -Path "ai-services\demand-insight\checks\check_temporal_features.py" -Content $checkPy

    $decisionSection = @'
<!-- DAY-09-TEMPORAL-FEATURES -->

## Decision 009 — Add temporal features to sales data

### Context

Sales data contains dates, but raw dates alone are not enough for demand analysis.

### Decision

Create temporal features from the date column:

```txt
day_of_week
month
year
is_weekend
```

### Why

Temporal signals help explain sales behavior across days, months and weekends.

### Status

Accepted.
'@

    $sprintSection = @'
<!-- DAY-09-TEMPORAL-FEATURES -->

## Day 9 — Temporal Features

### Goal

Create temporal features from the sales date column.

### Expected files

```txt
ai-services/demand-insight/src/features/feature_engineering.py
ai-services/demand-insight/checks/check_temporal_features.py
data/processed/demand-insight/sales_temporal_features.csv
reports/summaries/demand-insight/temporal_features_summary.md
```

### Definition of Done

- Temporal features are generated.
- The processed temporal dataset exists.
- The check script passes.
'@

    Add-DaySection -Marker "DAY-09-TEMPORAL-FEATURES" -DecisionSection $decisionSection -SprintSection $sprintSection
    Write-Ok "Setup Día 9 completado. Ejecuta: .\.venv\Scripts\python.exe ai-services\demand-insight\checks\check_temporal_features.py"
}

function Setup-Day10 {
    Assert-Branch -ExpectedBranch "feature/s1-d10-revenue-processed-dataset"
    Ensure-CommonDirectories
    Ensure-FeatureEngineeringTemporalFunction
    Ensure-FeatureEngineeringRevenueFunction

    $checkPy = @'
"""Check Day 10 revenue and processed dataset."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.features.feature_engineering import add_revenue_column  # noqa: E402

INPUT_CANDIDATES = [
    "data/processed/demand-insight/sales_temporal_features.csv",
    "data/processed/demand-insight/sales_pipeline_ready.csv",
    "data/processed/demand-insight/sales_clean.csv",
]


def find_input_dataset() -> Path:
    for relative_path in INPUT_CANDIDATES:
        candidate = PROJECT_ROOT / relative_path
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No processed dataset found for revenue calculation.")


def write_summary(data: pd.DataFrame, input_path: Path, output_path: Path) -> None:
    total_revenue = float(data["revenue"].sum())
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "revenue_processed_dataset_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        f"""# Revenue and Processed Dataset Summary

## Day

Day 10 — Revenue and Processed Dataset

## Input

```txt
{input_path.as_posix()}
```

## Output

```txt
{output_path.as_posix()}
```

## Rule

```txt
revenue = units_sold * unit_price
```

## Result

| Metric | Value |
| ------ | ----: |
| Rows | {len(data)} |
| Columns | {len(data.columns)} |
| Total revenue | {total_revenue:.2f} |

## Status

```txt
Completed
```
""",
        encoding="utf-8",
    )


def main() -> None:
    input_path = find_input_dataset()
    data = pd.read_csv(input_path)
    with_revenue = add_revenue_column(data)

    expected_revenue = with_revenue["units_sold"] * with_revenue["unit_price"]
    if not expected_revenue.equals(with_revenue["revenue"]):
        raise AssertionError("Revenue column does not match units_sold * unit_price.")

    output_path = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_revenue.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with_revenue.to_csv(output_path, index=False)
    write_summary(with_revenue, input_path, output_path)

    print("OK - Day 10 revenue processed dataset check passed")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Rows: {len(with_revenue)}")
    print(f"Columns: {len(with_revenue.columns)}")
    print(f"Total revenue: {with_revenue['revenue'].sum():.2f}")


if __name__ == "__main__":
    main()
'@

    New-FileIfMissing -Path "ai-services\demand-insight\checks\check_revenue_processed_dataset.py" -Content $checkPy

    $decisionSection = @'
<!-- DAY-10-REVENUE-PROCESSED-DATASET -->

## Decision 010 — Add revenue as a business signal

### Context

Units sold explain volume, but retail analysis also needs monetary value.

### Decision

Create a revenue column using:

```txt
revenue = units_sold * unit_price
```

### Why

Revenue allows the Demand Insight Module to compare products by business value, not only by units sold.

### Status

Accepted.
'@

    $sprintSection = @'
<!-- DAY-10-REVENUE-PROCESSED-DATASET -->

## Day 10 — Revenue and Processed Dataset

### Goal

Create the revenue column and export a revenue-ready processed dataset.

### Expected files

```txt
ai-services/demand-insight/checks/check_revenue_processed_dataset.py
data/processed/demand-insight/sales_revenue.csv
reports/summaries/demand-insight/revenue_processed_dataset_summary.md
```

### Definition of Done

- Revenue is calculated from units and price.
- The revenue processed dataset exists.
- The check script passes.
'@

    Add-DaySection -Marker "DAY-10-REVENUE-PROCESSED-DATASET" -DecisionSection $decisionSection -SprintSection $sprintSection
    Write-Ok "Setup Día 10 completado. Ejecuta: .\.venv\Scripts\python.exe ai-services\demand-insight\checks\check_revenue_processed_dataset.py"
}

function Setup-Day11 {
    Assert-Branch -ExpectedBranch "feature/s1-d11-feature-engineering"
    Ensure-CommonDirectories
    Ensure-FeatureEngineeringTemporalFunction
    Ensure-FeatureEngineeringRevenueFunction
    Ensure-FeatureEngineeringBuildFunction

    $checkPy = @'
"""Check Day 11 feature engineering integration."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.features.feature_engineering import build_sales_features  # noqa: E402

INPUT_CANDIDATES = [
    "data/processed/demand-insight/sales_pipeline_ready.csv",
    "data/processed/demand-insight/sales_clean.csv",
]

REQUIRED_FEATURES = ["day_of_week", "month", "year", "is_weekend", "revenue"]


def find_input_dataset() -> Path:
    for relative_path in INPUT_CANDIDATES:
        candidate = PROJECT_ROOT / relative_path
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No processed dataset found for feature engineering.")


def write_summary(data: pd.DataFrame, input_path: Path, output_path: Path) -> None:
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "feature_engineering_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        f"""# Feature Engineering Summary

## Day

Day 11 — Feature Engineering Integration

## Input

```txt
{input_path.as_posix()}
```

## Output

```txt
{output_path.as_posix()}
```

## Features

```txt
{', '.join(REQUIRED_FEATURES)}
```

## Result

| Metric | Value |
| ------ | ----: |
| Rows | {len(data)} |
| Columns | {len(data.columns)} |

## Status

```txt
Completed
```
""",
        encoding="utf-8",
    )


def main() -> None:
    input_path = find_input_dataset()
    data = pd.read_csv(input_path)
    features = build_sales_features(data)

    missing = [column for column in REQUIRED_FEATURES if column not in features.columns]
    if missing:
        raise AssertionError(f"Missing engineered features: {missing}")

    output_path = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_features.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(output_path, index=False)
    write_summary(features, input_path, output_path)

    print("OK - Day 11 feature engineering check passed")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Rows: {len(features)}")
    print(f"Columns: {len(features.columns)}")


if __name__ == "__main__":
    main()
'@

    New-FileIfMissing -Path "ai-services\demand-insight\checks\check_feature_engineering.py" -Content $checkPy

    $decisionSection = @'
<!-- DAY-11-FEATURE-ENGINEERING-INTEGRATION -->

## Decision 011 — Build a final feature engineering output

### Context

Temporal features and revenue exist as separate enrichments.

### Decision

Create a feature engineering integration step that produces the final feature dataset for the Demand Insight Module.

### Why

Later baseline and metric work should use one clear feature output.

### Status

Accepted.
'@

    $sprintSection = @'
<!-- DAY-11-FEATURE-ENGINEERING-INTEGRATION -->

## Day 11 — Feature Engineering Integration

### Goal

Combine temporal features and revenue into the final feature dataset.

### Expected files

```txt
ai-services/demand-insight/src/features/feature_engineering.py
ai-services/demand-insight/checks/check_feature_engineering.py
data/processed/demand-insight/sales_features.csv
reports/summaries/demand-insight/feature_engineering_summary.md
```

### Definition of Done

- The final feature dataset exists.
- Temporal features exist.
- Revenue exists.
- The check script passes.
'@

    Add-DaySection -Marker "DAY-11-FEATURE-ENGINEERING-INTEGRATION" -DecisionSection $decisionSection -SprintSection $sprintSection
    Write-Ok "Setup Día 11 completado. Ejecuta: .\.venv\Scripts\python.exe ai-services\demand-insight\checks\check_feature_engineering.py"
}

function Setup-Day12 {
    Assert-Branch -ExpectedBranch "feature/s1-d12-eda-flow-lab"
    Ensure-CommonDirectories
    Ensure-Directory "labs\tec-labs\tec-sales-eda-lab\src"
    Ensure-Directory "labs\tec-labs\tec-sales-eda-lab\outputs"

    $labPy = @'
"""Compare raw, clean and processed EDA flows for Demand Insight."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[4]


def find_raw_csv() -> Path:
    raw_dir = PROJECT_ROOT / "data" / "raw" / "demand-insight"
    csv_files = sorted(raw_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No raw CSV files found in {raw_dir}")
    return csv_files[0]


def dataset_info(label: str, path: Path) -> dict[str, object]:
    if not path.exists():
        return {"label": label, "path": path.as_posix(), "exists": False, "rows": 0, "columns": 0, "column_names": []}

    data = pd.read_csv(path)
    return {
        "label": label,
        "path": path.as_posix(),
        "exists": True,
        "rows": len(data),
        "columns": len(data.columns),
        "column_names": list(data.columns),
    }


def write_report(infos: list[dict[str, object]]) -> Path:
    output_path = PROJECT_ROOT / "labs" / "tec-labs" / "tec-sales-eda-lab" / "outputs" / "eda_flow_comparison.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for info in infos:
        status = "yes" if info["exists"] else "no"
        rows.append(f"| {info['label']} | {status} | {info['rows']} | {info['columns']} | `{info['path']}` |")

    content = f"""# EDA Flow Comparison

## Lab

`tec-sales-eda-lab`

## Goal

Compare the raw, clean and processed data flows of the Demand Insight Module.

## Comparison

| Dataset | Exists | Rows | Columns | Path |
| ------- | ------ | ---: | ------: | ---- |
{chr(10).join(rows)}

## Interpretation

```txt
raw shows what arrived
clean shows what was validated
processed shows what was enriched
```

## Status

```txt
Completed
```
"""

    output_path.write_text(content, encoding="utf-8")
    return output_path


def main() -> None:
    raw_path = find_raw_csv()
    clean_path = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_clean.csv"
    processed_path = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_features.csv"

    infos = [
        dataset_info("raw", raw_path),
        dataset_info("clean", clean_path),
        dataset_info("processed", processed_path),
    ]

    output_path = write_report(infos)
    print("OK - EDA flow comparison generated")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
'@

    $labReadme = @'
# tec-sales-eda-lab

## Goal

Compare the raw, clean and processed data flows of the Demand Insight Module.

## Flow

```txt
raw
→ clean
→ processed
```

## Central idea

```txt
raw shows what arrived
clean shows what was validated
processed shows what was enriched
```

## Output

```txt
outputs/eda_flow_comparison.md
```
'@

    $checkPy = @'
"""Check Day 12 EDA flow lab."""

from __future__ import annotations

import runpy
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
LAB_SCRIPT = PROJECT_ROOT / "labs" / "tec-labs" / "tec-sales-eda-lab" / "src" / "compare_eda_flows.py"
OUTPUT = PROJECT_ROOT / "labs" / "tec-labs" / "tec-sales-eda-lab" / "outputs" / "eda_flow_comparison.md"


def main() -> None:
    if not LAB_SCRIPT.exists():
        raise AssertionError(f"Missing lab script: {LAB_SCRIPT}")

    runpy.run_path(str(LAB_SCRIPT), run_name="__main__")

    if not OUTPUT.exists():
        raise AssertionError(f"Expected EDA comparison output was not created: {OUTPUT}")

    content = OUTPUT.read_text(encoding="utf-8")
    required_terms = ["raw", "clean", "processed"]
    missing_terms = [term for term in required_terms if term not in content.lower()]
    if missing_terms:
        raise AssertionError(f"EDA report is missing terms: {missing_terms}")

    print("OK - Day 12 EDA flow lab check passed")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
'@

    New-FileIfMissing -Path "labs\tec-labs\tec-sales-eda-lab\src\compare_eda_flows.py" -Content $labPy
    New-FileIfMissing -Path "labs\tec-labs\tec-sales-eda-lab\README.md" -Content $labReadme
    New-FileIfMissing -Path "ai-services\demand-insight\checks\check_eda_flow_lab.py" -Content $checkPy

    $decisionSection = @'
<!-- DAY-12-EDA-FLOW-LAB -->

## Decision 012 — Compare raw, clean and processed EDA flows

### Context

The project now has multiple data stages.

### Decision

Create a technical lab that compares raw, clean and processed data.

### Why

The lab makes the data transformation story visible and easier to explain.

### Status

Accepted.
'@

    $sprintSection = @'
<!-- DAY-12-EDA-FLOW-LAB -->

## Day 12 — EDA Flow Lab

### Goal

Compare the raw, clean and processed data flows.

### Expected files

```txt
labs/tec-labs/tec-sales-eda-lab/src/compare_eda_flows.py
labs/tec-labs/tec-sales-eda-lab/outputs/eda_flow_comparison.md
labs/tec-labs/tec-sales-eda-lab/README.md
ai-services/demand-insight/checks/check_eda_flow_lab.py
```

### Definition of Done

- The lab script runs.
- The EDA comparison report exists.
- The check script passes.
'@

    Add-DaySection -Marker "DAY-12-EDA-FLOW-LAB" -DecisionSection $decisionSection -SprintSection $sprintSection
    Write-Ok "Setup Día 12 completado. Ejecuta: .\.venv\Scripts\python.exe ai-services\demand-insight\checks\check_eda_flow_lab.py"
}

function Ensure-BaselineMeanFunctions {
    $block = @'
# DAY-13-MEAN-BASELINE
import pandas as pd


def calculate_mean_baseline(target: pd.Series) -> float:
    """Calculate the mean baseline value for a numeric target."""
    numeric_target = pd.to_numeric(target, errors="coerce").dropna()

    if numeric_target.empty:
        raise ValueError("Target is empty after numeric conversion.")

    return float(numeric_target.mean())


def create_mean_baseline_predictions(target: pd.Series) -> pd.Series:
    """Create constant predictions using the mean baseline value."""
    baseline_value = calculate_mean_baseline(target)
    return pd.Series([baseline_value] * len(target), index=target.index, name="mean_baseline_prediction")
'@

    Add-PythonBlockIfMissing -Path "ai-services\demand-insight\src\baselines\baseline.py" -Marker "def calculate_mean_baseline" -Block $block
}

function Ensure-BaselineMaeFunction {
    $block = @'
# DAY-14-BASELINE-MAE
import pandas as pd


def calculate_mae(y_true: pd.Series, y_pred: pd.Series) -> float:
    """Calculate mean absolute error between true and predicted values."""
    true_values = pd.to_numeric(y_true, errors="coerce")
    predicted_values = pd.to_numeric(y_pred, errors="coerce")

    if len(true_values) != len(predicted_values):
        raise ValueError("y_true and y_pred must have the same length.")

    valid = true_values.notna() & predicted_values.notna()
    if not valid.any():
        raise ValueError("No valid values available to calculate MAE.")

    return float((true_values[valid] - predicted_values[valid]).abs().mean())
'@

    Add-PythonBlockIfMissing -Path "ai-services\demand-insight\src\baselines\baseline.py" -Marker "def calculate_mae" -Block $block
}

function Setup-Day13 {
    Assert-Branch -ExpectedBranch "feature/s1-d13-mean-baseline"
    Ensure-CommonDirectories
    Ensure-BaselineMeanFunctions

    $checkPy = @'
"""Check Day 13 mean baseline."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.baselines.baseline import (  # noqa: E402
    calculate_mean_baseline,
    create_mean_baseline_predictions,
)

DATASET = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_features.csv"
TARGET_COLUMN = "units_sold"


def write_summary(baseline_value: float, rows: int) -> None:
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "mean_baseline_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        f"""# Mean Baseline Summary

## Day

Day 13 — Mean Baseline

## Target

```txt
{TARGET_COLUMN}
```

## Baseline

```txt
{baseline_value:.2f} units
```

## Result

| Metric | Value |
| ------ | ----: |
| Rows | {rows} |
| Baseline | {baseline_value:.2f} |

## Interpretation

The mean baseline does not learn patterns.

It gives the minimum reference that future models should beat.

## Status

```txt
Completed
```
""",
        encoding="utf-8",
    )


def main() -> None:
    if not DATASET.exists():
        raise FileNotFoundError(f"Missing feature dataset: {DATASET}")

    data = pd.read_csv(DATASET)
    if TARGET_COLUMN not in data.columns:
        raise AssertionError(f"Missing target column: {TARGET_COLUMN}")

    target = data[TARGET_COLUMN]
    baseline_value = calculate_mean_baseline(target)
    predictions = create_mean_baseline_predictions(target)

    if len(predictions) != len(target):
        raise AssertionError("Baseline predictions length does not match target length.")

    write_summary(baseline_value=baseline_value, rows=len(data))

    print("OK - Day 13 mean baseline check passed")
    print(f"Baseline: {baseline_value:.2f}")
    print("Summary: reports/summaries/demand-insight/mean_baseline_summary.md")


if __name__ == "__main__":
    main()
'@

    New-FileIfMissing -Path "ai-services\demand-insight\checks\check_mean_baseline.py" -Content $checkPy

    $decisionSection = @'
<!-- DAY-13-MEAN-BASELINE -->

## Decision 013 — Use mean baseline as first prediction reference

### Context

Before comparing models, the Demand Insight Module needs a basic reference prediction.

### Decision

Use the mean of `units_sold` as the first baseline.

### Why

A baseline provides a minimum standard that future models must beat.

### Status

Accepted.
'@

    $sprintSection = @'
<!-- DAY-13-MEAN-BASELINE -->

## Day 13 — Mean Baseline

### Goal

Calculate the first baseline for `units_sold`.

### Expected files

```txt
ai-services/demand-insight/src/baselines/baseline.py
ai-services/demand-insight/checks/check_mean_baseline.py
reports/summaries/demand-insight/mean_baseline_summary.md
```

### Definition of Done

- Mean baseline is calculated.
- Baseline predictions are generated.
- The summary exists.
- The check script passes.
'@

    Add-DaySection -Marker "DAY-13-MEAN-BASELINE" -DecisionSection $decisionSection -SprintSection $sprintSection
    Write-Ok "Setup Día 13 completado. Ejecuta: .\.venv\Scripts\python.exe ai-services\demand-insight\checks\check_mean_baseline.py"
}

function Setup-Day14 {
    Assert-Branch -ExpectedBranch "feature/s1-d14-baseline-mae"
    Ensure-CommonDirectories
    Ensure-BaselineMeanFunctions
    Ensure-BaselineMaeFunction

    $checkPy = @'
"""Check Day 14 baseline MAE."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.baselines.baseline import (  # noqa: E402
    calculate_mae,
    calculate_mean_baseline,
    create_mean_baseline_predictions,
)

DATASET = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_features.csv"
TARGET_COLUMN = "units_sold"


def write_summary(baseline_value: float, baseline_mae: float, rows: int) -> None:
    summary_path = PROJECT_ROOT / "reports" / "summaries" / "demand-insight" / "baseline_mae_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        f"""# Baseline MAE Summary

## Day

Day 14 — Baseline MAE

## Target

```txt
{TARGET_COLUMN}
```

## Results

| Metric | Value |
| ------ | ----: |
| Rows | {rows} |
| Baseline | {baseline_value:.2f} |
| Baseline MAE | {baseline_mae:.2f} |

## Interpretation

The baseline gives the base prediction.

MAE says how wrong that prediction is on average.

## Status

```txt
Completed
```
""",
        encoding="utf-8",
    )


def main() -> None:
    if not DATASET.exists():
        raise FileNotFoundError(f"Missing feature dataset: {DATASET}")

    data = pd.read_csv(DATASET)
    if TARGET_COLUMN not in data.columns:
        raise AssertionError(f"Missing target column: {TARGET_COLUMN}")

    target = data[TARGET_COLUMN]
    predictions = create_mean_baseline_predictions(target)
    baseline_value = calculate_mean_baseline(target)
    baseline_mae = calculate_mae(target, predictions)

    if baseline_mae < 0:
        raise AssertionError("MAE cannot be negative.")

    write_summary(baseline_value=baseline_value, baseline_mae=baseline_mae, rows=len(data))

    print("OK - Day 14 baseline MAE check passed")
    print(f"Baseline: {baseline_value:.2f}")
    print(f"Baseline MAE: {baseline_mae:.2f}")
    print("Summary: reports/summaries/demand-insight/baseline_mae_summary.md")


if __name__ == "__main__":
    main()
'@

    New-FileIfMissing -Path "ai-services\demand-insight\checks\check_baseline_mae.py" -Content $checkPy

    $decisionSection = @'
<!-- DAY-14-BASELINE-MAE -->

## Decision 014 — Evaluate the baseline with MAE

### Context

A baseline value alone does not say how wrong the prediction is.

### Decision

Use Mean Absolute Error to evaluate the mean baseline.

### Why

MAE gives an understandable average error in the same unit as the target: units sold.

### Status

Accepted.
'@

    $sprintSection = @'
<!-- DAY-14-BASELINE-MAE -->

## Day 14 — Baseline MAE

### Goal

Calculate MAE for the mean baseline.

### Expected files

```txt
ai-services/demand-insight/src/baselines/baseline.py
ai-services/demand-insight/checks/check_baseline_mae.py
reports/summaries/demand-insight/baseline_mae_summary.md
```

### Definition of Done

- Baseline value is calculated.
- Baseline predictions are generated.
- MAE is calculated.
- The summary exists.
- The check script passes.
'@

    Add-DaySection -Marker "DAY-14-BASELINE-MAE" -DecisionSection $decisionSection -SprintSection $sprintSection
    Write-Ok "Setup Día 14 completado. Ejecuta: .\.venv\Scripts\python.exe ai-services\demand-insight\checks\check_baseline_mae.py"
}

Assert-ProjectRoot

switch ($Day) {
    "8" { Setup-Day8 }
    "9" { Setup-Day9 }
    "10" { Setup-Day10 }
    "11" { Setup-Day11 }
    "12" { Setup-Day12 }
    "13" { Setup-Day13 }
    "14" { Setup-Day14 }
}
