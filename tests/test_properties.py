"""Ported from the legacy Properties placeholders: real minimal coverage for the
properties category against the current search endpoint. Scraper mocked."""
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def _scraper(listings):
    inst = MagicMock()
    inst.search = AsyncMock(return_value=listings)
    return inst


def test_properties_category_passed_to_scraper():   # was: Properties(search_category='properties')
    ms = _scraper([])
    with patch("app.main.CraigslistScraper", return_value=ms):
        r = client.post("/api/search", json={"city": "city1", "query": "condo",
                                             "category": "properties"})
    assert r.status_code == 200
    assert ms.search.await_args.args[2] == "properties"

def test_properties_empty_results_ok():
    with patch("app.main.CraigslistScraper", return_value=_scraper([])):
        r = client.post("/api/search", json={"city": "city1", "query": "condo",
                                             "category": "properties"})
    assert r.status_code == 200
    assert r.json()["results"] == []
