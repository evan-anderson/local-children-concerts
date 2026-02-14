"""Service layer for loading and filtering concert data."""

import json
from functools import lru_cache
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent.parent / "data" / "concerts.json"


@lru_cache(maxsize=1)
def load_concerts() -> list[dict]:
    """Load concerts from JSON file. Cached in memory."""
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH) as f:
        return json.load(f)


def get_filtered_concerts(
    towns: list[str] | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> list[dict]:
    """Filter concerts by town and date range."""
    concerts = load_concerts()

    if towns:
        towns_lower = [t.lower() for t in towns]
        concerts = [c for c in concerts if c["town"].lower() in towns_lower]

    if start_date:
        concerts = [c for c in concerts if c["date"] >= start_date]

    if end_date:
        concerts = [c for c in concerts if c["date"] <= end_date]

    # Sort by date ascending
    concerts.sort(key=lambda c: c["date"])

    return concerts


def get_available_towns() -> list[str]:
    """Get unique towns from all concerts, sorted alphabetically."""
    concerts = load_concerts()
    return sorted(set(c["town"] for c in concerts))
