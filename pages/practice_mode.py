from __future__ import annotations

from datetime import date

import streamlit as st

from src.analytics import due_practice
from src.database import load_errors, update_error_status
from src.practice import next_review_for_status

st.title("Practice Mode")
st.write(
    "Practice Mode shows old mistakes as active-recall cards. First try to remember the fix, "
    "then reveal the cause and solution."
)

full_df = load_errors()

today = str(date.today())
practice_df = due_practice(full_df, today)

if full_df.empty:
    st.info("No errors yet. Add your first error.")
    st.stop()

if practice_df.empty:
    st.success("No cards are due today. You can still practice any non-mastered error below.")
    practice_df = full_df[full_df["status"].isin(["New", "Need Practice", "Practiced"])]

if practice_df.empty:
    st.success("Everything is mastered. Add new errors when you find them.")
    st.stop()

st.sidebar.subheader("Practice filters")
selected_topic = st.sidebar.selectbox(
    "Topic", ["All"] + sorted(practice_df["topic"].dropna().unique().tolist())
)
selected_status = st.sidebar.selectbox(
    "Status", ["All"] + sorted(practice_df["status"].dropna().unique().tolist())
)

filtered = practice_df.copy()
if selected_topic != "All":
    filtered = filtered[filtered["topic"] == selected_topic]
if selected_status != "All":
    filtered = filtered[filtered["status"] == selected_status]

if filtered.empty:
    st.warning("No cards match the selected filters.")
    st.stop()

card_options = {
    f"#{int(row.id)} | {row.topic} | {row.error_type} | {row.project}": int(row.id)
    for row in filtered.itertuples(index=False)
}

selected_card = st.selectbox("Choose a card", list(card_options.keys()))
card_id = card_options[selected_card]
card = filtered[filtered["id"] == card_id].iloc[0]

st.subheader("Problem")
st.markdown(f"**Project:** {card['project']}")
st.markdown(f"**Topic:** {card['ml_type']} → {card['topic']} → {card['algorithm']}")
st.markdown(f"**Mistake:** {card['mistake']}")

user_answer = st.text_area("How would you fix it? Write your answer before revealing the solution.")

if st.button("Show solution"):
    st.subheader("Cause")
    st.write(card["cause"])

    st.subheader("Correct fix")
    st.write(card["fix"])

    st.subheader("Mini practice task")
    st.write(card["practice_task"])

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("I still need practice"):
        new_status = "Need Practice"
        update_error_status(card_id, new_status, next_review_for_status(new_status))
        st.success("Card updated: Need Practice.")
        st.rerun()

with col2:
    if st.button("I practiced it"):
        new_status = "Practiced"
        update_error_status(card_id, new_status, next_review_for_status(new_status))
        st.success("Card updated: Practiced.")
        st.rerun()

with col3:
    if st.button("I mastered it"):
        new_status = "Mastered"
        update_error_status(card_id, new_status, next_review_for_status(new_status))
        st.success("Card updated: Mastered.")
        st.rerun()
