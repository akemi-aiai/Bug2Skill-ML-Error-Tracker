# Bug2Skill: ML Error & Practice Tracker

**Bug2Skill** is a Streamlit-based portfolio project for tracking programming and machine learning mistakes and turning them into deliberate practice tasks.

## Project idea

When learning machine learning, students often repeat the same mistakes: `KeyError` in pandas, data leakage, wrong train/test split, incorrect metrics, K-Means without scaling, PCA misinterpretation, rolling mean leakage, or wrong RMSE calculation.

Bug2Skill helps transform each mistake into a learning card:

```text
Mistake → Cause → Fix → Mini practice task → Review → Mastery
```

## Features

- Add new ML/programming error cards.
- Store errors in a local SQLite database.
- Edit the error library directly in the UI with `st.data_editor`.
- Save table edits back to SQLite.
- Filter by topic, status, ML type, and difficulty.
- Practice Mode for active recall.
- Spaced-review style status updates.
- Dashboard with learning analytics.
- ML checklists for supervised learning, unsupervised learning, time series, and NLP.
- 15 demo records included.

## Demo records include

- KeyError in pandas
- Data Leakage
- Wrong train/test split
- Accuracy with imbalanced classes
- K-Means without scaling
- PCA misinterpretation
- Rolling mean target leakage
- Wrong RMSE calculation
- Target leakage
- NLP vectorizer leakage
- Random Forest overfitting
- Incorrect clustering interpretation
- OneHotEncoder unseen categories
- Notebook execution order error
- Missing baseline in time series

## Tech stack

- Python
- Streamlit
- pandas
- SQLite
- Plotly
- scikit-learn


## How to run

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

4. Open the local Streamlit URL in your browser.

## How to use

### Add Error

Create a new learning card with:

- project
- ML type
- topic
- algorithm/library
- error type
- mistake
- cause
- fix
- mini practice task
- status
- difficulty
- next review date

### Error Library

Use filters and edit records directly in the table. Click **Save changes to database** to persist edits to SQLite.

### Practice Mode

Practice old mistakes as active-recall cards. Try to remember the fix before revealing the solution.

### Dashboard

Track:

- total errors
- cards needing practice
- mastered cards
- mastery rate
- errors by topic
- errors by status
- errors by ML type
- errors over time

## Portfolio description

**Bug2Skill: ML Error & Practice Tracker**  
Developed a Streamlit-based learning analytics application for tracking programming and machine learning errors. Designed a SQLite database to store error cards, including mistake type, cause, fix, practice task, status, and review date. Implemented editable data tables, filtering, dashboard analytics, supervised/unsupervised ML checklists, and active-recall Practice Mode to support deliberate coding practice.
