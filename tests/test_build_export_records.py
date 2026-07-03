"""Tests for build_export_records — verifying price_deviation is included in export records."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from unittest.mock import MagicMock, patch
from app.reports import build_export_records, compute_price_deviation
from app.models import AlertORM, Listing


def test_build_export_includes_price_deviation():
    """Assert that build_export_records returns dicts containing 'price_deviation'
    whose value matches the expected deviation computed by compute_price_deviation."""

    # Build a mock alert ORM row.
    mock_alert = MagicMock(spec=AlertORM)
    mock_alert.city = "sfbay"
    mock_alert.query = "road bike"
    mock_alert.max_price = 500
    mock_alert.category = "bik"
    mock_alert.priority_score = None

    # Build a mock listing with a known price.
    mock_listing = MagicMock(spec=Listing)
    mock_listing.price = 400

    expected_deviation = compute_price_deviation(mock_listing, float(mock_alert.max_price))

    # Mock db.query(AlertORM).all() to return our alert.
    mock_db = MagicMock()
    mock_db.query.return_value.all.return_value = [mock_alert]

    # Patch _deviation_for_alert so it uses our known listing → known deviation.
    with patch("app.reports._deviation_for_alert", return_value=expected_deviation):
        records = build_export_records(mock_db)

    assert len(records) == 1
    record = records[0]
    assert "price_deviation" in record, "Export record must contain 'price_deviation' key"
    assert record["price_deviation"] == expected_deviation, (
        f"Expected deviation {expected_deviation}, got {record['price_deviation']}"
    )


def test_build_export_records_price_deviation_zero_when_no_listing():
    """When no listing is associated with an alert, price_deviation should be 0.0."""

    mock_alert = MagicMock(spec=AlertORM)
    mock_alert.city = "sfbay"
    mock_alert.query = "road bike"
    mock_alert.max_price = 500
    mock_alert.category = "bik"
    mock_alert.priority_score = None

    mock_db = MagicMock()
    mock_db.query.return_value.all.return_value = [mock_alert]

    # Patch _deviation_for_alert to return 0.0 (simulating missing listing).
    with patch("app.reports._deviation_for_alert", return_value=0.0):
        records = build_export_records(mock_db)

    assert len(records) == 1
    assert records[0]["price_deviation"] == 0.0


def test_compute_price_deviation_with_none_listing():
    """compute_price_deviation should return 0.0 when listing is None."""
    result = compute_price_deviation(listing=None, reference_price=100.0)
    assert result == 0.0
