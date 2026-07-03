# GOAL — CraigSail

Tool for finding, reporting, and tracking things on Craigslist: multi-city search,
saved searches, alerts, price analytics, and exports — useful to a real person hunting
deals (boats, bikes, RVs, property).

## Done means
- Saved searches persist across restarts and alert scheduling actually executes.
- A user can search N cities at once, export results (CSV), and see price stats.

## Constraints
- Stack: fastapi
- Test command: `python -m pytest -q`
- Write scope: backend
- Never: real scraping in tests (mock the scraper); breaking existing /api routes.

## Hints for the implementor
- Entry point: backend/app/main.py
