"""Base scraper class for concert data collection."""

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd

from scraper import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Concert:
    """Represents a concert event."""

    def __init__(
        self,
        title: str,
        venue: str,
        town: str,
        date: str,
        url: str = None,
        description: str = None,
        address: str = None,
        source: str = None,
    ):
        self.title = title
        self.venue = venue
        self.town = town
        self.date = date
        self.url = url
        self.description = description
        self.address = address
        self.source = source
        self.scraped_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert concert to dictionary."""
        return {
            "title": self.title,
            "venue": self.venue,
            "town": self.town,
            "date": self.date,
            "url": self.url,
            "description": self.description,
            "address": self.address,
            "source": self.source,
            "scraped_at": self.scraped_at,
        }


class BaseScraper(ABC):
    """Base class for concert scrapers."""

    def __init__(self):
        self.concerts: List[Concert] = []

    @abstractmethod
    def scrape(self) -> List[Concert]:
        """Scrape concert data from source."""
        pass

    def save_results(self):
        """Save scraped concerts to JSON and CSV files."""
        if not self.concerts:
            logger.warning("No concerts to save")
            return

        # Convert to list of dictionaries
        concerts_data = [concert.to_dict() for concert in self.concerts]

        # Save as JSON
        Path(config.CONCERTS_JSON).parent.mkdir(parents=True, exist_ok=True)
        with open(config.CONCERTS_JSON, "w") as f:
            json.dump(concerts_data, f, indent=2)
        logger.info(f"Saved {len(concerts_data)} concerts to {config.CONCERTS_JSON}")

        # Save as CSV
        df = pd.DataFrame(concerts_data)
        df.to_csv(config.CONCERTS_CSV, index=False)
        logger.info(f"Saved {len(concerts_data)} concerts to {config.CONCERTS_CSV}")

    def filter_child_friendly(self, keywords: List[str]) -> List[Concert]:
        """Filter concerts for child-friendly events."""
        filtered = []
        keywords_lower = [k.lower() for k in keywords]

        for concert in self.concerts:
            text = f"{concert.title} {concert.description or ''}".lower()
            if any(keyword in text for keyword in keywords_lower):
                filtered.append(concert)

        logger.info(
            f"Filtered {len(filtered)} child-friendly concerts from {len(self.concerts)} total"
        )
        return filtered
