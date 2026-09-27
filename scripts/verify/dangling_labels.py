#!/usr/bin/env python3
"""Find lettered citation markers that resolve to no entry in their article.

WHY THIS EXISTS. On 2026-09-08 traditions/canoe-trips.md was found using the
marker ^mc five times -- for the article's whole 1945-1964 chronology, the tiered
route system, the 1959 choice of La Verendrye, the Lac Landron lease -- with no
entry "mc" anywhere in the file. Every verify check passed. verify_harness
resolves NUMERIC markers and ignores lettered ones, so a lettered marker can
point at nothing indefinitely; the uncited-entries report saw the other half of
the same defect, the McMorris entry sitting unpointed-at, and did not connect
them. A whole-wiki sweep then found four more articles in the same state,
including six uses of ^mc in history/founding-1894.md with no McMorris entry at
all. See f_5730, f_5731.

HOW IT DECIDES. Markers are `^label` in the body, where label starts with a
letter (so ^12 and the ordinal suffixes in "4^th" are not markers). An entry is
"defined" if the label appears anywhere in the article's `## Sources` section as
a standalone token -- deliberately loose, because the wiki writes labels three
ways (`- ^kw:`, `- **nb59** --`, `- **^ymcayb** --`) and a strict pattern
produced false positives on all three. Loose here means a real dangling marker
is never missed and a label that merely occurs in prose inside the section is
forgiven, which is the right way round for a check whose findings each need
reading.

BLOCKING. Unlike uncited_sources, this has no legitimate case: a marker that
resolves to nothing is always wrong, and the backlog was cleared to zero the day
the check was written. If it ever fires, either the entry was dropped in an edit
or the label was mistyped -- and the fix is to restore the entry, never to delete
the marker, since the marker is evidence that a claim was sourced.
"""
import re
import sys
from pathlib import Path

WIKI = Path(__file__).resolve().parents[2] / "wiki"
ORDINALS = {"th", "st", "nd", "rd"}


def dangling(path: Path):
    text = path.read_text(encoding="utf-8")
    if "\n## Sources" not in text:
        return []
    body, rest = text.split("\n## Sources", 1)
    sources = rest.split("\n## ", 1)[0]
    marks = set(re.findall(r"\^([a-z][a-z0-9]{0,7})\b", body)) - ORDINALS
    return sorted(
        m for m in marks
        if not re.search(r"(?<![a-z0-9])" + re.escape(m) + r"(?![a-z0-9])", sources)
    )


def main() -> int:
    print("=" * 70)
    print("DANGLING LETTERED MARKERS")
    print("=" * 70)
    findings = []
    for path in sorted(WIKI.rglob("*.md")):
        missing = dangling(path)
        if missing:
            findings.append((path, missing))
    if not findings:
        print("  No lettered marker resolves to a missing entry.")
        return 0
    total = sum(len(m) for _, m in findings)
    print(f"  {total} marker(s) in {len(findings)} article(s) point at no entry.")
    for path, missing in findings:
        print(f"     {path.relative_to(WIKI.parent)}: {', '.join('^' + m for m in missing)}")
    print("  Restore the entry. Do not delete the marker -- it is evidence that")
    print("  the claim was sourced, and deleting it loses the provenance.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
