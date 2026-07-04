# CraigSail Agent Run — Summary (2026-07-04T00:55:48.814922)

- cycles: 8 | merged: 3 | kept-unmerged (review): 5
- final tests on agent/loop: 57 passed / 0 failed
- feature ledger: 49 shipped features (FEATURES.json)
- calibration (broke something, loop must re-fix it): PASS
- config: lang=python fastapi=True scope=backend tests=python -m pytest -q

## Branch log
```
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
e8b1e1c agent: ledger/log update
6b963a8 sync: controller round-5 brief
cfb409b agent: run summary
b3c3e04 agent: ledger/log update
1c57ab7 agent: run summary
```

Each improvement was gated by syntax+test-files+integration+dup-routes+tests+probe, then an adversarial critic.
Unmerged attempts are on `agent/imp-N` branches for review. See IMPROVEMENTS.md for rationale and LOOP_REPORT.json for per-attempt gate outcomes.
