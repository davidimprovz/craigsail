# CraigSail Agent Run — Summary (2026-07-02T19:54:27.086837)

- cycles: 37 | merged: 2 | kept-unmerged (review): 35
- final tests on agent/overnight: 29 passed / 0 failed
- feature ledger: 20 shipped features (FEATURES.json)
- calibration (broke a route, loop must re-fix it): FAIL (Warning: OPENAI_API_KEY not set. AI features will mock response.
PROBE FAIL: GET /api/models: NOT REGISTERED on the app (defined but not wired - forgot include_)

## Branch log
```
2e872ef agent: ledger/log update
7b49549 agent: ledger/log update
56cd767 agent: ledger/log update
e82652a agent: ledger/log update
f325b68 agent: ledger/log update
8de7fe0 agent: ledger/log update
69110d3 agent: ledger/log update
056ee90 merge: Compute price deviation using saved-search statistics
e6d2c4e agent attempt 2: Compute price deviation using saved-search statistics
40c8682 agent attempt 1: Compute price deviation using saved-search statistics
ef47540 agent: ledger/log update
b2d0b74 agent: ledger/log update
9badb86 agent: ledger/log update
4e2f0d5 agent: ledger/log update
5f029bb agent: ledger/log update
98a7c30 agent: ledger/log update
58581c8 agent: ledger/log update
9d8ceaf agent: ledger/log update
eaf52a2 agent: ledger/log update
87503d5 agent: ledger/log update
```

Each improvement was gated by syntax+test-files+integration+dup-routes+tests+probe, then an adversarial critic.
Unmerged attempts are on `agent/imp-N` branches for review. See IMPROVEMENTS.md for rationale.
