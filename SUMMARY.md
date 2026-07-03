# CraigSail Agent Run — Summary (2026-07-03T03:21:49.895535)

- cycles: 20 | merged: 5 | kept-unmerged (review): 15
- final tests on agent/loop: 34 passed / 0 failed
- feature ledger: 27 shipped features (FEATURES.json)
- calibration (broke something, loop must re-fix it): FAIL (Warning: OPENAI_API_KEY not set. AI features will mock response.
PROBE FAIL: GET /api/models: NOT REGISTERED on the app (defined but not wired - forgot include_)
- config: lang=python fastapi=True scope=backend tests=python -m pytest -q

## Branch log
```
090214d agent: ledger/log update
c022d89 agent: ledger/log update
c6eb486 agent: ledger/log update
9a1e026 agent: ledger/log update
0db96eb agent: ledger/log update
44cd1eb agent: ledger/log update
b7b89e7 agent: ledger/log update
32706ad agent: ledger/log update
a986fe2 agent: ledger/log update
b37f729 agent: ledger/log update
4475bac merge: Integrate price_deviation into build_export_records
94e39a0 agent attempt 1: Integrate price_deviation into build_export_records
c4b5f12 agent: ledger/log update
384c34d merge: Add compute_price_deviation utility function
60ae6dc agent attempt 3: Add compute_price_deviation utility function
a83ce7b agent attempt 2: Add compute_price_deviation utility function
fd9c874 agent attempt 1: Add compute_price_deviation utility function
c639076 agent: ledger/log update
b619f98 agent: ledger/log update
48ce347 agent: ledger/log update
```

Each improvement was gated by syntax+test-files+integration+dup-routes+tests+probe, then an adversarial critic.
Unmerged attempts are on `agent/imp-N` branches for review. See IMPROVEMENTS.md for rationale and LOOP_REPORT.json for per-attempt gate outcomes.
