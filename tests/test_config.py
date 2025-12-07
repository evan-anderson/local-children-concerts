"""Tests for configuration."""

from scraper.config import BOSTON_METRO_TOWNS, CHILD_FRIENDLY_KEYWORDS


def test_boston_metro_towns():
    """Test that all expected towns are configured."""
    expected_towns = [
        "Waltham",
        "Newton",
        "Lexington",
        "Arlington",
        "Somerville",
        "Cambridge",
        "Boston",
    ]

    assert len(BOSTON_METRO_TOWNS) == len(expected_towns)
    for town in expected_towns:
        assert town in BOSTON_METRO_TOWNS


def test_child_friendly_keywords():
    """Test that child-friendly keywords are defined."""
    assert len(CHILD_FRIENDLY_KEYWORDS) > 0
    assert "kids" in CHILD_FRIENDLY_KEYWORDS
    assert "children" in CHILD_FRIENDLY_KEYWORDS
    assert "family" in CHILD_FRIENDLY_KEYWORDS
