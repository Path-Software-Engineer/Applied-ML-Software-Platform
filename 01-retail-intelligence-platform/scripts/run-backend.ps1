param(
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    throw "Project virtual environment not found: $Python"
}

Push-Location $ProjectRoot
try {
    & $Python -m uvicorn backend.api.app.main:app `
        --host 127.0.0.1 `
        --port $Port
    if ($LASTEXITCODE -ne 0) {
        throw "Retail Intelligence API stopped with an error."
    }
}
finally {
    Pop-Location
}
