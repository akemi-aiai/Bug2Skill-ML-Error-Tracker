# Bug2Skill: ML Error & Practice Tracker

Bug2Skill is a bilingual Streamlit app for tracking programming and machine learning mistakes and turning them into deliberate practice tasks.

## What problem does it solve?

When learning ML, students often repeat the same mistakes: data leakage, wrong train/test split, weak metric choice, incorrect preprocessing, K-Means without scaling, PCA misinterpretation, rolling mean leakage, and incorrect RMSE calculation.

## Features

- Add and categorize ML/programming errors
- Track supervised learning, unsupervised learning, time series, NLP, and general Python mistakes
- Edit records directly in the UI with `st.data_editor`
- Save edits back to SQLite
- Practice Mode with active recall cards
- Dashboard with learning analytics
- ML project checklists
- English/Russian language switcher
- 15 demo records included

## Tech Stack

- Python
- Streamlit
- pandas
- SQLite
- Plotly

## How to run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
