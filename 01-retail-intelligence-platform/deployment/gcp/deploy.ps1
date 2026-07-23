[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern("^[a-z][a-z0-9-]{4,28}[a-z0-9]$")]
    [string]$ProjectId,

    [ValidatePattern("^[a-z]+-[a-z]+[0-9]+$")]
    [string]$Region = "us-central1",

    [ValidatePattern("^[a-z][a-z0-9-]{0,62}$")]
    [string]$Repository = "retail-intelligence",

    [ValidatePattern("^[A-Za-z0-9_.-]+$")]
    [string]$ImageTag = "",

    [switch]$ReusePublishedImages,

    [switch]$ReuseExistingApi,

    [switch]$SmokeOnly,

    [ValidatePattern("^[a-z][a-z0-9-]{0,47}[a-z0-9]$")]
    [string]$ApiService = "retail-intelligence-api",

    [ValidatePattern("^[a-z][a-z0-9-]{0,47}[a-z0-9]$")]
    [string]$WebService = "retail-intelligence-web"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$RuntimeServiceAccountName = "retail-platform-runtime"
$RuntimeServiceAccount = "$RuntimeServiceAccountName@$ProjectId.iam.gserviceaccount.com"
$GCloudCommandInfo = Get-Command gcloud.cmd -ErrorAction SilentlyContinue
if (-not $GCloudCommandInfo) {
    $GCloudCommandInfo = Get-Command gcloud -ErrorAction SilentlyContinue
}
if (-not $GCloudCommandInfo) {
    throw "Google Cloud CLI is not installed or is not available in PATH."
}
$GCloudCommand = $GCloudCommandInfo.Source

function Invoke-GCloud {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)

    $PreviousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        & $script:GCloudCommand @Arguments
        $ExitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $PreviousErrorActionPreference
    }
    if ($ExitCode -ne 0) {
        throw "gcloud command failed: gcloud $($Arguments -join ' ')"
    }
}

function Read-GCloudValue {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)

    $PreviousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $Value = & $script:GCloudCommand @Arguments
        $ExitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $PreviousErrorActionPreference
    }
    if ($ExitCode -ne 0) {
        throw "gcloud query failed: gcloud $($Arguments -join ' ')"
    }
    return ($Value | Out-String).Trim()
}

function Wait-GCloudCommand {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string[]]$Arguments,
        [ValidateRange(1, 60)][int]$Attempts = 24,
        [ValidateRange(1, 30)][int]$DelaySeconds = 5
    )

    for ($Attempt = 1; $Attempt -le $Attempts; $Attempt++) {
        $PreviousErrorActionPreference = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        try {
            & $script:GCloudCommand @Arguments *> $null
            $ExitCode = $LASTEXITCODE
        }
        finally {
            $ErrorActionPreference = $PreviousErrorActionPreference
        }
        if ($ExitCode -eq 0) {
            return
        }
        if ($Attempt -eq $Attempts) {
            throw "$Label did not become ready after $Attempts attempts."
        }
        Write-Host "$Label is still propagating ($Attempt/$Attempts); retrying in $DelaySeconds seconds."
        Start-Sleep -Seconds $DelaySeconds
    }
}

function Invoke-RestMethodWithRetry {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string]$Uri,
        [ValidateRange(1, 30)][int]$Attempts = 12,
        [ValidateRange(1, 30)][int]$DelaySeconds = 5
    )

    for ($Attempt = 1; $Attempt -le $Attempts; $Attempt++) {
        try {
            return Invoke-RestMethod -Uri $Uri -Method Get -TimeoutSec 30 -ErrorAction Stop
        }
        catch {
            if ($Attempt -eq $Attempts) {
                throw "$Label did not become reachable after $Attempts attempts. Last error: $($_.Exception.Message)"
            }
            Write-Host "$Label is not reachable yet ($Attempt/$Attempts); retrying in $DelaySeconds seconds."
            Start-Sleep -Seconds $DelaySeconds
        }
    }
}

function Test-RemoteDeployment {
    param(
        [Parameter(Mandatory = $true)][string]$ApiUrl,
        [Parameter(Mandatory = $true)][string]$WebUrl
    )

    $ApiHealth = Invoke-RestMethodWithRetry -Label "API health endpoint" -Uri "$ApiUrl/health"
    $WebHealth = Invoke-RestMethodWithRetry -Label "Frontend health endpoint" -Uri "$WebUrl/health"
    $Demand = Invoke-RestMethodWithRetry -Label "Demand Insight endpoint" -Uri "$ApiUrl/api/v1/demand-insights/summary"
    $Comparison = Invoke-RestMethodWithRetry -Label "Model Comparison endpoint" -Uri "$ApiUrl/api/v1/model-comparisons/summary"
    $Inventory = Invoke-RestMethodWithRetry -Label "Inventory Decision endpoint" -Uri "$ApiUrl/api/v1/inventory-decisions/summary"

    if ($ApiHealth.status -ne "ok" -or $WebHealth.status -ne "ok") {
        throw "A deployed health endpoint returned an unexpected payload."
    }
    if (
        $Demand.schema_version -ne "1.0" -or
        $Comparison.schema_version -ne "1.0" -or
        $Inventory.schema_version -ne "1.0"
    ) {
        throw "A deployed resource returned an unsupported schema version."
    }
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is required to derive and verify the immutable image tag."
}

Push-Location $ProjectRoot
try {
    $Dirty = git status --porcelain -- .
    if ($LASTEXITCODE -ne 0) { throw "Unable to inspect the Git working tree." }
    if ($Dirty) {
        throw "Deployment requires a clean working tree. Commit and validate first."
    }

    if ($ReusePublishedImages -and -not $ImageTag) {
        throw "ReusePublishedImages requires the explicit ImageTag that completed both builds."
    }
    if ($ReusePublishedImages -and $ReuseExistingApi) {
        throw "ReusePublishedImages and ReuseExistingApi are mutually exclusive."
    }

    if (-not $ImageTag) {
        $ImageTag = (git rev-parse --short=12 HEAD).Trim()
        if ($LASTEXITCODE -ne 0 -or -not $ImageTag) {
            throw "Unable to derive the image tag from Git."
        }
    }

    $Account = Read-GCloudValue @(
        "auth", "list", "--filter=status:ACTIVE", "--format=value(account)", "--limit=1"
    )
    if (-not $Account) {
        throw "No active gcloud account was found. Run gcloud auth login first."
    }

    if ($SmokeOnly) {
        Write-Host "Verifying the existing Cloud Run deployment without changing resources"
        $ApiUrl = Read-GCloudValue @(
            "run", "services", "describe", $ApiService,
            "--project=$ProjectId",
            "--region=$Region",
            "--format=value(status.url)"
        )
        $WebUrl = Read-GCloudValue @(
            "run", "services", "describe", $WebService,
            "--project=$ProjectId",
            "--region=$Region",
            "--format=value(status.url)"
        )
        if ($ApiUrl -notmatch "^https://[^/]+$" -or $WebUrl -notmatch "^https://[^/]+$") {
            throw "Cloud Run did not return valid HTTPS service origins."
        }

        Test-RemoteDeployment -ApiUrl $ApiUrl -WebUrl $WebUrl
        Write-Host "Deployment verified."
        Write-Host "Frontend: $WebUrl"
        Write-Host "API:      $ApiUrl"
        return
    }

    Write-Host "[1/9] Selecting project and enabling required APIs"
    Invoke-GCloud @("config", "set", "project", $ProjectId, "--quiet")
    Invoke-GCloud @(
        "services", "enable",
        "artifactregistry.googleapis.com",
        "cloudbuild.googleapis.com",
        "run.googleapis.com",
        "--project=$ProjectId",
        "--quiet"
    )

    Write-Host "Waiting for enabled APIs to become queryable"
    Wait-GCloudCommand -Label "Artifact Registry API" -Arguments @(
        "artifacts", "repositories", "list",
        "--project=$ProjectId",
        "--location=$Region",
        "--limit=1",
        "--format=value(name)"
    )
    Wait-GCloudCommand -Label "Cloud Build API" -Arguments @(
        "builds", "list",
        "--project=$ProjectId",
        "--region=$Region",
        "--limit=1",
        "--format=value(id)"
    )
    Wait-GCloudCommand -Label "Cloud Run API" -Arguments @(
        "run", "services", "list",
        "--project=$ProjectId",
        "--region=$Region",
        "--limit=1",
        "--format=value(metadata.name)"
    )

    Write-Host "[2/9] Ensuring the Artifact Registry repository exists"
    $RepositoryNames = Read-GCloudValue @(
        "artifacts", "repositories", "list",
        "--project=$ProjectId",
        "--location=$Region",
        "--format=value(name)"
    )
    $RepositoryExists = @(
        $RepositoryNames -split "`r?`n" | Where-Object {
            $Name = $_.Trim()
            $Name -eq $Repository -or $Name.EndsWith("/$Repository")
        }
    ).Count -gt 0
    if (-not $RepositoryExists) {
        Invoke-GCloud @(
            "artifacts", "repositories", "create", $Repository,
            "--project=$ProjectId",
            "--location=$Region",
            "--repository-format=docker",
            "--description=Retail Intelligence Platform container images",
            "--quiet"
        )
    }

    Write-Host "[3/9] Ensuring the least-privilege runtime identity exists"
    $ServiceAccounts = Read-GCloudValue @(
        "iam", "service-accounts", "list",
        "--project=$ProjectId",
        "--filter=email=$RuntimeServiceAccount",
        "--format=value(email)"
    )
    if (-not $ServiceAccounts) {
        Invoke-GCloud @(
            "iam", "service-accounts", "create", $RuntimeServiceAccountName,
            "--project=$ProjectId",
            "--display-name=Retail Intelligence Cloud Run runtime",
            "--description=Runtime identity with no project roles for the read-only platform",
            "--quiet"
        )
    }

    $Registry = "$Region-docker.pkg.dev/$ProjectId/$Repository"
    $ApiImage = "$Registry/retail-intelligence-api:$ImageTag"
    $WebImage = "$Registry/retail-intelligence-web:$ImageTag"

    if ($ReuseExistingApi) {
        Write-Host "[4/9] Reading the existing API service"
        $ApiUrl = Read-GCloudValue @(
            "run", "services", "describe", $ApiService,
            "--project=$ProjectId",
            "--region=$Region",
            "--format=value(status.url)"
        )
        if ($ApiUrl -notmatch "^https://[^/]+$") {
            throw "Cloud Run did not return a valid existing API origin."
        }
    }
    elseif ($ReusePublishedImages) {
        Write-Host "[4/9] Verifying the published API image"
        $ApiDigest = Read-GCloudValue @(
            "artifacts", "docker", "images", "describe", $ApiImage,
            "--project=$ProjectId",
            "--format=value(image_summary.digest)"
        )
        if (-not $ApiDigest) {
            throw "Artifact Registry did not return a digest for $ApiImage."
        }
    }
    else {
        Write-Host "[4/9] Building and publishing the API image with Cloud Build"
        Invoke-GCloud @(
            "builds", "submit", ".",
            "--project=$ProjectId",
            "--region=$Region",
            "--config=deployment/gcp/cloudbuild-backend.yaml",
            "--substitutions=_REGION=$Region,_REPOSITORY=$Repository,_TAG=$ImageTag",
            "--quiet"
        )
    }

    if ($ReuseExistingApi) {
        Write-Host "[5/9] Keeping the existing API revision"
    }
    else {
        $ExistingWebOrigin = Read-GCloudValue @(
            "run", "services", "list",
            "--project=$ProjectId",
            "--region=$Region",
            "--filter=metadata.name=$WebService",
            "--format=value(status.url)"
        )
        $CorsOrigin = if ($ExistingWebOrigin) {
            $ExistingWebOrigin
        }
        else {
            "https://placeholder.invalid"
        }

        Write-Host "[5/9] Deploying the API to Cloud Run"
        Invoke-GCloud @(
            "run", "deploy", $ApiService,
            "--project=$ProjectId",
            "--region=$Region",
            "--image=$ApiImage",
            "--service-account=$RuntimeServiceAccount",
            "--port=8080",
            "--cpu=1",
            "--memory=512Mi",
            "--cpu-throttling",
            "--no-cpu-boost",
            "--concurrency=40",
            "--min=0",
            "--max=1",
            "--timeout=60",
            "--execution-environment=gen2",
            "--set-env-vars=CORS_ALLOWED_ORIGINS=$CorsOrigin",
            "--allow-unauthenticated",
            "--quiet"
        )
        $ApiUrl = Read-GCloudValue @(
            "run", "services", "describe", $ApiService,
            "--project=$ProjectId",
            "--region=$Region",
            "--format=value(status.url)"
        )
        if ($ApiUrl -notmatch "^https://[^/]+$") {
            throw "Cloud Run did not return a valid HTTPS API origin."
        }
    }

    if ($ReusePublishedImages) {
        Write-Host "[6/9] Verifying the published frontend image"
        $WebDigest = Read-GCloudValue @(
            "artifacts", "docker", "images", "describe", $WebImage,
            "--project=$ProjectId",
            "--format=value(image_summary.digest)"
        )
        if (-not $WebDigest) {
            throw "Artifact Registry did not return a digest for $WebImage."
        }
    }
    else {
        Write-Host "[6/9] Building and publishing the frontend image with Cloud Build"
        Invoke-GCloud @(
            "builds", "submit", ".",
            "--project=$ProjectId",
            "--region=$Region",
            "--config=deployment/gcp/cloudbuild-frontend.yaml",
            "--substitutions=_REGION=$Region,_REPOSITORY=$Repository,_TAG=$ImageTag,_API_BASE_URL=$ApiUrl",
            "--quiet"
        )
    }

    Write-Host "[7/9] Deploying the frontend to Cloud Run"
    Invoke-GCloud @(
        "run", "deploy", $WebService,
        "--project=$ProjectId",
        "--region=$Region",
        "--image=$WebImage",
        "--service-account=$RuntimeServiceAccount",
        "--port=8080",
        "--cpu=1",
        "--memory=512Mi",
        "--cpu-throttling",
        "--no-cpu-boost",
        "--concurrency=80",
        "--min=0",
        "--max=1",
        "--timeout=30",
        "--execution-environment=gen2",
        "--allow-unauthenticated",
        "--quiet"
    )
    $WebUrl = Read-GCloudValue @(
        "run", "services", "describe", $WebService,
        "--project=$ProjectId",
        "--region=$Region",
        "--format=value(status.url)"
    )
    if ($WebUrl -notmatch "^https://[^/]+$") {
        throw "Cloud Run did not return a valid HTTPS frontend origin."
    }

    Write-Host "[8/9] Restricting API CORS to the deployed frontend"
    Invoke-GCloud @(
        "run", "services", "update", $ApiService,
        "--project=$ProjectId",
        "--region=$Region",
        "--update-env-vars=CORS_ALLOWED_ORIGINS=$WebUrl",
        "--quiet"
    )

    Write-Host "[9/9] Running remote smoke checks"
    Test-RemoteDeployment -ApiUrl $ApiUrl -WebUrl $WebUrl

    Write-Host "Deployment verified."
    Write-Host "Frontend: $WebUrl"
    Write-Host "API:      $ApiUrl"
    Write-Host "Image tag: $ImageTag"
}
finally {
    Pop-Location
}
