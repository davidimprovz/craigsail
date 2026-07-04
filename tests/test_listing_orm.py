"""Test that ListingORM can be inserted and read back via SessionLocal."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the ORM model we just defined.
from app.models import Base, ListingORM


def _make_engine():
    """Create an in-memory SQLite engine and tables."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


def test_listing_orm_insert_and_read_back():
    """Insert one row into listings and read it back."""
    engine = _make_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    listing = ListingORM(
        title="2019 Yamaha FZ-09",
        price_num=7500.0,
        city="seattle",
        query="yamaha fz09",
        url="https://seattle.craigslist.org/sss/d/seattle-2019-yamaha-fz09/6890123456.html",
        first_seen="2026-07-01T10:00:00Z",
        last_seen="2026-07-02T10:00:00Z",
    )
    db.add(listing)
    db.commit()

    # Read it back.
    row = db.query(ListingORM).filter_by(title=listing.title).first()
    assert row is not None, "Row should exist after insert"
    assert row.id == 1
    assert row.price_num == 7500.0
    assert row.city == "seattle"
    assert row.query == "yamaha fz09"
    assert row.url == "https://seattle.craigslist.org/sss/d/seattle-2019-yamaha-fz09/6890123456.html"
    assert row.first_seen == "2026-07-01T10:00:00Z"
    assert row.last_seen == "2026-07-02T10:00:00Z"

    db.close()
