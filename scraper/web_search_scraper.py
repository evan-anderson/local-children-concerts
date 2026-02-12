"""Generic scraper for web event listing pages.

A single parameterized class replaces what was three near-identical scrapers.
Source-specific behavior (endpoints, filters, limits) is passed as config
at instantiation time in main.py.
"""

import logging
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper, Concert
from scraper.config import BOSTON_METRO_TOWNS

logger = logging.getLogger(__name__)


def _detect_town(text: str) -> str:
    """Guess which Boston metro town is mentioned in free text. Falls back to Boston."""
    text_lower = text.lower()
    for town in BOSTON_METRO_TOWNS:
        if town.lower() in text_lower:
            return town
    return "Boston"


class WebEventScraper(BaseScraper):
    """Scrape event listings from a web page.

    Args:
        name: Human-readable source name (used as Concert.source).
        base_url: Origin of the site (e.g. "https://www.timeout.com").
        endpoints: URL paths to scrape (appended to base_url).
        per_page_limit: Max events to extract per endpoint.
        title_filter: If set, skip items whose title contains none of these words.
    """

    def __init__(
        self,
        name: str,
        base_url: str,
        endpoints: List[str],
        per_page_limit: int = 20,
        title_filter: Optional[List[str]] = None,
    ):
        super().__init__()
        self.name = name
        self.base_url = base_url
        self.endpoints = endpoints
        self.per_page_limit = per_page_limit
        self.title_filter = [kw.lower() for kw in title_filter] if title_filter else None

    def scrape(self) -> List[Concert]:
        logger.info(f"Scraping {self.name}...")

        for endpoint in self.endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "lxml")

                candidates = soup.find_all("article") or soup.find_all("div", class_="card")

                for item in candidates[:self.per_page_limit]:
                    try:
                        title_elem = item.find("h3") or item.find("h2")
                        if not title_elem:
                            continue
                        title = title_elem.get_text(strip=True)

                        if self.title_filter and not any(kw in title.lower() for kw in self.title_filter):
                            continue

                        link_elem = item.find("a")
                        url = link_elem.get("href", "") if link_elem else ""
                        if url and not url.startswith("http"):
                            url = f"{self.base_url}{url}"

                        desc_elem = item.find("p")
                        description = desc_elem.get_text(strip=True) if desc_elem else ""

                        venue_elem = item.find("div", class_="venue") or item.find("span", class_="location")
                        venue = venue_elem.get_text(strip=True) if venue_elem else f"{self.name} Venue"

                        date_elem = item.find("time") or item.find("span", class_="date")
                        date = date_elem.get("datetime", "") if date_elem else ""

                        town = _detect_town(f"{venue} {description}")

                        self.concerts.append(Concert(
                            title=title,
                            venue=venue,
                            town=town,
                            date=date,
                            url=url,
                            description=description,
                            source=self.name,
                        ))

                    except Exception as e:
                        logger.debug(f"Error parsing {self.name} item: {e}")
                        continue

            except requests.RequestException as e:
                logger.error(f"Error scraping {self.name} {endpoint}: {e}")

        logger.info(f"Found {len(self.concerts)} events from {self.name}")
        return self.concerts
