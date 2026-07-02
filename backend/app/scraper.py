from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from typing import Optional
from app.models import Listing
from app.parser import parser
import asyncio
import re

class CraigslistScraper:
    @staticmethod
    def _parse_price(price_str: str) -> Optional[int]:
        """Convert price strings like '$1,200' to an integer."""
        if not price_str or price_str == "N/A":
            return None
        # Remove $ and commas, then convert to int
        cleaned = re.sub(r'[,$]', '', price_str)
        try:
            return int(cleaned)
        except ValueError:
            return None

    async def search(self, city: str, query: str, category: str = "sss", max_price: Optional[float] = None):
        """
        Searches Craigslist using Playwright to handle dynamic content.
        Filters results by max_price if provided.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Construct URL (basic version, can be enhanced)
            url = f"https://{city}.craigslist.org/search/{category}?query={query}"
            print(f"Navigating to: {url}")
            
            await page.goto(url)
            # Wait for results to load
            try:
                await page.wait_for_selector(".cl-search-result, .result-row", timeout=5000)
            except:
                print("Timeout waiting for selector, attempting to parse anyway.")
                
            content = await page.content()
            await browser.close()
            
            results = await self._parse_search_results(content, city)
            
            # Filter by max_price if provided
            if max_price is not None:
                filtered_results = []
                for listing in results:
                    parsed_price = self._parse_price(listing.price)
                    if parsed_price is not None and parsed_price <= max_price:
                        filtered_results.append(listing)
                print(f"Filtered by max_price={max_price}: {len(filtered_results)} of {len(results)} listings")
                results = filtered_results
            
            return results

    async def _parse_search_results(self, html: str, city: str):
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # Try new gallery view first
        items = soup.select(".cl-search-result")
        if not items:
            items = soup.select(".result-row")
            
        for item in items[:200]: # Limit for now, increased from 20
            try:
                title_el = item.select_one(".titlestring") or item.select_one(".posting-title")
                if not title_el: continue
                title = title_el.text.strip()
                
                link_el = item.select_one("a.main") or item.select_one("a.result-title") or item.find('a')
                url = link_el['href'] if link_el else ""
                
                price_el = item.select_one(".priceinfo") or item.select_one(".result-price")
                price = price_el.text.strip() if price_el else "N/A"
                
                meta_el = item.select_one(".meta") or item.select_one(".result-meta")
                raw_location = ""
                raw_date = ""
                
                if meta_el:
                    meta_text = meta_el.text.strip()
                    parts = meta_text.split('·')
                    if len(parts) > 1:
                         raw_location = parts[-1].strip()
                         raw_date = parts[0].strip()
                    else:
                         raw_location = meta_text

                    # Try to get specific date element
                    date_span = meta_el.select_one("span[title]") 
                    if date_span:
                        raw_date = date_span['title'] # Use full date string if available
                
                # PARSE WITH OLLAMA - DISABLED FOR V5 (LAZY PARSING)
                # parsed_data = await parser.parse_listing_fragment(raw_location, raw_date)
                
                results.append(Listing(
                    title=title,
                    price=price,
                    location=raw_location, # Use raw location initially
                    raw_location=raw_location,
                    url=url,
                    date_posted=raw_date, # Use raw date initially
                    date_updated=None
                ))
            except Exception as e:
                print(f"Error parsing item: {e}")
                continue
                
        return results

    async def get_details(self, url: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            content = await page.content()
            await browser.close()
            
            soup = BeautifulSoup(content, 'html.parser')
            body = soup.select_one("#postingbody")
            text = body.get_text(strip=True) if body else "No content found"
            text = text.replace("QR Code Link to This Post", "")
            
            # Extract Images (High Res)
            images = []
            thumbs = soup.select("a.thumb")
            for thumb in thumbs:
                if 'href' in thumb.attrs:
                    images.append(thumb['href'])
            
            # Fallback for lazy loaded or single images
            if not images:
                imgs = soup.select(".swipe-wrap img")
                images = [img['src'] for img in imgs if 'src' in img.attrs]

            # Extract Updated Date
            date_updated = None
            # Look for "updated: <time>"
            posting_infos = soup.select(".postinginfo.reveal")
            for info in posting_infos:
                if "updated:" in info.text.lower():
                    time_el = info.select_one("time")
                    if time_el:
                        date_updated = time_el.text.strip()

            return {
                "description": text,
                "images": images,
                "date_updated": date_updated
            }
