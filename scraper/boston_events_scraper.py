"""Scraper for Boston.gov calendar events."""

import logging
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper, Concert

logger = logging.getLogger(__name__)


class BostonEventsScaper(BaseScraper):
    """Scraper for Boston.gov events calendar."""

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.boston.gov"
        self.calendar_url = f"{self.base_url}/calendar"

    def scrape(self) -> List[Concert]:
        """Scrape events from Boston.gov calendar."""
        logger.info("Scraping Boston.gov events calendar...")

        try:
            response = requests.get(self.calendar_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")

            # Look for event listings
            events = soup.find_all("article", class_="listing-event") or soup.find_all("div", class_="event")

            for event in events:
                try:
                    # Extract title
                    title_elem = event.find("h3") or event.find("h2") or event.find("a")
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)

                    # Extract link
                    link_elem = event.find("a")
                    url = link_elem.get("href", "") if link_elem else ""
                    if url and not url.startswith("http"):
                        url = f"{self.base_url}{url}"

                    # Extract date
                    date_elem = event.find("time") or event.find("span", class_="date")
                    date = date_elem.get("datetime", "") if date_elem else ""
                    if not date and date_elem:
                        date = date_elem.get_text(strip=True)

                    # Extract description
                    desc_elem = event.find("p") or event.find("div", class_="description")
                    description = desc_elem.get_text(strip=True) if desc_elem else ""

                    # Extract location
                    loc_elem = event.find("div", class_="location") or event.find("span", class_="venue")
                    venue = loc_elem.get_text(strip=True) if loc_elem else "Boston Location"

                    concert = Concert(
                        title=title,
                        venue=venue,
                        town="Boston",
                        date=date,
                        url=url,
                        description=description,
                        source="Boston.gov",
                    )
                    self.concerts.append(concert)

                except Exception as e:
                    logger.debug(f"Error parsing event: {e}")
                    continue

            logger.info(f"Found {len(self.concerts)} events from Boston.gov")

        except requests.RequestException as e:
            logger.error(f"Error scraping Boston.gov: {e}")

        return self.concerts
