$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$ModuleRoot = Join-Path $ProjectRoot "ai-services\model-comparison\src"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Project virtual environment not found: $Python"
}

$PreviousPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = $ModuleRoot
    Push-Location $ProjectRoot
    try {
        & $Python -m model_comparison.data
        if ($LASTEXITCODE -ne 0) {
            throw "Model Comparison preparation failed."
        }
    }
    finally {
        Pop-Location
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
}
