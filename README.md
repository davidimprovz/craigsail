# CraigSail.py

**Track craigslist items and use statistical patterns to optimize sales and purchases.**

Have you ever wanted to use Craigslist to:
- search multiple cities at once for the same type of product? 
- track the price of your item and get alerts when the price reaches your buy level?
- benchmark prices for the same or similar products in your area?
- talk to a craigslist expert to find deals or post your items for sale?

Craigsail will let you do all of this with the added benefit of visualizing prices and locations on a map. Use the AI chat bot to interact with Craigslist postings and get AI-recommended buy / sell info. You are in the driver's seat now.

Hooks in to https://github.com/juliomalegria/python-craigslist API with added capabilities.

## Run with Docker (recommended)

```bash
docker compose up -d web          # map UI at http://localhost:5001
docker compose run --rm search \
    --search_category boo --data_path /app/data --cities sfbay seattle
```

Both services share the `craigsail-data` volume, so searches run from the
`search` service show up in the map immediately. Host port is 5001 because
macOS AirPlay Receiver occupies 5000.

## Install

```bash
pip install -e .
```

If you are working against a local clone of the craigslist wrapper, install it
first: `pip install -e ./python-craigslist`.

## Run a search

Cities are craigslist site subdomains (`sfbay`, `seattle`, `newyork`), not
display names. Mistyped cities are rejected before the scrape starts.

```bash
craigsail --search_category boo --data_path data --cities sfbay seattle \
          --filters max_price=25000 --csv
```

Results are upserted into `data/craigsail.db`. Re-running the same search
updates existing listings rather than duplicating them, and records a
`price_history` row whenever a listing's price moves.

## Map the results

```bash
CRAIGSAIL_DB=data/craigsail.db flask --app web_app.app run
```

Then open http://localhost:5000. Markers are colour-coded cheapest (green) to
priciest (red), and the category/city filters rescale the ramp.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

The suite is hermetic - no network access required.

This project is for research and infomrational purposes only.