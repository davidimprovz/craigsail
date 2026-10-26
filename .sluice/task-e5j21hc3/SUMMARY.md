# CraigSail Agent Run — Summary (2026-10-26T18:38:56.742737)

- cycles: 1 | merged: 1 | kept-unmerged (review): 0
- final tests on agent/task-e5j21hc3: 60 passed / 0 failed
- feature ledger: 0 shipped features (FEATURES.json)
- calibration (broke something, loop must re-fix it): skipped (task mode)
- Sluice task: Dedupe by posting URL, not title+location | done_check: pass
- config: lang=python fastapi=True scope=backend tests=python -m pytest -q

## Branch log
```
a6cbf8e agent: Dedupe by posting URL, not title+location
65693fa agent: the task's failing test tests/dedupe_url/test_dedupe_url.py (check_test)
d64cfe4 agent: start task on agent/task-e5j21hc3
a0aedcd Merge loop round-5 (agent pipeline, QC 57/0 clean Docker on pecan)
07f5c31 agent: run summary
8695be6 agent: ledger/log update
b84296f agent: ledger/log update
7207bcf merge: Define ListingORM model
0deabf3 agent attempt 1: Define ListingORM model
eab6813 agent: ledger/log update
74e3b19 merge: Remove obsolete SAVED_SEARCHES and SAVED_SEARCH_STORE globals
ff773c7 agent attempt 3: Remove obsolete SAVED_SEARCHES and SAVED_SEARCH_STORE globals
a070d1e agent attempt 2: Remove obsolete SAVED_SEARCHES and SAVED_SEARCH_STORE globals
97d06d9 agent: ledger/log update
911b2cd agent: ledger/log update
f9d8a7d merge: Run saved search endpoint loads from DB and executes scraper
9d79d9d agent attempt 2: Run saved search endpoint loads from DB and executes scraper
8574683 agent attempt 1: Run saved search endpoint loads from DB and executes scraper
939b5e8 agent: ledger/log update
596d2be agent: ledger/log update
```

Each improvement was gated by syntax+test-files+integration+dup-routes+tests+probe, then an adversarial critic.
Unmerged attempts are on `agent/imp-N` branches for review. See IMPROVEMENTS.md for rationale and LOOP_REPORT.json for per-attempt gate outcomes.
