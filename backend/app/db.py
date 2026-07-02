"""Minimal SQLAlchemy session factory for CraigSail."""
from sqlalchemy import Column, String, Boolean, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./craigsail.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class SavedSearch(Base):
    """SQLAlchemy ORM model for saved searches."""

    __tablename__ = "saved_searches"

    id = Column(String, primary_key=True)
    query = Column(String, nullable=False)
    cities = Column(String, default="[]")  # JSON-encoded list of city slugs
    category = Column(String, default="sss")
    max_price = Column(String, nullable=True)
    target_price = Column(Float, nullable=True)  # User-defined price threshold for alerts.
    is_active = Column(Boolean, default=True)
    schedule_cron = Column(String, nullable=True)


def get_db():
    """FastAPI dependency that yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
