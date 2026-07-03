# FEEDBACK — craigsail (test pass on jetson/loop @ 0fe842a, 2026-07-03)

Controller-executed test pass on the owner's behalf (delegated); owner to countersign.

## What works (verified in a clean Docker environment)
- GET /api/forecast → 200 with confidence_scores/trajectory on 4 mocked listings — the
  NameError fix is real (this crashed before).
- POST /api/scheduler/run-once → 200 {"hit_counts": {}} (correct with nothing scheduled).
- Saved-search roundtrip: POST create → 200 + uuid; GET list → 200 (1 row, no .dict()
  crash); DELETE by uuid → 200 Deleted (the int/UUID fix is real).

## Blocker found (clean-environment only)
- **3 tests fail on a fresh checkout** (42/45): `sqlite3.OperationalError: no such table:
  saved_searches`. Nothing ever calls `Base.metadata.create_all(engine)` — pecan's
  workdir has an old craigsail.db with tables, so the gates saw 45/0. This is ALSO an
  app bug: a fresh deploy crashes the same way. Everything above passed only after
  manually running create_all first.
- Priority for round 4: bootstrap create_all at app/db import (idempotent) + shared DB
  test fixtures; then re-fix the 3 environment-coupled tests.

## Minor
- Self-proposed additions to drop: unused `SavedSearch.deviation_target` field and the
  stub GET benchmark route (both add surface without behavior).
