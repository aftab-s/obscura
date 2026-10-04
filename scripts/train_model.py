"""Train a simple grade-prediction model for the workshop.

The model predicts a student's final grade (0–100) from four features.
The dataset is intentionally tiny — the learning objective is the
DevOps lifecycle, not model quality.
"""

from pathlib import Path

import joblib
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Tiny synthetic dataset for workshop purposes.
# Columns:
#   study_hours_per_week, attendance_percentage, assignments_completed, previous_grade

X = [
    [1,  40, 2, 35],
    [2,  50, 3, 42],
    [2,  55, 4, 48],
    [3,  60, 4, 50],
    [4,  65, 5, 55],
    [5,  70, 6, 60],
    [6,  75, 7, 65],
    [7,  80, 7, 68],
    [8,  85, 8, 72],
    [9,  88, 8, 75],
    [10, 90, 9, 80],
    [12, 92, 9, 82],
    [14, 95, 10, 88],
    [15, 98, 10, 92],
    [3,  45, 3, 40],
    [5,  60, 5, 52],
    [7,  78, 7, 70],
    [10, 85, 9, 78],
    [1,  30, 1, 28],
    [15, 99, 10, 95],
]

# Final grades (0–100)
y = [
    30, 40, 44, 50, 55,
    62, 68, 72, 78, 80,
    85, 88, 92, 96,
    38, 56, 70, 82,
    22, 98,
]

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("regressor", LinearRegression()),
])

pipeline.fit(X, y)

output = Path(__file__).resolve().parent.parent / "model" / "grade_model.joblib"
output.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(pipeline, output)

print(f"Saved model to {output}")
