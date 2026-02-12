"""Core data pipeline: deduplicate, filter, persist, and summarize concert data.

This is the single place where data processing decisions live. Scrapers collect;
this module decides what to keep, where to save it, and what to report.
"""

import json
import logging
from collections import Counter
from pathlib import Path
from typing import List

import pandas as pd

from scraper import config
from scraper.base_scraper import Concert

logger = logging.getLogger(__name__)


def deduplicate(concerts: List[Concert]) -> List[Concert]:
    """Remove duplicates keyed on (title, venue, date).

    Keeps the first occurrence. Two scrapers finding the same event
    should not produce two rows in the output.
    """
    seen: set = set()
    unique: List[Concert] = []
    for concert in concerts:
        key = (concert.title.lower().strip(), concert.venue.lower().strip(), concert.date)
        if key not in seen:
            seen.add(key)
            unique.append(concert)

    removed = len(concerts) - len(unique)
    if removed:
        logger.info(f"Deduplicated: removed {removed} duplicates, {len(unique)} unique remain")
    return unique


def filter_child_friendly(concerts: List[Concert]) -> List[Concert]:
    """Keep only concerts whose title or description contain a child-friendly keyword."""
    keywords = [k.lower() for k in config.CHILD_FRIENDLY_KEYWORDS]
    filtered = [
        c for c in concerts
        if any(kw in f"{c.title} {c.description or ''}".lower() for kw in keywords)
    ]
    logger.info(f"Filtered {len(filtered)} child-friendly from {len(concerts)} total")
    return filtered


def save(concerts: List[Concert]):
    """Persist concerts to JSON and CSV."""
    if not concerts:
        logger.warning("No concerts to save")
        return

    data = [c.to_dict() for c in concerts]

    Path(config.CONCERTS_JSON).parent.mkdir(parents=True, exist_ok=True)
    with open(config.CONCERTS_JSON, "w") as f:
        json.dump(data, f, indent=2)

    pd.DataFrame(data).to_csv(config.CONCERTS_CSV, index=False)
    logger.info(f"Saved {len(data)} concerts to {config.CONCERTS_JSON} and {config.CONCERTS_CSV}")


def summarize(concerts: List[Concert]):
    """Print a distribution summary of the final dataset."""
    if not concerts:
        logger.info("No concerts to summarize")
        return

    towns = Counter(c.town for c in concerts)
    sources = Counter(c.source for c in concerts)
    venues = Counter(c.venue for c in concerts)

    max_count = max(towns.values())

    logger.info("=" * 60)
    logger.info("DATASET SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Total child-friendly concerts: {len(concerts)}")
    logger.info("")
    logger.info("By town:")
    for town, count in towns.most_common():
        bar = "\u2588" * (count * 30 // max_count)
        logger.info(f"  {town:>15}  {bar} ({count})")
    logger.info("")
    logger.info("By source:")
    for source, count in sources.most_common():
        logger.info(f"  {source}: {count}")
    logger.info("")
    logger.info("Top 5 venues:")
    for venue, count in venues.most_common(5):
        logger.info(f"  {venue}: {count}")
    logger.info("=" * 60)
