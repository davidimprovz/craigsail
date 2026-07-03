"""Ported from the legacy craigsail.search.Search suite: same behavioral intents
(category/city handling, price cleaning, dedup, CSV/stats export) tested against
the current FastAPI app in backend/app. Scraper is mocked: no network."""
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

from app.main import app
from app.models import Listing, SearchRequest, MultiSearchRequest
from app.scraper import CraigslistScraper

client = TestClient(app, raise_server_exceptions=False)


def make_listing(title="item1", price="$100", location="city1", url="http://x/1"):
    return Listing(title=title, price=price, location=location, url=url)


def mock_scraper(listings):
    inst = MagicMock()
    inst.search = AsyncMock(return_value=listings)
    return inst


# --- price parsing (was: clean_* price cleaning) ---
def test_parse_price_dollar_comma():
    assert CraigslistScraper._parse_price("$1,200") == 1200

def test_parse_price_plain():
    assert CraigslistScraper._parse_price("$100") == 100

def test_parse_price_na():
    assert CraigslistScraper._parse_price("N/A") is None

def test_parse_price_empty():
    assert CraigslistScraper._parse_price("") is None

def test_parse_price_garbage():
    assert CraigslistScraper._parse_price("call me") is None


# --- request models (was: get/set category, add/update cities) ---
def test_search_request_default_category():
    r = SearchRequest(city="city1", query="bike")
    assert r.category == "sss"
    assert r.max_price is None

def test_search_request_custom_category():
    r = SearchRequest(city="city1", query="bike", category="bia")
    assert r.category == "bia"

def test_multi_search_request_cities():
    r = MultiSearchRequest(cities=["city1", "city2"], query="boat")
    assert r.cities == ["city1", "city2"]

def test_listing_optional_fields_default_none():
    listing = make_listing()
    assert listing.priority_score is None
    assert listing.ai_recommendation is None


# --- search endpoint (was: get_city_items / get_all_daily_postings) ---
def test_search_returns_results():
    with patch("app.main.CraigslistScraper",
               return_value=mock_scraper([make_listing(), make_listing(title="item2")])):
        r = client.post("/api/search", json={"city": "city1", "query": "bike"})
    assert r.status_code == 200
    assert len(r.json()["results"]) == 2

def test_search_multi_city_fans_out():
    ms = mock_scraper([make_listing()])
    with patch("app.main.CraigslistScraper", return_value=ms):
        r = client.post("/api/search", json={"city": "city1,city2", "query": "bike"})
    assert r.status_code == 200
    assert ms.search.await_count == 2

def test_search_deduplicates_identical_listings():
    dup = make_listing(title="same", location="cityX")
    with patch("app.main.CraigslistScraper", return_value=mock_scraper([dup, dup])):
        r = client.post("/api/search", json={"city": "city1", "query": "bike"})
    assert r.status_code == 200
    assert len(r.json()["results"]) == 1


# --- export + stats (was: save_data_as_csv / send_to_sqlitedb) ---
def test_csv_export_returns_csv():
    with patch("app.main.CraigslistScraper", return_value=mock_scraper([make_listing()])):
        r = client.get("/api/search/csv", params={"city": "city1", "query": "bike"})
    assert r.status_code == 200
    assert "csv" in r.headers.get("content-type", "")

def test_price_stats_returns_dict():
    with patch("app.main.CraigslistScraper",
               return_value=mock_scraper([make_listing(price="$100"), make_listing(price="$300")])):
        r = client.get("/api/price-stats", params={"city": "city1", "query": "bike"})
    assert r.status_code == 200
    assert isinstance(r.json(), dict)


# --- app surface ---
def test_core_routes_registered():
    paths = {getattr(rt, "path", "") for rt in app.routes}
    assert "/health" in paths
    assert "/api/search" in paths
    assert "/multi_search" in paths

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
