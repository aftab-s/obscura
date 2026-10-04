# Exercise 4 — Observability

## Goal

See what is happening inside the application instead of treating it as a black box.

Start everything:

```bash
docker compose up --build
```

Services:

- Application: http://localhost:8000 (landing page)
- Swagger UI: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Grafana login:

- Username: `admin`
- Password: `admin`

## Generate traffic

Open the landing page and submit several predictions with different study habits.

Try students who:
- Study 15 hours, 99% attendance, 10 assignments, previous grade 95
- Study 1 hour, 30% attendance, 2 assignments, previous grade 28

Then open Prometheus and query:

```text
grade_api_requests_total
```

Try:

```text
rate(grade_api_requests_total[1m])
```

And:

```text
grade_api_predictions_total
```

This shows how many predictions were made **per grade letter**. If the model is predicting mostly F's, that tells us something!

## Grafana

The dashboard is provisioned automatically.

Look at:

- Request rate
- Predictions by grade letter
- Request latency

## Discussion

Ask:

- What would you monitor in a real ML API?
- What happens if latency suddenly increases?
- What if the model starts predicting only F's for everyone?
- What is the difference between logs, metrics, and traces?
