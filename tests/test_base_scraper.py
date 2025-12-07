"""Tests for the base scraper functionality."""

import json
from pathlib import Path

import pandas as pd
import pytest

from scraper.base_scraper import BaseScraper, Concert
from scraper.config import CHILD_FRIENDLY_KEYWORDS


class MockScraper(BaseScraper):
    """Mock scraper for testing."""

    def scrape(self):
        """Return mock concert data."""
        self.concerts = [
            Concert(
                title="Kids Rock Concert",
                venue="Family Music Hall",
                town="Boston",
                date="2024-12-15T14:00:00",
                url="https://example.com/kids-rock",
                description="A fun concert for children and families",
                address="123 Music St, Boston, MA",
                source="MockSource",
            ),
            Concert(
                title="Adult Jazz Night",
                venue="Jazz Club",
                town="Cambridge",
                date="2024-12-20T21:00:00",
                url="https://example.com/jazz",
                description="An evening of sophisticated jazz music",
                address="456 Jazz Ave, Cambridge, MA",
                source="MockSource",
            ),
            Concert(
                title="Family Sing-Along",
                venue="Community Center",
                town="Somerville",
                date="2024-12-18T10:00:00",
                url="https://example.com/singalong",
                description="All ages welcome for a morning of music",
                address="789 Community Rd, Somerville, MA",
                source="MockSource",
            ),
        ]
        return self.concerts


def test_concert_creation():
    """Test Concert object creation."""
    concert = Concert(
        title="Test Concert",
        venue="Test Venue",
        town="Boston",
        date="2024-12-01T19:00:00",
        url="https://example.com",
        description="Test description",
        address="123 Test St",
        source="TestSource",
    )

    assert concert.title == "Test Concert"
    assert concert.venue == "Test Venue"
    assert concert.town == "Boston"
    assert concert.date == "2024-12-01T19:00:00"
    assert concert.url == "https://example.com"
    assert concert.description == "Test description"
    assert concert.address == "123 Test St"
    assert concert.source == "TestSource"
    assert concert.scraped_at is not None


def test_concert_to_dict():
    """Test Concert to dictionary conversion."""
    concert = Concert(
        title="Test Concert",
        venue="Test Venue",
        town="Boston",
        date="2024-12-01T19:00:00",
    )

    concert_dict = concert.to_dict()

    assert concert_dict["title"] == "Test Concert"
    assert concert_dict["venue"] == "Test Venue"
    assert concert_dict["town"] == "Boston"
    assert concert_dict["date"] == "2024-12-01T19:00:00"
    assert "scraped_at" in concert_dict


def test_scraper_scrape():
    """Test scraper returns concerts."""
    scraper = MockScraper()
    concerts = scraper.scrape()

    assert len(concerts) == 3
    assert all(isinstance(c, Concert) for c in concerts)


def test_filter_child_friendly():
    """Test filtering for child-friendly concerts."""
    scraper = MockScraper()
    scraper.scrape()

    filtered = scraper.filter_child_friendly(CHILD_FRIENDLY_KEYWORDS)

    # Should find 2 child-friendly concerts (Kids Rock Concert and Family Sing-Along)
    assert len(filtered) == 2
    titles = [c.title for c in filtered]
    assert "Kids Rock Concert" in titles
    assert "Family Sing-Along" in titles
    assert "Adult Jazz Night" not in titles


def test_save_results(tmp_path):
    """Test saving concerts to JSON and CSV."""
    # Create a temporary config for testing
    from scraper import config

    original_json = config.CONCERTS_JSON
    original_csv = config.CONCERTS_CSV

    # Use temporary paths
    config.CONCERTS_JSON = str(tmp_path / "concerts.json")
    config.CONCERTS_CSV = str(tmp_path / "concerts.csv")

    try:
        scraper = MockScraper()
        scraper.scrape()
        scraper.save_results()

        # Check JSON file was created
        json_file = Path(config.CONCERTS_JSON)
        assert json_file.exists()

        with open(json_file) as f:
            data = json.load(f)
        assert len(data) == 3
        assert data[0]["title"] == "Kids Rock Concert"

        # Check CSV file was created
        csv_file = Path(config.CONCERTS_CSV)
        assert csv_file.exists()

        df = pd.read_csv(csv_file)
        assert len(df) == 3
        assert "title" in df.columns
        assert "venue" in df.columns
        assert "town" in df.columns

    finally:
        # Restore original config
        config.CONCERTS_JSON = original_json
        config.CONCERTS_CSV = original_csv


def test_empty_scraper_save(tmp_path, caplog):
    """Test saving with no concerts."""
    from scraper import config

    original_json = config.CONCERTS_JSON
    config.CONCERTS_JSON = str(tmp_path / "concerts.json")

    try:
        scraper = MockScraper()
        scraper.concerts = []  # Empty list
        scraper.save_results()

        # Should log warning about no concerts
        assert "No concerts to save" in caplog.text

    finally:
        config.CONCERTS_JSON = original_json
