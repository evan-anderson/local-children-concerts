"""Mock scraper with sample data for testing without API keys.

This scraper generates realistic sample data for testing the application
without needing to set up API keys or scrape real websites.
"""

import logging
from datetime import datetime, timedelta
from typing import List

from scraper.base_scraper import BaseScraper, Concert
from scraper.config import BOSTON_METRO_TOWNS

logger = logging.getLogger(__name__)


class MockDataScraper(BaseScraper):
    """Generates mock concert data for testing."""

    def __init__(self):
        super().__init__()
        self.mock_data = self._generate_mock_concerts()

    def _generate_mock_concerts(self) -> List[Concert]:
        """Generate realistic mock concert data."""
        base_date = datetime.now() - timedelta(days=180)  # Start 6 months ago

        mock_concerts = [
            # Boston concerts
            Concert(
                title="Boston Children's Chorus Winter Concert",
                venue="Symphony Hall",
                town="Boston",
                date=(base_date + timedelta(days=30)).isoformat(),
                url="https://example.com/bcc-winter",
                description="Annual winter concert featuring the Boston Children's Chorus with holiday favorites for the whole family",
                address="301 Massachusetts Ave, Boston, MA 02115",
                source="MockData",
            ),
            Concert(
                title="Kidz Bop Live Tour",
                venue="House of Blues Boston",
                town="Boston",
                date=(base_date + timedelta(days=60)).isoformat(),
                url="https://example.com/kidzbop",
                description="The ultimate kids concert experience! Kidz Bop kids perform today's biggest hits.",
                address="15 Lansdowne St, Boston, MA 02215",
                source="MockData",
            ),
            Concert(
                title="Jazz at Lincoln Center Orchestra",
                venue="Boston Symphony Hall",
                town="Boston",
                date=(base_date + timedelta(days=90)).isoformat(),
                url="https://example.com/jazz-lincoln",
                description="An evening of sophisticated jazz performances",
                address="301 Massachusetts Ave, Boston, MA 02115",
                source="MockData",
            ),
            # Cambridge concerts
            Concert(
                title="Family Folk Festival",
                venue="Sanders Theatre",
                town="Cambridge",
                date=(base_date + timedelta(days=45)).isoformat(),
                url="https://example.com/folk-fest",
                description="All ages welcome! Traditional folk music and sing-alongs for children and families",
                address="45 Quincy St, Cambridge, MA 02138",
                source="MockData",
            ),
            Concert(
                title="Cambridge Youth Orchestra Spring Concert",
                venue="First Church Cambridge",
                town="Cambridge",
                date=(base_date + timedelta(days=120)).isoformat(),
                url="https://example.com/cyo-spring",
                description="Young musicians showcase their talents in this family-friendly classical concert",
                address="11 Garden St, Cambridge, MA 02138",
                source="MockData",
            ),
            # Somerville concerts
            Concert(
                title="Toddler Music & Movement Class Concert",
                venue="Somerville Arts Center",
                town="Somerville",
                date=(base_date + timedelta(days=15)).isoformat(),
                url="https://example.com/toddler-music",
                description="Interactive music class culminating in a toddler-friendly performance for preschool age children",
                address="143 Highland Ave, Somerville, MA 02143",
                source="MockData",
            ),
            Concert(
                title="Rock Night at ONCE Ballroom",
                venue="ONCE Ballroom",
                town="Somerville",
                date=(base_date + timedelta(days=75)).isoformat(),
                url="https://example.com/rock-night",
                description="21+ rock concert featuring local indie bands",
                address="156 Highland Ave, Somerville, MA 02143",
                source="MockData",
            ),
            # Newton concerts
            Concert(
                title="Newton Community Music School Family Concert",
                venue="Newton Community Music School",
                town="Newton",
                date=(base_date + timedelta(days=50)).isoformat(),
                url="https://example.com/ncms-family",
                description="Family concert featuring young students and professional musicians. All ages welcome!",
                address="321 Chestnut St, Newton, MA 02465",
                source="MockData",
            ),
            # Waltham concerts
            Concert(
                title="Waltham Philharmonic: Music for Young People",
                venue="Waltham High School Auditorium",
                town="Waltham",
                date=(base_date + timedelta(days=100)).isoformat(),
                url="https://example.com/waltham-phil",
                description="Educational concert designed for elementary school children with interactive elements",
                address="617 Lexington St, Waltham, MA 02452",
                source="MockData",
            ),
            # Arlington concerts
            Concert(
                title="Arlington Children's Theater Musical",
                venue="Arlington Town Hall",
                town="Arlington",
                date=(base_date + timedelta(days=80)).isoformat(),
                url="https://example.com/act-musical",
                description="Youth theater presents a family-friendly musical performance",
                address="730 Massachusetts Ave, Arlington, MA 02476",
                source="MockData",
            ),
            # Lexington concerts
            Concert(
                title="Lexington Symphony: Young People's Concert",
                venue="Cary Memorial Hall",
                town="Lexington",
                date=(base_date + timedelta(days=110)).isoformat(),
                url="https://example.com/lexington-youth",
                description="Interactive orchestra concert for kids featuring classic works explained for young audiences",
                address="1605 Massachusetts Ave, Lexington, MA 02420",
                source="MockData",
            ),
            # Additional Boston concerts
            Concert(
                title="Disney Princess Concert",
                venue="Boston Convention Center",
                town="Boston",
                date=(base_date + timedelta(days=150)).isoformat(),
                url="https://example.com/disney-princess",
                description="Magical concert featuring Disney princess songs performed live. Perfect for kids and families!",
                address="415 Summer St, Boston, MA 02210",
                source="MockData",
            ),
        ]

        return mock_concerts

    def scrape(self) -> List[Concert]:
        """Return mock concert data."""
        logger.info("Generating mock concert data...")
        self.concerts = self.mock_data
        logger.info(f"Generated {len(self.concerts)} mock concerts")
        return self.concerts
