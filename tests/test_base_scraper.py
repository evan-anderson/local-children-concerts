"""Tests for the Concert model, BaseScraper, and pipeline functions."""

import json
from pathlib import Path

import pandas as pd
import pytest

from scraper.base_scraper import BaseScraper, Concert
from scraper.config import CHILD_FRIENDLY_KEYWORDS


class MockScraper(BaseScraper):
    """Minimal scraper for testing."""

    def scrape(self):
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
    """Test pipeline filtering for child-friendly concerts."""
    from scraper.pipeline import filter_child_friendly

    scraper = MockScraper()
    scraper.scrape()

    filtered = filter_child_friendly(scraper.concerts)

    # Should find 2 child-friendly concerts (Kids Rock Concert and Family Sing-Along)
    assert len(filtered) == 2
    titles = [c.title for c in filtered]
    assert "Kids Rock Concert" in titles
    assert "Family Sing-Along" in titles
    assert "Adult Jazz Night" not in titles


def test_deduplicate():
    """Test that pipeline deduplication removes duplicates keyed on (title, venue, date)."""
    from scraper.pipeline import deduplicate

    concerts = [
        Concert(title="Concert A", venue="Venue X", town="Boston", date="2024-12-15T14:00:00"),
        Concert(title="Concert A", venue="Venue X", town="Boston", date="2024-12-15T14:00:00"),  # exact dup
        Concert(title="Concert A", venue="Venue X", town="Boston", date="2024-12-16T14:00:00"),  # different date
        Concert(title="Concert B", venue="Venue Y", town="Cambridge", date="2024-12-15T14:00:00"),
    ]

    result = deduplicate(concerts)

    assert len(result) == 3
    # First occurrence is kept
    assert result[0].title == "Concert A"
    assert result[0].date == "2024-12-15T14:00:00"
    assert result[1].title == "Concert A"
    assert result[1].date == "2024-12-16T14:00:00"
    assert result[2].title == "Concert B"


def test_deduplicate_case_insensitive():
    """Deduplication key is case-insensitive on title and venue."""
    from scraper.pipeline import deduplicate

    concerts = [
        Concert(title="Kids Concert", venue="Symphony Hall", town="Boston", date="2024-12-15T14:00:00"),
        Concert(title="kids concert", venue="symphony hall", town="Boston", date="2024-12-15T14:00:00"),
    ]

    result = deduplicate(concerts)
    assert len(result) == 1


def test_detect_town():
    """Test town detection from free text in web scraper."""
    from scraper.web_search_scraper import _detect_town

    assert _detect_town("Event at Sanders Theatre in Cambridge") == "Cambridge"
    assert _detect_town("Show happening in Somerville tonight") == "Somerville"
    assert _detect_town("Something in Newton center") == "Newton"
    assert _detect_town("No town mentioned here") == "Boston"  # fallback


def test_save_results(tmp_path):
    """Test saving concerts to JSON and CSV."""
    from scraper import config

    original_json = config.CONCERTS_JSON
    original_csv = config.CONCERTS_CSV

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
        config.CONCERTS_JSON = original_json
        config.CONCERTS_CSV = original_csv


def test_empty_scraper_save(tmp_path, caplog):
    """Test saving with no concerts logs a warning."""
    from scraper import config

    original_json = config.CONCERTS_JSON
    original_csv = config.CONCERTS_CSV
    config.CONCERTS_JSON = str(tmp_path / "concerts.json")
    config.CONCERTS_CSV = str(tmp_path / "concerts.csv")

    try:
        scraper = MockScraper()
        scraper.concerts = []
        scraper.save_results()

        assert "No concerts to save" in caplog.text

    finally:
        config.CONCERTS_JSON = original_json
        config.CONCERTS_CSV = original_csv
