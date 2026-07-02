"""Ported from the legacy Boats suite: price cleaning + boats-category ('boo')
search against the current backend/app stack. Scraper mocked: no network."""
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

from app.main import app
from app.models import Listing
from app.scraper import CraigslistScraper

client = TestClient(app, raise_server_exceptions=False)


def test_price_cleaning_dollar_comma():   # was: clean_city_sailboats_data '$1,000' -> 1000.0
    assert CraigslistScraper._parse_price("$1,000") == 1000

def test_price_cleaning_missing_is_none():
    assert CraigslistScraper._parse_price("N/A") is None

def test_boats_category_search():          # was: Boats(search_category='boo')
    inst = MagicMock()
    inst.search = AsyncMock(return_value=[
        Listing(title="Boat 1999", price="$1,000", location="city1", url="http://x/b")])
    with patch("app.main.CraigslistScraper", return_value=inst):
        r = client.post("/api/search", json={"city": "city1", "query": "sailboat", "category": "boo"})
    assert r.status_code == 200
    assert inst.search.await_args.args[2] == "boo"
    assert r.json()["results"][0]["price"] == "$1,000"
