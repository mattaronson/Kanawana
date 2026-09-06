#!/usr/bin/env python3
"""Run the project's checks the way CI runs them, and EXIT NONZERO IF ANY FAILS.

Why this exists. The seven checks have always been run by hand, in an ad-hoc
shell loop, and on 2026-09-06 that loop turned out to print "FAIL" while
returning success -- so a `... && git commit && git push` chain after it pushed a
commit that CI then failed on A2 ninety seconds later. CI was doing its job; the
local check was not a gate, only a display. This makes the local check a gate.

It runs exactly the steps in .github/workflows/verify.yml, in that order, so a
clean run here means a clean run there. Two of them (staleness, footnote_labels)
are advisory and exit 0 by design; they are still run, because their output is
worth reading, and their exit code is still honoured, because if one ever starts
failing that is news.

Usage:
    python scripts/verify/all.py            # summary lines only
    python scripts/verify/all.py --verbose  # full output of every check
"""
import subprocess
import sys
from pathlib import Path

# The order is CI's order. Keep it that way: a divergence here is a divergence
# in what "passing" means locally versus on the branch.
CHECKS = [
    ("data_integrity",   "Data integrity"),
    ("verify_harness",   "Citation and link integrity"),
    ("consistency",      "Internal consistency"),
    ("citation_aim",     "Citation aim"),
    ("staleness",        "Staleness (advisory)"),
    ("footnote_labels",  "Footnote labels (advisory)"),
    ("restricted_guard", "Embargo labelling"),
]

def main() -> int:
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    here = Path(__file__).resolve().parent
    failed = []

    for script, label in CHECKS:
        path = here / f"{script}.py"
        if not path.exists():
            print(f"  {label:32s} MISSING  ({path})")
            failed.append(script)
            continue
        proc = subprocess.run(
            [sys.executable, str(path)],
            capture_output=True,
            text=True,
        )
        ok = proc.returncode == 0
        print(f"  {label:32s} {'ok' if ok else 'FAILED'}")
        if verbose or not ok:
            body = (proc.stdout or "") + (proc.stderr or "")
            for line in body.rstrip().splitlines():
                print(f"      {line}")
        if not ok:
            failed.append(script)

    print()
    if failed:
        print(f"FAILED: {', '.join(failed)}")
        print("Do not commit. CI runs these same checks and will fail the same way.")
        return 1
    print("All checks pass. This is the same set CI runs, in the same order.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
