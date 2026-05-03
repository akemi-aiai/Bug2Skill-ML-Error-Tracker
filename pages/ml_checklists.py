from __future__ import annotations

import streamlit as st

st.title("ML Project Checklists")
st.write("Use these checklists before submitting ML projects or adding new errors to the tracker.")

tab1, tab2, tab3, tab4 = st.tabs([
    "Supervised Learning",
    "Unsupervised Learning",
    "Time Series",
    "NLP",
])

with tab1:
    st.subheader("Supervised Learning Checklist")
    st.checkbox("Checked missing values and duplicates")
    st.checkbox("Separated features X and target y correctly")
    st.checkbox("Used train/test split correctly")
    st.checkbox("Avoided data leakage in preprocessing")
    st.checkbox("Used Pipeline or fitted preprocessing only on train")
    st.checkbox("Selected a metric that matches the task")
    st.checkbox("Compared model with a baseline")
    st.checkbox("Checked overfitting: train score vs validation/test score")
    st.checkbox("Explained the final result in the conclusion")

with tab2:
    st.subheader("Unsupervised Learning Checklist")
    st.checkbox("Scaled features before distance-based algorithms")
    st.checkbox("Checked outliers")
    st.checkbox("Selected number of clusters with elbow/silhouette/domain logic")
    st.checkbox("Compared several clustering configurations")
    st.checkbox("Used PCA for visualization carefully")
    st.checkbox("Checked explained variance ratio for PCA")
    st.checkbox("Did not treat clusters as true labels without validation")
    st.checkbox("Described cluster interpretation as a hypothesis")

with tab3:
    st.subheader("Time Series Checklist")
    st.checkbox("Sorted data by datetime")
    st.checkbox("Resampled data correctly")
    st.checkbox("Created calendar features if relevant")
    st.checkbox("Created lag features using shift()")
    st.checkbox("Created rolling mean without target leakage")
    st.checkbox("Split train/test without shuffling")
    st.checkbox("Used TimeSeriesSplit for cross-validation")
    st.checkbox("Compared with naive baselines")
    st.checkbox("Reported RMSE correctly")

with tab4:
    st.subheader("NLP Checklist")
    st.checkbox("Split data before vectorization")
    st.checkbox("Used Pipeline for vectorizer and model")
    st.checkbox("Checked class imbalance")
    st.checkbox("Selected suitable text preprocessing steps")
    st.checkbox("Evaluated model with precision, recall, F1 or ROC-AUC when needed")
    st.checkbox("Inspected errors manually")
    st.checkbox("Explained examples of false positives and false negatives")
