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
        self.events_url = f"{self.base_url}/events"

    def scrape(self) -> List[Concert]:
        """Scrape events from Boston.gov events page."""
        logger.info("Scraping Boston.gov events...")

        try:
            # Fetch multiple pages to get more events
            for page in range(3):  # Get first 3 pages
                url = f"{self.events_url}?page={page}" if page > 0 else self.events_url
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "lxml")

                # Look for event detail drawers
                events = soup.find_all("div", class_="event-details")

                for event in events:
                    try:
                        # Extract title from link
                        title_link = event.find("a")
                        if not title_link:
                            continue
                        title = title_link.get_text(strip=True)
                        url = title_link.get("href", "")
                        if url and not url.startswith("http"):
                            url = f"{self.base_url}{url}"

                        # Extract time/date info
                        time_elem = event.find("p", class_="cd m-t100")
                        date = time_elem.get_text(strip=True) if time_elem else ""

                        # Extract location
                        location_elem = event.find(text=lambda t: t and ("Virtual" in t or "Boston" in t or "," in t))
                        venue = location_elem.strip() if location_elem else "Boston"

                        # Extract description from following paragraphs
                        desc_elems = event.find_all("p")
                        description = " ".join([p.get_text(strip=True) for p in desc_elems if p.get_text(strip=True)])

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

                logger.info(f"Processed page {page + 1}, total events: {len(self.concerts)}")

            logger.info(f"Found {len(self.concerts)} events from Boston.gov")

        except requests.RequestException as e:
            logger.error(f"Error scraping Boston.gov: {e}")

        return self.concerts
