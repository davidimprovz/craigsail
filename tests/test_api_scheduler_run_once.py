"""Test for POST /api/scheduler/run-once endpoint."""
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from app.main import app


def test_run_once_returns_200_and_dict():
    with patch('app.main.CraigslistScraper') as mock_scraper_class:
        mock_scraper = MagicMock()
        mock_scraper.search = AsyncMock(return_value=5)
        mock_scraper_class.return_value = mock_scraper
        response = TestClient(app).post('/api/scheduler/run-once')

    assert response.status_code == 200
    json_body = response.json()
    # The endpoint returns a dict; ensure it is a dict and contains the mocked value
    assert isinstance(json_body, dict)


def test_run_once_returns_hit_counts_key():
    """The run-once endpoint should return hit_counts in its JSON body."""
    with patch('app.main.CraigslistScraper') as mock_scraper_class:
        mock_scraper = MagicMock()
        mock_scraper.search = AsyncMock(return_value=5)
        mock_scraper_class.return_value = mock_scraper
        response = TestClient(app).post('/api/scheduler/run-once')

    assert response.status_code == 200
    json_body = response.json()
    assert "hit_counts" in json_body


def test_run_once_calls_scraper():
    """The run-once endpoint should instantiate a CraigslistScraper."""
    with patch('app.main.CraigslistScraper') as mock_scraper_class:
        mock_scraper = MagicMock()
        mock_scraper.search = AsyncMock(return_value=5)
        mock_scraper_class.return_value = mock_scraper
        TestClient(app).post('/api/scheduler/run-once')

    mock_scraper_class.assert_called_once()


def test_run_once_calls_run_scheduling_pass():
    """The run-once endpoint should call run_scheduling_pass."""
    with patch('app.main.CraigslistScraper') as mock_scraper_class, \
         patch('app.main.run_scheduling_pass', new_callable=AsyncMock) as mock_run:
        mock_scraper = MagicMock()
        mock_scraper.search = AsyncMock(return_value=5)
        mock_scraper_class.return_value = mock_scraper
        mock_run.return_value = {1: 3}
        response = TestClient(app).post('/api/scheduler/run-once')

    assert response.status_code == 200
    json_body = response.json()
    # JSON serializes int keys to strings, so compare the set of values instead.
    assert set(json_body["hit_counts"].values()) == {3}
    mock_run.assert_called_once()
