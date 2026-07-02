"""Report helpers for CraigSail — building export data from the database."""

from typing import List, Dict
from sqlalchemy.orm import Session as DBSession

from app.models import ExportItem
from app.db import AlertORM


def build_export_records(db: DBSession) -> List[dict]:
    """Fetch all alerts and their associated data from the DB and return a list of dicts matching ExportItem.

    Each record contains title, price, location, forecast_low, forecast_high,
    recommendation, priority_score (optional), and url — the exact shape defined
    by :class:`ExportItem`.

    The function is intentionally synchronous for simplicity; no new dependencies.
    """
    records: List[dict] = []

    # Query all alerts from the database. AlertORM stores alert metadata; we build
    # export records from each alert's stored fields.
    alerts = db.query(AlertORM).all()

    for alert in alerts:
        records.append({
            "title": f"[{alert.city}] {alert.query}",
            "price": str(alert.max_price) if alert.max_price is not None else "",
            "location": alert.city,
            "forecast_low": 0.0,
            "forecast_high": 0.0,
            "recommendation": "",
            "priority_score": float(alert.priority_score) if alert.priority_score is not None else None,
            "url": f"https://{alert.city}.craigslist.org/search/{alert.category or 'sss'}?query={alert.query}",
        })

    return records


def compute_price_deviation(listing: dict, ss_avg_price: float) -> float:
    """Compute the percentage price deviation of a listing relative to a saved-search average price.

    Returns (listing.price - ss_avg_price) / ss_avg_price * 100.
    A positive value means the listing is above the historical average;
    negative means it's below (a potential deal).
    """
    return (listing["price"] - ss_avg_price) / ss_avg_price * 100
