$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    $Python = "python"
}

Push-Location $ProjectRoot
try {
    $PreviousPythonPath = $env:PYTHONPATH
    $env:PYTHONPATH = Join-Path $ProjectRoot "ai-services\demand-insight"
    & $Python -c "from pathlib import Path; from src.data.data_cleaner import run_data_cleaning_pipeline; root=Path.cwd(); run_data_cleaning_pipeline(root/'data/raw/demand-insight/sales.csv', root/'data/processed/demand-insight/sales_clean.csv', root/'reports/summaries/demand-insight/data_cleaning_summary.md')"
    & $Python "ai-services/demand-insight/src/pipelines/first_data_pipeline.py"
    & $Python "ai-services/demand-insight/src/pipelines/feature_baseline_metric_pipeline.py"
    & $Python "ai-services/demand-insight/src/analysis/product_ranking.py"
    & $Python "ai-services/demand-insight/src/analysis/temporal_sales_analysis.py"
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    Pop-Location
}
