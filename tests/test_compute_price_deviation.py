"""Tests for compute_price_deviation in app.reports."""
from fastapi.testclient import TestClient
from app.main import app


def test_compute_price_deviation_basic():
    from app.reports import compute_price_deviation
    listing = {"price": 120}
    ref = 100
    dev = compute_price_deviation(listing, ref)
    assert dev == 20.0
