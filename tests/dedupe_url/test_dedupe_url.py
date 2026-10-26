"""_dedup_listings must treat one posting URL as one listing: two different postings with the same title and location are both kept; the same posting seen twice is kept once.
Data: real Craigslist search-result markup from the dev set (sfbay/seattle, captured 2026-10-26 with Playwright,
image carousel and buttons trimmed). No network: Playwright is faked."""
import asyncio

from app.main import _dedup_listings
from app.scraper import CraigslistScraper

SF_VANE_100 = (  # dev sfbay-sss-sailboat pid 7947903076
    '<div class="cl-search-result cl-search-view-mode-gallery" data-pid="7947903076" title="VINTAGE SAILBOAT MONITOR WOOD SELF STEERING RUDDER WEATHERVANE AIRVANE"><div class="gallery-card"><a class="cl-app-anchor cl-search-anchor text-only posting-title" href="https://www.craigslist.org/view/d/sacramento-vintage-sailboat-monitor/8Z3BBhb5eoBptmYCiYyeBz" tabindex="0"><span class="label">VINTAGE SAILBOAT MONITOR WOOD SELF STEERING RUDDER WEATHERVANE AIRVANE</span></a><div class="meta-line"><div class="meta"><span class="result-posted-date">&lt;1hr ago</span><span class="separator"></span><span class="result-location">marina / cow hollow</span></div></div><span class="priceinfo">$100</span></div></div>'
)
SF_VANE_75 = (  # dev sfbay-sss-sailboat pid 7942547783
    '<div class="cl-search-result cl-search-view-mode-gallery" data-pid="7942547783" title="VINTAGE SAILBOAT MONITOR WOOD SELF STEERING RUDDER WEATHERVANE AIRVANE"><div class="gallery-card"><a class="cl-app-anchor cl-search-anchor text-only posting-title" href="https://www.craigslist.org/view/d/sacramento-vintage-sailboat-monitor/nMGqbq5u2UWNSyf4tDz3e1" tabindex="0"><span class="label">VINTAGE SAILBOAT MONITOR WOOD SELF STEERING RUDDER WEATHERVANE AIRVANE</span></a><div class="meta-line"><div class="meta"><span class="result-posted-date">&lt;1hr ago</span><span class="separator"></span><span class="result-location">marina / cow hollow</span></div></div><span class="priceinfo">$75</span></div></div>'
)
SF_J24_4000 = (  # dev sfbay-boo-sailboat pid 7960809963
    '<div class="cl-search-result cl-search-view-mode-gallery" data-pid="7960809963" title="J 24 Sailboat"><div class="gallery-card"><a class="cl-app-anchor cl-search-anchor text-only posting-title" href="https://www.craigslist.org/view/d/burson-24-sailboat/1kyTQJqoghFi8i9t6HUNCq" tabindex="0"><span class="label">J 24 Sailboat</span></a><div class="meta-line"><div class="meta"><span class="result-posted-date">10/21</span><span class="separator"></span><span class="result-location">Valley Springs</span></div></div><span class="priceinfo">$4,000</span></div></div>'
)
SF_J24_2500 = (  # dev sfbay-boo-sailboat pid 7948823002
    '<div class="cl-search-result cl-search-view-mode-gallery" data-pid="7948823002" title="J 24 Sailboat"><div class="gallery-card"><a class="cl-app-anchor cl-search-anchor text-only posting-title" href="https://www.craigslist.org/view/d/burson-24-sailboat/jBubEMSeAr77kkE2L3yS5m" tabindex="0"><span class="label">J 24 Sailboat</span></a><div class="meta-line"><div class="meta"><span class="result-posted-date">10/20</span><span class="separator"></span><span class="result-location">Valley Springs</span></div></div><span class="priceinfo">$2,500</span></div></div>'
)


def parse(*items):
    html = '<html><body><div class="cl-search-results">' + "".join(items) + "</div></body></html>"
    return asyncio.run(CraigslistScraper()._parse_search_results(html, "sfbay"))


def test_distinct_postings_same_title_are_kept():
    listings = parse(SF_VANE_100, SF_VANE_75)  # $100 and $75, same title, place and time
    assert len(_dedup_listings(listings)) == 2


def test_same_title_same_clean_location_kept():
    a, b = parse(SF_J24_4000, SF_J24_2500)
    a.location = b.location = "Valley Springs"  # what the location fix produces for both
    assert [l.price for l in _dedup_listings([a, b])] == ["$4,000", "$2,500"]


def test_same_posting_twice_is_one():
    a, b = parse(SF_J24_4000, SF_J24_4000)
    assert len(_dedup_listings([a, b])) == 1
