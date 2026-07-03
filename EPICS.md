# EPICS — craigsail (control-authored; round 3, 2026-07-03)

Ranked. The loop consumes `proposed` items IN ORDER before self-proposing. Follow-ups
carry NEW names (attempted names are exact-match deduped). Statuses:
proposed | active | shipped | rejected.

## 1. dead-code-purge [maintenance] — proposed
- value: four zombie endpoints from pre-gate-era runs mislead users and bloat main.py.
- evidence: controller audit 2026-07-02 (ISSUES.md); no test references any of them
  (`tests/test_search.py::test_core_routes_registered` asserts only /health, /api/search,
  /multi_search).
- outcome: TWO remaining deletions in `backend/app/main.py`, ONE subtask each; suite
  stays green. (The 123-run handler and the create echo stub are ALREADY DELETED —
  merged f26e04b + 9bca577 — do not look for them.)
  (a) DELETE the stub `run_pending_searches` with `@app.get("/api/saved-searches/run")`.
  (b) DELETE the stub `report_download` with `@app.get('/api/report/download')`.
  Delete completely — no commented-out remains.

## 2. endpoint-repairs [maintenance] — proposed
- value: three endpoints crash or can never work; reports.py carries a self-import.
- evidence: controller audit (ISSUES.md).
- outcome, one subtask each:
  (a) `backend/app/main.py` `forecast_route`: the `confidence_scores` dict references
  itself during construction — NameError whenever len(prices)>=2. Fix: compute
  `vol = min(len(prices)/20.0, 1.0)` and `tc = max(0.0, 1.0 - abs(slope)/(recent[-1] or 1))`
  as locals, then `confidence_scores = {"volume": vol, "trend_consistency": tc,
  "overall": round((vol+tc)/2, 3)}`. Add ONE new test `tests/test_forecast_route.py`:
  patch `app.main.CraigslistScraper` exactly like `tests/test_search.py` does, have
  `search` return >=3 listings with numeric string prices, GET
  `/api/forecast?city=sfbay&query=bike`, assert `r.status_code == 200` and
  `"confidence_scores" in r.json()`.
  (b) `list_saved_searches`: SQLAlchemy rows have no `.dict()` — build the dict
  explicitly: `{"id": s.id, "query": s.query, "cities": s.cities, "category": s.category,
  "max_price": s.max_price, "target_price": s.target_price, "is_active": s.is_active,
  "schedule_cron": s.schedule_cron}`.
  (c) `delete_saved_search(ss_id: int, ...)` → `ss_id: str` (ids are uuid4 strings
  minted by `save_search`).
  (d) `toggle_saved_search` declares `id: str = Path(...)` but the route has no path
  parameter — change the route to `@app.post('/api/saved-searches/{id}/toggle')`.
  (e) `backend/app/reports.py`: inside `_deviation_for_alert` remove the self-import
  `from app.reports import compute_price_deviation` (same module — call it directly)
  and remove the unused `Listing` import at the top.

## 3. saved-search-store-unification [core] — proposed
- value: saved searches live in THREE disjoint stores — DB (`save_search`/list/delete),
  an in-memory dict `SAVED_SEARCHES` that `{id}/run` reads but nothing writes (running a
  saved search ALWAYS 404s), and a `SAVED_SEARCH_STORE` list the alerts runner iterates
  but nothing fills. The flagship feature cannot work end-to-end.
- evidence: `backend/app/main.py` lines ~41-48 declare all three; controller audit.
- outcome (ordered):
  (a) `run_saved_search` (`@app.post('/api/saved-searches/{saved_search_id}/run')`)
  loads from the DB: `saved = db.query(DBSavedSearch).get(saved_search_id)` (404 if
  None), `cities = json.loads(saved.cities or "[]")`, use `saved.query`,
  `saved.category`, `float(saved.max_price) if saved.max_price else None`. Use
  `db: DBSession = Depends(get_db)`. New test `tests/test_run_saved_search.py`: insert a
  `DBSavedSearch` row via `SessionLocal()`, patch `app.main.CraigslistScraper`
  (`AsyncMock` search returning one listing), POST the route, assert 200 and one alert id.
  (b) `run_saved_alerts` (`@app.post('/api/alerts/run-saved')`) iterates
  `db.query(DBSavedSearch).filter_by(is_active=True)` instead of `SAVED_SEARCH_STORE`;
  same mocking pattern in its own new test file.
  (c) DELETE the now-unused globals `SAVED_SEARCHES` and `SAVED_SEARCH_STORE`
  (keep `ALERTS`).

## 4. listing-persistence [core] — proposed
- value: nothing scraped is stored, so export price_deviation is hardcoded 0.0
  (`_deviation_for_alert` admits "listings are transient") and no price history can
  exist. Persisting listings makes deviation, history, and lifecycle features REAL.
  Owner focus: durable persistence + listing data quality.
- outcome (ordered):
  (a) `ListingORM` in `backend/app/models.py` next to `AlertORM`: id Integer pk
  autoincrement, title String, price_num Float nullable, city String, query String,
  url String unique, first_seen String, last_seen String. New test constructs a row
  against a tmp sqlite engine.
  (b) persist on search: in `search_listings` after dedup, best-effort upsert each
  result by url into ListingORM (`CraigslistScraper._parse_price` for price_num,
  wrapped in try/except so persistence can never break search). New test: POST
  /api/search with mocked scraper, then assert the row count via SessionLocal.
  (c) real deviation: `_deviation_for_alert` computes the mean `price_num` of
  ListingORM rows matching `alert.city` and `alert.query`; if rows exist return
  `compute_price_deviation({"price": float(alert.max_price or 0)}, mean_price)`,
  else return None (honest absence — never fake 0.0). Do NOT modify
  `tests/test_build_export_records.py` (it patches the helper and stays green);
  add `tests/test_deviation_real.py` seeding two ListingORM rows and asserting the
  computed deviation value.

## 5. run-once-scheduler [core] — proposed
- value: `is_scheduled`/`schedule_cron` persist but nothing executes; one on-demand
  scheduling pass is the smallest real execution step. (Third re-scope; prior stalls
  were test-authoring — the tests are specified below, just adapt them.)
- outcome (ordered):
  (a) new `backend/app/scheduler.py`:
  `def select_scheduled(db): return db.query(DBSavedSearch).filter(DBSavedSearch.is_active == True, DBSavedSearch.schedule_cron != None).all()`
  New test `tests/test_select_scheduled.py` skeleton to adapt:
  `from app.scheduler import select_scheduled` / build a MagicMock db whose
  `query(...).filter(...).all()` returns two fake rows / assert len == 2.
  (b) `async def run_scheduling_pass(db, scraper)` in the same module: for each
  selected search, for each city in `json.loads(cities or "[]")`,
  `await scraper.search(...)`, return `{search.id: total_hits}`. New test with
  `AsyncMock` scraper returning one listing; `asyncio.run(...)`; assert the dict maps
  the id to 1.
  (c) `@app.post('/api/scheduler/run-once')` in main.py calling
  `run_scheduling_pass(db, CraigslistScraper())`; TestClient test patching
  `app.main.CraigslistScraper`, assert 200 and a dict body.

## 6. scam-heuristics [data-quality] — proposed
- value: scam listings waste the user's time; a local heuristic risk score is a decision
  aid no basic client has. (Re-scope of listing-risk-scoring with tests specified.)
- outcome (ordered):
  (a) new `backend/app/risk.py`: `def risk_score(listing: dict, typical_price=None) -> int`
  — 0-100: +40 if typical_price and price < 0.2*typical_price; +30 if any keyword in
  title/description lower ("wire transfer", "shipping only", "cashier check", "urgent");
  +15 if listing.get("no_image"); cap at 100. New test `tests/test_risk_score.py` with
  three fixture dicts (clean → 0, cheap+keywords → >=70, keywords only → 30).
  (b) attach to search: add `risk_score: Optional[int] = None` to the `Listing` model;
  in `search_listings` set it per result via `risk_score({"price": ..., "title": ...})`.
  TestClient test with mocked scraper asserting the field is an int on each result.

## 7. deals-route [analytics] — proposed
- value: reports.py (build_export_records + deviation) is still not reachable via HTTP —
  this completes the deal-report epic (2/4 last run).
- outcome: (a) `@app.get('/api/reports/deals')` in main.py returning
  `build_export_records(db)` with `db: DBSession = Depends(get_db)` (import from
  `app.reports`); TestClient test asserting 200 and a list body.
  (b) optional `?format=csv` variant streaming the same rows as CSV.

## 8. cleanup-jul2-round2 [maintenance] — shipped (3/3, 2026-07-02 night run)
## 9. deal-report-endpoint [analytics] — shipped-partial (2/4; remainder = deals-route)
## 10. scheduler-pass-execution / listing-risk-scoring — rejected
   (0/6 across two runs; re-scoped as run-once-scheduler + scam-heuristics with
   embedded test skeletons)

## Post-overnight statuses (controller review 2026-07-03 morning)
- dead-code-purge — shipped-partial (3 of 4 stubs deleted; one carried to round 4)
- endpoint-repairs — shipped-partial (4/5; toggle path-param repair carried)
- run-once-scheduler — shipped (3/3 with tests)
- saved-search-store-unification, listing-persistence, scam-heuristics, deals-route —
  carried to round 4 BEHIND a new db-test-fixtures [maintenance] prerequisite epic
  (all four died on DB test scaffolding; see NEXT_STEPS.md)
