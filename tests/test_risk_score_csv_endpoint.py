"""Test that /api/search/csv includes the risk_score column."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app


def test_csv_endpoint_includes_risk_score_column():
    """Verify the CSV endpoint streams a header containing 'risk_score'."""
    client = TestClient(app, raise_server_exceptions=False)

    # Build dummy listings that mimic what CraigslistScraper.search would return.
    mock_listings = [
        {
            "title": "Test Bike",
            "price": 200,
            "location": "NYC",
            "url": "https://example.com/listing1",
            "image_url": None,
            "description": "A test bike listing.",
        },
    ]

    with patch("app.main.CraigslistScraper") as MockScraper:
        mock_instance = AsyncMock()
        mock_instance.search = AsyncMock(return_value=mock_listings)
        MockScraper.return_value = mock_instance

        response = client.get("/api/search/csv?city=NY")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    csv_text = response.content.decode("utf-8", errors="replace")
    assert "risk_score" in csv_text, (
        f"CSV output missing 'risk_score' column. Got:\n{csv_text[:500]}"
    )
