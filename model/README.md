# Model

A tiny linear regression trained on synthetic student data.

**Features:**

1. `study_hours_per_week` — hours spent studying per week (0–24)
2. `attendance_percentage` — class attendance as a percentage (0–100)
3. `assignments_completed` — number of assignments completed out of 10
4. `previous_grade` — grade from the previous semester (0–100)

**Target:** predicted final grade (0–100)

The model is intentionally simple. The workshop objective is the software delivery lifecycle, not model quality.

To retrain:

```bash
python scripts/train_model.py
```
