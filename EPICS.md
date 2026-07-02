# EPICS — craigsail (control-authored; refreshed 2026-07-02 evening, round 2)

Ranked implementation candidates. The loop consumes `proposed` items IN ORDER before
self-proposing. Statuses: proposed | active | shipped | rejected. Attempted names are
archive-deduped — follow-ups get NEW names (hence the renames below).

## 1. cleanup-jul2-round2 [maintenance] — proposed
- value: three precise fixes left over from the jul-2 review + fix cycle (see ISSUES.md).
- evidence: controller review of jetson/loop @ b5bd097.
- outcome: one subtask each, exact changes:
  (a) backend/app/reports.py — the function build_export_records calls `db.query(AlertORM)`
  (line ~20) and documents ExportItem, but the file no longer imports either symbol: add
  back `from app.models import ExportItem, AlertORM` at the top (plain import, NO
  try/except). Definition of done: `python -c "import sys; sys.path.insert(0,'backend');
  from app.reports import build_export_records"` exits 0 AND the file contains the import.
  (b) tests/test_deviation_calculation.py — both tests import
  `from backend.app.reports import compute_price_deviation`; change BOTH lines to
  `from app.reports import compute_price_deviation` (tests must import modules exactly
  as the app does). Touch nothing else in the file.
  (c) tests/test_saved_search_scheduled.py — the third test still inspects
  `model_fields` conditionally; replace its body with direct behavior asserts:
  construct `SavedSearch(cities=["sf"], query="bike", is_scheduled=True)` and assert
  `.is_scheduled is True`, and assert `"is_scheduled" in SavedSearch(cities=["sf"],
  query="bike").model_dump()`. Keep the other two tests unchanged.

## 2. scheduler-pass-execution [core] — proposed
- value: saved searches marked is_scheduled still do nothing; recurring execution is the
  point of alerts. (Renamed re-scope of background-jobs-runner, which stalled 0/3 —
  smaller steps this time.)
- evidence: FEATURES.json has the flag + persistence but no executor.
- outcome, in THIS order of subtasks: (1) a pure function in a new module
  backend/app/scheduler.py: `select_scheduled(db) -> list[SavedSearch-like]` returning
  rows flagged is_scheduled, with a new test seeding an in-memory DB; (2) a function
  `run_scheduling_pass(db, scraper)` that executes each scheduled search via the passed
  scraper (mock in the test) and returns a per-search hit count, with its own new test;
  (3) POST /api/scheduler/run-once wiring run_scheduling_pass into the app with a
  TestClient test that mocks the scraper. Each subtask = one function + one new test file.

## 3. listing-risk-scoring [data-quality] — proposed
- value: scam listings waste the user's time; a per-listing risk score is a decision aid.
  (Renamed re-scope of scam-risk-score, 0/4 — smaller steps.)
- evidence: owner-approved feature list (2026-07-02).
- outcome: (1) pure function `risk_score(listing: dict) -> int` (0-100) in a new module,
  from local heuristics only (price far below typical, keywords like "wire transfer" /
  "shipping only" / urgency phrases, missing images) + new test with 3 fixture listings;
  (2) attach `risk_score` to each result in the search response + TestClient test with a
  mocked scraper asserting the field exists and is an int.

## 4. deal-report-endpoint [analytics] — proposed
- value: backend/app/reports.py (build_export_records, compute_price_deviation) is dead
  code — nothing imports it; wiring it turns stored alerts into a usable deal report.
- evidence: `git grep "app.reports"` on agent/loop returns no importers.
- outcome: GET /api/reports/deals returning export records enriched with a
  price_deviation column, covered by a test with a seeded in-memory DB. Depends on 1(a).

## 5. review-cleanup-jul2 [maintenance] — shipped
- 2/4 merged (hasattr shim removed + behavior tests; zero-division guard landed via the
  test subtask). Remainder folded into cleanup-jul2-round2.
