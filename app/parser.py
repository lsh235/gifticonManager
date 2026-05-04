import re
from datetime import datetime
from typing import List

from dateutil.parser import parse as dateutil_parse

_DATE_PATTERNS = [
    r"(20\d{2})\s*[./-]\s*(1[0-2]|0?[1-9])\s*[./-]\s*(3[01]|[12]\d|0?[1-9])",
    r"(\d{2})\s*[./-]\s*(1[0-2]|0?[1-9])\s*[./-]\s*(3[01]|[12]\d|0?[1-9])",
    r"(20\d{2})\s*년\s*(1[0-2]|0?[1-9])\s*월\s*(3[01]|[12]\d|0?[1-9])\s*일",
]


def _safe_date(year: int, month: int, day: int):
    try:
        dt = datetime(year, month, day)
    except ValueError:
        return None

    if dt.year < 2000 or dt.year > 2100:
        return None
    return dt


def parse_dates(text: str) -> List[str]:
    candidates = []

    for pattern in _DATE_PATTERNS:
        for match in re.finditer(pattern, text):
            y, m, d = match.groups()
            year = int(y)
            if len(y) == 2:
                year += 2000
            dt = _safe_date(year, int(m), int(d))
            if dt:
                candidates.append(dt.date().isoformat())

    # fallback fuzzy parsing on lines containing date-ish separators
    for line in text.splitlines():
        if any(sep in line for sep in [".", "-", "/", "년", "월"]):
            try:
                dt = dateutil_parse(line, fuzzy=True, dayfirst=False, yearfirst=True)
                if 2000 <= dt.year <= 2100:
                    candidates.append(dt.date().isoformat())
            except Exception:
                continue

    # deduplicate while keeping order
    unique = []
    seen = set()
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    return unique
