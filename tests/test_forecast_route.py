"""Test /api/forecast endpoint — verifies confidence_scores fix (no NameError)."""
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

from app.main import app
from app.models import Listing
from app.scraper import CraigslistScraper

client = TestClient(app, raise_server_exceptions=False)


def _make_listings(prices):
    return [Listing(title=f"item{i}", price=p, location="city1", url=f"http://x/{i}") for i, p in enumerate(prices)]


def test_forecast_route_status_200_and_confidence_scores():
    """GET /api/forecast with 3 numeric prices must return 200 and confidence_scores."""
    listings = _make_listings(["$100", "$200", "$150"])

    mock_inst = MagicMock()
    mock_inst.search = AsyncMock(return_value=listings)

    with patch.object(CraigslistScraper, "search", new=AsyncMock(return_value=listings)):
        r = client.get("/api/forecast?city=sfbay&query=bike")

    assert r.status_code == 200
    body = r.json()
    assert "confidence_scores" in body, f"Response missing confidence_scores: {body.keys()}"


def test_forecast_route_too_few_prices():
    """With fewer than 2 numeric prices the endpoint should still return 200."""
    listings = [Listing(title="x", price="$100", location="c", url="u")]

    mock_inst = MagicMock()
    mock_inst.search = AsyncMock(return_value=listings)

    with patch.object(CraigslistScraper, "search", new=AsyncMock(return_value=listings)):
        r = client.get("/api/forecast?city=sfbay&query=bike")

    assert r.status_code == 200


def test_forecast_route_no_listings():
    """With zero listings the endpoint should still return 200."""
    mock_inst = MagicMock()
    mock_inst.search = AsyncMock(return_value=[])

    with patch.object(CraigslistScraper, "search", new=AsyncMock(return_value=[])):
        r = client.get("/api/forecast?city=sfbay&query=bike")

    assert r.status_code == 200
