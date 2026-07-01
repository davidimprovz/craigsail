# CraigSail Agent Run — Summary (2026-07-01T22:44:08.273183)

- cycles: 6 | merged: 4 | kept-unmerged (review): 2
- final tests on agent/overnight: 0 passed / 5 failed
- feature ledger: 4 shipped features (FEATURES.json)
- calibration (broke a route, loop must re-fix it): PASS

## Branch log
```
6fa2a8e agent: ledger/log update
cdd41a5 merge: Add prioritize_listings function to rank listings by priority_score
2092299 agent attempt 1: Add prioritize_listings function to rank listings by priority_score
3245982 agent: ledger/log update
07ddc92 merge: Add priority_score field to Listing model
1aa40fb agent attempt 2: Add priority_score field to Listing model
f8e2d47 agent attempt 1: Add priority_score field to Listing model
7effc97 agent: ledger/log update
85a4d21 agent: ledger/log update
78f6e6e merge: Add generate_forecast utility function
6c36da0 agent attempt 2: Add generate_forecast utility function
77eb2ac agent: ledger/log update
99eda6e merge: Add Forecast field to Listing model
b9c2925 agent attempt 1: Add Forecast field to Listing model
069c2f9 agent: ledger/log update
b792de8 snapshot: starting state
833a692 merge: Add predictive_alert_enabled flag to Alert model
e799e23 agent: Add predictive_alert_enabled flag to Alert model
c80b3b0 merge: Define ForecastResponse Pydantic model
300724f agent: Define ForecastResponse Pydantic model
```

Each improvement was gated by syntax+test-files+integration+dup-routes+tests+probe, then an adversarial critic.
Unmerged attempts are on `agent/imp-N` branches for review. See IMPROVEMENTS.md for rationale.
