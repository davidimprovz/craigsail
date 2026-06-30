from fastapi import FastAPI, HTTPException, Query
from app.models import SearchRequest, MultiSearchRequest, SearchResponse, AiAnalysisRequest, AiAnalysisResponse, Listing
from app.scraper import CraigslistScraper
from app.agent import CraigAgent
import os
import aiohttp
import asyncio
import json
from typing import List, Optional
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Craigsail API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development convenience. In production restrict this.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# scraper = CraigslistScraper() # Instantiate per request for safety or keep global? Global is fine for stateless.
agent = CraigAgent()

# Debug Configuration
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

def log_debug(message: str):
    if DEBUG:
        print(f"[DEBUG] {message}")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/cities")
def get_cities():
    """Returns the list of scraped US cities."""
    log_debug("Fetching city list...")
    try:
        path = "/app/src/data/cities.json"
        
        # improving local dev support:
        if not os.path.exists(path):
            # Try relative
            path = "src/data/cities.json"
            
        if os.path.exists(path):
            log_debug(f"Loading cities from {path}")
            with open(path, 'r') as f:
                data = json.load(f)
                log_debug(f"Loaded {len(data)} cities.")
                return data
        else:
            log_debug(f"Cities file not found at {path}")
            return []
    except Exception as e:
        print(f"Error loading cities: {e}")
        return []

@app.get("/api/models")
async def get_models():
    """Fetches available models from Ollama."""
    log_debug("Fetching models from Ollama...")
    try:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
        url = f"{base_url}/api/tags"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=2) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        models = [m["name"] for m in data.get("models", [])]
                        log_debug(f"Found models: {models}")
                        return {"models": models}
            except:
                log_debug("Failed to connect to Ollama.")
                pass
                
        # Fallback if connection fails
        return {"models": ["mistral", "gemma:2b", "llama3"]}
    except Exception as e:
        print(f"Error fetching models: {e}")
        return {"models": ["mistral", "gemma:2b"]} 

class ParseRequest(BaseModel):
    listings: List[Listing]
    model: str = "mistral"

@app.post("/api/parse", response_model=SearchResponse)
async def parse_data(request: ParseRequest):
    """
    Lazily parses a batch of listings using the selected AI model.
    """
    from app.parser import parser

    log_debug(f"Parse request: {len(request.listings)} items, model={request.model}")

    parsed_listings = []
    parsed_count = 0
    changed_count = 0

    for item in request.listings:
        if item.raw_location:
            parsed_count += 1
            original_location = item.location
            p_data = await parser.parse_listing_fragment(item.raw_location, item.date_posted or "")

            item.location = p_data.get("location", item.location)
            item.date_posted = p_data.get("date_posted", item.date_posted)
            item.date_updated = p_data.get("date_updated", item.date_updated)

            if item.location != original_location:
                changed_count += 1

        parsed_listings.append(item)

    log_debug(f"Parse complete: {parsed_count} processed, {changed_count} changed")
    return SearchResponse(results=parsed_listings)

@app.get("/api/search/price-limited", response_model=SearchResponse)
async def price_limited_search(
    city: str = Query(..., description="Craigslist city slug (e.g. sfbay)"),
    query: str = Query(..., description="Search query string"),
    category: Optional[str] = Query("sss", description="Craigslist category"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
):
    """
    Price-limited search endpoint. Returns listings whose parsed price is at most max_price.
    Accepts query parameters matching SearchRequest fields so callers don't need a JSON body.
    """
    log_debug(f"Price-limited search: City={city}, Query={query}, Category={category}, MaxPrice={max_price}")

    scraper = CraigslistScraper()

    # Handle multi-city: city string might be "sfbay,sacramento,stockton"
    cities = [c.strip() for c in city.split(',') if c.strip()]

    all_results = []

    tasks = [scraper.search(c, query, category or "sss", max_price=max_price) for c in cities]
    results_list = await asyncio.gather(*tasks)

    for res in results_list:
        all_results.extend(res)

    # Auto-deduplicate listings based on title and location combination
    deduplicated_results = _dedup_listings(all_results)

    log_debug(f"Price-limited search complete. Found {len(deduplicated_results)} results.")
    return SearchResponse(results=deduplicated_results)

@app.get("/api/search/stats")
async def search_stats(
    city: str = Query(..., description="Craigslist city slug (e.g. sfbay)"),
    query: str = Query(..., description="Search query string"),
    category: Optional[str] = Query("sss", description="Craigslist category"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
):
    """
    Returns average price and listing count for a search query.
    Provides an instant snapshot of market pricing so users can benchmark deals.
    """
    log_debug(f"Search stats: City={city}, Query={query}, Category={category}, MaxPrice={max_price}")

    scraper = CraigslistScraper()

    # Handle multi-city: city string might be "sfbay,sacramento,stockton"
    cities = [c.strip() for c in city.split(',') if c.strip()]

    all_results = []

    tasks = [scraper.search(c, query, category or "sss", max_price=max_price) for c in cities]
    results_list = await asyncio.gather(*tasks)

    for res in results_list:
        all_results.extend(res)

    # Extract numeric prices using _parse_price, ignore None
    prices = []
    for listing in all_results:
        parsed = CraigslistScraper._parse_price(listing.price)
        if parsed is not None:
            prices.append(parsed)

    listing_count = len(prices)
    average_price = round(sum(prices) / listing_count, 2) if listing_count > 0 else None

    log_debug(f"Search stats complete. Count={listing_count}, AveragePrice={average_price}")
    return {"count": listing_count, "average_price": average_price}

@app.post("/api/search", response_model=SearchResponse)
async def search_listings(request: SearchRequest):
    log_debug(f"Searching request: City={request.city}, Query={request.query}, Category={request.category}, MaxPrice={request.max_price}")
    scraper = CraigslistScraper()
    
    # Handle multi-city: city string might be "sfbay,sacramento,stockton"
    # Filter empty strings
    cities = [c.strip() for c in request.city.split(',') if c.strip()]
    
    all_results = []
    
    # Run concurrent searches with max_price filter
    tasks = [scraper.search(city, request.query, request.category, max_price=request.max_price) for city in cities]
    results_list = await asyncio.gather(*tasks)
    
    for res in results_list:
        all_results.extend(res)
        
    # Auto-deduplicate listings based on title and location combination
    deduplicated_results = _dedup_listings(all_results)
    
    log_debug(f"Search complete. Found {len(all_results)} total results, {len(deduplicated_results)} after deduplication.")
    return SearchResponse(results=deduplicated_results)

@app.post("/multi_search", response_model=SearchResponse)
async def multi_city_search(request: MultiSearchRequest):
    """
    Searches Craigslist across multiple cities in a single request.
    Returns combined results from all specified cities.
    """
    log_debug(f"Multi-city search: Cities={request.cities}, Query={request.query}, Category={request.category}, MaxPrice={request.max_price}")
    
    scraper = CraigslistScraper()
    all_results = []
    
    # Create tasks for each city, catching errors individually
    async def safe_search(city: str):
        try:
            return await scraper.search(city, request.query, request.category, max_price=request.max_price)
        except Exception as e:
            log_debug(f"Error searching {city}: {e}")
            return []
    
    # Run all city searches concurrently with error handling
    tasks = [safe_search(city) for city in request.cities]
    results_list = await asyncio.gather(*tasks, return_exceptions=False)
    
    for res in results_list:
        if isinstance(res, list):
            all_results.extend(res)
    
    log_debug(f"Multi-city search complete. Found {len(all_results)} total results across {len(request.cities)} cities.")
    return SearchResponse(results=all_results)

@app.post("/api/analyze", response_model=AiAnalysisResponse)
async def analyze_listing(request: AiAnalysisRequest):
    scraper = CraigslistScraper()
    try:
        # First scrape the details
        details = await scraper.get_details(request.listing_url)
        # Then analyze with AI
        analysis = await agent.analyze(details, request.user_query)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _dedup_listings(listings: List[Listing]) -> List[Listing]:
    """
    Filters out duplicate listings based on the combination of title and location.
    Preserves the first occurrence of each unique title+location pair.
    """
    seen = set()
    deduplicated = []
    
    for listing in listings:
        # Create a tuple key from title and location for deduplication
        key = (listing.title, listing.location)
        
        if key not in seen:
            seen.add(key)
            deduplicated.append(listing)
    
    return deduplicated
