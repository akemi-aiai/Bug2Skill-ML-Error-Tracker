from __future__ import annotations

from datetime import date

import plotly.express as px
import streamlit as st

from src.analytics import count_by_column, due_practice, mastery_rate
from src.database import load_errors
from src.i18n import t

st.title(f"{t('dashboard_title')}")
st.write(t("dashboard_desc"))

with st.expander(t("dashboard_theory_title")):
    st.write(t("dashboard_theory_text"))


df = load_errors()

if df.empty:
    st.info(t("no_data_yet"))
    st.stop()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(t("total_errors"), len(df))
col2.metric(t("need_practice"), int(df["status"].eq("Need Practice").sum()))
col3.metric(t("practiced"), int(df["status"].eq("Practiced").sum()))
col4.metric(t("mastered"), int(df["status"].eq("Mastered").sum()))
col5.metric(t("mastery_rate"), f"{mastery_rate(df)}%")

st.subheader(t("cards_due_today"))
due_df = due_practice(df, str(date.today()))
st.write(t("cards_due_count").format(count=len(due_df)))

st.divider()

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader(t("errors_by_topic"))
    topic_counts = count_by_column(df, "topic")
    fig = px.bar(topic_counts, x="topic", y="count", text="count")
    st.plotly_chart(fig, width="stretch")

with chart_col2:
    st.subheader(t("errors_by_status"))
    status_counts = count_by_column(df, "status")
    fig = px.pie(status_counts, names="status", values="count")
    st.plotly_chart(fig, width="stretch")

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.subheader(t("errors_by_ml_type"))
    ml_counts = count_by_column(df, "ml_type")
    fig = px.bar(ml_counts, x="ml_type", y="count", text="count")
    st.plotly_chart(fig, width="stretch")

with chart_col4:
    st.subheader(t("difficulty_distribution"))
    difficulty_counts = count_by_column(df, "difficulty")
    fig = px.pie(difficulty_counts, names="difficulty", values="count")
    st.plotly_chart(fig, width="stretch")

st.subheader(t("errors_over_time"))
date_counts = count_by_column(df, "date").sort_values("date")
fig = px.line(date_counts, x="date", y="count", markers=True)
st.plotly_chart(fig, width="stretch")

st.subheader(t("top_repeated_types"))
error_type_counts = count_by_column(df, "error_type").head(10)
st.dataframe(error_type_counts, width="stretch", hide_index=True)
