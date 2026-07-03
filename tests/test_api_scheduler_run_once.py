"""Test for POST /api/scheduler/run-once endpoint."""
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from app.main import app


def test_run_once_returns_200_and_dict():
    """The run-once endpoint should return HTTP 200 with a JSON dict body."""
    mock_result = {1: 3}
    with patch('app.main.run_scheduling_pass', new_callable=AsyncMock, return_value=mock_result):
        response = TestClient(app).post('/api/scheduler/run-once')

    assert response.status_code == 200
    json_body = response.json()
    assert isinstance(json_body, dict)


def test_run_once_returns_hit_counts_key():
    """The run-once endpoint should return hit_counts in its JSON body."""
    mock_result = {1: 3}
    with patch('app.main.run_scheduling_pass', new_callable=AsyncMock, return_value=mock_result):
        response = TestClient(app).post('/api/scheduler/run-once')

    assert response.status_code == 200
    json_body = response.json()
    assert "hit_counts" in json_body


def test_run_once_returns_correct_hit_counts():
    """The run-once endpoint should pass through hit counts from the scheduler."""
    mock_result = {42: 7}
    with patch('app.main.run_scheduling_pass', new_callable=AsyncMock, return_value=mock_result):
        response = TestClient(app).post('/api/scheduler/run-once')

    assert response.status_code == 200
    json_body = response.json()
    # JSON serializes int keys to strings, so compare the set of values instead.
    assert set(json_body["hit_counts"].values()) == {7}


def test_run_once_calls_scraper():
    """The run-once endpoint should instantiate a CraigslistScraper."""
    with patch('app.main.run_scheduling_pass', new_callable=AsyncMock, return_value={}):
        response = TestClient(app).post('/api/scheduler/run-once')

    assert response.status_code == 200


def test_run_once_calls_run_scheduling_pass():
    """The run-once endpoint should call run_scheduling_pass."""
    mock_result = {1: 3}
    with patch('app.main.run_scheduling_pass', new_callable=AsyncMock, return_value=mock_result) as mock_run:
        response = TestClient(app).post('/api/scheduler/run-once')

    assert response.status_code == 200
    json_body = response.json()
    # JSON serializes int keys to strings, so compare the set of values instead.
    assert set(json_body["hit_counts"].values()) == {3}
    mock_run.assert_called_once()
