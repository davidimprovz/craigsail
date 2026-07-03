"""Report helpers for CraigSail — building export data from the database."""

from typing import List, Dict
from sqlalchemy.orm import Session as DBSession
from app.models import ExportItem, AlertORM, Listing


def build_export_records(db: DBSession) -> List[dict]:
    """Fetch all alerts and their associated data from the DB and return a list of dicts matching ExportItem.

    Each record contains title, location, forecast_low, forecast_high,
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


def compute_price_deviation(listing: Listing, reference_price: float = 0) -> float:
    """Compute the percentage price deviation of a listing relative to a reference price.

    Returns ``(listing.price - reference_price) / reference_price * 100``.
    A positive value means the listing is above the reference; negative means below.
    Returns ``0.0`` when the reference price is zero (guards against division by zero).
    """
    if reference_price == 0:
        return 0.0

    # Support both Listing model objects and raw dicts/objects with a numeric price
    if hasattr(listing, 'price'):
        raw = listing.price
    else:
        raw = listing.get('price', 0)

    try:
        if isinstance(raw, (int, float)):
            price = float(raw)
        elif isinstance(raw, str):
            price = float(raw.replace("$", "").replace(",", ""))
        else:
            return 0.0
    except (ValueError, AttributeError):
        return 0.0

    return (price - reference_price) / reference_price * 100
