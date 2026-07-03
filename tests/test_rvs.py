"""Ported from the legacy RVs placeholders: real minimal coverage for the RVs
category ('rva') against the current search endpoint. Scraper mocked."""
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

from app.main import app
from app.models import Listing

client = TestClient(app, raise_server_exceptions=False)


def test_rvs_category_passed_to_scraper():     # was: RVs(search_category='rva')
    inst = MagicMock()
    inst.search = AsyncMock(return_value=[
        Listing(title="RV", price="$9,000", location="c", url="http://x/rv")])
    with patch("app.main.CraigslistScraper", return_value=inst):
        r = client.post("/api/search", json={"city": "city1", "query": "camper", "category": "rva"})
    assert r.status_code == 200
    assert inst.search.await_args.args[2] == "rva"

def test_rvs_result_shape():
    inst = MagicMock()
    inst.search = AsyncMock(return_value=[
        Listing(title="RV", price="$9,000", location="c", url="http://x/rv")])
    with patch("app.main.CraigslistScraper", return_value=inst):
        r = client.post("/api/search", json={"city": "city1", "query": "camper", "category": "rva"})
    item = r.json()["results"][0]
    assert set(["title", "price", "url"]).issubset(item.keys())
