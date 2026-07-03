# NEXT_STEPS — craigsail (controller review of the 2026-07-03 overnight, jetson/loop @ 0fe842a)

## Run verdict: SUCCESS — best night on record
10 merged / 44 kept over 8h; suite 34 → 45 green; calibration PASS (first in 5 runs —
the read_file truncation fix also cured the one-shot route repair); env_v=3 stamps and
terminated/truncated labels all correct; mechanical check clean.

## Shipped (merged on agent/loop, ready for owner testing)
- dead-code purge: 3 of 4 zombie endpoints deleted (123-run, create echo stub, +1 more;
  ONE stub remains — carried).
- endpoint repairs 4/5: forecast NameError fixed (with behavior test), list .dict()
  crash fixed, delete int/UUID mismatch fixed, reports.py self-import removed.
  Remaining: toggle path-param repair (critic rejected attempt; carried).
- run-once-scheduler 3/3: backend/app/scheduler.py (select_scheduled +
  run_scheduling_pass) + POST /api/scheduler/run-once, each with its own test —
  the twice-failed epic went perfect once the brief embedded test skeletons.
- Self-proposed (thin): SavedSearch.deviation_target field (unused — wire or drop),
  GET benchmark route "skeleton" (a NEW stub — purge or implement next round).

## Blocked pattern → round-4 prerequisite
All four 0/N epics (store-unification, listing-persistence, scam-heuristics,
deals-route) died on tests+probe: they are DB-touching, and the coder cannot
bootstrap SQLAlchemy test scaffolding alone (temp engine, create_all, get_db
override). ROUND-4 EPIC 1 must be a [maintenance] "db-test-fixtures" epic that adds a
shared tests/db_fixtures.py (tmp sqlite engine + TestClient dependency-override
helper) with one example test; later epics then reference it by name.

## Efficiency finding for the owner
The control brief exhausted at 07:46; the last 4.5h of self-proposals produced 2 thin
merges + ~30 failures. Recommend: stop-on-brief-exhaustion (or require EPIC_FOCUS for
self-proposals) — a 1-line loop change, owner call.

## Owner actions
- Test on this Mac (Docker): `git checkout jetson/loop` in this repo — suite 45/0;
  try POST /api/scheduler/run-once, GET /api/forecast, saved-search delete.
- Write FEEDBACK.md with anything off; merge jetson/loop → your branch when satisfied
  (branch + tags are kept).
- Approve round-4 brief (db-test-fixtures first, then carried epics) and Tier-2
  research items (interface-contract decomposition attacks exactly this composition
  class).
