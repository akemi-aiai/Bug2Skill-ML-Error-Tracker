from __future__ import annotations

from datetime import date, timedelta


REVIEW_INTERVALS = {
    "New": 1,
    "Need Practice": 3,
    "Practiced": 7,
    "Mastered": 14,
}


def next_review_for_status(status: str) -> str:
    days = REVIEW_INTERVALS.get(status, 3)
    return str(date.today() + timedelta(days=days))
