"""Scraper for Boston Public Library and other library events."""

import logging
from typing import List

import requests
from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper, Concert
from scraper.config import BOSTON_METRO_TOWNS

logger = logging.getLogger(__name__)


class BostonPublicLibraryScaper(BaseScraper):
    """Scraper for Boston Public Library events."""

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.bpl.org"
        self.events_url = f"{self.base_url}/calendar/"

    def scrape(self) -> List[Concert]:
        """Scrape events from Boston Public Library."""
        logger.info("Scraping Boston Public Library events...")

        try:
            response = requests.get(self.events_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")

            # Look for event listings
            events = soup.find_all("div", class_="event") or soup.find_all("article")

            for event in events:
                try:
                    # Extract title
                    title_elem = event.find("h2") or event.find("h3") or event.find("a")
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)

                    # Skip if not music/concert related
                    music_keywords = ["music", "concert", "sing", "performance", "orchestra", "band"]
                    if not any(keyword in title.lower() for keyword in music_keywords):
                        continue

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

                    # Extract location/branch
                    loc_elem = event.find("div", class_="location") or event.find("span", class_="branch")
                    venue = loc_elem.get_text(strip=True) if loc_elem else "Boston Public Library"

                    concert = Concert(
                        title=title,
                        venue=venue,
                        town="Boston",
                        date=date,
                        url=url,
                        description=description,
                        source="Boston Public Library",
                    )
                    self.concerts.append(concert)

                except Exception as e:
                    logger.debug(f"Error parsing library event: {e}")
                    continue

            logger.info(f"Found {len(self.concerts)} music events from BPL")

        except requests.RequestException as e:
            logger.error(f"Error scraping Boston Public Library: {e}")

        return self.concerts


class CambridgePublicLibraryScaper(BaseScraper):
    """Scraper for Cambridge Public Library events."""

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.cambridgema.gov"
        self.events_url = f"{self.base_url}/departments/library/events"

    def scrape(self) -> List[Concert]:
        """Scrape events from Cambridge Public Library."""
        logger.info("Scraping Cambridge Public Library events...")

        try:
            response = requests.get(self.events_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")

            # Look for event listings
            events = soup.find_all("div", class_="event") or soup.find_all("article")

            for event in events:
                try:
                    # Extract title
                    title_elem = event.find("h2") or event.find("h3") or event.find("a")
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)

                    # Skip if not music/concert related
                    music_keywords = ["music", "concert", "sing", "performance", "orchestra", "band"]
                    if not any(keyword in title.lower() for keyword in music_keywords):
                        continue

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

                    # Extract location/branch
                    loc_elem = event.find("div", class_="location") or event.find("span", class_="branch")
                    venue = loc_elem.get_text(strip=True) if loc_elem else "Cambridge Public Library"

                    concert = Concert(
                        title=title,
                        venue=venue,
                        town="Cambridge",
                        date=date,
                        url=url,
                        description=description,
                        source="Cambridge Public Library",
                    )
                    self.concerts.append(concert)

                except Exception as e:
                    logger.debug(f"Error parsing library event: {e}")
                    continue

            logger.info(f"Found {len(self.concerts)} music events from Cambridge Library")

        except requests.RequestException as e:
            logger.error(f"Error scraping Cambridge Public Library: {e}")

        return self.concerts
