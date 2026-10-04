from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Grade Predictor" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_prediction():
    response = client.post(
        "/predict",
        json={
            "study_hours_per_week": 5,
            "attendance_percentage": 85,
            "assignments_completed": 8,
            "previous_grade": 72,
        },
    )
    assert response.status_code == 200

    body = response.json()
    assert "predicted_grade" in body
    assert "grade_letter" in body
    assert "tip" in body


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "grade_api_requests_total" in response.text
