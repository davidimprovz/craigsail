# ISSUES — craigsail (auto-check 2026-07-02, jetson/loop @ 914dcf9)

Mechanical post-pull findings. Controller turns these into the next [maintenance]
epic in EPICS.md; the fix cycle re-runs THIS project before the queue advances.

- added a try/except ImportError fallback import (banned by LOOP_TUNING)
- calibration FAILED this run (gates/coder self-check broken)

## Controller review round 3 (2026-07-03, jetson/loop @ 914dcf9)
- The 'except ImportError' mechanical flag above was a FALSE POSITIVE (the check grepped
  ledger prose naming the fixed pattern; check now scopes code patterns to *.py diffs).
- reports.py `_deviation_for_alert` is HOLLOW: always returns 0.0 (calls the deviation
  fn with listing=None; the None-guard returns 0.0). Its test patches the helper, so the
  suite can't see it. Real fix = listing persistence (EPICS round-3 epic 4).
- reports.py contains a self-import (`from app.reports import ...` inside its own
  module) and an unused `Listing` import — repairs epic 2(e).
- Calibration FAIL #4 in a row (GET /api/models one-shot repair never lands). Pattern,
  not noise: single-attempt calibration under-measures; consider giving calibration the
  retry ladder (morning item — not changed mid-experiment).
- Legacy audit items (123-route, echo stub, theater endpoints, .dict() crash, int/UUID
  delete, Path-param toggle, forecast NameError, three-store split) → round-3 epics 1-3.
