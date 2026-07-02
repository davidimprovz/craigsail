# CraigSail Agent Run — Summary (2026-07-02T11:16:48.852591)

- cycles: 55 | merged: 10 | kept-unmerged (review): 45
- final tests on agent/overnight: 0 passed / 5 failed
- feature ledger: 18 shipped features (FEATURES.json)
- calibration (broke a route, loop must re-fix it): PASS

## Branch log
```
759dbcc agent: ledger/log update
30ae303 agent: ledger/log update
ee982cb agent: ledger/log update
fed75be agent: ledger/log update
a63db65 agent: ledger/log update
6ba26e9 agent: ledger/log update
5d21f7c agent: ledger/log update
e6bfdac agent: ledger/log update
7f92496 agent: ledger/log update
74fe5a7 agent: ledger/log update
543deba agent: ledger/log update
fd5e1eb agent: ledger/log update
4b38031 merge: Add export data builder function
641327a agent attempt 1: Add export data builder function
e605518 agent: ledger/log update
9e9d928 merge: Add ExportItem model
2e11eb2 agent attempt 1: Add ExportItem model
a2a7b72 agent: ledger/log update
6535126 agent: ledger/log update
00b567f merge: Implement analysis logic in CraigAgent
```

Each improvement was gated by syntax+test-files+integration+dup-routes+tests+probe, then an adversarial critic.
Unmerged attempts are on `agent/imp-N` branches for review. See IMPROVEMENTS.md for rationale.
