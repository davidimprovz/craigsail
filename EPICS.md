# EPICS — craigsail (control-authored; round 4, 2026-07-03)

Ranked. The loop consumes `proposed` items IN ORDER before self-proposing. Follow-ups
carry NEW names (attempted names are exact-match deduped; maintenance epics may re-run).

## 1. db-bootstrap-and-fixtures [maintenance] — proposed
- value: the suite is green only in a dirty workdir — 3 tests fail on ANY fresh checkout
  with `sqlite3.OperationalError: no such table: saved_searches`, and a fresh production
  deploy crashes identically: nothing ever calls `Base.metadata.create_all(engine)`.
  Owner test pass confirmed every endpoint works once tables exist (FEEDBACK.md).
- outcome (ordered):
  (a) `backend/app/db.py`: after the ORM classes are registered, add the idempotent
  bootstrap `Base.metadata.create_all(engine)` at module import (bottom of db.py, after
  the `SavedSearch` class and the `Group` import so both tables register). Verify:
  `rm -f craigsail.db && python -m pytest -q` passes from a clean tree — run exactly
  that with run_shell.
  (b) new `tests/db_fixtures.py` shared helper, content to adapt:
  `import os, tempfile` / `from sqlalchemy import create_engine` /
  `from sqlalchemy.orm import sessionmaker` / `from app.db import Base` /
  `def make_test_db():` / `    path = tempfile.mktemp(suffix=".db")` /
  `    eng = create_engine(f"sqlite:///{path}", connect_args={"check_same_thread": False})` /
  `    Base.metadata.create_all(eng)` /
  `    return eng, sessionmaker(bind=eng)`
  plus `def override_get_db(app, Session):` registering a FastAPI dependency override
  for `app.db.get_db` that yields a Session and closes it. Add ONE example test
  `tests/test_db_fixtures.py` inserting a DBSavedSearch row through the fixture and
  reading it back.
  (c) repair the 3 environment-coupled tests (the scheduler run-once API tests et al.):
  make each create its tables via `tests/db_fixtures.py` (or rely on (a)'s bootstrap)
  so the whole suite passes after `rm -f craigsail.db`. Do not weaken any assertion.

## 2. surface-cleanup-jul3 [maintenance] — proposed
- value: leftovers from earlier rounds — two stubs, one broken route, two thin additions.
- outcome, one subtask each:
  (a) DELETE the stub `run_pending_searches` with `@app.get("/api/saved-searches/run")`
  in `backend/app/main.py` (if still present).
  (b) DELETE the stub `report_download` with `@app.get('/api/report/download')` (if
  still present).
  (c) `toggle_saved_search`: it declares `id: str = Path(...)` but its route has no
  path parameter, so it can never be called — change the decorator to
  `@app.post('/api/saved-searches/{id}/toggle')` (keep the function body).
  (d) DELETE the stub benchmark route added on 2026-07-03 (search `grep -n benchmark
  backend/app/main.py`) AND its test file `tests/test_api_benchmark.py`; DELETE the
  unused `deviation_target` field from `SavedSearch` in `backend/app/models.py` AND its
  test file `tests/test_deviation_target_field.py` (both add surface without behavior).

## 3. store-unification-v2 [core] — proposed
- value: saved searches still split across three stores; `{id}/run` reads an in-memory
  dict nothing writes (running ALWAYS 404s); the alerts runner iterates an always-empty
  list. Epic 1's fixtures + bootstrap now make the DB tests writable.
- outcome (ordered):
  (a) `run_saved_search` (`@app.post('/api/saved-searches/{saved_search_id}/run')`)
  loads from the DB: `saved = db.query(DBSavedSearch).get(saved_search_id)` (404 if
  None), `cities = json.loads(saved.cities or "[]")`, `db: DBSession = Depends(get_db)`.
  New test `tests/test_run_saved_search.py` using `tests/db_fixtures.py`
  (make_test_db + override_get_db), insert one row, patch `app.main.CraigslistScraper`
  with an AsyncMock search returning one listing, POST, assert 200 and one alert id.
  (b) `run_saved_alerts` iterates `db.query(DBSavedSearch).filter_by(is_active=True)`
  instead of `SAVED_SEARCH_STORE`; own new test, same pattern.
  (c) DELETE the now-unused globals `SAVED_SEARCHES` and `SAVED_SEARCH_STORE` (keep
  `ALERTS`).

## 4. listing-store [core] — proposed
- value: nothing scraped is persisted, so export price_deviation is a hardcoded 0.0 and
  no price history can exist. Owner focus: durable persistence + listing data quality.
- outcome (ordered):
  (a) `ListingORM` in `backend/app/models.py` next to `AlertORM` (id Integer pk
  autoincrement, title String, price_num Float nullable, city String, query String,
  url String unique, first_seen String, last_seen String). New test via
  `tests/db_fixtures.py` constructing and reading back a row.
  (b) persist on search: in `search_listings` after dedup, best-effort upsert by url
  into ListingORM (price via `CraigslistScraper._parse_price`, whole block in
  try/except so persistence can never break search). New test: POST /api/search with
  mocked scraper, assert rows via the fixture session.
  (c) real deviation: `_deviation_for_alert` computes mean `price_num` of ListingORM
  rows matching alert.city+alert.query; return
  `compute_price_deviation({"price": float(alert.max_price or 0)}, mean_price)` when
  rows exist, else None (honest absence — never fake 0.0). Do NOT modify
  `tests/test_build_export_records.py`; add `tests/test_deviation_real.py` seeding two
  rows through the fixture.

## 5. scam-scoring-v2 [data-quality] — proposed
- value: scam listings waste the user's time; local heuristic score, no external APIs.
- outcome (ordered):
  (a) new `backend/app/risk.py` — imports NOTHING from app.* (pure stdlib):
  `def risk_score(listing: dict, typical_price=None) -> int` — +40 if typical_price and
  price < 0.2*typical_price; +30 if any of ("wire transfer","shipping only","cashier
  check","urgent") in (title+description).lower(); +15 if listing.get("no_image");
  cap 100. New test `tests/test_risk_score.py` with three fixture dicts
  (clean → 0, cheap+keywords → >=70, keywords-only → 30).
  (b) add `risk_score: Optional[int] = None` to the `Listing` pydantic model and set it
  in `search_listings` per result via `risk_score({"price": ..., "title": ...})`.
  TestClient test with mocked scraper asserting the field is an int on every result.

## 6. deals-endpoint-v2 [analytics] — proposed
- value: reports.py (export records + deviation) is still unreachable over HTTP.
- outcome: (a) `@app.get('/api/reports/deals')` returning `build_export_records(db)`
  with `db: DBSession = Depends(get_db)` (`from app.reports import
  build_export_records` at top of main.py). Test via `tests/db_fixtures.py` +
  override_get_db: with an empty DB assert 200 and `[]`; seed one AlertORM row and
  assert one record. (b) `?format=csv` variant streaming the same rows as CSV
  (reuse the csv/io pattern from `export_search_csv`).

## Status ledger
- round-3 shipped: cleanup-jul2-round2 3/3 · dead-code-purge 3 of 4 · endpoint-repairs
  4/5 · run-once-scheduler 3/3. Round-3 carried → epics 2-6 above.
