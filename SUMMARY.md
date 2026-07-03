# CraigSail Agent Run — Summary (2026-07-03T04:29:28.142507)

- cycles: 3 | merged: 2 | kept-unmerged (review): 1
- final tests on agent/loop: 34 passed / 0 failed
- feature ledger: 29 shipped features (FEATURES.json)
- calibration (broke something, loop must re-fix it): skipped (no time)
- config: lang=python fastapi=True scope=backend tests=python -m pytest -q

## Branch log
```
15fe1ab agent: ledger/log update
dae107d agent: ledger/log update
b156e0a merge: Delete stub create‑saved-search endpoint
9bca577 agent attempt 1: Delete stub create‑saved-search endpoint
3cce690 agent: ledger/log update
aa91907 merge: Delete literal‑path saved-search runner endpoint
f26e04b agent attempt 2: Delete literal‑path saved-search runner endpoint
7199ed2 agent: run summary
d916e8b agent: ledger/log update
1336c9b merge: owner mac-main
34c5170 sync: owner/control cycle files
bf01f3b Tuning: line-surgery rule for large-file edits (coder no-ops on whole-file rewrites of 682-line main.py)
ad2ba16 agent: run summary
82b34eb agent: ledger/log update
0dbdd94 merge: owner mac-main
db4478a sync: owner/control cycle files
7da22ed Control brief round 3: dead-code purge + endpoint repairs (audit findings), saved-search store unification, listing persistence (make deviation real), re-scoped scheduler + scam-score epics with embedded test skeletons; ISSUES controller findings; three new tuning rules
914dcf9 agent: run summary
090214d agent: ledger/log update
c022d89 agent: ledger/log update
```

Each improvement was gated by syntax+test-files+integration+dup-routes+tests+probe, then an adversarial critic.
Unmerged attempts are on `agent/imp-N` branches for review. See IMPROVEMENTS.md for rationale and LOOP_REPORT.json for per-attempt gate outcomes.
