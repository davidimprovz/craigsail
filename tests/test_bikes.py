"""Ported from the legacy Bikes placeholders: real minimal coverage for the
bikes category ('bia') against the current search endpoint. Scraper mocked."""
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

from app.main import app
from app.models import Listing

client = TestClient(app, raise_server_exceptions=False)


def _scraper(listings):
    inst = MagicMock()
    inst.search = AsyncMock(return_value=listings)
    return inst


def test_bikes_category_passed_to_scraper():   # was: Bikes(search_category='bia')
    ms = _scraper([Listing(title="bike", price="$50", location="c", url="http://x/1")])
    with patch("app.main.CraigslistScraper", return_value=ms):
        r = client.post("/api/search", json={"city": "city1", "query": "bmx", "category": "bia"})
    assert r.status_code == 200
    assert ms.search.await_args.args[2] == "bia"

def test_bikes_max_price_forwarded():
    ms = _scraper([])
    with patch("app.main.CraigslistScraper", return_value=ms):
        r = client.post("/api/search", json={"city": "city1", "query": "bmx",
                                             "category": "bia", "max_price": 500})
    assert r.status_code == 200
    assert ms.search.await_args.kwargs.get("max_price") == 500
