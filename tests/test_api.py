"""Tests for the FastAPI concert API."""

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_towns():
    response = client.get("/api/towns")
    assert response.status_code == 200
    towns = response.json()
    assert isinstance(towns, list)
    assert len(towns) > 0
    # Towns should be sorted alphabetically
    assert towns == sorted(towns)


def test_get_concerts_no_filters():
    response = client.get("/api/concerts")
    assert response.status_code == 200
    data = response.json()
    assert "concerts" in data
    assert "total" in data
    assert isinstance(data["concerts"], list)
    assert data["total"] == len(data["concerts"])


def test_get_concerts_filter_by_town():
    response = client.get("/api/concerts?towns=Boston")
    assert response.status_code == 200
    data = response.json()
    for concert in data["concerts"]:
        assert concert["town"].lower() == "boston"


def test_get_concerts_filter_by_multiple_towns():
    response = client.get("/api/concerts?towns=Boston&towns=Cambridge")
    assert response.status_code == 200
    data = response.json()
    for concert in data["concerts"]:
        assert concert["town"].lower() in ["boston", "cambridge"]


def test_get_concerts_filter_by_date_range():
    response = client.get("/api/concerts?start_date=2025-06-01&end_date=2025-12-31")
    assert response.status_code == 200
    data = response.json()
    for concert in data["concerts"]:
        assert concert["date"] >= "2025-06-01"
        assert concert["date"] <= "2025-12-31"


def test_get_concerts_sorted_by_date():
    response = client.get("/api/concerts")
    assert response.status_code == 200
    data = response.json()
    dates = [c["date"] for c in data["concerts"]]
    assert dates == sorted(dates)


def test_concert_response_fields():
    response = client.get("/api/concerts")
    assert response.status_code == 200
    data = response.json()
    if data["concerts"]:
        concert = data["concerts"][0]
        assert "title" in concert
        assert "venue" in concert
        assert "town" in concert
        assert "date" in concert
        assert "scraped_at" in concert
