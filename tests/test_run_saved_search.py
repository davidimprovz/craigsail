"""Test for the run_saved_search endpoint — loads from DB and executes scraper."""
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

from app.main import app
from app.scraper import CraigslistScraper
from app.db import SessionLocal, SavedSearch as DBSavedSearch

client = TestClient(app, raise_server_exceptions=False)


def _insert_saved_search(db_session, id="t-run-1", query="bike", cities='["sfbay"]'):
    """Insert a saved search row into the test DB."""
    record = DBSavedSearch(
        id=id,
        query=query,
        cities=cities,
        category="sss",
        max_price=None,
    )
    db_session.add(record)
    db_session.commit()


def _mock_scraper(listings):
    inst = MagicMock()
    inst.search = AsyncMock(return_value=listings)
    return inst


def test_run_saved_search_from_db():
    """Insert a DBSavedSearch row, patch the scraper, POST /run, assert 200 and one alert id."""
    db_session = SessionLocal()
    try:
        _insert_saved_search(db_session, id="t-run-1", query="bike", cities='["sfbay"]')
    finally:
        db_session.close()

    mock_listing = MagicMock()
    mock_listing.title = "test bike"
    mock_listing.price = "$200"
    mock_listing.url = "http://x/1"

    with patch("app.main.CraigslistScraper", return_value=_mock_scraper([mock_listing])):
        r = client.post("/api/saved-searches/t-run-1/run")

    assert r.status_code == 200
    body = r.json()
    assert len(body["alert_ids"]) == 1


def test_run_saved_search_404():
    """Non-existent saved search ID returns 404."""
    r = client.post("/api/saved-searches/nonexistent/run")
    assert r.status_code == 404
