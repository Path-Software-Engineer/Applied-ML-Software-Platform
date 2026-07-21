$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$RuntimeRoot = Join-Path $ProjectRoot ".runtime"
$FrontendRoot = Join-Path $ProjectRoot "frontend\dashboard-app"
$FrontendCompiler = Join-Path $FrontendRoot "node_modules\@esbuild\win32-x64\esbuild.exe"

if (-not (Test-Path $Python)) {
    throw "Project virtual environment not found: $Python"
}
if (-not (Test-Path $FrontendCompiler)) {
    throw "Frontend dependencies not found. Run npm ci in $FrontendRoot."
}

New-Item -ItemType Directory -Force -Path $RuntimeRoot | Out-Null

Push-Location $ProjectRoot
try {
    $PreviousMatplotlibConfig = $env:MPLCONFIGDIR
    $env:MPLCONFIGDIR = Join-Path $RuntimeRoot "matplotlib"
    New-Item -ItemType Directory -Force -Path $env:MPLCONFIGDIR | Out-Null

    Write-Host "[1/7] Verifying the repository structure inventory"
    & $Python "scripts/update-project-structure.py" --check
    if ($LASTEXITCODE -ne 0) { throw "Project structure inventory is stale." }

    Write-Host "[2/7] Compiling Python sources and checks"
    & $Python -m compileall -q `
        "ai-services/demand-insight/src" `
        "ai-services/demand-insight/checks" `
        "ai-services/model-comparison/src" `
        "ai-services/model-comparison/checks" `
        "backend/api/app" `
        "backend/api/checks" `
        "checks" `
        "tests/ai-services/demand-insight" `
        "tests/ai-services/model-comparison" `
        "tests/backend" `
        "scripts"
    if ($LASTEXITCODE -ne 0) { throw "Python compilation failed." }

    Write-Host "[3/7] Running automated Python tests"
    & $Python -m pytest -q
    if ($LASTEXITCODE -ne 0) { throw "Automated tests failed." }

    Write-Host "[4/7] Running frontend contract tests"
    Push-Location $FrontendRoot
    try {
        & npm test
        if ($LASTEXITCODE -ne 0) { throw "Frontend contract tests failed." }
    }
    finally {
        Pop-Location
    }

    Write-Host "[5/7] Compiling the frontend bundle"
    $FrontendOutput = Join-Path $RuntimeRoot "quality-gate\dashboard.js"
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $FrontendOutput) | Out-Null
    & $FrontendCompiler `
        (Join-Path $FrontendRoot "src\main.jsx") `
        "--bundle" `
        "--outfile=$FrontendOutput" `
        "--loader:.jsx=jsx" `
        "--format=esm" `
        "--platform=browser" `
        "--define:import.meta.env={}"
    if ($LASTEXITCODE -ne 0) { throw "Frontend bundle compilation failed." }

    Write-Host "[6/7] Building the local smoke dashboard"
    & (Join-Path $ProjectRoot "scripts\build-smoke-dashboard.ps1")
    if ($LASTEXITCODE -ne 0) { throw "Smoke dashboard compilation failed." }

    Write-Host "[7/7] Running manual end-to-end checks"
    $Checks = @(
        Get-ChildItem "ai-services/demand-insight/checks/check_*.py"
        Get-ChildItem "ai-services/model-comparison/checks/check_*.py"
        Get-ChildItem "backend/api/checks/check_*.py"
        Get-ChildItem "checks/check_*.py"
    ) | Sort-Object FullName

    foreach ($Check in $Checks) {
        Write-Host "  -> $($Check.Name)"
        & $Python $Check.FullName
        if ($LASTEXITCODE -ne 0) {
            throw "Manual check failed: $($Check.Name)"
        }
    }

    Write-Host (
        "Quality gate passed: Python and frontend tests, frontend compilation, " +
        "and $($Checks.Count) manual checks."
    )
}
finally {
    $env:MPLCONFIGDIR = $PreviousMatplotlibConfig
    Pop-Location
}
