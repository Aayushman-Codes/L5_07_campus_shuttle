# Lab 5 Report: Static Code Analysis (shuttle_system.py)

## Summary

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.25 / 10 (18 messages) | **10.00 / 10** (0) |
| Bandit | 2 issues (B110, B311, both Low) | **0** |
| Flake8 | 10 violations | **0** |

Commits (one per tool): `Fix Bandit findings`, `Fix Pylint findings`, `Fix Flake8 findings`.
Reports are in `reports/before/` and `reports/after/`.

## Issue table

| Issue | Type | Line(s) (original) | Description | Fix Approach |
|-------|------|------|-------------|--------------|
| Try / except / pass (Bandit B110) | Security / Bug | 26-30 | Errors in `underused_routes` were silently swallowed. | Removed the try block; skip routes with no trips explicitly. |
| Weak PRNG (Bandit B311) | Security | 35 | `random.choice` is not cryptographically secure. | Switched to `secrets.choice`. |
| Bare except (Pylint W0702, Flake8 E722) | Bug | 29 | Catches everything, including KeyboardInterrupt, and hides real errors. | Removed; the cause (division by zero on empty trips) is handled by a check. |
| Mutable default argument (W0102) | Bug | 11 | `logs=[]` is shared across calls. | Default `None`, create a new list inside. |
| Unvalidated passenger count | Bug (not tool-flagged) | 49-50 | `-6` and `"full"` were stored; `"full"` would break averages. | Raise `ValueError` for non-integer/negative counts; `main` reports rejected entries. |
| Crash on removed route | Bug (not tool-flagged) | 55-58 | `average_load("R3")` after `remove_route("R3")` raised KeyError. | Guard with a membership check; `average_load` returns None when no trips. |
| Unchecked user input | Bug (not tool-flagged) | 57 | An unknown route typed at the prompt raised KeyError. | Check `choice in routes`. |
| Global statement / needless reload (W0603) | Design | 38, 42-43 | Function rebinds the global `routes` by re-reading the file it just wrote. | Dropped the reload; function only writes. |
| Files not closed safely, no encoding (W1514, R1732) | Resource leak | 39-43 | Manual `open`/`close`; the read handle was never closed. | `with open(..., encoding="utf-8")` and `json.dump`. |
| Old-style `%` formatting (C0209) | Style | 13 | Harder to read than f-strings. | f-string. |
| Unused argument (W0613) | Code smell | 33 | `route_id` never used in `assignDriver`. | Removed the parameter. |
| Non-snake_case name (C0103) | Style | 33 | `assignDriver`. | Renamed to `assign_driver`. |
| Missing docstrings (C0114, C0116) | Docs | 1, 11, 16, ... | Module and 7 functions had none. | Added docstrings. |
| Blank lines (E302, E305) | Style | 11-60 | Need 2 blank lines around top-level defs. | Added blank lines. |
| Line too long (E501) | Style | 13 | 82 > 79 characters. | Resolved by the shorter f-string. |
| Missing `__main__` guard | Design | 60 | `main()` ran on import. | Added `if __name__ == "__main__":`. |

## Behaviour change to note

The demo now sends the bad inputs (-6 and "full") to route R3 and rejects them, so R2's trips are `[4]` and R3 has none. The program runs to the end without a traceback.
