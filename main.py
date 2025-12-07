"""Main script to run concert scrapers and generate data files."""

import argparse
import logging
import os

from scraper.config import BOSTON_METRO_TOWNS, CHILD_FRIENDLY_KEYWORDS, CONCERTS_CSV, CONCERTS_JSON
from scraper.boston_events_scraper import BostonEventsScaper
from scraper.eventbrite_scraper import EventbriteScraper
from scraper.library_events_scraper import BostonPublicLibraryScaper, CambridgePublicLibraryScaper
from scraper.web_search_scraper import TimeOutBostonScraper, BostonComScraper, BostonCentralScraper

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Run all scrapers and save results."""
    parser = argparse.ArgumentParser(description="Scrape concert data from Boston metro area")
    parser.add_argument(
        "--use-mock",
        action="store_true",
        help="Use mock data instead of scraping real websites",
    )
    parser.add_argument(
        "--scrapers",
        nargs="+",
        choices=["boston", "libraries", "timeout", "bostoncom", "bostoncentral", "eventbrite", "all"],
        default=["all"],
        help="Which scrapers to run (default: all)",
    )
    args = parser.parse_args()

    logger.info("Starting concert scraping...")
    logger.info(f"Target towns: {', '.join(BOSTON_METRO_TOWNS)}")

    all_concerts = []

    # Use mock data if requested
    if args.use_mock:
        logger.info("=" * 60)
        logger.info("Running Expanded Mock Data scraper...")
        from scraper.expanded_mock_scraper import ExpandedMockScraper
        mock_scraper = ExpandedMockScraper()
        mock_concerts = mock_scraper.scrape()
        all_concerts.extend(mock_concerts)
    else:
        # Run real web scrapers
        scrapers_to_run = args.scrapers
        if "all" in scrapers_to_run:
            scrapers_to_run = ["boston", "libraries", "timeout", "bostoncom", "bostoncentral", "eventbrite"]

        # Boston.gov events
        if "boston" in scrapers_to_run:
            logger.info("=" * 60)
            logger.info("Running Boston.gov scraper...")
            boston_scraper = BostonEventsScaper()
            all_concerts.extend(boston_scraper.scrape())

        # Library events
        if "libraries" in scrapers_to_run:
            logger.info("=" * 60)
            logger.info("Running Library Events scrapers...")

            bpl_scraper = BostonPublicLibraryScaper()
            all_concerts.extend(bpl_scraper.scrape())

            cpl_scraper = CambridgePublicLibraryScaper()
            all_concerts.extend(cpl_scraper.scrape())

        # Time Out Boston
        if "timeout" in scrapers_to_run:
            logger.info("=" * 60)
            logger.info("Running Time Out Boston scraper...")
            timeout_scraper = TimeOutBostonScraper()
            all_concerts.extend(timeout_scraper.scrape())

        # Boston.com
        if "bostoncom" in scrapers_to_run:
            logger.info("=" * 60)
            logger.info("Running Boston.com scraper...")
            bostoncom_scraper = BostonComScraper()
            all_concerts.extend(bostoncom_scraper.scrape())

        # BostonCentral
        if "bostoncentral" in scrapers_to_run:
            logger.info("=" * 60)
            logger.info("Running BostonCentral scraper...")
            bostoncentral_scraper = BostonCentralScraper()
            all_concerts.extend(bostoncentral_scraper.scrape())

        # Eventbrite (only if API key is set)
        if "eventbrite" in scrapers_to_run:
            if os.getenv("EVENTBRITE_API_KEY"):
                logger.info("=" * 60)
                logger.info("Running Eventbrite scraper...")
                eventbrite = EventbriteScraper(location="Boston, MA")
                all_concerts.extend(eventbrite.scrape())
            else:
                logger.info("=" * 60)
                logger.info("Skipping Eventbrite scraper (no API key set)")
                logger.info("To use Eventbrite, set EVENTBRITE_API_KEY environment variable")

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

        # Save using a temporary scraper instance
        from scraper.mock_scraper import MockDataScraper
        saver = MockDataScraper()
        saver.concerts = child_friendly_concerts
        saver.save_results()

        logger.info(f"Results saved to:")
        logger.info(f"  - {CONCERTS_JSON}")
        logger.info(f"  - {CONCERTS_CSV}")
    else:
        logger.warning("No child-friendly concerts found. No files saved.")

    logger.info("=" * 60)
    logger.info("Scraping complete!")


if __name__ == "__main__":
    main()
