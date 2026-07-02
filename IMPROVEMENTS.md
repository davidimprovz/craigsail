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

## 2026-07-01T21:59:57.000076 — Repair the failing pytest suite so it runs green  [kept-unmerged] (b792de8)
- why useful: a green suite turns the tests gate into a real regression signal for every future merge
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-01T22:06:26.933038 — Add Forecast field to Listing model  [MERGED] (b9c2925)
- why useful: Stores AI-generated price forecasts alongside each listing so downstream logic can reference them without extra DB migrations.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-01T22:12:45.329835 — Add generate_forecast utility function  [MERGED] (6c36da0)
- why useful: Provides a deterministic way to compute a price‑trend forecast from a collection of listings, enabling the new endpoint to return meaningful predictions.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-01T22:22:09.587854 — Add /api/forecast endpoint  [kept-unmerged] (85a4d21)
- why useful: Exposes the forecast capability to the frontend, allowing interactive price‑trend charts and alert triggers to be built on top of real API data.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-01T22:38:04.110179 — Add priority_score field to Listing model  [MERGED] (1aa40fb)
- why useful: Provides a place to store the ranking value that will be used to prioritize recommended listings.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-01T22:44:08.210340 — Add prioritize_listings function to rank listings by priority_score  [MERGED] (2092299)
- why useful: Creates a sorted list of listings that can be exposed as recommended items.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-01T22:52:21.087687 — Repair the failing pytest suite so it runs green  [kept-unmerged] (8ba4f82)
- why useful: a green suite turns the tests gate into a real regression signal for every future merge
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-01T22:59:03.710208 — Add price alert thresholds to SavedSearch model  [MERGED] (6de1e9c)
- why useful: Stores user-defined min/max price limits that later alerts will evaluate against current listings.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-01T23:11:42.840604 — Repair the failing pytest suite so it runs green  [kept-unmerged] (d899fa3)
- why useful: a green suite turns the tests gate into a real regression signal for every future merge
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-01T23:22:16.046862 — Add SavedSearch query parameters to DB model  [kept-unmerged] (289b322)
- why useful: Stores the search criteria (city, query, category, max_price) so they can be reused for alerts and trend analysis.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-01T23:29:37.004167 — Expose POST /api/saved-searches endpoint to persist saved search  [MERGED] (f3e8ee8)
- why useful: Allows a user to create and store a SmartSearchTemplate with its parameters.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-01T23:39:43.724724 — Schedule daily execution of saved search checks  [kept-unmerged] (231f257)
- why useful: Runs the scraper on each saved search every day and triggers notifications when matches appear.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-01T23:48:01.111140 — Add endpoint to fetch aggregated price trend and priority score  [kept-unmerged] (698efdf)
- why useful: Provides the dashboard with predicted low/high prices and a recommendation based on recent listings.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T00:06:02.614965 — Add RecommendationResult model  [MERGED] (dcf9947)
- why useful: Provides a typed schema for the price recommendation output that the API and frontend will use.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-02T00:13:31.223945 — Create recommendation router with stub endpoint  [kept-unmerged] (e876408)
- why useful: Introduces the /recommendation route so that later code can be wired to it without further file changes.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T00:19:45.805844 — Implement recommendation logic in CraigAgent  [kept-unmerged] (7731e84)
- why useful: Provides the actual AI‑driven price range and reasoning that the endpoint will return.
- tests: 0 passed / 5 failed
- note: tool-gates failed

## 2026-07-02T00:28:16.936484 — Add UI button and display recommendation  [kept-unmerged] (6835dde)
- why useful: Completes the user flow by letting a user click “Get Recommendation” on a listing grid and see the AI‑generated price range.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T00:42:44.233248 — Add SavedSearch creation schema and endpoint  [kept-unmerged] (8ac64ce)
- why useful: Enables users to store multi‑city query parameters as a reusable saved search.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T00:54:37.668373 — Expose endpoint to run a saved search and return listings  [kept-unmerged] (0322bd9)
- why useful: Allows one‑click retrieval of fresh results based on previously stored criteria.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T01:06:30.136912 — Add toggle active flag and endpoint to enable/disable saved searches  [kept-unmerged] (88944b7)
- why useful: Lets users pause or resume alerts without deleting the saved search configuration.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T01:16:28.305444 — Expose saved-searches list via /api/dashboard/saved-searches  [kept-unmerged] (892695a)
- why useful: Provides the data source for the dashboard to render a list of all saved searches, enabling the UI to display them in a single view.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T01:24:50.169674 — Add parameter update endpoint for saved searches  [kept-unmerged] (b11bfb9)
- why useful: Allows the dashboard to modify query parameters (e.g., max_price, category) of an existing saved search without creating a new one.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T01:41:36.928521 — Expose price‑trend data for a saved search  [kept-unmerged] (04b6a0d)
- why useful: The dashboard needs trend information to draw price‑trend graphs for each saved search.
- tests: 22 passed / 4 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T01:51:31.278283 — Trigger AI analysis for a saved search via one‑click endpoint  [kept-unmerged] (98dd259)
- why useful: Enables the dashboard’s “Analyze” button to launch an AI‑driven price forecast and recommendation with a single request.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T02:01:51.357765 — Add target_price field to SavedSearch model  [MERGED] (f17f6c6)
- why useful: Stores the user-defined price threshold that triggers alerts when a listing’s price drops below it.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-02T02:13:14.528978 — Expose scheduled-run endpoint for saved searches  [kept-unmerged] (b76acaf)
- why useful: Allows the system to trigger a saved search automatically at 9 AM daily and process newly found listings.
- tests: 0 passed / 5 failed
- note: critic=FAIL

## 2026-07-02T02:23:40.946500 — Implement price-drop alert logic  [kept-unmerged] (8cbc4bf)
- why useful: When a listing’s price falls below the saved search’s target_price, send an email or push notification to the user.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T02:27:14.105046 — Add price forecast generation for new listings  [kept-unmerged] (0ec0895)
- why useful: Generates AI‑driven low/high price forecasts for each newly discovered listing so they can be displayed on the dashboard.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T02:46:17.931352 — Add GET /api/saved-searches/list endpoint  [kept-unmerged] (5e823c1)
- why useful: Provides the dashboard with a complete inventory of saved searches so it can render the list of queries, their current filters, and activation state.
- tests: 21 passed / 5 failed
- note: tool-gates failed

## 2026-07-02T02:55:49.023894 — Add PATCH /api/saved-searches/{saved_search_id} endpoint  [kept-unmerged] (8ef9bba)
- why useful: Allows the dashboard to modify filter parameters (max_price or category) of an existing saved search without creating a new one, enabling on‑the‑fly adjustments.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T03:05:33.093162 — Add POST /api/saved-searches/{saved_search_id}/toggle-alert endpoint  [kept-unmerged] (97c544a)
- why useful: Enables the dashboard to activate or deactivate price‑alert notifications for a saved search with a single click.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T03:17:23.017212 — Port legacy test file tests/test_bikes.py to the current backend/app layout  [kept-unmerged] (a4c70a9)
- why useful: each ported file adds real regression coverage guarding every future merge
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T03:21:49.136002 — Port legacy test file tests/test_boats.py to the current backend/app layout  [kept-unmerged] (780c9da)
- why useful: each ported file adds real regression coverage guarding every future merge
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T03:28:26.890810 — Port legacy test file tests/test_properties.py to the current backend/app layout  [kept-unmerged] (b753ef1)
- why useful: each ported file adds real regression coverage guarding every future merge
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T03:38:27.784186 — Port legacy test file tests/test_rvs.py to the current backend/app layout  [kept-unmerged] (db11e26)
- why useful: each ported file adds real regression coverage guarding every future merge
- tests: 0 passed / 5 failed
- note: tool-gates failed

## 2026-07-02T03:44:38.798465 — Port legacy test file tests/test_search.py to the current backend/app layout  [kept-unmerged] (ccd8df5)
- why useful: each ported file adds real regression coverage guarding every future merge
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T03:59:12.222310 — Add editable filter parameters (max_price, category) to saved searches  [kept-unmerged] (524016b)
- why useful: Users need to adjust search filters without recreating the saved search, enabling quick parameter tweaks.
- tests: 0 passed / 5 failed
- note: tool-gates failed

## 2026-07-02T04:06:22.151889 — Add alert toggle (enable/disable) for saved searches  [kept-unmerged] (0d8b2a9)
- why useful: Users must be able to turn price‑alert notifications on or off per saved search without deleting the search.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T04:19:39.946765 — Add target_price field to saved searches for price‑alert thresholds  [kept-unmerged] (ce97b34)
- why useful: Users want alerts only when a listing reaches a specific target price, not just any price change.
- tests: 25 passed / 1 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T04:30:24.809501 — Add deactivate flag and toggle endpoint for saved searches  [kept-unmerged] (2dd349e)
- why useful: Users need to temporarily hide or permanently remove a saved search without deleting it, enabling clean UI management.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T04:40:26.356888 — Add reorder endpoint to change saved‑search ordering  [kept-unmerged] (5fad749)
- why useful: Users must rearrange the displayed order of their saved searches (e.g., priority) without recreating them.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T04:54:44.466778 — Add SavedSearchGroup model  [kept-unmerged] (5bcc488)
- why useful: Introduces the Group concept that saved searches can belong to, enabling grouping and bulk operations.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T04:59:02.634084 — Expose POST /api/groups endpoint  [kept-unmerged] (030a24e)
- why useful: Allows the frontend or API client to create a new group, which is the first functional step for grouping saved searches.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T05:04:08.850210 — Expose GET /api/groups endpoint  [kept-unmerged] (3353124)
- why useful: Provides a way to list existing groups, which is required before any bulk actions or alerts can be shown on the dashboard.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T05:13:05.306590 — Expose DELETE /api/groups/{group_id} endpoint  [kept-unmerged] (e4b33cf)
- why useful: Enables bulk disabling of a group (e.g., to pause alerts or hide its listings) as part of the required group‑wide actions.
- tests: 0 passed / 5 failed
- note: tool-gates failed

## 2026-07-02T05:27:25.558217 — Add Group model  [MERGED] (f145986)
- why useful: Provides the data structure needed to represent a saved-search group and store its alert status.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-02T05:30:49.032921 — Expose Group to SQLAlchemy metadata  [MERGED] (5dcc5bf)
- why useful: Ensures the ORM can create the groups table on first run.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-02T05:39:03.043833 — Add POST /api/groups endpoint (create group)  [kept-unmerged] (e03e3e3)
- why useful: Allows a user to create a new saved-search group via the API.
- tests: 0 passed / 5 failed
- note: tool-gates failed

## 2026-07-02T05:44:33.259529 — Add PATCH /api/groups/{group_id} endpoint (toggle alert)  [kept-unmerged] (7872ce8)
- why useful: Enables toggling the alert_enabled flag of an existing group, fulfilling the EPIC’s toggle requirement.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T05:54:00.946577 — Add DELETE /api/groups/{group_id} endpoint (delete group)  [kept-unmerged] (cc420cb)
- why useful: Allows removal of a saved-search group, completing the CRUD surface described in the EPIC.
- tests: 0 passed / 5 failed
- note: tool-gates failed

## 2026-07-02T06:06:12.694827 — Add a new API route for pricing advice  [kept-unmerged] (fc12870)
- why useful: Creates the public endpoint that will eventually return ranked items with price, time and alert recommendations. This is the smallest unit of work that introduces the required URL without any logic yet.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T06:09:33.623765 — Define the response model for pricing advice  [MERGED] (33febe9)
- why useful: Introduces a concrete Pydantic schema that later will carry recommended_price, optimal_posting_time and alert_trigger fields. This makes downstream code type‑safe and testable.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-02T06:14:23.543208 — Add advice generation method to the CraigAgent  [MERGED] (055f752)
- why useful: Provides the first piece of actual logic that turns a raw listing into a `PricingAdvice` object. Keeping it isolated allows independent testing.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-02T06:20:02.058258 — Implement the endpoint logic using the new advice method  [kept-unmerged] (da8bca0)
- why useful: Connects everything: fetches saved search results, calls `CraigAgent.generate_advice` for each listing and returns a list of `PricingAdvice` objects. This completes the minimal end‑to‑end feature.
- tests: 0 passed / 5 failed
- note: tool-gates failed

## 2026-07-02T06:29:43.160091 — Add ordering support (position field) to SavedSearch  [kept-unmerged] (48a7eaf)
- why useful: Drag‑and‑drop reordering of saved search groups requires a stable position column; this endpoint provides the backend contract for UI to send new positions and persist them.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T06:38:44.199264 — Add bulk toggle‑alert endpoint  [kept-unmerged] (7e73088)
- why useful: Users need to enable/disable multiple alerts at once; a dedicated POST route that accepts a list of alert IDs and a target state fulfills this single concern.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T06:50:49.261561 — Add one‑click delete endpoint for saved searches  [MERGED] (714e069)
- why useful: A single DELETE call removes a saved search (or its group) from the dashboard, completing the minimal CRUD operation needed for bulk management.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-02T07:02:10.596048 — Expose listing priority score in search response  [kept-unmerged] (6a6a750)
- why useful: Provides a ranked value needed for bulk alert prioritization and later AI script generation.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T07:10:21.475504 — Bulk priority & negotiation script API  [kept-unmerged] (a7594cb)
- why useful: Implements the core user-facing endpoint that returns ranked alerts together with AI‑generated negotiation scripts.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T07:17:15.438267 — Add dynamic alert threshold field  [kept-unmerged] (5a80ecc)
- why useful: Allows users to set rule‑based activation limits that later steps will respect when enabling or disabling alerts.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T07:26:06.992681 — Auto‑disable alerts when purchase occurs  [kept-unmerged] (9d6e719)
- why useful: Closes the loop of the workflow by automatically turning off an alert once its associated item is purchased.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T07:39:51.132597 — Add aggregates report endpoint  [kept-unmerged] (aab0c50)
- why useful: Provides a dedicated API to return aggregated listing counts and average prices per category and city, which is the foundation for any further reporting (CSV, forecast, alerts).
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T07:49:40.750451 — Add CSV streaming endpoint  [kept-unmerged] (137b6d3)
- why useful: Enables the UI to download a CSV report with one click; the endpoint will stream generated CSV data derived from the aggregates endpoint.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T08:01:38.171342 — Add forecast aggregation endpoint  [kept-unmerged] (1cb4be3)
- why useful: Supplies the AI‑generated price forecasts per category and city that the final report will visualize; this endpoint will be reused by later reporting features.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T08:09:35.895087 — Add combined download endpoint (single‑click UI trigger)  [MERGED] (b921bac)
- why useful: Provides the final API surface that the UI will call to obtain a full report; this endpoint ties together aggregates, CSV, and forecast data into one request.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-02T08:20:47.327087 — Add alert evaluation endpoint  [kept-unmerged] (73fc78b)
- why useful: Kicks off the alert pipeline by processing saved searches and creating Alert records, which all downstream features (priority management, advice, export) will act upon.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T08:27:34.559360 — Add priority_score field to Alert model  [MERGED] (83061ac)
- why useful: Allows the system to rank alerts and let users prioritize them, enabling the one‑click UI management described in the EPIC.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-02T08:36:29.992958 — Add AI negotiation advice endpoint for alerts  [kept-unmerged] (1ac632e)
- why useful: Provides the AI‑driven negotiation advice per alert, fulfilling a core requirement of the EPIC and using the existing CraigAgent.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T08:45:46.962916 — Add CSV export endpoint for all alerts  [kept-unmerged] (fb794af)
- why useful: Completes the one‑click UI management by letting users download every alert in a machine‑readable format, enabling easy reporting and further processing.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T08:54:00.917377 — Add analysis router and stub endpoint  [kept-unmerged] (c82d98e)
- why useful: Creates a concrete URL that the UI button can call and registers a place for later logic.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T09:04:36.397192 — Add service function to fetch saved search listings  [kept-unmerged] (71be6c4)
- why useful: Isolates DB access so the endpoint can retrieve the correct saved search without coupling to router logic.
- tests: 0 passed / 5 failed
- note: critic=FAIL

## 2026-07-02T09:10:17.376386 — Implement analysis logic in CraigAgent  [MERGED] (8a932ff)
- why useful: Provides the AI aggregation that produces price ranges and recommended actions.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-02T09:17:53.853346 — Wire endpoint to return aggregated report  [kept-unmerged] (6535126)
- why useful: Connects the new service method to the previously created route and returns JSON that matches the EPIC spec.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T09:29:18.004458 — Add ExportItem model  [MERGED] (2e11eb2)
- why useful: Defines the exact shape of data to be exported so downstream code can type-check and serialize correctly.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-02T09:34:26.980218 — Add export data builder function  [MERGED] (641327a)
- why useful: Creates a reusable function that fetches all alerts, their forecasts and listings from the DB and returns a list of dictionaries matching ExportItem.
- tests: 0 passed / 5 failed
- note: gates+critic passed

## 2026-07-02T09:43:25.410836 — Add /api/report/export endpoint  [kept-unmerged] (fd5e1eb)
- why useful: Exposes a downloadable CSV stream that clients can call to get every active alert with its forecast, priority score and listing details.
- tests: 0 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T09:59:32.166998 — Add DealRadar enabled flag to SavedSearch model  [kept-unmerged] (98bb3b2)
- why useful: Marks which saved searches should be processed by the radar system.
- tests: 0 passed / 5 failed
- note: critic=FAIL

## 2026-07-02T10:09:10.548501 — Add POST endpoint to enable DealRadar for a saved search  [kept-unmerged] (afc96ae)
- why useful: Allows the UI or API client to turn radar on for a specific saved search.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T10:15:27.870256 — Add GET endpoint to return DealRadar top listings with forecasts  [kept-unmerged] (7fbab00)
- why useful: Provides the ranked list of best deals together with price forecasts and recommended actions.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T10:20:32.289195 — Add POST endpoint to generate AI negotiation message for a listing  [kept-unmerged] (01a5acb)
- why useful: Optionally returns an AI‑crafted negotiation message when a listing matches radar criteria.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T10:35:07.045917 — Add group_id field to SavedSearch model  [kept-unmerged] (df54356)
- why useful: Introduces the concept of grouping saved searches so later endpoints can associate listings with a specific group.
- tests: 0 passed / 5 failed
- note: critic=FAIL

## 2026-07-02T10:42:27.577389 — Create POST /api/saved-searches/{ss_id}/assign-group endpoint  [kept-unmerged] (d4fa88e)
- why useful: Allows the UI to associate an existing saved search with a newly created group by setting its `group_id`.
- tests: 0 passed / 5 failed
- note: tool-gates failed

## 2026-07-02T10:51:47.356848 — Add GET /api/groups/{group_id}/listings endpoint  [kept-unmerged] (139c9ec)
- why useful: Returns a consolidated list of top listings with AI price forecasts for all saved searches that belong to the specified group – the core of the dashboard view.
- tests: 0 passed / 5 failed
- note: tool-gates failed

## 2026-07-02T10:55:54.887178 — Add PUT /api/groups/{group_id}/toggle-radar endpoint  [kept-unmerged] (728f246)
- why useful: Enables the one‑click radar toggle per group, persisting the setting so the dashboard can respect it when consolidating listings.
- tests: 0 passed / 5 failed
- note: no progress between attempts — stopped early

## 2026-07-02T11:12:10.904606 — Add forecast toggle flag to SavedSearch model  [kept-unmerged] (555c297)
- why useful: Allows saved searches to be selected for automated price‑forecast alerts.
- tests: 0 passed / 5 failed
- note: critic=FAIL

## 2026-07-02T11:16:47.012484 — Implement endpoint that returns AI‑generated price forecast for a saved search  [kept-unmerged] (30ae303)
- why useful: Provides the core predictive data (low/high range and recommendation) needed by the alert system.
- tests: 0 passed / 5 failed
- note: time budget hit mid-subtask

## 2026-07-02T12:07:00.601179 — Add schedule flag to SavedSearch model  [MERGED] (a4a1b2e)
- why useful: Introduces a persistent boolean field that marks a saved search as scheduled for alerts, enabling the system to remember user preferences across server restarts.
- tests: 28 passed / 0 failed
- note: gates+critic passed

## 2026-07-02T12:15:50.008439 — Expose endpoint to enable scheduling for a saved search  [kept-unmerged] (72add4c)
- why useful: Provides a user-facing API to turn on scheduling for any saved search, setting the new `is_scheduled` flag and persisting it.
- tests: 28 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T12:28:43.774788 — Add startup scheduler that runs alerts for scheduled saved searches  [kept-unmerged] (ab4b7bd)
- why useful: Automatically checks and triggers alerts for all saved searches marked as scheduled, ensuring users receive timely notifications without manual intervention.
- tests: 29 passed / 2 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T12:37:17.618963 — Add pytest test confirming scheduling persistence  [kept-unmerged] (fdf0f94)
- why useful: Guarantees that the new scheduling flow works end‑to‑end and adds a fresh passing test to the suite, satisfying the merge requirement.
- tests: 0 passed / 6 failed
- note: tool-gates failed

## 2026-07-02T13:09:45.897822 — Add standardized price integer field to Listing model  [kept-unmerged] (04daa23)
- why useful: Enables downstream cleaning and analytics to work with a numeric price representation instead of raw string, which is required for accurate price history and alerts.
- tests: 29 passed / 0 failed
- note: critic=FAIL

## 2026-07-02T13:19:08.055958 — Expose /api/search/clean endpoint that returns standardized listing data  [kept-unmerged] (6700ec3)
- why useful: Provides a public API for downstream services (alerts, reports) to retrieve clean price and location fields without manual post‑processing.
- tests: 28 passed / 0 failed
- note: tool-gates failed

## 2026-07-02T13:23:10.508258 — Add /api/saved-searches/{ss_id}/run-clean endpoint to trigger cleaning pipeline  [kept-unmerged] (b9f171d)
- why useful: Completes the end‑to‑end flow where a saved search can be automatically cleaned, stored with standardized fields, and made available for alerts and reporting.
- tests: 15 passed / 13 failed
- note: no progress between attempts — stopped early

## 2026-07-02T13:35:02.133520 — Add smoke‑test command verification for all new routes  [kept-unmerged] (743f9aa)
- why useful: Ensures CI will only merge when each subtask has been correctly wired into the application, preventing incomplete merges.
- tests: 28 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T13:56:14.017733 — Add stub comparable endpoint returning empty list  [kept-unmerged] (dfea241)
- why useful: Creates the public API contract early, lets CI pass immediately, and provides a stable hook for later logic.
- tests: 28 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T14:10:14.940083 — Implement comparable retrieval using saved search ID  [kept-unmerged] (2efaaaa)
- why useful: Begins pulling real listings from the database, turning the stub into a functional endpoint that can later be filtered or ranked.
- tests: 28 passed / 0 failed
- note: tool-gates failed

## 2026-07-02T14:19:11.291809 — Add ComparableItem response model with price_deviation field  [kept-unmerged] (7ebe0cd)
- why useful: Introduces the standardized output structure (price, deviation) required for downstream ranking and alerting.
- tests: 28 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T14:31:17.011753 — Add deviation filter parameter and alert trigger logic  [kept-unmerged] (bbb54a4)
- why useful: Enables the engine to automatically flag listings whose price deviates beyond a user‑defined threshold, fulfilling the core comparable‑listings use case.
- tests: 28 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T14:45:23.691600 — Add price_delta field to SavedSearch model  [kept-unmerged] (cc3b964)
- why useful: Enables users to specify a price deviation threshold for saved searches, which is required for alert generation and history tracking.
- tests: 29 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T15:02:31.449022 — Expose /api/alerts/check/{saved_search_id} endpoint  [kept-unmerged] (0fcbbae)
- why useful: Provides a way to evaluate saved searches against their price_delta and optionally create alerts, forming the core alert‑checking functionality.
- tests: 28 passed / 0 failed
- note: tool-gates failed

