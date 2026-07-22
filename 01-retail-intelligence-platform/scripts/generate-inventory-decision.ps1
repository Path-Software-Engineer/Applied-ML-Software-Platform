$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$ModuleRoot = Join-Path $ProjectRoot "ai-services\inventory-decision\src"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Project virtual environment not found: $Python"
}

$PreviousPythonPath = $env:PYTHONPATH
$PreviousMatplotlibConfig = $env:MPLCONFIGDIR
try {
    $env:PYTHONPATH = $ModuleRoot
    $env:MPLCONFIGDIR = Join-Path $ProjectRoot ".runtime\matplotlib"
    New-Item -ItemType Directory -Force -Path $env:MPLCONFIGDIR | Out-Null
    Push-Location $ProjectRoot
    try {
        $Commands = @(
            "from pathlib import Path; from inventory_decision.reporting import run_inventory_decision_report; run_inventory_decision_report(Path.cwd())",
            "from pathlib import Path; from inventory_decision.reporting import run_decision_trace; run_decision_trace(Path.cwd())",
            "from pathlib import Path; from inventory_decision.reporting import run_inventory_visual_report; run_inventory_visual_report(Path.cwd())"
        )
        foreach ($Command in $Commands) {
            & $Python -c $Command
            if ($LASTEXITCODE -ne 0) {
                throw "Inventory Decision evidence generation failed."
            }
        }
    }
    finally {
        Pop-Location
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:MPLCONFIGDIR = $PreviousMatplotlibConfig
}

Write-Host "Inventory Decision evidence generated: report, trace and figures"
