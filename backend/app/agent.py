from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from typing import List

from app.models import Listing, PricingAdvice


class CraigAgent:
    def __init__(self):
        # Default to OpenAI for now, but structure allows swapping
        # In a real app, we'd load provider from env vars
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
             print("Warning: OPENAI_API_KEY not set. AI features will mock response.")
             self.llm = None
        else:
            self.llm = ChatOpenAI(model="gpt-3.5-turbo")

    async def analyze(self, details: dict, user_query: str):
        if not self.llm:
            return "AI Analysis Unavailable: Please set OPENAI_API_KEY."
            
        description = details.get("description", "No description")
        images = details.get("images", [])
        date_updated = details.get("date_updated", "Not updated")
        
        # Format images for context (list of URLs)
        image_context = "\n".join(images[:5]) # Limit to top 5 to save tokens/make it readable
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a savvy Craigslist expert: specific, cynical, and helpful. You are acting as a broker for the user. Analyze the listing details provided."),
            ("user", """
            Listing Description: {description}
            
            Date Updated: {date_updated}
            
            Image URLs (for context):
            {image_context}
            
            User Question: {user_query}
            
            Provide a concise analysis, a recommendation (Buy/Pass/Risky), and a priority level (High/Med/Low).
            """)
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        response = await chain.invoke({
            "description": description, 
            "date_updated": date_updated, 
            "image_context": image_context, 
            "user_query": user_query
        })
        return response

    async def generate_advice(self, listing: Listing) -> PricingAdvice:
        # Placeholder implementation – will be expanded later.
        return PricingAdvice(
            recommended_price=0.0,
            optimal_posting_time="any",
            alert_trigger=False
        )

    async def analyze_saved_search(self, ss_id: int) -> dict:
        """Aggregate analysis across all listings from a saved search.

        Fetches listings via the scraper for each city in the saved search,
        feeds each listing description into ``self.analyze()``, and returns a
        summary with ``predicted_low``, ``predicted_high``, and
        ``recommendation`` derived from the collected price data.
        """
        from app.scraper import CraigslistScraper

        # Resolve the saved search definition (in-memory store).
        saved = SAVED_SEARCHES.get(ss_id)
        if not saved:
            return {
                "predicted_low": 0,
                "predicted_high": 0,
                "recommendation": f"Saved search '{ss_id}' not found.",
            }

        scraper = CraigslistScraper()
        all_listings: List[Listing] = []

        for city in saved.cities:
            listings = await scraper.search(
                city, saved.query, saved.category or "sss", max_price=saved.max_price
            )
            all_listings.extend(listings)

        # Feed each listing through the AI analyzer.
        analyses: List[str] = []
        for lst in all_listings:
            details = {
                "title": lst.title,
                "price": lst.price,
                "url": lst.url,
                "description": lst.description or "",
                "date_updated": lst.date_updated or "Not updated",
                "images": [],
            }
            analysis = await self.analyze(details, f"Analyze this listing: {lst.title} at ${lst.price}")
            analyses.append(analysis)

        # Aggregate price statistics.
        prices: List[int] = []
        for lst in all_listings:
            parsed = CraigslistScraper._parse_price(lst.price)
            if parsed is not None:
                prices.append(parsed)

        if not prices:
            return {
                "predicted_low": 0,
                "predicted_high": 0,
                "recommendation": "No price data available.",
            }

        predicted_low = min(prices)
        predicted_high = max(prices)
        avg_price = sum(prices) / len(prices)

        # Simple heuristic: if average is below $500 recommend buying.
        if avg_price < 500:
            recommendation = "Buy"
        else:
            recommendation = "Wait"

        return {
            "predicted_low": predicted_low,
            "predicted_high": predicted_high,
            "recommendation": recommendation,
            "listings_analyzed": len(all_listings),
            "analyses": analyses[:10],  # cap for payload size
        }


async def generate_forecast(listings: List) -> dict:
    """Compute a deterministic price-trend forecast from a collection of listings.

    Extracts integer prices from the provided listings, computes min/max/avg, and
    returns a recommendation based on whether the average is below a threshold.
    """
    # Extract numeric prices using the scraper's parser
    prices = []
    from app.scraper import CraigslistScraper

    for listing in listings:
        parsed = CraigslistScraper._parse_price(listing.price)
        if parsed is not None:
            prices.append(parsed)

    if not prices:
        return {
            "predicted_low": 0,
            "predicted_high": 0,
            "recommendation": "No price data available.",
        }

    predicted_low = min(prices)
    predicted_high = max(prices)
    avg_price = sum(prices) / len(prices)

    # Threshold: if average price is below $500, recommend buying now.
    threshold = 500
    if avg_price < threshold:
        recommendation = "Buy"
    else:
        recommendation = "Wait"

    return {
        "predicted_low": predicted_low,
        "predicted_high": predicted_high,
        "recommendation": recommendation,
    }


def prioritize_listings(listings: List) -> List:
    """Return listings sorted by priority_score (or price if not set)."""
    from app.models import Listing

    return sorted(listings, key=lambda l: getattr(l, 'priority_score', float('inf')))
