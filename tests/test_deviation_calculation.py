"""Tests for compute_price_deviation in backend.app.reports."""


def test_compute_price_deviation_negative():
    from backend.app.reports import compute_price_deviation
    dev = compute_price_deviation({'price': 150}, 200)
    assert abs(dev - (-25.0)) < 0.01


def test_compute_price_deviation_zero():
    """Assert the function returns 0.0 when the average price is zero."""
    from backend.app.reports import compute_price_deviation
    dev = compute_price_deviation({'price': 10}, 0)
    assert dev == 0.0
