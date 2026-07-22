$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Project virtual environment not found: $Python"
}

function Invoke-ProjectScript {
    param([Parameter(Mandatory = $true)][string]$RelativePath)

    Write-Host "  -> $RelativePath"
    & (Join-Path $ProjectRoot $RelativePath)
    if ($LASTEXITCODE -ne 0) {
        throw "Evidence step failed: $RelativePath"
    }
}

Push-Location $ProjectRoot
try {
    Write-Host "[1/3] Generating Demand Insight evidence"
    Invoke-ProjectScript "scripts\run-ai-service.ps1"
    foreach ($Module in @(
        "ai-services\demand-insight\src\analysis\sales_summary.py",
        "ai-services\demand-insight\src\insights\insight_cards.py",
        "ai-services\demand-insight\src\visualization\sales_visual_report.py"
    )) {
        & $Python $Module
        if ($LASTEXITCODE -ne 0) { throw "Demand Insight step failed: $Module" }
    }
    Invoke-ProjectScript "scripts\generate-report.ps1"

    Write-Host "[2/3] Generating Model Comparison evidence"
    foreach ($Script in @(
        "scripts\prepare-model-comparison.ps1",
        "scripts\run-model-comparison-baseline.ps1",
        "scripts\run-linear-regression.ps1",
        "scripts\run-random-forest.ps1",
        "scripts\run-gradient-boosting.ps1",
        "scripts\consolidate-model-comparison.ps1",
        "scripts\generate-model-comparison-table.ps1",
        "scripts\generate-model-error-analysis.ps1",
        "scripts\generate-model-decision.ps1",
        "scripts\generate-model-cards.ps1",
        "scripts\generate-model-comparison-report.ps1"
    )) {
        Invoke-ProjectScript $Script
    }

    Write-Host "[3/3] Generating Inventory Decision evidence"
    Invoke-ProjectScript "scripts\generate-inventory-decision.ps1"
}
finally {
    Pop-Location
}

Write-Host "Platform evidence generated for all three modules."
