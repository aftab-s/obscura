#!/usr/bin/env bash
set -u

PASS=0
FAIL=0

ok() {
  echo "[OK]   $1"
  PASS=$((PASS + 1))
}

fail() {
  echo "[FAIL] $1"
  FAIL=$((FAIL + 1))
}

echo "=========================================="
echo " DevOps ML Workshop - Preflight Check"
echo "=========================================="
echo

if command -v git >/dev/null 2>&1; then
  ok "Git: $(git --version)"
else
  fail "Git is not installed"
fi

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  PYTHON=""
fi

if [ -n "$PYTHON" ]; then
  VERSION=$($PYTHON -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')
  MAJOR=$($PYTHON -c 'import sys; print(sys.version_info.major)')
  MINOR=$($PYTHON -c 'import sys; print(sys.version_info.minor)')
  if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 11 ]; then
    ok "Python: $VERSION"
  else
    fail "Python 3.11+ required (found $VERSION)"
  fi
else
  fail "Python is not installed"
fi

if command -v docker >/dev/null 2>&1; then
  ok "Docker CLI: $(docker --version)"
  if docker info >/dev/null 2>&1; then
    ok "Docker daemon is reachable"
  else
    fail "Docker daemon is not reachable. Start Docker Desktop."
  fi
  if docker compose version >/dev/null 2>&1; then
    ok "Docker Compose: $(docker compose version --short)"
  else
    fail "Docker Compose is not available"
  fi
else
  fail "Docker is not installed"
fi

for path in app/main.py app/model.py model/grade_model.joblib requirements.txt Dockerfile docker-compose.yml .github/workflows/ci.yml; do
  if [ -f "$path" ]; then
    ok "Project file: $path"
  else
    fail "Missing project file: $path"
  fi
done

if [ -n "$PYTHON" ]; then
  if $PYTHON -c "import fastapi, sklearn, joblib, prometheus_client, pytest" >/dev/null 2>&1; then
    ok "Python dependencies are available"
  else
    echo "[INFO] Python dependencies are not installed in the current environment."
    echo "       This is expected for a fresh clone."
    echo "       Run: pip install -r requirements.txt"
  fi
fi

echo
echo "=========================================="
echo " Result: $PASS passed, $FAIL failed"
echo "=========================================="

if [ "$FAIL" -eq 0 ]; then
  echo "You are ready for the workshop!"
  exit 0
else
  echo "Please fix the failed checks before the workshop."
  exit 1
fi
