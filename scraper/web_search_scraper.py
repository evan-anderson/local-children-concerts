"""Web search-based scraper for finding concert events across multiple sources."""

import logging
from typing import List
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper, Concert
from scraper.config import BOSTON_METRO_TOWNS

logger = logging.getLogger(__name__)


class TimeOutBostonScraper(BaseScraper):
    """Scraper for Time Out Boston events."""

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.timeout.com"
        self.boston_url = f"{self.base_url}/boston"

    def scrape(self) -> List[Concert]:
        """Scrape events from Time Out Boston."""
        logger.info("Scraping Time Out Boston events...")

        endpoints = [
            "/boston/music",
            "/boston/kids",
            "/boston/things-to-do/family-friendly-boston",
        ]

        for endpoint in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "lxml")

                # Look for event cards/articles
                events = soup.find_all("article") or soup.find_all("div", class_="card")

                for event in events[:20]:  # Limit to first 20 per page
                    try:
                        # Extract title
                        title_elem = event.find("h3") or event.find("h2")
                        if not title_elem:
                            continue
                        title = title_elem.get_text(strip=True)

                        # Extract link
                        link_elem = event.find("a")
                        event_url = link_elem.get("href", "") if link_elem else ""
                        if event_url and not event_url.startswith("http"):
                            event_url = f"{self.base_url}{event_url}"

                        # Extract description
                        desc_elem = event.find("p")
                        description = desc_elem.get_text(strip=True) if desc_elem else ""

                        # Extract venue/location
                        venue_elem = event.find("div", class_="venue") or event.find("span", class_="location")
                        venue = venue_elem.get_text(strip=True) if venue_elem else "Boston Venue"

                        # Determine town from venue or description
                        town = "Boston"
                        for t in BOSTON_METRO_TOWNS:
                            if t.lower() in venue.lower() or t.lower() in description.lower():
                                town = t
                                break

                        concert = Concert(
                            title=title,
                            venue=venue,
                            town=town,
                            date="",  # Time Out doesn't always have structured dates
                            url=event_url,
                            description=description,
                            source="Time Out Boston",
                        )
                        self.concerts.append(concert)

                    except Exception as e:
                        logger.debug(f"Error parsing Time Out event: {e}")
                        continue

            except requests.RequestException as e:
                logger.error(f"Error scraping Time Out Boston {endpoint}: {e}")

        logger.info(f"Found {len(self.concerts)} events from Time Out Boston")
        return self.concerts


class BostonComScraper(BaseScraper):
    """Scraper for Boston.com events."""

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.boston.com"

    def scrape(self) -> List[Concert]:
        """Scrape events from Boston.com."""
        logger.info("Scraping Boston.com events...")

        endpoints = [
            "/things-to-do/",
            "/culture/music/",
        ]

        for endpoint in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "lxml")

                # Look for event/article listings
                events = soup.find_all("article") or soup.find_all("div", class_="post")

                for event in events[:15]:  # Limit to first 15 per page
                    try:
                        # Extract title
                        title_elem = event.find("h2") or event.find("h3")
                        if not title_elem:
                            continue
                        title = title_elem.get_text(strip=True)

                        # Filter for music/concert content
                        music_keywords = ["concert", "music", "show", "performance", "band", "singer"]
                        if not any(keyword in title.lower() for keyword in music_keywords):
                            continue

                        # Extract link
                        link_elem = event.find("a")
                        event_url = link_elem.get("href", "") if link_elem else ""
                        if event_url and not event_url.startswith("http"):
                            event_url = f"{self.base_url}{event_url}"

                        # Extract description
                        desc_elem = event.find("p")
                        description = desc_elem.get_text(strip=True) if desc_elem else ""

                        # Determine town from content
                        town = "Boston"
                        content = f"{title} {description}".lower()
                        for t in BOSTON_METRO_TOWNS:
                            if t.lower() in content:
                                town = t
                                break

                        concert = Concert(
                            title=title,
                            venue="Boston Area Venue",
                            town=town,
                            date="",
                            url=event_url,
                            description=description,
                            source="Boston.com",
                        )
                        self.concerts.append(concert)

                    except Exception as e:
                        logger.debug(f"Error parsing Boston.com event: {e}")
                        continue

            except requests.RequestException as e:
                logger.error(f"Error scraping Boston.com {endpoint}: {e}")

        logger.info(f"Found {len(self.concerts)} events from Boston.com")
        return self.concerts


class BostonCentralScraper(BaseScraper):
    """Scraper for BostonCentral events."""

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.bostoncentral.com"

    def scrape(self) -> List[Concert]:
        """Scrape events from BostonCentral."""
        logger.info("Scraping BostonCentral events...")

        try:
            # Try events page
            url = f"{self.base_url}/events/"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")

            # Look for event listings
            events = soup.find_all("div", class_="event") or soup.find_all("article")

            for event in events[:20]:
                try:
                    # Extract title
                    title_elem = event.find("h2") or event.find("h3") or event.find("a")
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)

                    # Extract link
                    link_elem = event.find("a")
                    event_url = link_elem.get("href", "") if link_elem else ""
                    if event_url and not event_url.startswith("http"):
                        event_url = f"{self.base_url}{event_url}"

                    # Extract date
                    date_elem = event.find("time") or event.find("span", class_="date")
                    date = date_elem.get("datetime", "") if date_elem else ""

                    # Extract description
                    desc_elem = event.find("p")
                    description = desc_elem.get_text(strip=True) if desc_elem else ""

                    # Extract venue
                    venue_elem = event.find("span", class_="venue") or event.find("div", class_="location")
                    venue = venue_elem.get_text(strip=True) if venue_elem else "Boston Venue"

                    concert = Concert(
                        title=title,
                        venue=venue,
                        town="Boston",
                        date=date,
                        url=event_url,
                        description=description,
                        source="BostonCentral",
                    )
                    self.concerts.append(concert)

                except Exception as e:
                    logger.debug(f"Error parsing BostonCentral event: {e}")
                    continue

            logger.info(f"Found {len(self.concerts)} events from BostonCentral")

        except requests.RequestException as e:
            logger.error(f"Error scraping BostonCentral: {e}")

        return self.concerts
