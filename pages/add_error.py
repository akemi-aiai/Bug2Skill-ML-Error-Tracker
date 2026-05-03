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
from src.i18n import option_label, t

st.title(f"{t('add_error_title')}")
st.write(t("add_error_desc"))

with st.expander(t("add_error_theory_title")):
    st.write(t("add_error_theory_text"))
    st.markdown(f"**{t('learning_loop')}:** {t('learning_loop_text')}")

with st.form("add_error_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        error_date = st.date_input(t("date"), value=date.today())
        project = st.text_input(t("project"), placeholder=t("project_placeholder"))
        ml_type = st.selectbox(t("ml_type"), ML_TYPE_OPTIONS, format_func=option_label)

    with col2:
        topic = st.selectbox(t("topic"), TOPIC_OPTIONS)
        algorithm = st.text_input(t("algorithm"), placeholder=t("algorithm_placeholder"))
        error_type = st.text_input(t("error_type"), placeholder=t("error_type_placeholder"))

    with col3:
        status = st.selectbox(t("status"), STATUS_OPTIONS, index=1, format_func=option_label)
        difficulty = st.selectbox(t("difficulty"), DIFFICULTY_OPTIONS, index=1, format_func=option_label)
        next_review_date = st.date_input(
            t("next_review_date"), value=date.today() + timedelta(days=3)
        )

    mistake = st.text_area(t("what_happened"), placeholder=t("what_happened_placeholder"))
    cause = st.text_area(t("why_happened"), placeholder=t("why_happened_placeholder"))
    fix = st.text_area(t("how_fix"), placeholder=t("how_fix_placeholder"))
    practice_task = st.text_area(
        t("mini_practice_task"),
        placeholder=t("mini_practice_placeholder"),
    )

    submitted = st.form_submit_button(t("save_error"))

    if submitted:
        if not project or not mistake:
            st.error(t("project_mistake_required"))
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
            st.success(t("error_saved"))
