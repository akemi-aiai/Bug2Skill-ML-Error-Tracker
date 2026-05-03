from __future__ import annotations

import streamlit as st

from src.database import init_db, reset_demo_data

st.set_page_config(
    page_title="Bug2Skill",
    layout="wide",
)

init_db(seed_demo=True)

st.sidebar.title("Bug2Skill")
st.sidebar.caption("ML Error & Practice Tracker")

st.sidebar.markdown(
)

if st.sidebar.button("Reset demo data"):
    reset_demo_data()
    st.sidebar.success("Demo data has been reset.")
    st.rerun()

pages = [
    st.Page("pages/add_error.py", title="Add Error"),
    st.Page("pages/error_library.py", title="Error Library"),
    st.Page("pages/practice_mode.py", title="Practice Mode"),
    st.Page("pages/dashboard.py", title="Dashboard"),
    st.Page("pages/ml_checklists.py", title="ML Checklists"),
]

navigation = st.navigation(pages)
navigation.run()
