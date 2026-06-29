$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "Running data pipeline..."
python -m src.pipeline

if ($LASTEXITCODE -ne 0) {
    throw "Data pipeline failed."
}

Write-Host "Data pipeline finished successfully."