"""GET /api/search/csv must search each city of a comma list (like POST /api/search), not one host 'sfbay,seattle'.
Data: real Craigslist search-result markup from the dev set (sfbay/seattle, captured 2026-10-26 with Playwright,
image carousel and buttons trimmed). No network: Playwright is faked."""
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

GOTO = []


def page(*items):
    return '<html><body><div class="cl-search-results">' + "".join(items) + "</div></body></html>"


class _Page:
    def __init__(self, pages):
        self.pages, self.html = pages, "<html></html>"

    async def goto(self, url, **kw):
        GOTO.append(url)
        city = url.split("//", 1)[1].split(".craigslist.org", 1)[0]
        if city not in self.pages:
            raise RuntimeError(f"net::ERR_NAME_NOT_RESOLVED at {url}")
        self.html = self.pages[city]

    async def wait_for_selector(self, *a, **k):
        return None

    async def content(self):
        return self.html


class _Browser:
    def __init__(self, pages):
        self.pages = pages

    async def new_page(self, *a, **k):
        return _Page(self.pages)

    async def close(self):
        return None


class _PW:
    def __init__(self, pages):
        self.chromium, self.pages = self, pages

    async def launch(self, *a, **k):
        return _Browser(self.pages)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


def fake_playwright(pages):
    """Patch target: app.scraper.async_playwright. pages maps a city slug to the HTML that city serves."""
    return lambda: _PW(pages)

SF_CATALINA27 = (  # dev sfbay-boo-sailboat pid 7953361781
    '<div class="cl-search-result cl-search-view-mode-gallery" data-pid="7953361781" title="Catalina 27 Sailboat - READY TO SAIL"><div class="gallery-card"><a class="cl-app-anchor cl-search-anchor text-only posting-title" href="https://www.craigslist.org/view/d/sausalito-catalina-27-sailboat-ready-to/eczRsLhLTwxHygZDgwZ6ZH" tabindex="0"><span class="label">Catalina 27 Sailboat - READY TO SAIL</span></a><div class="meta-line"><div class="meta"><span class="result-posted-date">10/23</span><span class="separator"></span><span class="result-location">sausalito</span></div></div><span class="priceinfo">$4,900</span></div></div>'
)
SF_LASER14 = (  # dev sfbay-boo-sailboat pid 7989669807
    '<div class="cl-search-result cl-search-view-mode-gallery" data-pid="7989669807" title="Laser 14\' Sailboat"><div class="gallery-card"><a class="cl-app-anchor cl-search-anchor text-only posting-title" href="https://www.craigslist.org/view/d/oakland-laser-14-sailboat/k4jDk7mmc3bQrcmKiv8wEs" tabindex="0"><span class="label">Laser 14\' Sailboat</span></a><div class="meta-line"><div class="meta"><span class="result-posted-date">10/25</span><span class="separator"></span><span class="result-location">Oakland</span></div></div><span class="priceinfo">$850</span></div></div>'
)
SEA_ISLANDER28 = (  # dev seattle-boo-sailboat pid 7989857430
    '<div class="cl-search-result cl-search-view-mode-gallery" data-pid="7989857430" title="Islander 28 Sailboat"><div class="gallery-card"><a class="cl-app-anchor cl-search-anchor text-only posting-title" href="https://www.craigslist.org/view/d/gig-harbor-islander-28-sailboat/aZSusHWG4DhaEjFXf7PBGi" tabindex="0"><span class="label">Islander 28 Sailboat</span></a><div class="meta-line"><div class="meta"><span class="result-posted-date">10/25</span><span class="separator"></span><span class="result-location">Gig Harbor</span></div></div><span class="priceinfo">$2,000</span></div></div>'
)
SEA_BRISTOL32 = (  # dev seattle-boo-sailboat pid 7956248660
    '<div class="cl-search-result cl-search-view-mode-gallery" data-pid="7956248660" title="Bristol 32 sailboat"><div class="gallery-card"><a class="cl-app-anchor cl-search-anchor text-only posting-title" href="https://www.craigslist.org/view/d/everett-bristol-32-sailboat/62ZX4AGt2Qc8C1DArTUdEb" tabindex="0"><span class="label">Bristol 32 sailboat</span></a><div class="meta-line"><div class="meta"><span class="result-posted-date">10/26</span><span class="separator"></span><span class="result-location">Everett</span></div></div><span class="priceinfo">$25,000</span></div></div>'
)

PAGES = {"sfbay": page(SF_CATALINA27, SF_LASER14), "seattle": page(SEA_ISLANDER28, SEA_BRISTOL32, SF_LASER14)}


def test_csv_multi_city_has_every_city():
    GOTO.clear()
    client = TestClient(app, raise_server_exceptions=False)
    with patch("app.scraper.async_playwright", fake_playwright(PAGES)):
        r = client.get("/api/search/csv", params={"city": "sfbay,seattle", "query": "sailboat", "category": "boo"})
    assert r.status_code == 200, r.text[:300]
    assert not [u for u in GOTO if "," in u.split("//", 1)[1].split("/", 1)[0]], f"one host for all cities: {GOTO}"
    body = r.content.decode("utf-8")
    for title in ("Catalina 27 Sailboat - READY TO SAIL", "Laser 14' Sailboat", "Islander 28 Sailboat",
                  "Bristol 32 sailboat"):
        assert title in body, f"{title!r} missing from CSV"
    assert body.count("Laser 14' Sailboat") == 1, "the listing both cities return must appear once (dedupe)"
