$passed = 0
$failed = 0

function Ok($message) {
    Write-Host "[OK]   $message"
    $script:passed++
}

function Fail($message) {
    Write-Host "[FAIL] $message"
    $script:failed++
}

Write-Host "=========================================="
Write-Host " DevOps ML Workshop - Preflight Check"
Write-Host "=========================================="
Write-Host ""

if (Get-Command git -ErrorAction SilentlyContinue) {
    Ok "Git: $(git --version)"
} else {
    Fail "Git is not installed"
}

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    $version = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
    $minor = python -c "import sys; print(sys.version_info.minor)"
    if ($minor -ge 11) {
        Ok "Python: $version"
    } else {
        Fail "Python 3.11+ required (found $version)"
    }
} else {
    Fail "Python is not installed"
}

if (Get-Command docker -ErrorAction SilentlyContinue) {
    Ok "Docker CLI: $(docker --version)"
    docker info *> $null
    if ($LASTEXITCODE -eq 0) {
        Ok "Docker daemon is reachable"
    } else {
        Fail "Docker daemon is not reachable. Start Docker Desktop."
    }
    docker compose version *> $null
    if ($LASTEXITCODE -eq 0) {
        Ok "Docker Compose is available"
    } else {
        Fail "Docker Compose is not available"
    }
} else {
    Fail "Docker is not installed"
}

$paths = @(
    "app/main.py",
    "app/model.py",
    "model/grade_model.joblib",
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml",
    ".github/workflows/ci.yml"
)

foreach ($path in $paths) {
    if (Test-Path $path) {
        Ok "Project file: $path"
    } else {
        Fail "Missing project file: $path"
    }
}

if ($pythonCmd) {
    python -c "import fastapi, sklearn, joblib, prometheus_client, pytest" *> $null
    if ($LASTEXITCODE -eq 0) {
        Ok "Python dependencies are available"
    } else {
        Write-Host "[INFO] Python dependencies are not installed in the current environment."
        Write-Host "       This is expected for a fresh clone."
        Write-Host "       Run: pip install -r requirements.txt"
    }
}

Write-Host ""
Write-Host "=========================================="
Write-Host " Result: $passed passed, $failed failed"
Write-Host "=========================================="

if ($failed -eq 0) {
    Write-Host "You are ready for the workshop!"
    exit 0
} else {
    Write-Host "Please fix the failed checks before the workshop."
    exit 1
}
