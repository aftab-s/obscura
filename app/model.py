from pathlib import Path
import joblib

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "grade_model.joblib"


def load_model():
    return joblib.load(MODEL_PATH)


model = load_model()


def predict(features: list[float]) -> tuple[float, str, str]:
    """Return (predicted_grade, letter, funny_tip)."""
    grade = float(model.predict([features])[0])
    grade = max(0, min(100, round(grade, 1)))

    letter = _to_letter(grade)
    tip = _get_tip(grade, features)

    return grade, letter, tip


def _to_letter(grade: float) -> str:
    if grade >= 90:
        return "A+"
    if grade >= 80:
        return "A"
    if grade >= 70:
        return "B"
    if grade >= 60:
        return "C"
    if grade >= 50:
        return "D"
    return "F"


def _get_tip(grade: float, features: list[float]) -> str:
    study_hours = features[0]
    attendance = features[1]

    # Roast-tier tips
    if grade >= 90:
        return "Suspicious. Are you sure you're not a TA?"
    if grade >= 80 and study_hours >= 10:
        return "You study more than you sleep. Respect... and concern."
    if grade >= 80:
        return "Look at you, overachiever. Your parents must be thrilled."
    if grade >= 70 and attendance < 70:
        return "Passing despite skipping class? Teach us your ways."
    if grade >= 70:
        return "Solid B. The 'I did the bare minimum but strategically' grade."
    if grade >= 60 and study_hours <= 3:
        return "A C with 3 hours of study? That's actually efficient."
    if grade >= 60:
        return "C's get degrees. That's not advice, that's a coping mechanism."
    if grade >= 50:
        return "You're one Netflix binge away from failing. Choose wisely."
    if study_hours <= 2:
        return "You study less than my phone's screen time. Bold move."
    if attendance < 40:
        return "The professor doesn't know your face. That's a problem."
    return "Have you considered switching to a major with less math?"
