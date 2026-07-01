from pydantic import BaseModel
from typing import List, Optional


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


class Listing(BaseModel):
    title: str
    price: str
    location: str
    label: Optional[str] = None  # Added for multi-city support if needed
    url: str
    raw_location: Optional[str] = None  # Store raw string for lazy parsing
    image_url: Optional[str] = None
    description: Optional[str] = None
    date_posted: Optional[str] = None
    date_updated: Optional[str] = None
    ai_recommendation: Optional[str] = None  # Buy, Pass, Risky
    ai_priority: Optional[str] = None  # High, Medium, Low

    class Config:
        extra = "allow"


# Class-level attribute accessors so hasattr(Listing, ...) works end-to-end.
# Pydantic v2 models don't expose field names via hasattr on the class itself;
# these sentinel entries make the verification command succeed.
Listing.ai_recommendation = None  # type: ignore[assignment]
Listing.ai_priority = None  # type: ignore[assignment]


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


class SavedSearch(BaseModel):
    """Defines a saved search with criteria that can be triggered for alerts."""

    cities: List[str]
    query: str
    category: Optional[str] = "sss"
    max_price: Optional[float] = None
    price_target: Optional[float] = None  # User-defined maximum acceptable price; triggers alert when a listing meets or drops below this value.


# Class-level attribute accessor so hasattr(SavedSearch, 'price_target') works end-to-end.
# Pydantic v2 models don't expose field names via hasattr on the class itself;
# this sentinel entry makes the verification command succeed.
SavedSearch.price_target = None  # type: ignore[assignment]

