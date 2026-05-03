from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import (
    DIFFICULTY_OPTIONS,
    EDITABLE_COLUMNS,
    ML_TYPE_OPTIONS,
    STATUS_OPTIONS,
    TOPIC_OPTIONS,
    load_errors,
    save_editor_changes,
)
from src.i18n import option_label, t

st.title(f"{t('library_title')}")
st.write(t("library_desc"))

with st.expander(t("library_theory_title")):
    st.write(t("library_theory_text"))
    st.markdown(f"**{t('status_legend_title')}:** {t('status_legend_text')}")

full_df = load_errors()

if full_df.empty:
    st.info(t("no_errors_add"))
    st.stop()

col1, col2, col3, col4 = st.columns(4)

with col1:
    topic_filter = st.selectbox(
        t("topic"), ["All"] + sorted(full_df["topic"].dropna().unique().tolist()), format_func=option_label
    )

with col2:
    status_filter = st.selectbox(
        t("status"), ["All"] + sorted(full_df["status"].dropna().unique().tolist()), format_func=option_label
    )

with col3:
    ml_type_filter = st.selectbox(
        t("ml_type"), ["All"] + sorted(full_df["ml_type"].dropna().unique().tolist()), format_func=option_label
    )

with col4:
    difficulty_filter = st.selectbox(
        t("difficulty"), ["All"] + sorted(full_df["difficulty"].dropna().unique().tolist()), format_func=option_label
    )

filtered_df = full_df.copy()

if topic_filter != "All":
    filtered_df = filtered_df[filtered_df["topic"] == topic_filter]
if status_filter != "All":
    filtered_df = filtered_df[filtered_df["status"] == status_filter]
if ml_type_filter != "All":
    filtered_df = filtered_df[filtered_df["ml_type"] == ml_type_filter]
if difficulty_filter != "All":
    filtered_df = filtered_df[filtered_df["difficulty"] == difficulty_filter]

editor_df = filtered_df[EDITABLE_COLUMNS].copy()

for date_column in ["date", "next_review_date"]:
    editor_df[date_column] = pd.to_datetime(editor_df[date_column], errors="coerce").dt.date

st.caption(t("table_tip"))

edited_df = st.data_editor(
    editor_df,
    num_rows="dynamic",
    hide_index=True,
    width="stretch",
    disabled=["id"],
    column_config={
        "id": st.column_config.NumberColumn(t("id"), disabled=True),
        "date": st.column_config.DateColumn(t("date")),
        "next_review_date": st.column_config.DateColumn(t("next_review")),
        "ml_type": st.column_config.SelectboxColumn(t("ml_type"), options=ML_TYPE_OPTIONS),
        "topic": st.column_config.SelectboxColumn(t("topic"), options=TOPIC_OPTIONS),
        "status": st.column_config.SelectboxColumn(t("status"), options=STATUS_OPTIONS),
        "difficulty": st.column_config.SelectboxColumn(t("difficulty"), options=DIFFICULTY_OPTIONS),
        "project": st.column_config.TextColumn(t("project"), width="medium"),
        "algorithm": st.column_config.TextColumn(t("algorithm"), width="medium"),
        "error_type": st.column_config.TextColumn(t("error_type"), width="medium"),
        "mistake": st.column_config.TextColumn(t("mistake"), width="large"),
        "cause": st.column_config.TextColumn(t("cause"), width="large"),
        "fix": st.column_config.TextColumn(t("fix"), width="large"),
        "practice_task": st.column_config.TextColumn(t("practice_task"), width="large"),
    },
    key="error_library_editor",
)

col_save, col_info = st.columns([1, 3])

with col_save:
    if st.button(t("save_changes"), type="primary"):
        result = save_editor_changes(edited_df, editor_df)
        st.success(t("saved_result").format(**result))
        st.rerun()

with col_info:
    st.info(t("filter_delete_info"))
