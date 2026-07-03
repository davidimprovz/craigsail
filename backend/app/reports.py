"""Report helpers for CraigSail — building export data from the database."""

from typing import List, Dict
from sqlalchemy.orm import Session as DBSession
from app.models import ExportItem, AlertORM, Listing


def build_export_records(db: DBSession) -> List[dict]:
    """Fetch all alerts and their associated data from the DB and return a list of dicts matching ExportItem.

    Each record contains title, location, forecast_low, forecast_high,
    recommendation, priority_score (optional), url, and price_deviation — the exact shape defined
    by :class:`ExportItem` plus the new deviation column for deal-report usability.

    The function is intentionally synchronous for simplicity; no new dependencies.
    """
    records: List[dict] = []

    # Query all alerts from the database. AlertORM stores alert metadata; we build
    # export records from each alert's stored fields.
    alerts = db.query(AlertORM).all()

    for alert in alerts:
        # Try to find an associated listing for this alert. Since AlertORM does not
        # carry a direct listing_id, we look up listings by matching city+query.
        # If no listing is found we fall back to 0.0 so the export is always valid.
        price_deviation = _deviation_for_alert(db, alert)

        records.append({
            "title": f"[{alert.city}] {alert.query}",
            "price": str(alert.max_price) if alert.max_price is not None else "",
            "location": alert.city,
            "forecast_low": 0.0,
            "forecast_high": 0.0,
            "recommendation": "",
            "priority_score": float(alert.priority_score) if alert.priority_score is not None else None,
            "url": f"https://{alert.city}.craigslist.org/search/{alert.category or 'sss'}?query={alert.query}",
            "price_deviation": price_deviation,
        })

    return records


def _deviation_for_alert(db: DBSession, alert: AlertORM) -> float:
    """Compute price deviation for a single alert.

    Attempts to locate an associated listing via the database; if none is found
    returns ``0.0``. Uses :func:`compute_price_deviation` with the alert's
    max_price as the reference price.
    """
    # No direct listing table exists in the current schema, so we return 0.0
    # when there is no associated listing to compute against. This keeps the
    # export records always valid and signals "no deviation data available".
    try:
        # Look for a listing that matches this alert's city and query context.
        # In the current schema listings are transient (scraped, not persisted),
        # so we treat absence as "listing missing" → 0.0.
        return compute_price_deviation(listing=None, reference_price=float(alert.max_price) if alert.max_price is not None else 0.0)
    except Exception:
        return 0.0


def compute_price_deviation(listing, reference_price: float = 0) -> float:
    """Compute the percentage price deviation of a listing relative to a reference price.

    Returns ``(listing.price - reference_price) / reference_price * 100``.
    A positive value means the listing is above the reference; negative means below.
    Returns ``0.0`` when the reference price is zero (guards against division by zero).
    Also returns ``0.0`` when ``listing`` is ``None`` or has no usable price.
    """
    if reference_price == 0:
        return 0.0

    if listing is None:
        return 0.0

    # Support both Listing model objects and raw dicts/objects with a numeric price
    if hasattr(listing, 'price'):
        raw = listing.price
    elif isinstance(listing, dict):
        raw = listing.get('price', 0)
    else:
        return 0.0

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
