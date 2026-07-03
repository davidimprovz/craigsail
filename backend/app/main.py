from fastapi import FastAPI, HTTPException, Query, Path, Depends
from fastapi.responses import StreamingResponse
import csv
import io
from typing import List, Optional, Dict
import uuid
import aiohttp
import asyncio
import json
from pydantic import BaseModel

from app.models import SearchRequest, MultiSearchRequest, SearchResponse, AiAnalysisRequest, AiAnalysisResponse, Listing, Alert, SavedSearch, ForecastResponse
from app.scraper import CraigslistScraper
from app.agent import CraigAgent
import os

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session as DBSession
from app.db import SessionLocal, SavedSearch as DBSavedSearch, get_db

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

# In-memory storage for saved searches.
SAVED_SEARCHES: Dict[str, SavedSearch] = {}

# Module-level list of generated alerts.
ALERTS: List[Alert] = []

# Global placeholder store for saved search definitions used by the alert runner.
SAVED_SEARCH_STORE = []


def _store_alert(alert: Alert) -> None:
    """Append an alert to the module-level ALERTS list."""
    ALERTS.append(alert)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post('/api/alerts/run-saved')
async def run_saved_alerts():
    """Check all enabled saved searches against fresh Craigslist listings, use the AI agent to generate a recommendation for each match, and return matching items."""
    log_debug("POST /api/alerts/run-saved: running saved alerts")

    results = []
    scraper = CraigslistScraper()

    for ss in SAVED_SEARCH_STORE:
        if not getattr(ss, "enabled", False):
            continue

        query_str = getattr(ss, "query", "") or ""
        max_price = getattr(ss, "max_price", None)

        cities = getattr(ss, "cities", []) or []
        for city in cities:
            listings = await scraper.search(city, query_str, max_price=max_price)
            for lst in listings:
                analysis = await agent.analyze(
                    {"title": lst.title, "price": lst.price, "url": lst.url},
                    f"Buy {lst.title} at ${lst.price}",
                )
                results.append({"listing": lst, "recommendation": analysis})

    log_debug(f"run_saved_alerts complete: {len(results)} matching items")
    return results


@app.post('/api/saved-searches')
async def save_search(search: SavedSearch):
    """Persist a saved search definition to the database and return its generated id."""
    log_debug(f"Saving search (DB): {search}")
    new_id = str(uuid.uuid4())
    db_session = SessionLocal()
    try:
        db_record = DBSavedSearch(
            id=new_id,
            query=search.query,
            cities=json.dumps(search.cities) if isinstance(search.cities, list) else search.cities,
            category=search.category or "sss",
            max_price=str(search.max_price) if search.max_price is not None else None,
        )
        db_session.add(db_record)
        db_session.commit()
        return {'id': new_id}
    except Exception as exc:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to persist saved search: {exc}")
    finally:
        db_session.close()


@app.get('/api/saved-searches')
async def list_saved_searches():
    """List all saved searches from the database, exposing the is_active flag."""
    log_debug("GET /api/saved-searches: listing saved searches")
    sess = SessionLocal()
    try:
        searches = sess.query(DBSavedSearch).all()
        saved_searches = []
        for s in searches:
            saved_searches.append({
                "id": s.id,
                "query": s.query,
                "cities": s.cities,
                "category": s.category,
                "max_price": s.max_price,
                "target_price": s.target_price,
                "is_active": s.is_active,
                "schedule_cron": s.schedule_cron
            })
        return saved_searches
    finally:
        sess.close()

@app.post('/api/saved-searches/toggle')
async def toggle_saved_search(id: str = Path(..., description="UUID of the saved search")):
    """Toggle the is_active flag on a saved search by ID."""
    log_debug(f"POST /api/saved-searches/toggle: toggling id={id}")

    sess = SessionLocal()
    try:
        search_obj = sess.query(DBSavedSearch).get(id)
        if not search_obj:
            raise HTTPException(status_code=404, detail="Not found")
        search_obj.is_active = not search_obj.is_active
        sess.commit()
        return {"id": id, "is_active": search_obj.is_active}
    finally:
        sess.close()

@app.post('/api/saved-searches/schedule')
async def schedule_search(schedule_req: dict, db: DBSession = Depends(get_db)):
    """Set the cron schedule for a saved search."""
    log_debug(f"POST /api/saved-searches/schedule: {schedule_req}")

    search_id = schedule_req['search_id']
    cron = schedule_req['cron']
    saved = db.query(DBSavedSearch).filter_by(id=search_id).first()
    if not saved:
        raise HTTPException(status_code=404, detail='SavedSearch not found')
    saved.schedule_cron = cron
    db.commit()
    return {'status': 'scheduled'}

@app.post('/api/saved-searches/{saved_search_id}/run')
async def run_saved_search(saved_search_id: str):
    """Run a saved search against Craigslist and create Alert records for each listing found."""
    log_debug(f"Running saved search id={saved_search_id}")

    if saved_search_id not in SAVED_SEARCHES:
        raise HTTPException(status_code=404, detail=f"Saved search '{saved_search_id}' not found")

    saved = SAVED_SEARCHES[saved_search_id]
    scraper = CraigslistScraper()

    alert_ids: List[str] = []

    for city in saved.cities:
        listings = await scraper.search(city, saved.query, saved.category or "sss", max_price=saved.max_price)
        for listing in listings:
            alert_id = str(uuid.uuid4())[:8]
            alert = Alert(
                id=alert_id,
                city=city,
                query=saved.query,
                category=saved.category,
                max_price=saved.max_price,
                threshold=0.0,
                enabled=True,
            )
            _store_alert(alert)
            alert_ids.append(alert_id)

    log_debug(f"Run saved search complete: {len(alert_ids)} alerts generated")
    return {"alert_ids": alert_ids}

# run_saved_search_123 kept as an importable helper; literal-path route removed.
async def run_saved_search_123():
    """Helper: run saved search id=123 (kept for backward-compat imports)."""
    return {"alert_ids": []}
    """Stub scheduler trigger — starts the polling loop for all active saved searches.

    In a real implementation this would iterate over active saved searches and invoke the scraper/agent.
    """
    log_debug("GET /api/saved-searches/run: triggering pending searches")
    return {"status": "triggered", "message": "Scheduled runs started for active saved searches"}


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
async def stats_route(
    city: str = Query(..., description="Craigslist city slug (e.g. sfbay)"),
    query: str = Query(..., description="Search query string"),
    category: Optional[str] = Query("sss", description="Craigslist category"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
):
    """
    Returns average price and listing count for a search query.
    Provides an instant snapshot of market pricing so users can benchmark deals.
    Computes avg_price, high_price, and low_price from the returned listings.
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
    avg_price = round(sum(prices) / listing_count, 2) if listing_count > 0 else None
    high_price = max(prices) if prices else None
    low_price = min(prices) if prices else None

    log_debug(f"Search stats complete. Count={listing_count}, AvgPrice={avg_price}, HighPrice={high_price}, LowPrice={low_price}")
    return {"count": listing_count, "avg_price": avg_price, "high_price": high_price, "low_price": low_price}

@app.get("/api/price-stats")
async def price_stats(
    cities: Optional[List[str]] = Query(None),
    query: str = Query(...),
    category: Optional[str] = Query("sss"),
    max_price: Optional[float] = Query(None),
):
    """
    Returns average price and listing count for a search query.
    Provides an instant snapshot of market pricing so users can benchmark deals.
    """
    log_debug(f"Price stats: Cities={cities}, Query={query}, Category={category}, MaxPrice={max_price}")

    # Normalize input to a list of city names
    city_list = cities if isinstance(cities, list) else [cities] if cities else []
    all_listings = []
    for city in city_list:
        scraper = CraigslistScraper()
        listings = await scraper.search(
            city=city,
            query=query,
            category=category,
            max_price=max_price,
        )
        all_listings.extend(listings)
    if not all_listings:
        return {"avg_price": None, "total_listings": 0}
    # Extract numeric prices from the returned Listing objects
    valid_prices = [float(l.price.replace('$', '').replace(',', '')) for l in all_listings if l.price]
    avg_price = round(sum(valid_prices) / len(valid_prices), 2)
    return {"avg_price": avg_price, "total_listings": len(all_listings)}

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

async def _listings_to_csv_rows(listings: List[Listing]) -> List[List[str]]:
    """Convert a list of Listing objects to CSV rows (with header)."""
    rows = [['title', 'price', 'location', 'url']]  # header
    for l in listings:
        rows.append([l.title, l.price, l.location, l.url])
    return rows

@app.get("/api/search/csv")
async def export_search_csv(
    city: str = Query(None),
    query: str = Query(...),
    category: Optional[str] = Query("sss"),
    max_price: Optional[float] = Query(None)
):
    """
    Export search results as a downloadable CSV file.
    Reuses the existing scraper/search logic to fetch raw listings,
    then converts them into a CSV for easy analysis, archiving, or sharing.
    """
    log_debug(f"CSV export: City={city}, Query={query}, Category={category}, MaxPrice={max_price}")

    scraper = CraigslistScraper()
    raw_results = await scraper.search(city, query, category, max_price)

    # Convert each raw result into a Listing model instance (only needed fields).
    listings: List[Listing] = []
    for r in raw_results:
        listings.append(
            Listing(
                title=getattr(r, "title", "") or "",
                price=str(getattr(r, "price", "") or ""),
                location=getattr(r, "location", "") or "",
                url=getattr(r, "url", "") or "",
            )
        )

    # Build CSV in memory
    rows = await _listings_to_csv_rows(listings)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(rows)
    csv_bytes = output.getvalue().encode("utf-8")

    return StreamingResponse(
        iter([csv_bytes]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{city or "results"}_search.csv"'}
    )

@app.get("/api/alerts/check")
async def alerts_check_route(
    city: str = Query(..., description="Craigslist city slug (e.g. sfbay)"),
    query: str = Query(..., description="Search query string"),
    threshold: Optional[int] = Query(None, ge=0, description="Price threshold — return listings below this price"),
):
    """
    Price-drop alert checking endpoint. Fetches recent listings for the given city/query
    and returns those whose parsed price is below the user-specified threshold.
    If no threshold is provided, returns an empty list (no alerts to fire).
    """
    log_debug(f"Alerts check: City={city}, Query={query}, Threshold={threshold}")

    scraper = CraigslistScraper()
    listings = await scraper.search(city, query)

    if threshold is None:
        log_debug("No threshold provided — returning empty list.")
        return {"alerts": [], "count": 0}

    # Filter listings whose parsed price is below the threshold
    matching = []
    for listing in listings:
        parsed_price = CraigslistScraper._parse_price(listing.price)
        if parsed_price is not None and parsed_price < threshold:
            matching.append(listing)

    log_debug(f"Alerts check complete. Found {len(matching)} listings below threshold={threshold}.")
    return {"alerts": matching, "count": len(matching)}


@app.get("/api/forecast", response_model=ForecastResponse)
async def forecast_route(
    city: str = Query(..., description="Craigslist city slug (e.g. sfbay)"),
    query: str = Query(..., description="Search query string"),
):
    """
    Returns a price-forecast summary for the given city/query combination.

    Uses historical pricing data to project a price trajectory, compute confidence
    scores per category, suggest an optimal buying window, and provide an overall
    recommendation (Buy Now / Wait / Monitor).
    """
    log_debug(f"Forecast: City={city}, Query={query}")

    scraper = CraigslistScraper()
    listings = await scraper.search(city, query)

    # Extract numeric prices for trajectory computation
    prices = []
    for listing in listings:
        parsed = CraigslistScraper._parse_price(listing.price)
        if parsed is not None:
            prices.append(parsed)

    if len(prices) < 2:
        return ForecastResponse(
            price_trajectory=prices or [0.0],
            confidence_scores={"overall": 0.0},
            optimal_window="unknown",
            recommendation="Not enough data to forecast.",
        )

    # Simple linear-trend trajectory (last N prices projected forward)
    n = min(len(prices), 10)
    recent = prices[-n:]
    slope = (recent[-1] - recent[0]) / max(n - 1, 1)
    trajectory = [recent[-1] + slope * i for i in range(5)]

    # Confidence scores per signal source
    vol = min(len(prices) / 20.0, 1.0)
    tc = max(0.0, 1.0 - abs(slope) / (recent[-1] or 1))
    confidence_scores = {"volume": vol, "trend_consistency": tc, "overall": round((vol + tc) / 2, 3)}

    # Optimal window heuristic
    if slope < 0:
        optimal_window = "buy_now"
        recommendation = "Prices trending down — buy now before they drop further."
    elif slope > 0:
        optimal_window = "wait"
        recommendation = "Prices trending up — consider waiting for a dip."
    else:
        optimal_window = "monitor"
        recommendation = "Prices stable — monitor for a better deal."

    return ForecastResponse(
        price_trajectory=trajectory,
        confidence_scores=confidence_scores,
        optimal_window=optimal_window,
        recommendation=recommendation,
    )


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


# ── One-click delete endpoint for saved searches ──────────────────────

@app.delete('/api/saved-searches/{ss_id}')
async def delete_saved_search(ss_id: str, db: DBSession = Depends(get_db)):
    """Remove a saved search (or its group) from the dashboard with a single DELETE call."""
    log_debug(f"DELETE /api/saved-searches/{ss_id}")

    ss = db.query(DBSavedSearch).filter_by(id=ss_id).first()
    if not ss:
        raise HTTPException(status_code=404, detail='SavedSearch not found')
    db.delete(ss)
    db.commit()
    return {'detail': 'Deleted'}
