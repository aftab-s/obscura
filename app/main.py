import time

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel, Field
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.metrics import REQUEST_COUNT, REQUEST_LATENCY, PREDICTION_COUNT
from app.model import predict

app = FastAPI(
    title="Grade Predictor API",
    version="1.0.0",
    description="Predict your grade. Get roasted. Learn DevOps.",
)


class PredictionRequest(BaseModel):
    study_hours_per_week: float = Field(..., ge=0, le=24, description="Hours spent studying per week")
    attendance_percentage: float = Field(..., ge=0, le=100, description="Class attendance percentage")
    assignments_completed: int = Field(..., ge=0, le=10, description="Number of assignments completed (out of 10)")
    previous_grade: float = Field(..., ge=0, le=100, description="Previous semester grade")


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start

    REQUEST_COUNT.labels(request.method, request.url.path).inc()
    REQUEST_LATENCY.labels(request.method, request.url.path).observe(elapsed)

    return response


@app.get("/", response_class=HTMLResponse)
def root():
    return LANDING_PAGE


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.post("/predict")
def prediction(request: PredictionRequest):
    features = [
        request.study_hours_per_week,
        request.attendance_percentage,
        request.assignments_completed,
        request.previous_grade,
    ]

    grade, letter, tip = predict(features)

    PREDICTION_COUNT.labels(letter).inc()

    return {
        "predicted_grade": grade,
        "grade_letter": letter,
        "tip": tip,
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# ---------------------------------------------------------------------------
# Monochrome landing page
# ---------------------------------------------------------------------------

LANDING_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Grade Predictor</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
<style>
  *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

  :root {
    --bg: #0a0a0a;
    --surface: #141414;
    --surface-hover: #1a1a1a;
    --border: #2a2a2a;
    --border-focus: #555;
    --text: #e8e8e8;
    --text-muted: #888;
    --text-dim: #555;
    --accent: #fff;
    --radius: 12px;
    --font: 'Inter', -apple-system, sans-serif;
    --mono: 'JetBrains Mono', monospace;
  }

  body {
    font-family: var(--font);
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    -webkit-font-smoothing: antialiased;
  }

  .container {
    width: 100%;
    max-width: 480px;
  }

  /* Header */
  .logo {
    font-family: var(--mono);
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 1rem;
  }

  h1 {
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.03em;
    margin-bottom: 0.5rem;
  }

  .tagline {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-bottom: 2.5rem;
    line-height: 1.5;
  }

  /* Form */
  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }

  .field.full { grid-column: 1 / -1; }

  label {
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
  }

  input {
    font-family: var(--mono);
    font-size: 1rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text);
    padding: 0.75rem 1rem;
    transition: border-color 0.2s, box-shadow 0.2s;
    outline: none;
    width: 100%;
  }

  input:focus {
    border-color: var(--border-focus);
    box-shadow: 0 0 0 3px rgba(255,255,255,0.05);
  }

  input::placeholder {
    color: var(--text-dim);
  }

  /* Button */
  .btn {
    font-family: var(--font);
    width: 100%;
    padding: 0.9rem;
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    background: var(--accent);
    color: var(--bg);
    transition: opacity 0.2s, transform 0.1s;
  }

  .btn:hover { opacity: 0.9; }
  .btn:active { transform: scale(0.98); }
  .btn:disabled { opacity: 0.4; cursor: not-allowed; }

  /* Result card */
  .result {
    margin-top: 2rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    opacity: 0;
    transform: translateY(8px);
    transition: opacity 0.4s ease, transform 0.4s ease;
  }

  .result.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem;
    border-bottom: 1px solid var(--border);
  }

  .grade-big {
    font-family: var(--mono);
    font-size: 3rem;
    font-weight: 700;
    line-height: 1;
  }

  .grade-num {
    font-family: var(--mono);
    font-size: 1.5rem;
    color: var(--text-muted);
  }

  .result-tip {
    padding: 1.25rem 1.5rem;
    font-size: 0.9rem;
    color: var(--text-muted);
    line-height: 1.5;
    font-style: italic;
  }

  /* Footer */
  .footer {
    margin-top: 3rem;
    display: flex;
    gap: 1.5rem;
    font-size: 0.75rem;
  }

  .footer a {
    color: var(--text-dim);
    text-decoration: none;
    transition: color 0.2s;
  }

  .footer a:hover { color: var(--text); }

  /* Error */
  .error {
    margin-top: 1rem;
    padding: 0.75rem 1rem;
    font-size: 0.8rem;
    color: #ff6b6b;
    background: rgba(255,107,107,0.08);
    border: 1px solid rgba(255,107,107,0.15);
    border-radius: 8px;
    display: none;
  }

  .error.visible { display: block; }

  /* Responsive */
  @media (max-width: 500px) {
    .form-grid { grid-template-columns: 1fr; }
    h1 { font-size: 2rem; }
  }
</style>
</head>
<body>
<div class="container">

  <div class="logo">DevOps Workshop</div>
  <h1>Grade Predictor</h1>
  <p class="tagline">Enter your study habits. Get your predicted grade.<br />Get roasted. Learn DevOps.</p>

  <form id="predict-form">
    <div class="form-grid">
      <div class="field">
        <label for="study_hours">Study hrs / week</label>
        <input type="number" id="study_hours" name="study_hours_per_week"
               placeholder="5" min="0" max="24" step="0.5" required />
      </div>
      <div class="field">
        <label for="attendance">Attendance %</label>
        <input type="number" id="attendance" name="attendance_percentage"
               placeholder="85" min="0" max="100" step="1" required />
      </div>
      <div class="field">
        <label for="assignments">Assignments (/ 10)</label>
        <input type="number" id="assignments" name="assignments_completed"
               placeholder="8" min="0" max="10" step="1" required />
      </div>
      <div class="field">
        <label for="prev_grade">Previous grade</label>
        <input type="number" id="prev_grade" name="previous_grade"
               placeholder="72" min="0" max="100" step="1" required />
      </div>
    </div>
    <button class="btn" type="submit">Predict my grade</button>
  </form>

  <div id="error" class="error"></div>

  <div id="result" class="result">
    <div class="result-header">
      <span id="grade-letter" class="grade-big"></span>
      <span id="grade-num" class="grade-num"></span>
    </div>
    <div id="tip" class="result-tip"></div>
  </div>

  <div class="footer">
    <a href="/docs">API Docs</a>
    <a href="/health">Health</a>
    <a href="/metrics">Metrics</a>
  </div>

</div>

<script>
const form = document.getElementById('predict-form');
const resultCard = document.getElementById('result');
const errorBox = document.getElementById('error');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  errorBox.classList.remove('visible');
  resultCard.classList.remove('visible');

  const btn = form.querySelector('.btn');
  btn.disabled = true;
  btn.textContent = 'Predicting...';

  const payload = {
    study_hours_per_week: parseFloat(form.study_hours_per_week.value),
    attendance_percentage: parseFloat(form.attendance_percentage.value),
    assignments_completed: parseInt(form.assignments_completed.value, 10),
    previous_grade: parseFloat(form.previous_grade.value),
  };

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const detail = await res.json();
      throw new Error(detail.detail?.[0]?.msg || `Error ${res.status}`);
    }

    const data = await res.json();

    document.getElementById('grade-letter').textContent = data.grade_letter;
    document.getElementById('grade-num').textContent = data.predicted_grade + ' / 100';
    document.getElementById('tip').textContent = '\"' + data.tip + '\"';

    resultCard.classList.add('visible');
  } catch (err) {
    errorBox.textContent = err.message;
    errorBox.classList.add('visible');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Predict my grade';
  }
});
</script>
</body>
</html>
"""
