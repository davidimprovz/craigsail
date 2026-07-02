# ISSUES — craigsail (auto-check 2026-07-02, jetson/loop @ b5bd097)

Mechanical post-pull findings. Controller turns these into the next [maintenance]
epic in EPICS.md; the fix cycle re-runs THIS project before the queue advances.

- calibration FAILED this run (gates/coder self-check broken)

## Controller review (deep diff, 2026-07-02 evening)
- backend/app/reports.py: build_export_records calls db.query(AlertORM) but the module
  no longer imports AlertORM/ExportItem (the ImportError-fallback "fix" deleted the
  import instead of simplifying it) — latent NameError whenever the function is called.
- tests/test_deviation_calculation.py imports `backend.app.reports` (dual module
  identity vs the app's `app.reports`) — banned pattern, still present after merge.
- tests/test_saved_search_scheduled.py third test still uses conditional model_fields
  introspection (subtask 4 stalled).
- Harness (fixed in improve.py, deployed): repeat-diff detection broke retries at
  attempt 2, so the fresh-resample escalation never ran — killed 8/8 value subtasks;
  now escalates instead of stopping. Test-only retries now include a code skeleton.
- Calibration FAIL 2 runs in a row (one-shot route-repair not performed) — watch next run.

All items above are encoded as epic `cleanup-jul2-round2` in EPICS.md (round-2 fix cycle).
