from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pandas as pd

from src.demo_data import DEMO_ERRORS

DB_PATH = Path("data/errors.db")

EDITABLE_COLUMNS = [
    "id",
    "date",
    "project",
    "ml_type",
    "topic",
    "algorithm",
    "error_type",
    "mistake",
    "cause",
    "fix",
    "practice_task",
    "status",
    "difficulty",
    "next_review_date",
]

DATA_COLUMNS = [column for column in EDITABLE_COLUMNS if column != "id"]

STATUS_OPTIONS = ["New", "Need Practice", "Practiced", "Mastered"]
DIFFICULTY_OPTIONS = ["Easy", "Medium", "Hard"]
ML_TYPE_OPTIONS = [
    "Supervised Learning",
    "Unsupervised Learning",
    "Time Series",
    "NLP",
    "General Python",
]
TOPIC_OPTIONS = [
    "Data Preprocessing",
    "Feature Engineering",
    "Train/Test Split",
    "Metrics",
    "Classification",
    "Regression",
    "Clustering",
    "Clustering Metrics",
    "PCA",
    "Time Series",
    "NLP",
    "Text Preprocessing",
    "Model Evaluation",
    "Preprocessing",
    "Notebook Workflow",
    "Baseline",
    "Visualization",
    "Other",
]


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db(seed_demo: bool = True) -> None:
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            project TEXT NOT NULL,
            ml_type TEXT NOT NULL,
            topic TEXT NOT NULL,
            algorithm TEXT,
            error_type TEXT,
            mistake TEXT NOT NULL,
            cause TEXT,
            fix TEXT,
            practice_task TEXT,
            status TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            next_review_date TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    conn.commit()

    if seed_demo and count_errors(conn) == 0:
        insert_many(DEMO_ERRORS, conn=conn)

    conn.close()


def count_errors(conn: Optional[sqlite3.Connection] = None) -> int:
    should_close = conn is None
    conn = conn or _connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM errors")
    count = int(cursor.fetchone()[0])
    if should_close:
        conn.close()
    return count


def insert_many(records: Iterable[Dict[str, str]], conn: Optional[sqlite3.Connection] = None) -> None:
    should_close = conn is None
    conn = conn or _connect()
    cursor = conn.cursor()
    now = datetime.now().isoformat(timespec="seconds")

    for record in records:
        cursor.execute(
            f"""
            INSERT INTO errors ({', '.join(DATA_COLUMNS)}, created_at, updated_at)
            VALUES ({', '.join(['?'] * len(DATA_COLUMNS))}, ?, ?)
            """,
            [str(record.get(column, "")) for column in DATA_COLUMNS] + [now, now],
        )

    conn.commit()
    if should_close:
        conn.close()


def reset_demo_data() -> None:
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM errors")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='errors'")
    conn.commit()
    insert_many(DEMO_ERRORS, conn=conn)
    conn.close()


def load_errors() -> pd.DataFrame:
    conn = _connect()
    df = pd.read_sql_query("SELECT * FROM errors ORDER BY id DESC", conn)
    conn.close()

    if df.empty:
        return pd.DataFrame(columns=EDITABLE_COLUMNS + ["created_at", "updated_at"])

    return df


def add_error(error_data: Dict[str, str]) -> None:
    conn = _connect()
    cursor = conn.cursor()
    now = datetime.now().isoformat(timespec="seconds")

    cursor.execute(
        f"""
        INSERT INTO errors ({', '.join(DATA_COLUMNS)}, created_at, updated_at)
        VALUES ({', '.join(['?'] * len(DATA_COLUMNS))}, ?, ?)
        """,
        [str(error_data.get(column, "")) for column in DATA_COLUMNS] + [now, now],
    )

    conn.commit()
    conn.close()


def update_error_status(error_id: int, status: str, next_review_date: Optional[str] = None) -> None:
    conn = _connect()
    cursor = conn.cursor()
    now = datetime.now().isoformat(timespec="seconds")

    if next_review_date is None:
        cursor.execute(
            "UPDATE errors SET status = ?, updated_at = ? WHERE id = ?",
            (status, now, int(error_id)),
        )
    else:
        cursor.execute(
            "UPDATE errors SET status = ?, next_review_date = ?, updated_at = ? WHERE id = ?",
            (status, next_review_date, now, int(error_id)),
        )

    conn.commit()
    conn.close()


def delete_error(error_id: int) -> None:
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM errors WHERE id = ?", (int(error_id),))
    conn.commit()
    conn.close()


def _clean_value(value) -> str:
    if pd.isna(value):
        return ""
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _clean_id(value) -> Optional[int]:
    if pd.isna(value) or value == "":
        return None
    return int(float(value))


def save_editor_changes(edited_df: pd.DataFrame, original_df: pd.DataFrame) -> Dict[str, int]:
    """Save changes from st.data_editor.

    Only rows that were visible in the editor are affected. If the user deletes a visible
    row, it is deleted from the database. Rows outside the current filter remain unchanged.
    New rows without id are inserted.
    """
    conn = _connect()
    cursor = conn.cursor()
    now = datetime.now().isoformat(timespec="seconds")

    edited_df = edited_df.copy()
    original_df = original_df.copy()

    for column in EDITABLE_COLUMNS:
        if column not in edited_df.columns:
            edited_df[column] = ""

    original_ids = set()
    if not original_df.empty and "id" in original_df.columns:
        original_ids = {
            int(float(value))
            for value in original_df["id"].dropna().tolist()
            if str(value) != ""
        }

    edited_ids = set()
    inserted = 0
    updated = 0

    for _, row in edited_df.iterrows():
        row_id = _clean_id(row.get("id"))
        values = [_clean_value(row.get(column, "")) for column in DATA_COLUMNS]

        # Skip completely empty new rows.
        if row_id is None and not any(values):
            continue

        if row_id is None:
            cursor.execute(
                f"""
                INSERT INTO errors ({', '.join(DATA_COLUMNS)}, created_at, updated_at)
                VALUES ({', '.join(['?'] * len(DATA_COLUMNS))}, ?, ?)
                """,
                values + [now, now],
            )
            inserted += 1
        else:
            edited_ids.add(row_id)
            cursor.execute(
                f"""
                UPDATE errors
                SET {', '.join([f'{column} = ?' for column in DATA_COLUMNS])}, updated_at = ?
                WHERE id = ?
                """,
                values + [now, row_id],
            )
            updated += cursor.rowcount

    ids_to_delete = original_ids - edited_ids
    for row_id in ids_to_delete:
        cursor.execute("DELETE FROM errors WHERE id = ?", (row_id,))

    conn.commit()
    conn.close()

    return {"inserted": inserted, "updated": updated, "deleted": len(ids_to_delete)}
