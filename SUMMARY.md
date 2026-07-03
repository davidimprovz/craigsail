# CraigSail Agent Run — Summary (2026-07-03T03:46:55.253945)

- cycles: 1 | merged: 0 | kept-unmerged (review): 1
- final tests on agent/loop: 34 passed / 0 failed
- feature ledger: 27 shipped features (FEATURES.json)
- calibration (broke something, loop must re-fix it): skipped (no time)
- config: lang=python fastapi=True scope=backend tests=python -m pytest -q

## Branch log
```
82b34eb agent: ledger/log update
0dbdd94 merge: owner mac-main
db4478a sync: owner/control cycle files
7da22ed Control brief round 3: dead-code purge + endpoint repairs (audit findings), saved-search store unification, listing persistence (make deviation real), re-scoped scheduler + scam-score epics with embedded test skeletons; ISSUES controller findings; three new tuning rules
914dcf9 agent: run summary
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
```

Each improvement was gated by syntax+test-files+integration+dup-routes+tests+probe, then an adversarial critic.
Unmerged attempts are on `agent/imp-N` branches for review. See IMPROVEMENTS.md for rationale and LOOP_REPORT.json for per-attempt gate outcomes.
