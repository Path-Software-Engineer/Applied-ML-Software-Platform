$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$ModuleRoot = Join-Path $ProjectRoot "ai-services\model-comparison\src"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Project virtual environment not found: $Python"
}

$PreviousPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = if ($PreviousPythonPath) {
        "$ModuleRoot;$PreviousPythonPath"
    }
    else {
        $ModuleRoot
    }
    Push-Location $ProjectRoot
    try {
        & $Python -m model_comparison.random_forest
        if ($LASTEXITCODE -ne 0) {
            throw "Random Forest evaluation failed."
        }
    }
    finally {
        Pop-Location
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
}
