# CraigSail — Agent Improvement Log

## 2026-06-30T15:10:50.800601 — Multi-City Search Endpoint  [kept-unmerged] (dbb9777)
- why useful: Allows users to search Craigslist across several cities in a single request, eliminating the need to repeat searches manually and making it far easier to compare prices and listings regionally.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-06-30T15:28:00.673595 — Deduplicate Craigslist Search Results  [kept-unmerged] (58d9585)
- why useful: Removes duplicate listings that appear across multiple searches, saving users time and preventing confusion when reviewing results.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-06-30T15:43:52.990405 — Auto-deduplicate search results  [MERGED] (49f1356)
- why useful: Removes duplicate Craigslist postings that appear across multiple searches, giving users a cleaner, faster overview and preventing confusion when reviewing results.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-06-30T16:05:59.755141 — Add /api/price-stats endpoint to provide average price and listing count for a search query  [kept-unmerged] (63b8c1c)
- why useful: Users can instantly see the typical market price for a product in a city, enabling faster buying/selling decisions and better benchmarking without manually scanning dozens of listings.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-06-30T16:48:56.304685 — Add /api/price-stats endpoint to return average price and listing count  [kept-unmerged] (375f386)
- why useful: Provides users with an immediate market snapshot—average price and how many items match a query—so they can decide quickly whether to buy, sell, or negotiate without manually scanning dozens of listings.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

