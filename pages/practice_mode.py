from __future__ import annotations

from datetime import date

import streamlit as st

from src.analytics import due_practice
from src.database import load_errors, update_error_status
from src.i18n import option_label, t
from src.practice import next_review_for_status

st.title(f"{t('practice_title')}")
st.write(t("practice_desc"))

with st.expander(t("practice_theory_title")):
    st.write(t("practice_theory_text"))
    st.markdown(f"**{t('learning_loop')}:** {t('learning_loop_text')}")

full_df = load_errors()

today = str(date.today())
practice_df = due_practice(full_df, today)

if full_df.empty:
    st.info(t("no_errors_yet"))
    st.stop()

if practice_df.empty:
    st.success(t("no_due_cards"))
    practice_df = full_df[full_df["status"].isin(["New", "Need Practice", "Practiced"])]

if practice_df.empty:
    st.success(t("all_mastered"))
    st.stop()

st.sidebar.subheader(t("practice_filters"))
selected_topic = st.sidebar.selectbox(
    t("topic"), ["All"] + sorted(practice_df["topic"].dropna().unique().tolist()), format_func=option_label
)
selected_status = st.sidebar.selectbox(
    t("status"), ["All"] + sorted(practice_df["status"].dropna().unique().tolist()), format_func=option_label
)

filtered = practice_df.copy()
if selected_topic != "All":
    filtered = filtered[filtered["topic"] == selected_topic]
if selected_status != "All":
    filtered = filtered[filtered["status"] == selected_status]

if filtered.empty:
    st.warning(t("no_cards_match"))
    st.stop()

card_options = {
    f"#{int(row.id)} | {row.topic} | {row.error_type} | {row.project}": int(row.id)
    for row in filtered.itertuples(index=False)
}

selected_card = st.selectbox(t("choose_card"), list(card_options.keys()))
card_id = card_options[selected_card]
card = filtered[filtered["id"] == card_id].iloc[0]

st.subheader(t("problem"))
st.markdown(f"**{t('project')}:** {card['project']}")
st.markdown(f"**{t('topic')}:** {card['ml_type']} → {card['topic']} → {card['algorithm']}")
st.markdown(f"**{t('mistake')}:** {card['mistake']}")

user_answer = st.text_area(t("how_would_fix"))

if st.button(t("show_solution")):
    st.subheader(t("cause"))
    st.write(card["cause"])

    st.subheader(t("correct_fix"))
    st.write(card["fix"])

    st.subheader(t("mini_practice_task"))
    st.write(card["practice_task"])

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button(t("need_practice_btn")):
        new_status = "Need Practice"
        update_error_status(card_id, new_status, next_review_for_status(new_status))
        st.success(t("card_updated_need"))
        st.rerun()

with col2:
    if st.button(t("practiced_btn")):
        new_status = "Practiced"
        update_error_status(card_id, new_status, next_review_for_status(new_status))
        st.success(t("card_updated_practiced"))
        st.rerun()

with col3:
    if st.button(t("mastered_btn")):
        new_status = "Mastered"
        update_error_status(card_id, new_status, next_review_for_status(new_status))
        st.success(t("card_updated_mastered"))
        st.rerun()
