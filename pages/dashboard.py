from __future__ import annotations

from datetime import date

import plotly.express as px
import streamlit as st

from src.analytics import count_by_column, due_practice, mastery_rate
from src.database import load_errors

st.title("Learning Dashboard")
st.write("Track your ML learning progress and find repeated weak spots.")

df = load_errors()

if df.empty:
    st.info("No data yet.")
    st.stop()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total errors", len(df))
col2.metric("Need practice", int(df["status"].eq("Need Practice").sum()))
col3.metric("Practiced", int(df["status"].eq("Practiced").sum()))
col4.metric("Mastered", int(df["status"].eq("Mastered").sum()))
col5.metric("Mastery rate", f"{mastery_rate(df)}%")

st.subheader("Cards due for practice today")
due_df = due_practice(df, str(date.today()))
st.write(f"You have **{len(due_df)}** card(s) due today.")

st.divider()

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Errors by topic")
    topic_counts = count_by_column(df, "topic")
    fig = px.bar(topic_counts, x="topic", y="count", text="count")
    st.plotly_chart(fig, use_container_width=True)

with chart_col2:
    st.subheader("Errors by status")
    status_counts = count_by_column(df, "status")
    fig = px.pie(status_counts, names="status", values="count")
    st.plotly_chart(fig, use_container_width=True)

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.subheader("Errors by ML type")
    ml_counts = count_by_column(df, "ml_type")
    fig = px.bar(ml_counts, x="ml_type", y="count", text="count")
    st.plotly_chart(fig, use_container_width=True)

with chart_col4:
    st.subheader("Difficulty distribution")
    difficulty_counts = count_by_column(df, "difficulty")
    fig = px.pie(difficulty_counts, names="difficulty", values="count")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Errors over time")
date_counts = count_by_column(df, "date").sort_values("date")
fig = px.line(date_counts, x="date", y="count", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Top repeated error types")
error_type_counts = count_by_column(df, "error_type").head(10)
st.dataframe(error_type_counts, use_container_width=True, hide_index=True)
