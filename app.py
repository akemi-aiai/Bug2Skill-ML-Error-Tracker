from __future__ import annotations

import streamlit as st

from src.database import init_db, reset_demo_data
from src.i18n import LANGUAGE_OPTIONS, set_language, t

st.set_page_config(
    page_title="Bug2Skill",
    layout="wide",
)

init_db(seed_demo=True)

if "language" not in st.session_state:
    st.session_state.language = "en"

selected_language = st.sidebar.radio(
    "Language / Язык",
    options=list(LANGUAGE_OPTIONS.keys()),
    format_func=lambda language_code: LANGUAGE_OPTIONS[language_code],
    horizontal=True,
    key="language_radio",
)
set_language(selected_language)

st.sidebar.title("Bug2Skill")
st.sidebar.caption(t("sidebar_subtitle"))
st.sidebar.markdown(f"**{t('learning_loop')}:**  \n{t('learning_loop_text')}")

with st.sidebar.expander(t("why_tracker_title")):
    st.write(t("why_tracker_text"))

if st.sidebar.button(t("reset_demo")):
    reset_demo_data()
    st.sidebar.success(t("demo_reset_success"))
    st.rerun()

pages = [
    st.Page("pages/add_error.py", title=t("add_error_page")),
    st.Page("pages/error_library.py", title=t("error_library_page")),
    st.Page("pages/practice_mode.py", title=t("practice_mode_page")),
    st.Page("pages/dashboard.py", title=t("dashboard_page")),
    st.Page("pages/ml_checklists.py", title=t("ml_checklists_page")),
]

navigation = st.navigation(pages)
navigation.run()
