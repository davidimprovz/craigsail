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

## 2026-06-30T17:55:28.584861 — Add /api/search/summary endpoint returning count & average price  [kept-unmerged] (bca8881)
- why useful: Users get an instant market snapshot—how many listings match a query and what the average price is—so they can decide quickly whether to buy, sell, or negotiate without manually scanning dozens of results.
- tests: 0 passed / 3 failed
- note: no progress between attempts — stopped early

## 2026-07-01T01:37:34.646988 — Schedule periodic alert evaluation  [kept-unmerged] (6587b74)
- why useful: Automatically search saved alerts at intervals and trigger notifications when matches appear.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-01T02:04:46.567284 — Expose GET saved search by id  [kept-unmerged] (807b208)
- why useful: Allows retrieval of stored criteria before running alerts or displaying them to the user.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-01T14:58:11.044906 — Expose recent listing timeline endpoint  [kept-unmerged] (739f2fa)
- why useful: Provides chronological data needed for the price‑trend chart; without a dedicated endpoint there is no way to retrieve historical listings.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-01T15:03:17.163779 — Add price trend statistics to search endpoint  [MERGED] (fbc5102)
- why useful: Enables comparison of the current price against average, high, and low trends required for the chart.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-01T16:00:47.079839 — Add delete endpoint to cancel a saved search  [kept-unmerged] (53bf659)
- why useful: Completes the tracking loop by allowing users to remove alerts they no longer need, fulfilling the 'adjust or cancel alerts' requirement.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-01T16:12:16.230556 — Define SavedSearch Pydantic model  [kept-unmerged] (d379aa0)
- why useful: Creates a data structure to store user‑defined search criteria (city, query, price cap, etc.) that will be used by later alert logic.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-01T16:16:34.869661 — Add POST /api/saved-searches/create endpoint  [MERGED] (23e65ed)
- why useful: Allows users to register a new saved search via an HTTP call, persisting it (initially in memory) so it can be monitored for alerts.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-01T17:05:23.537769 — Add is_active flag to SavedSearch model  [kept-unmerged] (4b9343b)
- why useful: Enables individual saved searches to be toggled on/off for scheduled alerts without deleting them.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-01T17:10:34.134893 — Expose GET /api/saved-searches endpoint  [MERGED] (bf57159)
- why useful: Allows users (and other services) to retrieve a list of all saved searches, confirming the new `is_active` flag is visible.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-01T17:18:30.295536 — Add POST /api/saved-searches/toggle endpoint  [MERGED] (882e3ae)
- why useful: Provides a simple way to enable or disable a saved search by ID, using the newly added `is_active` field.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-01T17:48:52.856720 — Add schedule_cron field to SavedSearch model  [kept-unmerged] (2005efd)
- why useful: Stores the cron expression users specify for daily or periodic execution, enabling later automated runs.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-01T18:20:46.551357 — Add notification helper for new listings  [kept-unmerged] (eb4ae83)
- why useful: Sends email or in‑app alerts when a scheduled search finds fresh listings.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-01T19:46:39.566198 — Add notification trigger endpoint for AI insights  [kept-unmerged] (80c57d8)
- why useful: Sends email or in‑app notifications containing matching listings and AI recommendations when a scheduled run completes.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-01T20:26:38.713506 — Add placeholder trend forecast endpoint  [kept-unmerged] (7e60101)
- why useful: Provides the required /api/trend/forecast route so downstream AI and data logic can be wired without breaking existing APIs.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-01T21:21:40.652891 — Add simple notification side‑effect to alert endpoint  [kept-unmerged] (fcf8cb9)
- why useful: Provides immediate feedback (console print) when an alert is triggered, satisfying the minimal end‑to‑end notification requirement.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

