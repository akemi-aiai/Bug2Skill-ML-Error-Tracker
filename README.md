![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Interactive%20App-ff4b4b)
![ML](https://img.shields.io/badge/ML-Error%20Tracking-purple)
![Practice](https://img.shields.io/badge/Practice-Active%20Recall-orange)
![SQLite](https://img.shields.io/badge/Storage-SQLite-lightgrey)
![Plotly](https://img.shields.io/badge/Charts-Plotly-green)
![Bilingual](https://img.shields.io/badge/Bilingual-English%20%7C%20Russian-7c5cff)


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
