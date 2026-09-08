#!/usr/bin/env python3
"""Find a person given two different year-spans in two different articles.

WHY THIS EXISTS. On 2026-09-07 people/bruce-netherwood.md corrected his
directorship from "1988 to 1994" to "1989 to 1994" and his brother Jay's from
"1986-1987" to "1986 to 1989", marked the old reading SUPERSEDED in its own
text, and stopped there. history/centennial-1994.md -- E1-reviewed, and one of
five articles naming him -- went on printing 1988 and 1986-1987 for another day,
until the 1995 annual report turned up saying "served as Kamp Director from 1989
to 1994" and the discrepancy was noticed by hand. ALL TEN CHECKS PASSED THROUGHOUT.
Nothing in the suite compares a claim in one article against the same claim in
another, so A CORRECTION THAT STOPS AT THE ARTICLE WHERE IT WAS FOUND LEAVES NO
TRACE ANYWHERE THAT IT DID NOT TRAVEL. See f_5772.

WHAT IT LOOKS FOR, and why it is narrow on purpose. Any person can honestly
carry several spans -- a directorship, a committee tenure, a later career, a
life. Two spans are only interesting when they NEARLY agree: they share one
endpoint and differ at the other by one or two years. That is the shape of a
transcription slip or an uncarried correction; it is not the shape of a
directorship sitting beside a committee tenure. A first whole-wiki run with a
90-character window and no name filter returned 272 names and was unusable --
it matched "Kamp Kanawana 1894-1967" as a person. Restricting the names to
wiki/people article ids and the pairs to near-misses takes it to a readable
number.

WHY IT CANNOT BE AUTO-FIXED, AND WHY IT IS ADVISORY. A near-miss pair is at
least four things and only reading tells them apart:

  1. AN UNCARRIED CORRECTION -- the case above. FIX: carry it, and say where.
  2. TWO REAL SPANS that happen to nearly agree: a man who directed 1974-1979
     and chaired a committee 1975-1979. LEGITIMATE.
  3. A DOCUMENTED AMBIGUITY the wiki is deliberately holding open, with both
     readings printed and a conflict record behind it. gary-white carries
     2000-2001, 2000-2002 and 2001-2002 on purpose. LEGITIMATE, and forcing
     one would destroy the evidence.
  4. THE CHECK'S OWN WINDOW picking up a range that belongs to the sentence
     rather than to the name 70 characters earlier. A false positive.

So this reports and NEVER fixes, and the count will not reach zero.

WHAT THE FIRST RUN FOUND, 2026-09-08: thirteen pairs across nine people, and
FOUR OF THEM ARE UNCARRIED CORRECTIONS OLDER THAN THE ONE THAT PROMPTED THIS.

  - A. Ross Seaman. The directors index says "**1959-1968** — Extended from
    1959-1967 on 2026-08-14," with the branch officers table and every YMCA Year
    Book volume behind it. NINE OTHER ARTICLES still say 1959-1967:
    a-ross-seaman.md itself (three times), postwar-gap.md (four),
    timeline-overview.md (two), cit-lit-program.md, order-of-owens.md,
    taylor-statten.md, camp-perrot.md, derek-walsh.md,
    les-voyageurs-de-la-verendrye.md.
  - Greig Macdiarmid. The index says 1935-1939; boys-work-secretaries.md,
    nelson-mcewen.md (twice), camp-becsies.md and timeline-overview.md say
    1935-1938.
  - G. David Twynam. The index says 1979-1982; timeline-overview.md says
    1979-1980.
  - Bruce Netherwood. Fixed in centennial-1994.md the same day, but the
    directors index's OWN plaque note still reads "(1988-1994)".

All four were corrected in people/directors-index.md ON THE SAME DAY,
2026-08-14, and none of the four travelled. bruce-netherwood.md even says so in
its own superseded note -- "those dates were corrected in the directors index on
2026-08-14 and this article did not catch up" -- so the project had already met
this failure once, for one person, and did not generalise it. That is what an
instrument is for.

The remaining rows are legitimate: gary-white's three spans are a documented
ambiguity held open on purpose, roy-locke's 1947-1954 and 1948-1954 are a
documented span against an open question about which seasons he was on site,
harold-cross's 1938-1957 is a manuscript's date range and not a tenure, and the
billy-ball and rob-braide pairs are this window catching a range that belongs to
a different person in the same sentence.

A RANGE QUOTED INSIDE A CORRECTION is skipped: "corrected from 1988-1994",
"this sentence read \"from 1988 to 1994\"", a struck-through open question. On its
first run this check reported the very fix that prompted it, because the
superseded span is still on the page and is supposed to be. See HISTORICAL.

LIMITS, STATED SO THEY ARE NOT MISREAD. It sees a person only if wiki/people
holds an article whose id ends in their surname, so anyone without an article
is invisible to it. It matches on SURNAME ALONE, which in this project is a
caution and not a formality -- see the three W. H. Balls in the directors index.
It reads a range only in the forms "1988-1994", "1988–1994" and "1988 to 1994".
A span given as prose ("from 1988 until his death") is invisible.
"""
import os
import re
import sys
from collections import defaultdict

BASELINE = 13   # 2026-09-08, first whole-wiki run; all thirteen read, see below

RANGE = re.compile(r'\b(1[89]\d\d|20\d\d)\s*(?:-|–|—|to )\s*(1[89]\d\d|20\d\d)\b')
WINDOW = 70

# A range QUOTED INSIDE A CORRECTION is not drift, it is the record of the fix.
# This check found its own repair work on the first run: centennial-1994.md now
# says 'this sentence read "from 1988 to 1994" until today', and the directors
# index says "Corrected from 1988-1994", so the superseded span is still on the
# page and still matches. Suppressing it is not hiding anything -- the article
# states the correction in the same breath, which is the opposite of drift.
HISTORICAL = re.compile(
    r'(corrected from|superseded|this sentence read|previously read|had it as'
    r'|used to read|until 2026|read ["“]|~~)', re.I)

# Collective and index articles: their id's last segment is not a surname, so
# it matches half the wiki. Excluded by name rather than by heuristic, because
# a heuristic here would silently drop a real person one day.
NOT_PEOPLE = {
    'directors-index', 'multi-year-index', 'notable-alumni', 'boys-work-secretaries',
    'cushing-family', 'page-family', 'kidd-brothers',
}


def people_surnames():
    out = {}
    for root, _dirs, files in os.walk('wiki/people'):
        for name in sorted(files):
            if not name.endswith('.md'):
                continue
            aid = name[:-3]
            if aid in NOT_PEOPLE:
                continue
            surname = aid.rsplit('-', 1)[-1]
            if len(surname) < 4:          # initials-only tails
                continue
            out[aid] = re.compile(r'(?<![A-Za-z])' + re.escape(surname) + r'(?![A-Za-z])',
                                  re.I)
    return out


def main() -> int:
    pats = people_surnames()
    seen = defaultdict(set)
    for root, _dirs, files in os.walk('wiki'):
        for name in sorted(files):
            if not name.endswith('.md'):
                continue
            path = os.path.join(root, name)
            with open(path, encoding='utf-8') as fh:
                text = fh.read()
            for m in RANGE.finditer(text):
                win = text[max(0, m.start() - WINDOW):m.start()]
                if HISTORICAL.search(win):
                    continue
                for aid, pat in pats.items():
                    if pat.search(win):
                        seen[aid].add((int(m.group(1)), int(m.group(2)), path))

    rows = []
    for aid, hits in seen.items():
        spans = defaultdict(set)
        for lo, hi, path in hits:
            spans[(lo, hi)].add(path)
        keys = sorted(spans)
        near = []
        for i, x in enumerate(keys):
            for y in keys[i + 1:]:
                # share exactly one endpoint, differ by 1-2 at the other
                if (x[0] == y[0]) == (x[1] == y[1]):
                    continue
                if abs(x[0] - y[0]) > 2 or abs(x[1] - y[1]) > 2:
                    continue
                # only interesting ACROSS files: one article free to hold both
                # readings side by side is discussing the ambiguity, not drifting
                if spans[x] | spans[y] == spans[x] & spans[y] and len(spans[x]) == 1:
                    continue
                near.append((x, y))
        if near:
            rows.append((len(near), aid, near, sorted({p for _, _, p in hits})))

    total = sum(r[0] for r in rows)
    print('=' * 70)
    print('NEAR-MISS YEAR SPANS FOR THE SAME PERSON (advisory)')
    print('=' * 70)
    if not rows:
        print('  PASS -- no person carries two nearly-agreeing spans')
        return 0
    print('  %d near-miss pair(s) across %d person article(s).' % (total, len(rows)))
    print('  Baseline 2026-09-08 was %d. %s' % (
        BASELINE,
        'UP BY %d -- a span has been edited in one place and not another.' % (total - BASELINE)
        if total > BASELINE else 'Not above baseline.'))
    for count, aid, near, paths in sorted(rows, reverse=True):
        pairs = '; '.join('%d-%d vs %d-%d' % (x[0], x[1], y[0], y[1]) for x, y in near[:4])
        more = '' if len(near) <= 4 else ' …+%d' % (len(near) - 4)
        print('    %3d  %-24s %s%s' % (count, aid, pairs, more))
        print('         in: %s' % ', '.join(os.path.basename(p) for p in paths[:6]))
    print('  Each is an uncarried correction, two real spans that nearly agree,')
    print('  an ambiguity held open on purpose, or this window misreading a range.')
    print('  Only reading tells them apart.')
    return 0


sys.exit(main())
