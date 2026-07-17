param(
    [int]$Port = 5173
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$FrontendRoot = Join-Path $ProjectRoot "frontend\dashboard-app"
$NodeModules = Join-Path $FrontendRoot "node_modules"

if (-not (Test-Path (Join-Path $FrontendRoot "package-lock.json"))) {
    throw "Frontend lock file not found. Install the pinned dependencies first."
}

if (-not (Test-Path $NodeModules)) {
    throw "Frontend dependencies not found. Run npm ci in $FrontendRoot."
}

Push-Location $FrontendRoot
try {
    & npm run dev -- --host 127.0.0.1 --port $Port
    if ($LASTEXITCODE -ne 0) {
        throw "Demand Insight dashboard stopped with an error."
    }
}
finally {
    Pop-Location
}
