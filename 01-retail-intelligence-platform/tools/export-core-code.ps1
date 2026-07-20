[CmdletBinding()]
param(
    [string]$OutputPath = "",
    [ValidateRange(1, 10240)]
    [int]$MaxFileSizeKB = 512
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$DefaultOutputName = "codigo-completo-retail-intelligence-platform.txt"

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $ResolvedOutputPath = Join-Path $ProjectRoot $DefaultOutputName
}
elseif ([System.IO.Path]::IsPathRooted($OutputPath)) {
    $ResolvedOutputPath = [System.IO.Path]::GetFullPath($OutputPath)
}
else {
    $ResolvedOutputPath = [System.IO.Path]::GetFullPath(
        (Join-Path $ProjectRoot $OutputPath)
    )
}

$AllowedExtensions = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)
@(
    ".css",
    ".cfg",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".mjs",
    ".properties",
    ".ps1",
    ".py",
    ".scss",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml"
) | ForEach-Object {
    [void]$AllowedExtensions.Add($_)
}

$ExcludedPrefixes = @(
    ".git/",
    ".runtime/",
    ".venv/",
    "data/",
    "deployment/",
    "docs/sprints/",
    "frontend/dashboard-app/dist/",
    "frontend/dashboard-app/node_modules/",
    "models/",
    "reports/",
    "tools/"
)

$ExcludedPathFragments = @(
    "/__pycache__/",
    "/.pytest_cache/",
    "/.pytest-tmp/",
    "/.angular/",
    "/coverage/",
    "/htmlcov/",
    "/outputs/"
)

$ExcludedFileNames = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)
@(
    ".gitkeep",
    "package-lock.json",
    "pnpm-lock.yaml",
    "poetry.lock",
    "project-structure.txt",
    "yarn.lock"
) | ForEach-Object {
    [void]$ExcludedFileNames.Add($_)
}

function Test-IsExcludedPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RelativePath
    )

    $NormalizedPath = $RelativePath.Replace("\", "/")

    foreach ($Prefix in $ExcludedPrefixes) {
        if ($NormalizedPath.StartsWith(
                $Prefix,
                [System.StringComparison]::OrdinalIgnoreCase
            )) {
            return $true
        }
    }

    foreach ($Fragment in $ExcludedPathFragments) {
        if ($NormalizedPath.IndexOf(
                $Fragment,
                [System.StringComparison]::OrdinalIgnoreCase
            ) -ge 0) {
            return $true
        }
    }

    return $false
}

function Test-IsProbablyBinary {
    param(
        [Parameter(Mandatory = $true)]
        [byte[]]$Bytes
    )

    foreach ($Byte in $Bytes) {
        if ($Byte -eq 0) {
            return $true
        }
    }

    return $false
}

$GitPaths = @(
    & git -C $ProjectRoot ls-files --cached --others --exclude-standard
)
if ($LASTEXITCODE -ne 0) {
    throw "Git could not enumerate repository files."
}

$CandidatePaths = @(
    $GitPaths |
        ForEach-Object { $_.Trim().Replace("\", "/") } |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
        Sort-Object -Unique
)

$IncludedFiles = [System.Collections.Generic.List[object]]::new()
$SkippedByType = 0
$SkippedByPath = 0
$SkippedEmpty = 0
$SkippedLarge = 0
$SkippedBinary = 0
$MaximumBytes = $MaxFileSizeKB * 1KB

foreach ($RelativePath in $CandidatePaths) {
    if (Test-IsExcludedPath -RelativePath $RelativePath) {
        $SkippedByPath++
        continue
    }

    $FileName = [System.IO.Path]::GetFileName($RelativePath)
    if ($ExcludedFileNames.Contains($FileName)) {
        $SkippedByPath++
        continue
    }

    $Extension = [System.IO.Path]::GetExtension($RelativePath)
    if (-not $AllowedExtensions.Contains($Extension)) {
        $SkippedByType++
        continue
    }

    $AbsolutePath = Join-Path $ProjectRoot $RelativePath
    if (-not (Test-Path -LiteralPath $AbsolutePath -PathType Leaf)) {
        $SkippedByPath++
        continue
    }

    $File = Get-Item -LiteralPath $AbsolutePath -Force
    if (($File.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
        $SkippedByPath++
        continue
    }
    if ($File.Length -eq 0) {
        $SkippedEmpty++
        continue
    }
    if ($File.Length -gt $MaximumBytes) {
        $SkippedLarge++
        continue
    }

    $Bytes = [System.IO.File]::ReadAllBytes($AbsolutePath)
    if (Test-IsProbablyBinary -Bytes $Bytes) {
        $SkippedBinary++
        continue
    }

    $Text = [System.IO.File]::ReadAllText($AbsolutePath)
    $IncludedFiles.Add(
        [PSCustomObject]@{
            RelativePath = $RelativePath
            Folder = [System.IO.Path]::GetDirectoryName($RelativePath)
            Text = $Text
        }
    )
}

if ($IncludedFiles.Count -eq 0) {
    throw "No core files matched the export rules."
}

$Builder = [System.Text.StringBuilder]::new()
[void]$Builder.AppendLine("RETAIL INTELLIGENCE PLATFORM - CORE CODE CONTEXT")
[void]$Builder.AppendLine("Repository: 01-retail-intelligence-platform")
[void]$Builder.AppendLine("Branch: $(& git -C $ProjectRoot branch --show-current)")
[void]$Builder.AppendLine("Included files: $($IncludedFiles.Count)")
[void]$Builder.AppendLine("Maximum file size: $MaxFileSizeKB KB")
[void]$Builder.AppendLine("")
[void]$Builder.AppendLine("PURPOSE")
[void]$Builder.AppendLine(
    "Curated source context for architecture, implementation, tests and product contracts."
)
[void]$Builder.AppendLine(
    "Generated data, reports, binaries, dependencies, caches, builds and weekly notes are excluded."
)
[void]$Builder.AppendLine("")

$CurrentFolder = $null
foreach ($Entry in $IncludedFiles) {
    $Folder = $Entry.Folder
    if ([string]::IsNullOrWhiteSpace($Folder)) {
        $Folder = "."
    }

    if ($Folder -ne $CurrentFolder) {
        [void]$Builder.AppendLine(
            "========================================================================"
        )
        [void]$Builder.AppendLine("CARPETA: $Folder")
        $CurrentFolder = $Folder
    }

    [void]$Builder.AppendLine(
        "------------------------------------------------------------------------"
    )
    [void]$Builder.AppendLine("ARCHIVO: $($Entry.RelativePath)")
    [void]$Builder.AppendLine(
        "------------------------------------------------------------------------"
    )
    [void]$Builder.Append($Entry.Text.TrimEnd())
    [void]$Builder.AppendLine("")
    [void]$Builder.AppendLine("")
}

$OutputDirectory = Split-Path -Parent $ResolvedOutputPath
if (-not (Test-Path -LiteralPath $OutputDirectory -PathType Container)) {
    [void](New-Item -ItemType Directory -Path $OutputDirectory)
}

$Utf8WithoutBom = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText(
    $ResolvedOutputPath,
    $Builder.ToString(),
    $Utf8WithoutBom
)

$OutputFile = Get-Item -LiteralPath $ResolvedOutputPath
$OutputSizeKB = [Math]::Round($OutputFile.Length / 1KB, 2)

Write-Output "Core-code export completed."
Write-Output "Output: $ResolvedOutputPath"
Write-Output "Included files: $($IncludedFiles.Count)"
Write-Output "Output size: $OutputSizeKB KB"
Write-Output "Skipped by path: $SkippedByPath"
Write-Output "Skipped by type: $SkippedByType"
Write-Output "Skipped empty: $SkippedEmpty"
Write-Output "Skipped over $MaxFileSizeKB KB: $SkippedLarge"
Write-Output "Skipped binary: $SkippedBinary"
