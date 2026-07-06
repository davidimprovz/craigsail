from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import declarative_base
from typing import List, Optional, Dict


class SearchRequest(BaseModel):
    city: str
    query: str
    category: Optional[str] = "sss"  # default: for sale
    max_price: Optional[float] = None


class MultiSearchRequest(BaseModel):
    cities: List[str]
    query: str
    category: Optional[str] = "sss"
    max_price: Optional[float] = None


class Forecast(BaseModel):
    """AI-generated price forecast for a listing."""

    predicted_low: float
    predicted_high: float
    recommendation: str


class Listing(BaseModel):
    title: str
    price: str
    location: str
    label: Optional[str] = None  # Added for multi-city support if needed
    url: str
    priority_score: Optional[float] = None
    raw_location: Optional[str] = None  # Store raw string for lazy parsing
    image_url: Optional[str] = None
    description: Optional[str] = None
    date_posted: Optional[str] = None
    date_updated: Optional[str] = None
    ai_recommendation: Optional[str] = None  # Buy, Pass, Risky
    ai_priority: Optional[str] = None  # High, Medium, Low
    forecast: Optional[Forecast] = None

    class Config:
        extra = "allow"


class SearchResponse(BaseModel):
    results: List[Listing]


class AiAnalysisRequest(BaseModel):
    listing_url: str
    user_query: str


class AiAnalysisResponse(BaseModel):
    analysis: str


class Alert(BaseModel):
    id: str
    city: str
    query: str
    category: Optional[str] = None
    max_price: Optional[float] = None
    threshold: float
    enabled: bool = True
    predictive_alert_enabled: bool = False
    priority_score: Optional[int] = None


class SavedSearch(BaseModel):
    """Defines a saved search with criteria that can be triggered for alerts."""

    cities: List[str]
    query: str
    category: Optional[str] = "sss"
    max_price: Optional[float] = None
    target_price: Optional[float] = None  # User-defined price threshold; triggers alert when a listing's price drops below it.
    price_alert_min: Optional[float] = None  # Minimum price threshold for alerts.
    price_alert_max: Optional[float] = None  # Maximum price threshold for alerts.
    is_scheduled: bool = False  # Marks this saved search as scheduled for recurring alerts
    deviation_target: Optional[float] = None  # User-defined price deviation threshold that triggers alerts


class ForecastResponse(BaseModel):
    """Typed response schema for price-forecast data matching the EPIC JSON contract."""

    price_trajectory: List[float]
    confidence_scores: Dict[str, float]
    optimal_window: str
    recommendation: str


class RecommendationResult(BaseModel):
    low_price: float
    high_price: float
    reasoning: str


# ── Export model ─────────────────────────────────────────────────────

class ExportItem(BaseModel):
    """Defines the exact shape of data to be exported so downstream code can type-check and serialize correctly."""

    title: str
    price: str
    location: str
    forecast_low: float
    forecast_high: float
    recommendation: str
    priority_score: Optional[float] = None
    url: str


# --- SQLAlchemy ORM models (Group is a DB model for saved-search groups) ---

Base = declarative_base()


class Group(Base):
    """A group of saved searches with shared alert status."""

    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    name = Column(String, nullable=False)
    alert_enabled = Column(Boolean, default=False)


class AlertORM(Base):
    """SQLAlchemy ORM model for alerts generated from saved searches."""

    __tablename__ = "alerts"

    id = Column(String, primary_key=True)
    city = Column(String, nullable=False)
    query = Column(String, nullable=False)
    category = Column(String, nullable=True)
    max_price = Column(Integer, nullable=True)
    threshold = Column(Float, default=0.0)
    enabled = Column(Boolean, default=True)
    predictive_alert_enabled = Column(Boolean, default=False)
    priority_score = Column(Integer, nullable=True)


class ListingORM(Base):
    """SQLAlchemy ORM model for persistent listing data."""

    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    price_num = Column(Float, nullable=True)
    city = Column(String, nullable=False)
    query = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    first_seen = Column(String, nullable=False)
    last_seen = Column(String, nullable=False)


class PricingAdvice(BaseModel):
    recommended_price: float
    optimal_posting_time: str
    alert_trigger: bool
