# LOOP_TUNING — craigsail (controller-revised 2026-07-02, from the jul-2 run review)

- NEVER assign attributes to a class after its definition to satisfy hasattr/verification
  (e.g. `Model.field = default` after a pydantic class). Declare fields inside the class
  body only; if a check needs an attribute, the check is wrong — test behavior instead.
- NEVER write try/except ImportError fallback imports. Backend code always imports as
  `from app.<module> import ...` (backend/ is on sys.path); tests import the same way.
- A new helper function MUST be called from a route or service in the SAME subtask.
  If you cannot wire it, do not add it.
- Tests assert BEHAVIOR: real values, status codes, model_dump contents. Never
  hasattr(...), never model_fields introspection, never asserts inside `if` blocks.
- Guard every division by a value that can be 0 (return a defined default).
- Prefer extending an existing module over creating a new one; one concern per file.
- When told "the implementation works, only a test is missing": write ONLY the new test
  file — do not re-edit app code, do not re-explore. Adapt the skeleton you are given.
- When removing a bad import pattern, KEEP the import the code needs (simplify it,
  never delete symbols that are still referenced).
- NEVER import a module from inside itself (`from app.X import f` within app/X.py) —
  call same-module functions directly.
- A new field/column must carry REAL data. If the data source does not exist, return
  None and say so in IMPROVEMENTS.md — never hardcode 0.0/placeholder values to satisfy
  a check; hollow integrations are rejected on review.
- When a brief says DELETE, remove the code entirely — no commented-out remains.
