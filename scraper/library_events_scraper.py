"""Scraper for public library event calendars.

A single parameterized class handles any library site. Adding a new library
source is a one-line config entry in main.py, not a new class.
"""

import logging
from typing import List

import requests
from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper, Concert

logger = logging.getLogger(__name__)

MUSIC_KEYWORDS = ["music", "concert", "sing", "performance", "orchestra", "band"]


class LibraryEventsScraper(BaseScraper):
    """Scrape music events from a public library calendar page."""

    def __init__(self, name: str, base_url: str, events_path: str, town: str):
        super().__init__()
        self.name = name
        self.base_url = base_url
        self.events_url = f"{base_url}{events_path}"
        self.town = town

    def scrape(self) -> List[Concert]:
        logger.info(f"Scraping {self.name} events...")

        try:
            response = requests.get(self.events_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")

            events = soup.find_all("div", class_="event") or soup.find_all("article")

            for event in events:
                try:
                    title_elem = event.find("h2") or event.find("h3") or event.find("a")
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)

                    if not any(kw in title.lower() for kw in MUSIC_KEYWORDS):
                        continue

                    link_elem = event.find("a")
                    url = link_elem.get("href", "") if link_elem else ""
                    if url and not url.startswith("http"):
                        url = f"{self.base_url}{url}"

                    date_elem = event.find("time") or event.find("span", class_="date")
                    date = date_elem.get("datetime", "") if date_elem else ""
                    if not date and date_elem:
                        date = date_elem.get_text(strip=True)

                    desc_elem = event.find("p") or event.find("div", class_="description")
                    description = desc_elem.get_text(strip=True) if desc_elem else ""

                    loc_elem = event.find("div", class_="location") or event.find("span", class_="branch")
                    venue = loc_elem.get_text(strip=True) if loc_elem else self.name

                    self.concerts.append(Concert(
                        title=title,
                        venue=venue,
                        town=self.town,
                        date=date,
                        url=url,
                        description=description,
                        source=self.name,
                    ))

                except Exception as e:
                    logger.debug(f"Error parsing {self.name} event: {e}")
                    continue

            logger.info(f"Found {len(self.concerts)} music events from {self.name}")

        except requests.RequestException as e:
            logger.error(f"Error scraping {self.name}: {e}")

        return self.concerts
