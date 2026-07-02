# EPICS — craigsail (control-authored; refreshed 2026-07-02)

Ranked implementation candidates. The loop consumes `proposed` items IN ORDER before
self-proposing. Statuses: proposed | active | shipped | rejected. Attempted names are
archive-deduped — follow-ups get NEW names.

## 1. review-cleanup-jul2 [maintenance] — proposed
- value: the 2026-07-02 run merged two features with defects that must be fixed before new work.
- evidence: controller code review of merges e9e97e9 and 056ee90 on agent/loop.
- outcome: three precise fixes, one subtask each:
  (a) backend/app/models.py — DELETE the post-class line `SavedSearch.is_scheduled = False`
  and its comment block (a hasattr shim; the field declared inside the class is correct and stays).
  (b) tests/test_saved_search_scheduled.py — REWRITE: drop hasattr/model_fields introspection;
  assert behavior instead: `SavedSearch(cities=["sf"], query="bike").is_scheduled is False`,
  `SavedSearch(cities=["sf"], query="bike", is_scheduled=True).is_scheduled is True`, and
  `"is_scheduled" in SavedSearch(cities=["sf"], query="bike").model_dump()`.
  (c) backend/app/reports.py — replace the try/except ImportError dual import with the plain
  `from app.models import ExportItem, AlertORM`; make compute_price_deviation return 0.0 when
  ss_avg_price is 0 (guard the division); update tests/test_deviation_calculation.py to import
  `from app.reports import compute_price_deviation` (NOT backend.app.reports) and add a
  zero-average case asserting 0.0.

## 2. background-jobs-runner [core] — proposed
- value: saved searches marked is_scheduled currently do nothing; recurring execution is the
  point of alerts (phase 2 of the PersistAlertScheduler epic, which merged only the model flag).
- evidence: FEATURES.json shows the flag shipped without an executor; owner focus = durable
  persistence + scheduler execution.
- outcome: a scheduler module under backend/app/ that runs one "scheduling pass" — find
  SavedSearch rows with is_scheduled, execute each search (scraper mocked in tests), record
  alert hits — plus a POST endpoint to trigger a single pass on demand so it is testable
  without sleeping or background threads in tests.

## 3. scam-risk-score [data-quality] — proposed
- value: scam listings waste the user's time; a per-listing risk score is a decision aid no
  basic craigslist client has.
- evidence: owner-approved next-iteration feature list (2026-07-02).
- outcome: a pure function scoring a listing 0-100 from local heuristics (price far below
  category median, keyword patterns like "wire transfer"/"shipping only"/urgency phrases,
  missing images flag) — no external APIs; score attached to search results and an optional
  min/max filter on the search endpoint.

## 4. deal-report-endpoint [analytics] — proposed
- value: backend/app/reports.py (build_export_records, compute_price_deviation) is currently
  dead code — nothing imports it; wiring it turns stored alerts into a usable deal report.
- evidence: `git grep "app.reports"` on agent/loop returns no importers.
- outcome: GET /api/reports/deals returning export records enriched with a price_deviation
  column (via compute_price_deviation against the saved-search average), covered by a test
  with a seeded in-memory DB.
