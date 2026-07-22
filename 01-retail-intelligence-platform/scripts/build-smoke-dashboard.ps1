$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$FrontendRoot = Join-Path $ProjectRoot "frontend\dashboard-app"
$Compiler = Join-Path $FrontendRoot "node_modules\@esbuild\win32-x64\esbuild.exe"
$OutputRoot = Join-Path $ProjectRoot ".runtime\smoke-dashboard"

if (-not (Test-Path -LiteralPath $Compiler)) {
    throw "Frontend compiler not found: $Compiler"
}

New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
& $Compiler `
    (Join-Path $FrontendRoot "src\main.jsx") `
    "--bundle" `
    ("--outfile=" + (Join-Path $OutputRoot "main.js")) `
    "--loader:.jsx=jsx" `
    "--format=esm" `
    "--platform=browser" `
    "--define:import.meta.env={}"
if ($LASTEXITCODE -ne 0) {
    throw "Smoke dashboard compilation failed."
}

$Html = @"
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Retail Intelligence decision support platform" />
    <meta name="theme-color" content="#07110f" />
    <title>Retail Intelligence Platform</title>
    <link rel="stylesheet" href="/main.css" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/main.js"></script>
  </body>
</html>
"@
[System.IO.File]::WriteAllText(
    (Join-Path $OutputRoot "index.html"),
    $Html,
    [System.Text.UTF8Encoding]::new($false)
)

Write-Host "Smoke dashboard compiled: $OutputRoot"
Write-Host "API requests: same-origin through the smoke proxy"
