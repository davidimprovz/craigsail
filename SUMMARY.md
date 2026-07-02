# craigsail Agent Run — Summary (2026-07-02T22:47:21.130712)

- cycles: 10 | merged: 2 | kept-unmerged (review): 8
- final tests on agent/loop: 30 passed / 0 failed
- feature ledger: 22 shipped features (FEATURES.json)
- calibration (broke something, loop must re-fix it): FAIL (Warning: OPENAI_API_KEY not set. AI features will mock response.
PROBE FAIL: GET /api/models: NOT REGISTERED on the app (defined but not wired - forgot include_)
- config: lang=python fastapi=True scope=backend tests=python -m pytest -q

## Branch log
```
503ca79 agent: ledger/log update
0b081b6 agent: ledger/log update
2863452 agent: ledger/log update
60b0bda agent: ledger/log update
ec9a56e agent: ledger/log update
c27f789 agent: ledger/log update
8b4e17c agent: ledger/log update
0300d33 agent: ledger/log update
1b75fb7 merge: Add zero‑average test case for price deviation
1efcbe1 agent attempt 2: Add zero‑average test case for price deviation
38ce849 agent attempt 1: Add zero‑average test case for price deviation
64505db agent: ledger/log update
5273864 agent: ledger/log update
31a03e9 merge: Remove stray is_scheduled assignment from SavedSearch model
1b5fe34 agent attempt 1: Remove stray is_scheduled assignment from SavedSearch model
22d15a1 sync: controller cycle files (fix brief)
a4e8a83 agent: run summary
2e872ef agent: ledger/log update
7b49549 agent: ledger/log update
56cd767 agent: ledger/log update
```

Each improvement was gated by syntax+test-files+integration+dup-routes+tests+probe, then an adversarial critic.
Unmerged attempts are on `agent/imp-N` branches for review. See IMPROVEMENTS.md for rationale and LOOP_REPORT.json for per-attempt gate outcomes.
