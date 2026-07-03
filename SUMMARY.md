# CraigSail Agent Run — Summary (2026-07-03T17:03:46.749874)

- cycles: 23 | merged: 7 | kept-unmerged (review): 16
- final tests on agent/loop: 51 passed / 0 failed
- feature ledger: 46 shipped features (FEATURES.json)
- calibration (broke something, loop must re-fix it): PASS
- config: lang=python fastapi=True scope=backend tests=python -m pytest -q

## Branch log
```
697903b agent: ledger/log update
7b3b12c merge: Expose CSV endpoint with risk_score column
94934ce agent attempt 2: Expose CSV endpoint with risk_score column
7deb066 agent attempt 1: Expose CSV endpoint with risk_score column
722fedb agent: ledger/log update
8b9fbc9 agent: ledger/log update
9c1e926 agent: ledger/log update
62a4fbd agent: ledger/log update
e211868 merge: Add build_export_records import to main.py
02b58c2 agent attempt 1: Add build_export_records import to main.py
7e51f40 agent: ledger/log update
6778280 agent: ledger/log update
33ecc3d agent: ledger/log update
7b6f0ef merge: Add pure stdlib scam risk scoring function
fb3d99c agent attempt 1: Add pure stdlib scam risk scoring function
e7b29e4 agent: ledger/log update
7d7440f agent: ledger/log update
69ff2fe agent: ledger/log update
668db45 agent: ledger/log update
2a1496c agent: ledger/log update
```

Each improvement was gated by syntax+test-files+integration+dup-routes+tests+probe, then an adversarial critic.
Unmerged attempts are on `agent/imp-N` branches for review. See IMPROVEMENTS.md for rationale and LOOP_REPORT.json for per-attempt gate outcomes.
