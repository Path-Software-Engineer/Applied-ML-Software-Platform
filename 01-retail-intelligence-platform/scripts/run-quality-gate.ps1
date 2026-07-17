$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$RuntimeRoot = Join-Path $ProjectRoot ".runtime"

if (-not (Test-Path $Python)) {
    throw "Project virtual environment not found: $Python"
}

New-Item -ItemType Directory -Force -Path $RuntimeRoot | Out-Null

Push-Location $ProjectRoot
try {
    $PreviousMatplotlibConfig = $env:MPLCONFIGDIR
    $env:MPLCONFIGDIR = Join-Path $RuntimeRoot "matplotlib"
    New-Item -ItemType Directory -Force -Path $env:MPLCONFIGDIR | Out-Null

    Write-Host "[1/4] Verifying the repository structure inventory"
    & $Python "scripts/update-project-structure.py" --check
    if ($LASTEXITCODE -ne 0) { throw "Project structure inventory is stale." }

    Write-Host "[2/4] Compiling Python sources and checks"
    & $Python -m compileall -q `
        "ai-services/demand-insight/src" `
        "ai-services/demand-insight/checks" `
        "backend/api/app" `
        "backend/api/checks" `
        "tests/ai-services/demand-insight" `
        "tests/backend"
    if ($LASTEXITCODE -ne 0) { throw "Python compilation failed." }

    Write-Host "[3/4] Running automated tests"
    & $Python -m pytest -q
    if ($LASTEXITCODE -ne 0) { throw "Automated tests failed." }

    Write-Host "[4/4] Running manual end-to-end checks"
    $Checks = @(
        Get-ChildItem "ai-services/demand-insight/checks/check_*.py"
        Get-ChildItem "backend/api/checks/check_*.py"
    ) | Sort-Object FullName

    foreach ($Check in $Checks) {
        Write-Host "  -> $($Check.Name)"
        & $Python $Check.FullName
        if ($LASTEXITCODE -ne 0) {
            throw "Manual check failed: $($Check.Name)"
        }
    }

    Write-Host "Quality gate passed: pytest suite and $($Checks.Count) manual checks."
}
finally {
    $env:MPLCONFIGDIR = $PreviousMatplotlibConfig
    Pop-Location
}
