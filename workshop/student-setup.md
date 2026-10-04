# Student Setup Guide

Please complete this **before the workshop**. The workshop will focus on building, not installing software.

## Required

Install:

1. Git
2. Python 3.11+
3. Docker Desktop
4. VS Code (or another code editor)
5. A GitHub account
6. A [Docker Hub](https://hub.docker.com/) account (free tier is fine)

### Verify manually

```bash
git --version
python --version
docker --version
```

Docker Desktop must be running.

## One-command preflight check

From the repository root:

### macOS / Linux

```bash
bash scripts/preflight.sh
```

### Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File scripts/preflight.ps1
```

The checker verifies:

- Git is installed
- Python is installed and supported
- Docker CLI is installed
- Docker daemon is reachable
- Required project files exist
- Python dependencies can be imported

If all checks pass, you are ready for the workshop.

## If a check fails

Do not spend workshop time troubleshooting unless necessary.

Send the exact error message to the workshop coordinator before the session.

## Important

You do **not** need:

- Kubernetes
- Minikube
- Terraform
- AWS CLI
- An AWS account
- Jenkins
- WSL
- A local Prometheus installation
- A local Grafana installation

Prometheus and Grafana will run as Docker containers during the workshop.

---

## Reference Snippets

Copy-paste these files as needed during the workshop.

### `.github/workflows/ci.yml`

```yaml
# Workflow name — appears in the GitHub Actions UI
name: CI

# Triggers: run this workflow on every push to any branch and on pull requests
on:
  push:
    branches: ["**"]       # matches every branch name
  pull_request:

jobs:
  # ---------------------------------------------------------------------------
  # Job 1: test — run the test suite
  # ---------------------------------------------------------------------------
  test:
    runs-on: ubuntu-latest  # use the latest Ubuntu runner provided by GitHub

    steps:
      # Clone the repository so the runner has access to the source code
      - name: Checkout
        uses: actions/checkout@v4

      # Install the required Python version on the runner
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"  # must match the version used in the project

      # Install all project dependencies from requirements.txt
      - name: Install dependencies
        run: pip install -r requirements.txt

      # Run the test suite using pytest in quiet mode
      - name: Run tests
        run: pytest -q

  # ---------------------------------------------------------------------------
  # Job 2: docker — build the image and push it to Docker Hub
  # ---------------------------------------------------------------------------
  docker:
    runs-on: ubuntu-latest
    needs: test              # only run after the test job succeeds

    steps:
      # Clone the repository so Docker can access the Dockerfile and source code
      - name: Checkout
        uses: actions/checkout@v4

      # Authenticate with Docker Hub using repository secrets
      # Requires two secrets configured in GitHub → Settings → Secrets:
      #   DOCKERHUB_USERNAME  — your Docker Hub username
      #   DOCKERHUB_TOKEN     — a Docker Hub personal access token
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # Set up Docker Buildx for advanced build features (multi-platform, caching)
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # Build the Docker image and push it to Docker Hub
      # Tags the image with both the Git SHA (unique per commit) and "latest"
      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          context: .                     # build context is the repo root
          push: true                     # push the image after building
          tags: |
            ${{ secrets.DOCKERHUB_USERNAME }}/grade-predictor:${{ github.sha }}
            ${{ secrets.DOCKERHUB_USERNAME }}/grade-predictor:latest
```

### `Dockerfile`

```dockerfile
# Workshop baseline Dockerfile
# The application should build successfully before the workshop.
# Exercise: inspect this file and improve it (image size, caching, security, etc.).

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY model ./model

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `docker-compose.yml`

```yaml
services:
  app:
    build: .
    container_name: grade-predictor
    ports:
      - "8000:8000"

  prometheus:
    image: prom/prometheus:v3.13.3
    container_name: workshop-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    depends_on:
      - app

  grafana:
    image: grafana/grafana:13.2.2
    container_name: workshop-grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin
      GF_AUTH_ANONYMOUS_ENABLED: "false"
    volumes:
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning:ro
      - ./monitoring/grafana/dashboard.json:/var/lib/grafana/dashboards/workshop.json:ro
    depends_on:
      - prometheus
```
