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

## 2026-07-02T15:19:33.066343 — Add /api/alerts/list endpoint for consolidated alerts  [kept-unmerged] (e06478f)
- why useful: Allows the UI to retrieve a unified list of all active alerts, satisfying the reporting requirement.
- tests: 28 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T15:31:50.384796 — Add PriceHistory model and /api/price-history/{listing_id}/csv endpoint  [kept-unmerged] (34b2c11)
- why useful: Stores historical price recordings for listings, enabling the UI to download a CSV of price history and complete the price‑history tracking loop.
- tests: 0 passed / 5 failed
- note: tool-gates failed

## 2026-07-02T15:51:02.363156 — Add tracked flag to Listing model  [kept-unmerged] (a826696)
- why useful: Introduces a boolean field that can be used to mark listings for later tracking, enabling subsequent tracking features.
- tests: 30 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T16:04:00.743962 — Add endpoint to toggle tracking flag  [kept-unmerged] (55d796c)
- why useful: Provides a public API that callers can use to set `tracked=True` (or False) on a specific listing, making the new field actionable.
- tests: 28 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T16:14:38.781923 — Add pytest test for tracking toggle  [kept-unmerged] (fcb8956)
- why useful: Ensures the newly added endpoint correctly updates the `tracked` field, giving a concrete verification that the feature works end-to-end.
- tests: 28 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T16:25:05.651096 — Add endpoint to report tracked-listing count  [kept-unmerged] (203723c)
- why useful: Lets users query how many listings are currently marked as tracked, enabling a simple reporting metric that builds on the tracking feature.
- tests: 28 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T16:44:45.690422 — Add price deviation threshold field to SavedSearch model  [kept-unmerged] (8cb316b)
- why useful: Stores a user-defined tolerance so the system can later filter listings by how much their price deviates from a saved baseline.
- tests: 27 passed / 2 failed
- note: tool-gates failed

## 2026-07-02T16:54:54.357274 — Expose endpoint to run saved search with deviation filtering  [kept-unmerged] (ab2deba)
- why useful: Runs a saved search and returns only listings that fall within the stored price‑deviation threshold, enabling downstream alert logic.
- tests: 28 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T17:03:17.997398 — Implement notification dispatch for matched alerts  [kept-unmerged] (1936da0)
- why useful: Sends an email or webhook to the user when a listing meets the deviation criteria, fulfilling the alerting requirement.
- tests: 28 passed / 1 failed
- note: tool-gates failed

## 2026-07-02T17:15:40.567918 — Add CSV download of historical price data per tracked listing  [kept-unmerged] (573faba)
- why useful: Provides users with a downloadable CSV containing the full price history for any listed item, completing the reporting requirement.
- tests: 28 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T17:29:42.427877 — Add price_history CSV generator utility  [kept-unmerged] (4456fbe)
- why useful: Provides a reusable function that can produce CSV content for any listing ID, laying the groundwork for the export endpoint.
- tests: 28 passed / 0 failed
- note: tool-gates failed

## 2026-07-02T17:42:13.158975 — Expose CSV export endpoint  [kept-unmerged] (13f87ce)
- why useful: Provides the public API route that callers will hit to download price history as CSV.
- tests: 28 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T17:58:22.372557 — Add validation and 404 handling for missing listing  [kept-unmerged] (5f029bb)
- why useful: Ensures the endpoint only serves valid listing IDs and returns proper HTTP errors, preventing accidental data exposure.
- tests: 28 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T18:06:53.238452 — Add comprehensive pytest for CSV export  [kept-unmerged] (ac2c1e6)
- why useful: Provides a test that guarantees the new functionality works end‑to‑end and will cause CI to reject merges without it.
- tests: 28 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T18:17:49.390771 — Add price_deviation field to Listing model and expose via response  [kept-unmerged] (d7dad45)
- why useful: Introduces a dedicated field that will later be used for deviation calculations, alerts, and CSV exports.
- tests: 28 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T18:30:58.074574 — Expose price_deviation in search endpoint  [kept-unmerged] (05f51e3)
- why useful: Makes the new field available to callers so downstream logic can use it.
- tests: 28 passed / 0 failed
- note: tool-gates failed

## 2026-07-02T18:41:54.678230 — Compute price deviation using saved-search statistics  [MERGED] (e6d2c4e)
- why useful: Provides actual deviation values based on historic averages, enabling meaningful alerts.
- tests: 29 passed / 0 failed
- note: gates+critic passed

## 2026-07-02T18:56:50.782512 — Add deviation‑based alert creation endpoint  [kept-unmerged] (69110d3)
- why useful: Automatically creates alerts when a listing's price deviates beyond a user‑defined threshold.
- tests: 29 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T19:09:19.209100 — Expose deviation alerts via CSV export  [kept-unmerged] (8de7fe0)
- why useful: Completes the EPIC by ensuring exported CSVs contain both price deviation and any related alert messages.
- tests: 29 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-02T19:25:30.700312 — Add PriceObservation model  [kept-unmerged] (5d4268e)
- why useful: Provides a persistent storage structure for individual price observations that will later be exported as CSV.
- tests: 29 passed / 0 failed
- note: tool-gates failed

## 2026-07-02T19:35:37.362320 — Implement price_history_csv function  [kept-unmerged] (9d0fba6)
- why useful: Creates the backend logic that will generate CSV content for a given listing_id, preparing it for exposure via an API endpoint.
- tests: 29 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T19:50:22.670578 — Expose endpoint in main FastAPI app  [kept-unmerged] (efc2ac6)
- why useful: Makes the newly created CSV generator accessible to clients via the required URL pattern.
- tests: 29 passed / 0 failed
- note: tool-gates failed

## 2026-07-02T19:54:27.005679 — Add pytest test for the new endpoint  [kept-unmerged] (7b49549)
- why useful: Guarantees that the endpoint returns a properly formatted CSV response, satisfying the merge requirement of at least one new passing test.
- tests: 29 passed / 0 failed
- note: time budget hit mid-subtask

## 2026-07-02T20:57:36.106881 — Remove stray is_scheduled assignment from SavedSearch model  [MERGED] (1b5fe34)
- why useful: Eliminates the erroneous post‑class attribute that causes false hasattr checks and aligns with Loop_Tuning rule against assigning to classes after definition.
- tests: 29 passed / 0 failed
- note: gates+critic passed

## 2026-07-02T21:11:02.845217 — Replace ImportError fallback and guard division in compute_price_deviation  [kept-unmerged] (737899e)
- why useful: Removes the prohibited try/except ImportError import pattern and adds a safe default for division by zero, ensuring the function behaves predictably.
- tests: 29 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T21:20:35.586472 — Add zero‑average test case for price deviation  [MERGED] (1efcbe1)
- why useful: Ensures the newly guarded behavior is covered by a concrete test that asserts the function returns 0.0 when the average price is zero.
- tests: 30 passed / 0 failed
- note: gates+critic passed

## 2026-07-02T21:26:58.351183 — Rewrite saved search scheduled tests to assert behavior directly  [kept-unmerged] (2b6db4d)
- why useful: Replaces fragile hasattr/model_fields introspection with explicit assertions about the `is_scheduled` attribute, making the test suite robust and aligned with Loop_Tuning.
- tests: 30 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T21:51:50.963632 — Add is_scheduled flag to SavedSearch model  [kept-unmerged] (4cf6579)
- why useful: The scheduler needs a boolean column to identify which saved searches should be executed. Adding the field establishes the persistence primitive required for phase‑2 scheduling.
- tests: 30 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T22:00:10.967359 — Implement scheduler module with scheduling pass function  [kept-unmerged] (1b6e142)
- why useful: Provides the core logic that finds scheduled saved searches, executes their scraper, and records alert hits. This single‑function module will be reused by the endpoint.
- tests: 30 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T22:13:33.747958 — Add POST endpoint to trigger a single scheduling pass  [kept-unmerged] (2ad5055)
- why useful: Exposes a testable, on‑demand entry point that runs the scheduler without background threads. This makes the whole flow verifiable in unit tests.
- tests: 30 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T22:29:37.059361 — Add scam risk calculation function  [kept-unmerged] (c9adc7e)
- why useful: Provides the core heuristic that will be used to score listings.
- tests: 30 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T22:43:03.369732 — Add scam_risk_score field and annotation helper  [kept-unmerged] (f4ac5c9)
- why useful: Stores the computed risk score on each Listing instance.
- tests: 30 passed / 0 failed
- note: no progress between attempts — stopped early

## 2026-07-02T22:47:19.172909 — Expose risk-score endpoint  [kept-unmerged] (f226c48)
- why useful: Allows clients to query the scam risk of a specific listing.
- tests: 30 passed / 1 failed
- note: time budget hit mid-subtask

## 2026-07-02T23:03:19.545893 — Add scheduler.select_scheduled function  [kept-unmerged] (3e392a6)
- why useful: Provides the backend logic to retrieve saved searches marked for recurring execution, enabling later scheduling pass.
- tests: 30 passed / 1 failed
- note: tool-gates failed

## 2026-07-02T23:26:54.958191 — Add missing imports to reports.py  [MERGED] (d2d4110)
- why useful: Ensures that the existing export functionality can import ExportItem and AlertORM, allowing build_export_records to run without ImportError.
- tests: 30 passed / 0 failed
- note: gates+critic passed

## 2026-07-02T23:30:14.467508 — Fix import path in test_deviation_calculation.py  [MERGED] (7fdc888)
- why useful: Aligns test imports with the application's package layout, preventing ImportError when running tests.
- tests: 30 passed / 0 failed
- note: gates+critic passed

## 2026-07-02T23:34:54.050763 — Replace third test body in test_saved_search_scheduled.py  [MERGED] (e494b03)
- why useful: Ensures the scheduled saved search test validates behavior directly without introspecting model_fields, matching the required assertion pattern.
- tests: 30 passed / 0 failed
- note: gates+critic passed

## 2026-07-02T23:58:39.527187 — Add select_scheduled pure function  [kept-unmerged] (8c77456)
- why useful: Identifies all saved searches flagged for recurring execution so they can be processed by the scheduler.
- tests: 30 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T00:11:33.624514 — Add run_scheduling_pass execution function  [kept-unmerged] (7270557)
- why useful: Performs the actual work of running each scheduled search via a scraper and reports hit counts.
- tests: 30 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T00:24:24.931403 — Expose POST /api/scheduler/run-once endpoint  [kept-unmerged] (b4ff391)
- why useful: Provides a public API for triggering the scheduling pass from external tools or UI, completing the end‑to‑end flow.
- tests: 30 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T00:37:40.024551 — Add pure risk_score function  [kept-unmerged] (674bba5)
- why useful: Provides the core heuristic to compute scam risk for a listing using only local listing data.
- tests: 30 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T00:48:29.142457 — Add risk_score field to Listing model  [kept-unmerged] (5d9996a)
- why useful: Allows each listing returned by the API to carry its computed risk score.
- tests: 30 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T00:58:51.185782 — Attach risk_score to search response  [kept-unmerged] (4d9aa92)
- why useful: Integrates the computed risk score into every listing returned by the search endpoint.
- tests: 30 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T01:16:22.064518 — Add compute_price_deviation utility function  [MERGED] (60ae6dc)
- why useful: Provides the calculation needed for the price deviation column that will be added to export records, enabling later report enrichment.
- tests: 31 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T01:23:10.689557 — Integrate price_deviation into build_export_records  [MERGED] (94e39a0)
- why useful: Ensures export records generated by the system include the new price_deviation column, making them usable for the deal report.
- tests: 34 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T01:37:14.221506 — Expose deal report endpoint  [kept-unmerged] (b37f729)
- why useful: Provides the HTTP GET `/api/reports/deals` route that streams a CSV of export records enriched with price_deviation, fulfilling the EPIC outcome.
- tests: 34 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T01:52:34.139790 — Add integration test for seeded DB  [kept-unmerged] (224b5b8)
- why useful: Validates the full flow: a saved search with alerts is transformed into export records containing price_deviation and returned by the new endpoint, ensuring end‑to‑end correctness.
- tests: 34 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T02:07:12.484027 — Add next_run_at field to SavedSearch model  [kept-unmerged] (91675f9)
- why useful: Stores the scheduled execution time for alerts so the batch scheduler can know when to trigger notifications.
- tests: 34 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T02:18:26.180456 — Add endpoint to schedule alerts for a saved search  [kept-unmerged] (cc5db7e)
- why useful: Allows users to set a future time for an alert, enabling the batch scheduler to automatically send notifications.
- tests: 34 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T02:27:50.206678 — Implement background task that executes due alerts  [kept-unmerged] (39ca90b)
- why useful: Runs automatically and sends notifications for saved searches whose scheduled time has arrived, achieving true hands‑free deal hunting.
- tests: 34 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T02:42:23.645697 — Add heatmap aggregation endpoint  [kept-unmerged] (e865f6a)
- why useful: Provides the backend API needed to retrieve aggregated listing counts and price statistics by city, category, and price range – the foundation for the interactive heatmap.
- tests: 34 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T02:55:21.949739 — Add CSV export endpoint for heatmap data  [kept-unmerged] (9a1e026)
- why useful: Allows users to download the aggregated heatmap results as a CSV file, satisfying one part of the export requirement.
- tests: 34 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T03:06:49.532823 — Add hot‑zone alert scheduling endpoint  [kept-unmerged] (c6eb486)
- why useful: Enables users to create alerts automatically when a heatmap zone is deemed 'hot' (e.g., high listing count), fulfilling the final part of the EPIC.
- tests: 34 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T03:21:49.819933 — Add target_price to SavedSearch and expose update endpoint  [kept-unmerged] (7c1e27e)
- why useful: Enables users to set a price threshold for alerts, which is required for the price‑fall‑below alert feature.
- tests: 34 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T03:46:53.553435 — Delete literal-path handler run_saved_search_123  [kept-unmerged] (0dbdd94)
- why useful: Removes a misleading endpoint that no longer exists, preventing user confusion and reducing code bloat.
- tests: 34 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T04:07:27.738901 — Fix forecast_route confidence_scores calculation and add test  [kept-unmerged] (1336c9b)
- why useful: The /api/forecast endpoint crashes with a NameError when more than one price is present; fixing it restores a core analytics endpoint used by downstream price‑stats and export features.
- tests: 34 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T04:20:46.031578 — Delete literal‑path saved-search runner endpoint  [MERGED] (f26e04b)
- why useful: Removes a dead route that misleads users and inflates the codebase.
- tests: 34 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T04:24:37.227090 — Delete stub create‑saved-search endpoint  [MERGED] (9bca577)
- why useful: Eliminates a duplicate route that adds no functional value.
- tests: 34 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T04:29:27.482769 — Delete stub run‑pending-searches endpoint  [kept-unmerged] (22c7d6f)
- why useful: Cleans up an unused route that contributes to dead code.
- tests: 34 passed / 0 failed
- note: time budget hit mid-subtask

## 2026-07-03T04:46:21.285281 — Remove run_pending_searches endpoint  [kept-unmerged] (dbf666b)
- why useful: Deletes a dead-code stub that misleads users and inflates main.py, satisfying the EPIC's first deletion requirement.
- tests: 34 passed / 0 failed
- note: critic=FAIL

## 2026-07-03T04:58:33.497166 — Remove report_download endpoint  [MERGED] (8e87136)
- why useful: Removes the second dead-code stub that provides no functionality and contributes to code bloat.
- tests: 34 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T05:12:11.535565 — Fix forecast_route confidence_scores calculation and add test  [MERGED] (e83fae2)
- why useful: The /api/forecast endpoint crashes with a NameError when more than one price is returned, preventing price analytics from being usable.
- tests: 37 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T05:17:28.411850 — Fix list_saved_searches to return explicit dicts  [MERGED] (8b57e86)
- why useful: The `list_saved_searches` endpoint currently returns SQLAlchemy model objects without converting them to dictionaries, causing serialization errors when clients consume the API.
- tests: 37 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T05:22:05.796588 — Update delete_saved_search signature to accept UUID string IDs  [MERGED] (b17ecb8)
- why useful: Saved search IDs are generated as UUID strings, but the current `delete_saved_search` view expects an integer parameter, leading to 404 errors when trying to delete a saved search.
- tests: 37 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T05:33:42.041715 — Add path parameter to toggle_saved_search route  [kept-unmerged] (f1b54ae)
- why useful: The `toggle_saved_search` endpoint must receive the saved‑search identifier in the URL; currently it declares a Path parameter but no route includes it, causing routing failures.
- tests: 37 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T05:38:22.770192 — Remove self‑import in reports._deviation_for_alert  [MERGED] (ed5ca33)
- why useful: The `_deviation_for_alert` function imports itself via `from app.reports import compute_price_de`, which creates a circular import and prevents price deviation calculations from working.
- tests: 37 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T05:51:08.082391 — Expose run_saved_search endpoint using DB  [kept-unmerged] (8f69c3f)
- why useful: Persist saved searches and allow them to be executed, enabling end‑to‑end saved‑search functionality.
- tests: 37 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T05:58:53.395814 — Modify alerts runner to use DB active saved searches  [kept-unmerged] (59c87c5)
- why useful: Ensures the scheduled alert job iterates over persisted, active saved searches instead of the now‑removed in‑memory list.
- tests: 37 passed / 1 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T06:11:18.989768 — Remove unused global store variables  [kept-unmerged] (100439f)
- why useful: Cleans up dead code and prevents accidental usage of the now‑unused globals.
- tests: 37 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T06:22:54.729001 — Add ListingORM model  [kept-unmerged] (98b6588)
- why useful: Provides durable storage for scraped listings so price history and deviation can be calculated.
- tests: 37 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T06:31:39.474270 — Persist listings on search  [kept-unmerged] (ba81c27)
- why useful: Stores each unique listing in the database so later analytics can use real price data.
- tests: 0 passed / 7 failed
- note: tool-gates failed

## 2026-07-03T06:42:06.468685 — Compute real price deviation for alerts  [kept-unmerged] (ddcd6b3)
- why useful: Replaces the hard-coded 0.0 deviation with a true mean of persisted listings, enabling accurate analytics.
- tests: 37 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T06:51:17.975974 — Add scheduler.select_scheduled function  [MERGED] (cb91fde)
- why useful: Provides a way to retrieve all active saved searches that have a schedule cron set, enabling the later scheduling pass to operate on real data.
- tests: 38 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T06:55:41.108986 — Add async run_scheduling_pass function  [MERGED] (a599e5c)
- why useful: Executes the actual search across selected cities for each saved search, returning hit counts; this is the core logic that will be triggered by the new endpoint.
- tests: 39 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T07:00:50.720376 — Add /api/scheduler/run-once endpoint and test it  [MERGED] (36fcb1a)
- why useful: Exposes the scheduling pass via an HTTP POST, allowing a user to trigger a one‑off execution of all scheduled searches; this completes the end‑to‑end flow.
- tests: 43 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T07:12:05.370502 — Add scam‑heuristic risk_score utility function  [kept-unmerged] (af0da87)
- why useful: Provides a deterministic scam risk score that can be reused across the app.
- tests: 0 passed / 8 failed
- note: tool-gates failed

## 2026-07-03T07:19:09.508776 — Add risk_score field to Listing model  [kept-unmerged] (5a60b6f)
- why useful: Stores the computed scam score on each listing for later retrieval.
- tests: 43 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T07:25:49.747250 — Expose risk_score in search response  [kept-unmerged] (32c69d7)
- why useful: Users can see a scam risk indicator for each result returned by the search endpoint.
- tests: 43 passed / 2 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T07:37:30.858682 — Expose /api/reports/deals endpoint returning JSON export records  [kept-unmerged] (6f87ccf)
- why useful: Makes the report data reachable via HTTP for the first time, enabling downstream CSV streaming and analytics.
- tests: 43 passed / 0 failed
- note: works-but-untested — test-only retry

## 2026-07-03T07:46:19.344717 — Add CSV streaming variant to /api/reports/deals  [kept-unmerged] (5164cc0)
- why useful: Provides the optional ?format=csv endpoint that streams the same export data as CSV, completing the deals‑report epic.
- tests: 43 passed / 1 failed
- note: tool-gates failed

## 2026-07-03T07:54:47.621782 — Add deviation_target field to SavedSearch model  [MERGED] (64c55b0)
- why useful: Persists the user‑defined price deviation threshold that will trigger alerts.
- tests: 44 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T08:01:24.943951 — Expose API to set deviation target on saved search  [kept-unmerged] (30c0dc3)
- why useful: Allows a client (UI or script) to configure the alert threshold for an existing saved search.
- tests: 41 passed / 4 failed
- note: tool-gates failed

## 2026-07-03T08:08:25.180479 — Add deviation‑based alert generation in scheduler  [kept-unmerged] (7daa82a)
- why useful: When the scheduled job runs, it will create an Alert if a listing's price deviates beyond the saved search's threshold.
- tests: 45 passed / 5 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T08:14:26.220670 — Export deviation alerts as CSV  [kept-unmerged] (59e2dd7)
- why useful: Provides a downloadable CSV of all alerts that were generated by the deviation logic for downstream analysis.
- tests: 44 passed / 2 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T08:29:52.483868 — Add benchmark search route skeleton  [MERGED] (4d08efe)
- why useful: Provides a dedicated endpoint for multi‑city price benchmark searches, the entry point for later aggregation and export features.
- tests: 45 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T08:39:18.559229 — Implement price aggregation helper and connect to route  [kept-unmerged] (01a8e8e)
- why useful: Adds real logic to compute per‑city average price and listing count, enabling meaningful benchmark data for the endpoint.
- tests: 45 passed / 1 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T08:59:27.777052 — Add CSV export endpoint for benchmark results  [kept-unmerged] (34ef8a7)
- why useful: Allows users to download the aggregated price statistics as a CSV file, completing one of the core user requirements.
- tests: 45 passed / 1 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T09:11:13.266155 — Add price_max and max_distance fields to SavedSearch model  [kept-unmerged] (9d86395)
- why useful: These filters are the core of multi‑facet saved searches; persisting them allows alerts and exports to respect user-defined price caps and geographic limits across restarts.
- tests: 42 passed / 3 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T09:17:38.252755 — Expose saved search filters via a detail endpoint  [kept-unmerged] (762d44a)
- why useful: Making the stored filter values accessible enables downstream steps (export, alert scheduling) to read the user's price and distance constraints without re‑entering them.
- tests: 42 passed / 5 failed
- note: tool-gates failed

## 2026-07-03T09:23:24.959564 — Export CSV results using stored filters  [kept-unmerged] (4bc07f4)
- why useful: Users can now download a CSV of listings that respect their saved price ceiling and distance radius, fulfilling the export requirement of the EPIC.
- tests: 42 passed / 3 failed
- note: tool-gates failed

## 2026-07-03T09:31:57.540634 — Integrate filter usage into scheduled alert runs  [kept-unmerged] (44dbf5b)
- why useful: Ensures that alerts triggered by saved searches honor the persisted price and distance limits, completing the persistence‑across‑restarts goal.
- tests: 43 passed / 3 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T09:46:52.408367 — Add score fields and scoring method  [kept-unmerged] (da9c565)
- why useful: Introduces the data model needed for numeric scores and rationales, providing the foundation for later scoring and alert logic.
- tests: 43 passed / 3 failed
- note: tool-gates failed

## 2026-07-03T09:54:13.782937 — Expose scored listings via search endpoint  [kept-unmerged] (824332d)
- why useful: Allows users to see the numeric score and rationale alongside each listing in search results.
- tests: 35 passed / 10 failed
- note: tool-gates failed

## 2026-07-03T09:59:01.435247 — Create alerts for high‑score listings  [kept-unmerged] (2da53b4)
- why useful: Enables automatic notifications when a listing reaches a high score, fulfilling the alerting requirement.
- tests: 42 passed / 3 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T10:05:51.172824 — Export search results as CSV with scores  [kept-unmerged] (bc4469a)
- why useful: Allows users to download scored data for offline comparison and analysis.
- tests: 41 passed / 5 failed
- note: tool-gates failed

## 2026-07-03T10:16:51.413774 — Add price trend computation function  [kept-unmerged] (84606ae)
- why useful: Provides the core logic to aggregate listing prices by city over the last 30 days, which is needed for heatmap and deviation calculations.
- tests: 42 passed / 3 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T10:21:30.183449 — Expose price trend endpoint  [kept-unmerged] (2b89b66)
- why useful: Makes the aggregated city‑level price data available via a REST API, enabling downstream features like alerts and CSV export.
- tests: 42 passed / 3 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T10:27:05.556289 — Add deviation score calculation and detailed endpoint  [kept-unmerged] (0b7bc44)
- why useful: Enables per‑listing deviation scores relative to city averages, a prerequisite for alert scheduling and export of trend metrics.
- tests: 42 passed / 3 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T10:32:01.560616 — Add CSV export of price trend metrics  [kept-unmerged] (5a29291)
- why useful: Allows users to download the full dataset—including city averages and deviation scores—as a CSV file for offline analysis.
- tests: 42 passed / 3 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T10:45:42.659757 — Add throttling configuration fields to SavedSearch model  [kept-unmerged] (485c5bf)
- why useful: Stores the timestamp of the last alert and cooldown period so the system can decide when to resend alerts, preventing duplicate or low‑relevance messages.
- tests: 50 passed / 3 failed
- note: tool-gates failed

## 2026-07-03T10:51:54.708911 — Implement throttling check function in scheduler  [kept-unmerged] (aa89ac7)
- why useful: Provides a reusable boolean that determines whether an alert for a saved search should be sent based on the cooldown period.
- tests: 41 passed / 4 failed
- note: tool-gates failed

## 2026-07-03T11:00:28.102096 — Integrate throttling into the alert dispatch endpoint  [kept-unmerged] (a22ed77)
- why useful: Ensures that only alerts meeting the cooldown condition are actually sent, reducing spam.
- tests: 42 passed / 3 failed
- note: tool-gates failed

## 2026-07-03T11:07:42.424141 — Add end‑to‑end integration test for throttling behavior  [kept-unmerged] (761a4e6)
- why useful: Confirms the full flow from scheduler filtering to API response respects the new throttling rules.
- tests: 42 passed / 4 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T11:20:24.180913 — Add geo-filtered search endpoint with city/radius query parameters  [kept-unmerged] (9d728d5)
- why useful: Enables users to filter listings by a specific city or radius, the first step toward location-based filtering and mapping.
- tests: 42 passed / 3 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T11:27:00.712326 — Implement radius filtering using haversine distance  [kept-unmerged] (20c24b0)
- why useful: Adds true radius-based filtering so users can search within a given distance from a city center.
- tests: 0 passed / 9 failed
- note: tool-gates failed

## 2026-07-03T11:32:50.568752 — Add price‑stats endpoint per location  [kept-unmerged] (c57d447)
- why useful: Provides aggregated price trends (average, count, min, max) for a given city, supporting the 'price analytics' part of the EPIC.
- tests: 42 passed / 3 failed
- note: tool-gates failed

## 2026-07-03T11:39:04.891082 — Export geo‑mapped results as CSV stream  [kept-unmerged] (5fcfb4e)
- why useful: Allows users to download mapped results for offline analysis, completing the export capability of the EPIC.
- tests: 42 passed / 3 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T11:48:35.210713 — Implement risk_score calculation function  [kept-unmerged] (5a9ba0f)
- why useful: The endpoint will delegate the actual scoring to a pure function that can be unit‑tested and reused.
- tests: 42 passed / 3 failed
- note: tool-gates failed

## 2026-07-03T11:57:38.527705 — Add /api/alerts/risk-score/{listing_id} endpoint  [kept-unmerged] (5f7beab)
- why useful: Exposes the computed risk score to callers, enabling filtering or prioritization of listings.
- tests: 42 passed / 3 failed
- note: tool-gates failed

## 2026-07-03T12:08:32.961518 — Add MultiCityPriceRequest model  [kept-unmerged] (6419d77)
- why useful: Defines the input schema for a list of cities so subsequent endpoints can accept and validate multi‑city queries.
- tests: 43 passed / 3 failed
- note: tool-gates failed

## 2026-07-03T12:14:36.538266 — Add multi‑city stats endpoint (JSON)  [kept-unmerged] (819fca0)
- why useful: Provides the first functional API that can receive multiple cities and return aggregated price statistics, enabling downstream CSV export.
- tests: 42 passed / 6 failed
- note: tool-gates failed

## 2026-07-03T12:21:33.413135 — Implement compute_price_stats with safe aggregation  [kept-unmerged] (a282e11)
- why useful: Provides the core logic that calculates average price, count, min/max and deviation for each city while handling empty or zero‑division cases.
- tests: 46 passed / 3 failed
- note: tool-gates failed

## 2026-07-03T12:28:03.702476 — Add CSV export endpoint for multi‑city stats  [kept-unmerged] (1ae84a3)
- why useful: Completes the user story by allowing a downloadable CSV containing city, average price, count, min/max and deviation metrics.
- tests: 41 passed / 4 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T13:07:43.164741 — Fix/port failing test file tests/test_api_scheduler_run_once.py  [MERGED] (300df00)
- why useful: each fixed file adds real regression coverage guarding every future merge
- tests: 46 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T13:16:02.308092 — Bootstrap DB creation on import  [MERGED] (9bbd2a9)
- why useful: Ensures tables are created automatically so tests and production start without manual migrations.
- tests: 46 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T13:22:17.515156 — Add shared test fixtures and example test  [kept-unmerged] (d119025)
- why useful: Provides a reusable fixture that creates an in‑memory SQLite DB, creates all tables, and overrides the FastAPI get_db dependency for isolated tests.
- tests: 47 passed / 1 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T13:31:07.893188 — Patch environment‑coupled scheduler tests to use fixture override  [kept-unmerged] (de4dcbf)
- why useful: Fixes flaky tests that fail because they rely on the real DB session; using the overridden dependency makes them deterministic.
- tests: 0 passed / 3 failed
- note: tool-gates failed

## 2026-07-03T13:41:55.710495 — Delete unused /api/saved-searches/run endpoint  [MERGED] (23e21ab)
- why useful: Removes dead code that never executes and prevents accidental calls to a non‑functional route.
- tests: 46 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T13:53:52.125865 — Delete unused /api/report/download endpoint  [kept-unmerged] (047c81b)
- why useful: Cleans up another dead route that offers no functionality and could confuse API consumers.
- tests: 46 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T13:57:05.376007 — Fix toggle_saved_search path parameter  [MERGED] (88bed6a)
- why useful: Adds the required `{id}` path placeholder so the route can be invoked; otherwise the endpoint is unreachable.
- tests: 46 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T14:11:55.842010 — Delete benchmark route and its test file  [kept-unmerged] (8926a6f)
- why useful: Removes a placeholder endpoint that was never completed and eliminates associated test noise.
- tests: 47 passed / 0 failed
- note: critic=FAIL

## 2026-07-03T14:23:27.883460 — Delete unused deviation_target field and its test file  [kept-unmerged] (6a3eca8)
- why useful: Cleans up a model field that is never persisted or used, reducing schema drift and test clutter.
- tests: 0 passed / 13 failed
- note: tool-gates failed

## 2026-07-03T14:34:05.943620 — Implement run_saved_search endpoint  [kept-unmerged] (f8fc89a)
- why useful: Enables execution of saved searches, creates alerts, and provides the foundation for alert scheduling.
- tests: 46 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T14:46:27.995545 — Modify alerts runner to query active saved searches from DB  [kept-unmerged] (08dde6c)
- why useful: Replaces the empty SAVED_SEARCH_STORE iteration with real active saved searches, allowing alerts to be scheduled and executed.
- tests: 47 passed / 1 failed
- note: tool-gates failed

## 2026-07-03T15:02:59.185449 — Delete unused global collections SAVED_SEARCHES and SAVED_SEARCH_STORE  [kept-unmerged] (1c24abf)
- why useful: Removes dead code that no longer serves any purpose, preventing accidental reuse and keeping the namespace clean.
- tests: 49 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T15:19:03.878849 — Add ListingORM model and DB fixture  [kept-unmerged] (7f80ab2)
- why useful: Create a persistent table for listings so that future analytics (price deviation) can query real data instead of using hardcoded zero.
- tests: 46 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T15:26:45.459531 — Persist listings on search via upsert  [kept-unmerged] (3177d1e)
- why useful: Store scraped results in the new ListingORM table so they survive server restarts and can be used for deviation calculations.
- tests: 46 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T15:35:44.013928 — Compute real price deviation for alerts  [kept-unmerged] (1370ee2)
- why useful: Replace the hardcoded `0.0` deviation with a calculation based on persisted listings, enabling accurate analytics and preventing false‑positive alerts.
- tests: 46 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T15:42:55.495816 — Add pure stdlib scam risk scoring function  [MERGED] (fb3d99c)
- why useful: Provides a deterministic heuristic to flag suspicious listings without external dependencies, forming the basis for downstream scam detection.
- tests: 49 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T15:51:34.207041 — Add risk_score field to Listing model and populate per listing  [kept-unmerged] (0324fba)
- why useful: Makes the scam score available to downstream API consumers and other services, enabling filtering or alerting based on risk.
- tests: 49 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T15:57:39.171298 — Integration test for risk_score presence in API response  [kept-unmerged] (0107d2d)
- why useful: Confirms that the end‑to‑end flow—scraper → model → response—correctly injects and exposes the scam score, satisfying the EPIC's requirement for observable risk data.
- tests: 49 passed / 1 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T16:07:00.333352 — Add build_export_records import to main.py  [MERGED] (02b58c2)
- why useful: The endpoint must call this function; importing it makes it available for later wiring.
- tests: 50 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T16:17:09.573455 — Implement /api/reports/deals JSON endpoint  [kept-unmerged] (754bddc)
- why useful: Provides HTTP access to exported deal records in JSON format.
- tests: 50 passed / 2 failed
- note: tool-gates failed

## 2026-07-03T16:24:19.465469 — Add CSV streaming support for ?format=csv  [kept-unmerged] (b357439)
- why useful: Allows clients to download the same exported rows as a streamed CSV file.
- tests: 0 passed / 9 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T16:52:51.104364 — Add risk_score column to export records  [kept-unmerged] (24002ab)
- why useful: The CSV export must include a computed risk_score for each listing so users can sort by safety.
- tests: 50 passed / 0 failed
- note: works-but-untested — test-only retry

## 2026-07-03T17:03:46.624167 — Expose CSV endpoint with risk_score column  [MERGED] (94934ce)
- why useful: The public `/api/search/csv` route must stream a CSV that now includes the new `risk_score` column.
- tests: 51 passed / 0 failed
- note: gates+critic passed

## 2026-07-03T17:29:27.331676 — Add engine initialization and bootstrap metadata creation in db.py  [kept-unmerged] (1c57ab7)
- why useful: Ensures that all SQLAlchemy tables (including saved_searches) are created automatically on import, fixing the OperationalError when a fresh SQLite DB is used.
- tests: 51 passed / 0 failed
- note: no-op attempt (no write) — retrying with nudge

## 2026-07-03T23:40:01.818310 — Delete unused deviation_target field from SavedSearch model and its test  [kept-unmerged] (772526d)
- why useful: Removes dead code and associated test to keep the codebase clean and maintain a green test suite.
- tests: 50 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-03T23:51:19.265221 — Delete stub benchmark route from main.py and its test  [kept-unmerged] (73fcf6a)
- why useful: Eliminates unused benchmark endpoint to reduce surface area and keep tests green.
- tests: 50 passed / 0 failed
- note: no progress after escalation — stopped (branch keeps best attempt)

## 2026-07-04T00:05:49.476899 — Add /api/reports/deals endpoint and test  [kept-unmerged] (88121ed)
- why useful: Provides the required JSON reports endpoint for deals and validates its output with an integration test.
- tests: 51 passed / 0 failed
- note: tool-gates failed

## 2026-07-04T00:19:44.818765 — Run saved search endpoint loads from DB and executes scraper  [MERGED] (9d79d9d)
- why useful: Ensures end‑to‑end saved search execution; fixes scraper patch target to backend.app.scraper.CraigslistScraper and ensures cities are stored as proper JSON for correct parsing.
- tests: 53 passed / 0 failed
- note: gates+critic passed

