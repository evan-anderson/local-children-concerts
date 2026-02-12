"""Base scraper class and Concert data model."""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List

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
        """Save scraped concerts to JSON and CSV via the pipeline."""
        from scraper.pipeline import save
        save(self.concerts)
