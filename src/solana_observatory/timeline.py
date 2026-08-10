"""Load and validate the observatory's sourced historical context."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "order",
    "period",
    "title",
    "fact",
    "interpretation",
    "source_label",
    "source_url",
    "source_type",
}


def validate_timeline(records: Any) -> list[dict[str, Any]]:
    """Return validated seven-era context or raise ValueError."""

    if not isinstance(records, list) or len(records) != 7:
        raise ValueError("Timeline must contain seven ordered eras")
    if [record.get("order") for record in records] != list(range(1, 8)):
        raise ValueError("Timeline eras must be ordered from 1 through 7")
    for record in records:
        if not isinstance(record, dict) or not REQUIRED_FIELDS.issubset(record):
            raise ValueError("Every ordered timeline era must be complete")
        if not all(
            isinstance(record[field], str) and record[field].strip()
            for field in REQUIRED_FIELDS - {"order"}
        ):
            raise ValueError("Every ordered timeline era must contain text")
        if not record["source_url"].startswith("https://"):
            raise ValueError("Timeline sources must use HTTPS")
        if record["source_type"] not in {"primary", "authoritative"}:
            raise ValueError("Timeline source type must be primary or authoritative")
    return records


def load_timeline(path: Path) -> list[dict[str, Any]]:
    """Return seven ordered, source-backed eras from a JSON file."""

    return validate_timeline(json.loads(path.read_text(encoding="utf-8")))
