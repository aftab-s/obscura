# From Code to Cloud: Hands-on DevOps Workshop

A 3-hour, project-focused DevOps workshop for 3rd/4th-year students, especially Data Science students.

> **👋 Student?** Start with [`workshop/student-setup.md`](workshop/student-setup.md) — complete the setup **before** you arrive.  
> 🎮 **Live Demo:** [https://beyond-code-beta.onrender.com](https://beyond-code-beta.onrender.com)  
> 📊 **Workshop Slides:** [https://canva.link/bftq3j82oegb38n](https://canva.link/bftq3j82oegb38n)  
> 📝 **Reference Snippets:** [Obscura Reference Snippets gist](https://gist.github.com/aftab-s/11db55af5a3c3535030e3eeff82a610b)

---

## Workshop story

We start with a small ML prediction API and progressively make it easier to test, package, automate, and observe:

**Code → Git → Test → Docker → CI (test + push to Docker Hub) → Observability**

The workshop deliberately avoids Kubernetes and cloud-account setup so that most of the time is spent building.

## What you'll build

A FastAPI service that predicts your grade based on your study habits — and roasts you in the process. Try the live version at [https://beyond-code-beta.onrender.com](https://beyond-code-beta.onrender.com).

Enter your study hours, attendance, assignments completed, and previous grade.
Get a predicted grade, a letter grade, and a brutally honest tip.

Endpoints:

- `GET /` — landing page with an interactive form
- `GET /health` — health check
- `GET /ready` — readiness check
- `POST /predict` — grade prediction
- `GET /metrics` — Prometheus metrics
- `GET /docs` — Swagger UI (auto-generated)

### Example

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"study_hours_per_week":2,"attendance_percentage":40,"assignments_completed":3,"previous_grade":35}'
```

Response:

```json
{
  "predicted_grade": 34.2,
  "grade_letter": "F",
  "tip": "You study less than my phone's screen time. Bold move."
}
```

## Before the workshop

Install the following:

- Git
- Python 3.11+
- Docker Desktop
- VS Code or another editor
- A GitHub account
- A [Docker Hub](https://hub.docker.com/) account (free tier is fine)
- A modern browser

Verify your setup:

```bash
git --version
python --version
docker --version
```

Make sure Docker Desktop is running.

For a full pre-workshop checklist and automated preflight check, see [`workshop/student-setup.md`](workshop/student-setup.md).

## Quick start

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000

Run tests:

```bash
pytest -q
```

## Workshop flow

| Time | Activity |
|---|---|
| 0:00–0:15 | DevOps context + play with the app |
| 0:15–0:40 | Git workflow |
| 0:40–1:25 | Containerize the application |
| 1:25–1:55 | GitHub Actions CI + Docker Hub push |
| 1:55–2:35 | Monitoring with Prometheus + Grafana |
| 2:35–3:00 | Challenge, discussion, production extensions |

## Student exercises

1. Create a Git branch and make a small application change.
2. Write/fix the Dockerfile and build the image.
3. Run the application as a container.
4. Configure Docker Hub secrets and push changes to trigger CI.
5. Verify the Docker image appears on Docker Hub.
6. Start Prometheus and Grafana.
7. Generate traffic and inspect application metrics.
8. Optional challenge: add a new metric or endpoint.
9. Optional: deploy the image to Render for public access — see [`workshop/05-deploy-render.md`](workshop/05-deploy-render.md).

Detailed step-by-step instructions are in `workshop/`.

## Instructor

See `workshop/instructor-guide.md` before the session.

The `solution/` directory contains reference implementations for the intentionally incomplete student exercises.
