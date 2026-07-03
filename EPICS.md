# EPICS — craigsail (control-authored; round 5, 2026-07-03 evening)

Ranked. The loop consumes `proposed` items IN ORDER and STOPS when they're done
(SELF_PROPOSE=0). One concern per lettered subtask. Facts: suite is 51/0 green;
`Base.metadata.create_all` runs at import (fresh DBs bootstrap themselves);
`from app.reports import build_export_records` already sits in main.py line ~22.

## 1. surface-trim [maintenance] — proposed
- value: two thin additions from an old self-proposal tail add surface without behavior.
- outcome, ONE subtask each:
  (a) DELETE the unused `deviation_target` field from `SavedSearch` in
  `backend/app/models.py` AND delete its test file
  `tests/test_deviation_target_field.py`. Suite must stay green afterwards.
  (b) DELETE the stub benchmark route from `backend/app/main.py` (find it with
  `grep -n benchmark backend/app/main.py`) AND delete `tests/test_api_benchmark.py`.

## 2. deals-json-route [analytics] — proposed
- value: reports.py is imported but unreachable as JSON — the deal report needs its
  endpoint (the CSV variant already exists).
- outcome, ONE subtask:
  (a) Add `@app.get('/api/reports/deals')` in `backend/app/main.py` returning
  `build_export_records(db)` with `db: DBSession = Depends(get_db)` (the import is
  already at the top). New test `tests/test_deals_route.py`: with a TestClient, GET
  the route on an empty DB and assert 200 + a list; then insert one AlertORM row via
  `SessionLocal()` (`from app.db import SessionLocal`; `from app.models import
  AlertORM`; city="sfbay", query="bike", max_price=500) and assert the response
  contains one record with a "price_deviation" key.

## 3. saved-search-live-run [core] — proposed
- value: running a saved search STILL always 404s — `run_saved_search` reads the
  in-memory `SAVED_SEARCHES` dict that nothing writes, while create/list/delete use
  the DB. The flagship feature cannot work end-to-end. (Third re-scope; the DB now
  bootstraps itself, so tests are straightforward.)
- outcome (ordered):
  (a) `run_saved_search` (`@app.post('/api/saved-searches/{saved_search_id}/run')` in
  `backend/app/main.py`) loads from the DB: `db: DBSession = Depends(get_db)`;
  `saved = db.query(DBSavedSearch).get(saved_search_id)`; 404 if None;
  `cities = json.loads(saved.cities or "[]")`; use `saved.query`, `saved.category`,
  `float(saved.max_price) if saved.max_price else None`. New test
  `tests/test_run_saved_search.py`: insert a DBSavedSearch row via SessionLocal
  (id="t-run-1", query="bike", cities='["sfbay"]'), patch `app.main.CraigslistScraper`
  like `tests/test_search.py` does (AsyncMock search returning one Listing), POST
  `/api/saved-searches/t-run-1/run`, assert 200 and one alert id.
  (b) `run_saved_alerts` (`@app.post('/api/alerts/run-saved')`) iterates
  `db.query(DBSavedSearch).filter_by(is_active=True)` instead of the module-global
  `SAVED_SEARCH_STORE`; same mock pattern in its own new test file.
  (c) DELETE the now-unused module globals `SAVED_SEARCHES` and `SAVED_SEARCH_STORE`
  from `backend/app/main.py` (KEEP `ALERTS`). Suite stays green.

## 4. listing-store-v2 [core] — proposed
- value: nothing scraped is persisted, so export price_deviation is a hardcoded 0.0
  (`_deviation_for_alert` admits it) and no price history can exist. Owner focus:
  durable persistence + listing data quality.
- outcome (ordered):
  (a) `ListingORM` in `backend/app/models.py` next to `AlertORM`: id Integer primary
  key autoincrement, title String, price_num Float nullable, city String, query
  String, url String unique, first_seen String, last_seen String. New test
  `tests/test_listing_orm.py`: insert and read back one row via SessionLocal.
  (b) persist on search: in `search_listings` in `backend/app/main.py`, after dedup,
  best-effort upsert each result by url into ListingORM (price via
  `CraigslistScraper._parse_price`), the whole block wrapped in try/except so
  persistence can never break search. New test `tests/test_listing_persist.py`:
  POST /api/search with the mocked scraper, then assert the row count grew via
  SessionLocal.
  (c) real deviation: `_deviation_for_alert` in `backend/app/reports.py` computes the
  mean `price_num` of ListingORM rows matching alert.city and alert.query; when rows
  exist return `compute_price_deviation({"price": float(alert.max_price or 0)},
  mean_price)`, else return None — NEVER a fake 0.0. Do NOT modify
  `tests/test_build_export_records.py` (it patches the helper); add
  `tests/test_deviation_real.py` seeding two ListingORM rows and asserting the value.

## Status ledger
- round-4 shipped: db bootstrap, endpoint repairs, purge, scheduler 3/3, scam scoring
  fn, reports import + CSV-with-risk. Merged to owner main (bdcf442, verified 51/51
  clean-env).
- deviation_target / benchmark stub — scheduled for deletion above (epic 1).
- store-unification / listing-persistence lineage — re-scoped above (epics 3-4).
