from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
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


class SavedSearch(BaseModel):
    """Defines a saved search with criteria that can be triggered for alerts."""

    cities: List[str]
    query: str
    category: Optional[str] = "sss"
    max_price: Optional[float] = None
    target_price: Optional[float] = None  # User-defined price threshold; triggers alert when a listing's price drops below it.
    price_alert_min: Optional[float] = None  # Minimum price threshold for alerts.
    price_alert_max: Optional[float] = None  # Maximum price threshold for alerts.


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


# --- SQLAlchemy ORM models (Group is a DB model for saved-search groups) ---

Base = declarative_base()


class Group(Base):
    """A group of saved searches with shared alert status."""

    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    name = Column(String, nullable=False)
    alert_enabled = Column(Boolean, default=False)
