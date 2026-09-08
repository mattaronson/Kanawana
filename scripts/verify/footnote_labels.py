"""Footnote labels: duplicates, and lettered markers with no entry.

WHY THIS EXISTS. On 2026-09-05 a new source was added to
canadian-camping-movement.md as "8t." — a label that article already used —
and a careless replace then re-pointed two existing ^8t markers at the new
entry. Nothing caught it. verify_harness's A1/B/C read Sources entries with
`^(\\d+)\\. `, so the sixty-eight LETTERED sub-entries in that article (8a, 8b,
… 8bq) are invisible to them: a duplicate among those changes no count and
resolves no differently, and two markers can quietly come to mean something
else than they did.

This checks what those cannot:

  L1. No label appears twice in one article's Sources section, numeric or
      lettered.
  L2. Every ^label marker in the body has an entry with that label. Numeric
      markers are already class B in the harness; this covers the lettered
      ones, which nothing did.
  L3. No entry sits outside the Sources section. An entry appended after
      "## Research Notes" — or, as happened the same day, inside that
      section's HTML comment — is not part of the list, and a reader
      following the marker finds nothing.

Advisory on purpose. It is new, and a check that fails on its first day for
reasons nobody has looked at gets switched off rather than fixed.
"""
import io
import os
import re
import sys
import glob
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HEAD = re.compile(r'^##\s+Sources\s*$', re.M)
NEXT_H2 = re.compile(r'^##\s', re.M)
ENTRY = re.compile(r'^(\d{1,3}[a-z]{0,3})\.\s', re.M)
MARKER = re.compile(r'\^(\d{1,3}[a-z]{0,3})\b')
COMMENT = re.compile(r'(?s)<!--.*?-->')


def check(rel):
    out = []
    text = io.open(os.path.join(ROOT, rel), encoding='utf-8').read()
    m = HEAD.search(text)
    if not m:
        return out
    nxt = NEXT_H2.search(text, m.end())
    end = nxt.start() if nxt else len(text)
    section, after = text[m.end():end], text[end:]
    body = text[:m.start()]

    labels = ENTRY.findall(section)
    dup = sorted(k for k, v in collections.Counter(labels).items() if v > 1)
    if dup:
        out.append('%s  L1: label used twice in Sources: %s' % (rel, dup))

    # L2, lettered markers only -- numeric ones are the harness's class B.
    have = set(labels)
    used = {x for x in MARKER.findall(COMMENT.sub(' ', body)) if not x.isdigit()}
    missing = sorted(used - have)
    if missing:
        out.append('%s  L2: lettered marker with no Sources entry: %s' % (rel, missing))

    # L3: an entry that landed after the Sources section, or inside a comment
    # in it. Only flags labels the body actually cites, so a numbered list in
    # some later section is not mistaken for a stray source.
    stray = sorted({x for x in ENTRY.findall(after) if x in used}
                   | {x for x in ENTRY.findall(' '.join(COMMENT.findall(section))) if x in used})
    if stray:
        out.append('%s  L3: cited entry sits outside the Sources list: %s' % (rel, stray))
    return out


def main():
    bad = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'wiki', '**', '*.md'), recursive=True)):
        bad += check(os.path.relpath(f, ROOT))
    print('=' * 70)
    print('FOOTNOTE LABELS -- duplicates, lettered markers, strays')
    print('=' * 70)
    if not bad:
        print('  every label is unique, every lettered marker resolves, no entry is stray')
        return 0
    print('  [advisory] %d finding(s):' % len(bad))
    for b in bad:
        print('  - %s' % b)
    return 0


sys.exit(main())
