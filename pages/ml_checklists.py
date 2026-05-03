from __future__ import annotations

import streamlit as st

from src.i18n import t

st.title(f"{t('checklists_title')}")
st.write(t("checklists_desc"))

with st.expander(t("checklists_theory_title")):
    st.write(t("checklists_theory_text"))

tab1, tab2, tab3, tab4 = st.tabs([
    t("supervised_tab"),
    t("unsupervised_tab"),
    t("time_series_tab"),
    t("nlp_tab"),
])

with tab1:
    st.subheader(t("supervised_tab"))
    st.checkbox("Checked missing values and duplicates / Проверены пропуски и дубликаты")
    st.checkbox("Separated features X and target y correctly / X и y разделены правильно")
    st.checkbox("Used train/test split correctly / Train/test split сделан корректно")
    st.checkbox("Avoided data leakage in preprocessing / Нет утечки данных в предобработке")
    st.checkbox("Used Pipeline or fitted preprocessing only on train / Pipeline или fit только на train")
    st.checkbox("Selected a metric that matches the task / Метрика соответствует задаче")
    st.checkbox("Compared model with a baseline / Модель сравнена с baseline")
    st.checkbox("Checked overfitting: train score vs validation/test score / Проверено переобучение")
    st.checkbox("Explained the final result in the conclusion / Результат объяснён в выводе")

with tab2:
    st.subheader(t("unsupervised_tab"))
    st.checkbox("Scaled features before distance-based algorithms / Признаки масштабированы")
    st.checkbox("Checked outliers / Проверены выбросы")
    st.checkbox("Selected number of clusters with elbow/silhouette/domain logic / Число кластеров обосновано")
    st.checkbox("Compared several clustering configurations / Сравнены разные настройки кластеризации")
    st.checkbox("Used PCA for visualization carefully / PCA использован осторожно")
    st.checkbox("Checked explained variance ratio for PCA / Проверена объяснённая дисперсия PCA")
    st.checkbox("Did not treat clusters as true labels without validation / Кластеры не приняты за истинные классы")
    st.checkbox("Described cluster interpretation as a hypothesis / Интерпретация кластеров описана как гипотеза")

with tab3:
    st.subheader(t("time_series_tab"))
    st.checkbox("Sorted data by datetime / Данные отсортированы по времени")
    st.checkbox("Resampled data correctly / Ресемплирование выполнено корректно")
    st.checkbox("Created calendar features if relevant / Созданы календарные признаки")
    st.checkbox("Created lag features using shift() / Лаги созданы через shift()")
    st.checkbox("Created rolling mean without target leakage / Скользящее среднее без утечки")
    st.checkbox("Split train/test without shuffling / Разбиение без перемешивания")
    st.checkbox("Used TimeSeriesSplit for cross-validation / Использован TimeSeriesSplit")
    st.checkbox("Compared with naive baselines / Есть сравнение с baseline")
    st.checkbox("Reported RMSE correctly / RMSE рассчитан корректно")

with tab4:
    st.subheader(t("nlp_tab"))
    st.checkbox("Split data before vectorization / Разбиение сделано до векторизации")
    st.checkbox("Used Pipeline for vectorizer + model / Использован Pipeline для векторизатора и модели")
    st.checkbox("Checked class imbalance / Проверен дисбаланс классов")
    st.checkbox("Selected suitable text preprocessing steps / Выбраны подходящие шаги предобработки текста")
    st.checkbox("Evaluated model with precision, recall, F1 or ROC-AUC when needed / Использованы подходящие метрики")
    st.checkbox("Inspected errors manually / Ошибки модели разобраны вручную")
    st.checkbox("Explained examples of false positives and false negatives / Объяснены FP и FN")
