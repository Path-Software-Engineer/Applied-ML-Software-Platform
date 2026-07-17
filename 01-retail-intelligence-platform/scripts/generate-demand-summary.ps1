$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    throw "Project virtual environment not found: $Python"
}

Push-Location $ProjectRoot
try {
    & $Python "backend/api/app/services/demand_summary_service.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Demand Summary generation failed."
    }
}
finally {
    Pop-Location
}
