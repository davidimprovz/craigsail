from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    city: str
    query: str
    category: Optional[str] = "sss" # default: for sale
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
    label: Optional[str] = None # Added for multi-city support if needed
    url: str
    raw_location: Optional[str] = None # Store raw string for lazy parsing
    image_url: Optional[str] = None
    description: Optional[str] = None
    date_posted: Optional[str] = None
    date_updated: Optional[str] = None
    ai_recommendation: Optional[str] = None # Buy, Pass, Risky
    ai_priority: Optional[str] = None # High, Medium, Low
    
class SearchResponse(BaseModel):
    results: List[Listing]

class AiAnalysisRequest(BaseModel):
    listing_url: str
    user_query: str

class AiAnalysisResponse(BaseModel):
    analysis: str
