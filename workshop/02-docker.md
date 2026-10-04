# Exercise 2 — Containerize the application

## Goal

Package the application so it runs consistently on another machine.

### Task

Complete the `Dockerfile`.

Hints:

1. Start from a Python image.
2. Set a working directory.
3. Copy `requirements.txt`.
4. Install dependencies.
5. Copy the application.
6. Expose port 8000.
7. Start Uvicorn.

### Build

```bash
docker build -t grade-predictor .
```

### Run

```bash
docker run --rm -p 8000:8000 grade-predictor
```

Open:

http://localhost:8000

You should see the Grade Predictor landing page. Try predicting your own grade!

### Test the API

```bash
curl http://localhost:8000/health
```

For a prediction:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"study_hours_per_week":5,"attendance_percentage":85,"assignments_completed":8,"previous_grade":72}'
```

## Baseline

The baseline image should already build successfully. If your changes break it, restore the baseline from `solution/Dockerfile` and continue.

## Discussion

Ask:

- What problem does a container solve?
- What is inside the image?
- Is a container a virtual machine?
- Why does the same image behave consistently?
