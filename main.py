"""Main script to run concert scrapers and generate data files."""

import logging
import os

from scraper.config import BOSTON_METRO_TOWNS, CHILD_FRIENDLY_KEYWORDS, CONCERTS_CSV, CONCERTS_JSON
from scraper.eventbrite_scraper import EventbriteScraper
from scraper.mock_scraper import MockDataScraper

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Run all scrapers and save results."""
    logger.info("Starting concert scraping...")
    logger.info(f"Target towns: {', '.join(BOSTON_METRO_TOWNS)}")

    all_concerts = []

    # Run Mock scraper (always runs - no API key needed)
    logger.info("=" * 60)
    logger.info("Running Mock Data scraper...")
    mock_scraper = MockDataScraper()
    mock_concerts = mock_scraper.scrape()
    all_concerts.extend(mock_concerts)

    # Run Eventbrite scraper (only if API key is set)
    if os.getenv("EVENTBRITE_API_KEY"):
        logger.info("=" * 60)
        logger.info("Running Eventbrite scraper...")
        eventbrite = EventbriteScraper(location="Boston, MA")
        eventbrite_concerts = eventbrite.scrape()
        all_concerts.extend(eventbrite_concerts)
    else:
        logger.info("=" * 60)
        logger.info("Skipping Eventbrite scraper (no API key set)")
        logger.info("To use Eventbrite, set EVENTBRITE_API_KEY environment variable")

    # Add additional scrapers here as you implement them
    # Example:
    # logger.info("=" * 60)
    # logger.info("Running City Calendar scraper...")
    # city_scraper = CityScraper()
    # city_concerts = city_scraper.scrape()
    # all_concerts.extend(city_concerts)

    # Filter for child-friendly concerts
    logger.info("=" * 60)
    logger.info("Filtering for child-friendly concerts...")
    child_friendly_concerts = []
    for concert in all_concerts:
        text = f"{concert.title} {concert.description or ''}".lower()
        if any(keyword.lower() in text for keyword in CHILD_FRIENDLY_KEYWORDS):
            child_friendly_concerts.append(concert)

    logger.info(
        f"Found {len(child_friendly_concerts)} child-friendly concerts "
        f"out of {len(all_concerts)} total concerts"
    )

    # Save results
    if child_friendly_concerts:
        logger.info("=" * 60)
        logger.info("Saving results...")

        # Save using a mock scraper instance
        mock_scraper.concerts = child_friendly_concerts
        mock_scraper.save_results()

        logger.info(f"Results saved to:")
        logger.info(f"  - {CONCERTS_JSON}")
        logger.info(f"  - {CONCERTS_CSV}")
    else:
        logger.warning("No child-friendly concerts found. No files saved.")

    logger.info("=" * 60)
    logger.info("Scraping complete!")


if __name__ == "__main__":
    main()
