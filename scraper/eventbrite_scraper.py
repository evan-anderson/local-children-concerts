"""Scraper for Eventbrite events.

Note: Eventbrite has an API that requires authentication. This scraper
shows how to use the API. You'll need to:
1. Create an Eventbrite account
2. Get an API key from https://www.eventbrite.com/platform/api
3. Set the EVENTBRITE_API_KEY environment variable
"""

import logging
import os
from datetime import datetime, timedelta
from typing import List

import requests

from scraper.base_scraper import BaseScraper, Concert

logger = logging.getLogger(__name__)


class EventbriteScraper(BaseScraper):
    """Scraper for Eventbrite events."""

    def __init__(self, location: str = "Boston, MA", search_terms: List[str] = None):
        super().__init__()
        self.api_key = os.getenv("EVENTBRITE_API_KEY")
        self.location = location
        self.search_terms = search_terms or ["kids concert", "children's music", "family concert"]
        self.base_url = "https://www.eventbriteapi.com/v3"

    def scrape(self) -> List[Concert]:
        """Scrape events from Eventbrite API."""
        if not self.api_key:
            logger.warning(
                "EVENTBRITE_API_KEY not set. Skipping Eventbrite scraper. "
                "Get an API key at https://www.eventbrite.com/platform/api"
            )
            return self.concerts

        headers = {"Authorization": f"Bearer {self.api_key}"}

        # Search for events in the last year
        start_date = (datetime.now() - timedelta(days=365)).isoformat() + "Z"
        end_date = datetime.now().isoformat() + "Z"

        for search_term in self.search_terms:
            try:
                params = {
                    "location.address": self.location,
                    "location.within": "25mi",  # 25 mile radius
                    "start_date.range_start": start_date,
                    "start_date.range_end": end_date,
                    "q": search_term,
                    "expand": "venue",
                }

                response = requests.get(
                    f"{self.base_url}/events/search/",
                    headers=headers,
                    params=params,
                    timeout=30,
                )
                response.raise_for_status()
                data = response.json()

                for event in data.get("events", []):
                    venue_info = event.get("venue", {})
                    concert = Concert(
                        title=event.get("name", {}).get("text", ""),
                        venue=venue_info.get("name", "Unknown Venue"),
                        town=venue_info.get("address", {}).get("city", "Unknown"),
                        date=event.get("start", {}).get("local", ""),
                        url=event.get("url", ""),
                        description=event.get("description", {}).get("text", ""),
                        address=venue_info.get("address", {}).get("localized_address_display", ""),
                        source="Eventbrite",
                    )
                    self.concerts.append(concert)

                logger.info(f"Found {len(data.get('events', []))} events for '{search_term}'")

            except requests.RequestException as e:
                logger.error(f"Error scraping Eventbrite for '{search_term}': {e}")

        logger.info(f"Total Eventbrite concerts scraped: {len(self.concerts)}")
        return self.concerts
