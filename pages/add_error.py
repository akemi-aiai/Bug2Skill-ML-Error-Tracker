from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

from src.database import (
    DIFFICULTY_OPTIONS,
    ML_TYPE_OPTIONS,
    STATUS_OPTIONS,
    TOPIC_OPTIONS,
    add_error,
)

st.title("Add New ML Error")
st.write(
    "Save a mistake as a learning card: what happened, why it happened, "
    "how to fix it, and what mini-task will help you practice it."
)

with st.form("add_error_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        error_date = st.date_input("Date", value=date.today())
        project = st.text_input("Project", placeholder="Taxi Demand Forecasting")
        ml_type = st.selectbox("ML type", ML_TYPE_OPTIONS)

    with col2:
        topic = st.selectbox("Topic", TOPIC_OPTIONS)
        algorithm = st.text_input("Algorithm / Library", placeholder="K-Means, Ridge, pandas, sklearn")
        error_type = st.text_input("Error type", placeholder="KeyError, Data Leakage, Wrong Metric")

    with col3:
        status = st.selectbox("Status", STATUS_OPTIONS, index=1)
        difficulty = st.selectbox("Difficulty", DIFFICULTY_OPTIONS, index=1)
        next_review_date = st.date_input("Next review date", value=date.today() + timedelta(days=3))

    mistake = st.text_area("What happened?", placeholder="Describe the error or weak point.")
    cause = st.text_area("Why did it happen?", placeholder="Explain the reason behind the mistake.")
    fix = st.text_area("How to fix it?", placeholder="Write the correct approach or code idea.")
    practice_task = st.text_area(
        "Mini practice task",
        placeholder="Create a small exercise that trains this exact skill.",
    )

    submitted = st.form_submit_button("Save error")

    if submitted:
        if not project or not mistake:
            st.error("Please fill at least Project and What happened.")
        else:
            add_error(
                {
                    "date": str(error_date),
                    "project": project,
                    "ml_type": ml_type,
                    "topic": topic,
                    "algorithm": algorithm,
                    "error_type": error_type,
                    "mistake": mistake,
                    "cause": cause,
                    "fix": fix,
                    "practice_task": practice_task,
                    "status": status,
                    "difficulty": difficulty,
                    "next_review_date": str(next_review_date),
                }
            )
            st.success("Error saved successfully.")
