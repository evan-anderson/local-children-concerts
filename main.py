"""Main entry point: wire sources through the pipeline.

Source configuration lives here as data. Adding a new library or web source
is a dict entry, not a new class.
"""

import argparse
import logging
import os

from scraper.boston_events_scraper import BostonEventsScaper
from scraper.eventbrite_scraper import EventbriteScraper
from scraper.library_events_scraper import LibraryEventsScraper
from scraper.web_search_scraper import WebEventScraper
from scraper.pipeline import deduplicate, filter_child_friendly, save, summarize

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# --- Source configurations ---------------------------------------------------
# To add a new library: append a dict here. No new class needed.
LIBRARY_SOURCES = [
    {
        "name": "Boston Public Library",
        "base_url": "https://www.bpl.org",
        "events_path": "/calendar/",
        "town": "Boston",
    },
    {
        "name": "Cambridge Public Library",
        "base_url": "https://www.cambridgema.gov",
        "events_path": "/departments/library/events",
        "town": "Cambridge",
    },
]

# To add a new web source: append a dict here. No new class needed.
WEB_SOURCES = [
    {
        "name": "Time Out Boston",
        "base_url": "https://www.timeout.com",
        "endpoints": ["/boston/music", "/boston/kids", "/boston/things-to-do/family-friendly-boston"],
        "per_page_limit": 20,
    },
    {
        "name": "Boston.com",
        "base_url": "https://www.boston.com",
        "endpoints": ["/things-to-do/", "/culture/music/"],
        "per_page_limit": 15,
        "title_filter": ["concert", "music", "show", "performance", "band", "singer"],
    },
    {
        "name": "BostonCentral",
        "base_url": "https://www.bostoncentral.com",
        "endpoints": ["/events/"],
        "per_page_limit": 20,
    },
]


def _build_scrapers(selection: set):
    """Instantiate scrapers based on the selected source groups."""
    scrapers = []

    if "boston" in selection:
        scrapers.append(BostonEventsScaper())

    if "libraries" in selection:
        for cfg in LIBRARY_SOURCES:
            scrapers.append(LibraryEventsScraper(**cfg))

    if "web" in selection:
        for cfg in WEB_SOURCES:
            scrapers.append(WebEventScraper(**cfg))

    if "eventbrite" in selection:
        if os.getenv("EVENTBRITE_API_KEY"):
            scrapers.append(EventbriteScraper(location="Boston, MA"))
        else:
            logger.info("Skipping Eventbrite: set EVENTBRITE_API_KEY to enable")

    return scrapers


def main():
    parser = argparse.ArgumentParser(description="Scrape child-friendly concerts in Boston metro")
    parser.add_argument("--use-mock", action="store_true", help="Use mock data instead of live scraping")
    parser.add_argument(
        "--scrapers",
        nargs="+",
        choices=["boston", "libraries", "web", "eventbrite", "all"],
        default=["all"],
        help="Which source groups to run (default: all)",
    )
    args = parser.parse_args()

    logger.info("Starting concert collection...")

    # --- Collect ---------------------------------------------------------
    if args.use_mock:
        from scraper.expanded_mock_scraper import ExpandedMockScraper
        all_concerts = ExpandedMockScraper().scrape()
    else:
        selection = {"boston", "libraries", "web", "eventbrite"} if "all" in args.scrapers else set(args.scrapers)
        all_concerts = []
        for scraper in _build_scrapers(selection):
            logger.info(f"Running {scraper.__class__.__name__}...")
            all_concerts.extend(scraper.scrape())

    # --- Pipeline: deduplicate -> filter -> save -> summarize ------------
    concerts = deduplicate(all_concerts)
    concerts = filter_child_friendly(concerts)
    save(concerts)
    summarize(concerts)


if __name__ == "__main__":
    main()
