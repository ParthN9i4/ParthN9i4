"""Minimal test harness — no pytest dependency.

Usage inside an exercise file:
    from check import check
    check("test name", got, expected)
    check("boolean test", condition)
"""

import sys

_pass = _fail = 0


def check(name, got, expected=True, tol=None):
    """Assert got == expected (or |got - expected| < tol for floats)."""
    global _pass, _fail
    ok = False
    if tol is not None:
        try:
            if hasattr(got, '__iter__') and hasattr(expected, '__iter__'):
                ok = all(abs(a - b) < tol for a, b in zip(got, expected))
            else:
                ok = abs(got - expected) < tol
        except TypeError:
            ok = False
    else:
        ok = (got == expected)

    if ok:
        _pass += 1
        print(f"  PASS  {name}")
    else:
        _fail += 1
        print(f"  FAIL  {name}")
        print(f"        got:      {got}")
        print(f"        expected: {expected}")


def summary():
    """Print pass/fail counts and exit with appropriate code."""
    total = _pass + _fail
    print(f"\n{'='*40}")
    print(f"  {_pass}/{total} passed", end="")
    if _fail:
        print(f"  ({_fail} FAILED)")
    else:
        print("  — all good!")
    print(f"{'='*40}")
    sys.exit(1 if _fail else 0)
