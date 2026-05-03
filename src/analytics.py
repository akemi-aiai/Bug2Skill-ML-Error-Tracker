from __future__ import annotations

import pandas as pd


def count_by_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if df.empty or column not in df.columns:
        return pd.DataFrame(columns=[column, "count"])

    result = df[column].fillna("Unknown").replace("", "Unknown").value_counts().reset_index()
    result.columns = [column, "count"]
    return result


def mastery_rate(df: pd.DataFrame) -> float:
    if df.empty:
        return 0.0
    return round((df["status"].eq("Mastered").sum() / len(df)) * 100, 1)


def due_practice(df: pd.DataFrame, today: str) -> pd.DataFrame:
    if df.empty:
        return df

    due_statuses = ["New", "Need Practice", "Practiced"]
    data = df.copy()
    data["next_review_date"] = data["next_review_date"].fillna("")

    return data[
        data["status"].isin(due_statuses)
        & (data["next_review_date"].astype(str) <= today)
    ]
