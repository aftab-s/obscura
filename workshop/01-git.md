# Exercise 1 — Git workflow

## Goal

Use Git to make a change without modifying the main branch directly.

### 1. Check the repository

```bash
git status
git log --oneline -5
```

### 2. Create a branch

```bash
git checkout -b workshop/<your-name>
```

Example:

```bash
git checkout -b workshop/aftab
```

### 3. Make a change

Open `app/model.py` and add a new roast tip. For example, find the `_get_tip` function and add a new condition:

```python
if grade >= 70 and study_hours <= 2:
    return "A B with 2 hours of study? Are you cheating or just built different?"
```

Or change the landing page title in `app/main.py`.

### 4. Commit it

```bash
git add .
git commit -m "Add new roast tip"
```

### 5. Push

```bash
git push -u origin workshop/<your-name>
```

If working from your own fork, open a Pull Request.

## Discussion

Ask:

- Why do we use branches?
- Why do we review code before merging?
- What happens if five developers work on the same application?
- Where does automation fit into this?
