from __future__ import annotations

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

st.title("Error Library")
st.write(
    "Filter your mistakes, edit records directly in the table, and save changes back to SQLite."
)

full_df = load_errors()

if full_df.empty:
    st.info("No errors yet. Add your first error on the Add Error page.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)

with col1:
    topic_filter = st.selectbox("Topic", ["All"] + sorted(full_df["topic"].dropna().unique().tolist()))

with col2:
    status_filter = st.selectbox("Status", ["All"] + sorted(full_df["status"].dropna().unique().tolist()))

with col3:
    ml_type_filter = st.selectbox("ML type", ["All"] + sorted(full_df["ml_type"].dropna().unique().tolist()))

with col4:
    difficulty_filter = st.selectbox("Difficulty", ["All"] + sorted(full_df["difficulty"].dropna().unique().tolist()))

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

st.caption(
    "Tip: You can edit existing rows, add new rows, or delete visible rows. "
    "Click Save changes to database when you finish."
)

edited_df = st.data_editor(
    editor_df,
    num_rows="dynamic",
    hide_index=True,
    use_container_width=True,
    disabled=["id"],
    column_config={
        "id": st.column_config.NumberColumn("ID", disabled=True),
        "date": st.column_config.DateColumn("Date"),
        "next_review_date": st.column_config.DateColumn("Next review"),
        "ml_type": st.column_config.SelectboxColumn("ML type", options=ML_TYPE_OPTIONS),
        "topic": st.column_config.SelectboxColumn("Topic", options=TOPIC_OPTIONS),
        "status": st.column_config.SelectboxColumn("Status", options=STATUS_OPTIONS),
        "difficulty": st.column_config.SelectboxColumn("Difficulty", options=DIFFICULTY_OPTIONS),
        "mistake": st.column_config.TextColumn("Mistake", width="large"),
        "cause": st.column_config.TextColumn("Cause", width="large"),
        "fix": st.column_config.TextColumn("Fix", width="large"),
        "practice_task": st.column_config.TextColumn("Practice task", width="large"),
    },
    key="error_library_editor",
)

col_save, col_info = st.columns([1, 3])

with col_save:
    if st.button("Save changes to database", type="primary"):
        result = save_editor_changes(edited_df, editor_df)
        st.success(
            f"Saved: {result['updated']} updated, {result['inserted']} inserted, {result['deleted']} deleted."
        )
        st.rerun()

with col_info:
    st.info(
        "Only rows currently visible under your filters are affected by delete operations. "
        "Rows hidden by filters remain unchanged."
    )
