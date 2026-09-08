#!/usr/bin/env python3
"""Find numbered source entries that no citation marker ever points at.

WHY THIS EXISTS. On 2026-09-07 a spinout moved 1,143 words out of
people/directors-index.md and stranded source entry 62, whose only two citations
left with the moved paragraphs. ALL EIGHT VERIFY CHECKS PASSED WITH THE ORPHAN
IN PLACE. verify_harness tests that every MARKER resolves to an ENTRY; the
reverse -- every entry reached by a marker -- was tested by nothing, so an entry
could sit uncited indefinitely. It was found by hand, following the mechanics
list in project-docs/spinout-rule.md.

WHY AN UNCITED ENTRY CANNOT BE AUTO-FIXED. It is SIX quite different things,
and only reading tells them apart. The first working pass, 2026-09-07, met the
first five inside a dozen articles; the sixth turned up on 2026-09-08:

  1. A citation LOST or never applied, so some claim in the article is now
     unsourced and the entry is the evidence that it once was not. FIX: mark the
     claim. (traditions-and-culture 31: the Shawbridge null was written into an
     open question and the entry recording it was never pointed at.)
  2. An entry added in anticipation of a passage NEVER WRITTEN. FIX: write the
     passage, or remove the entry.
  3. A HIDDEN NULL -- an entry whose whole content is a search that found
     nothing, sitting in a source list, which is the one place no reader looks
     for a null. FIX: put the null in the body where it can be found.
     (maureen-mcbride 3.)
  4. A TOMBSTONE, deliberately retained to record an entry that was withdrawn.
     LEGITIMATELY UNCITED -- do not "fix" it. (winter-programming 4, which says
     so in its own text: "Superseded 2026-09-06.")
  5. A POINTER rather than a source: to a cache file, to a conflict record, or
     to a lead not yet consulted. LEGITIMATELY UNCITED. (wallace-forgie 5 and 6
     point at a cache path and at conflict c_069; edgar-smee 8 is "Concordia
     University Archives... Potential staff records," a lead.)
  6. A SUPERSEDED GENERIC -- a collection-level entry ("YMCA of Montreal Annual
     Reports", "Fong's biography, borrowable") that a later pass replaced with
     entries naming the individual volume or the passage actually recovered.
     LEGITIMATELY UNCITED, and the opposite of a defect: it is the citation
     improving. FIX: say in the entry that it was superseded and by which note.
     Do not delete it and do not force a marker onto it. (t-duncan-patton 3,
     superseded by notes 15-17; j-w-mcconnell 5 by note 14; camp-perrot 2 by
     note 8. Found 2026-09-08, f_5729.)

Deleting all of them would risk (1); keeping all of them guarantees (2) and (3);
forcing a marker onto (4), (5) or (6) would assert a provenance that does not exist.
So this reports and NEVER fixes, and the count will never reach zero -- some of
these entries are supposed to be here.

That last point is why this stays advisory even after the backlog is worked: the
number to watch is the DELTA, not the total.

A SIXTH THING AN UNCITED ENTRY CAN BE, and the reason this check earns its keep
beyond tidiness: THE SHADOW OF A MIS-AIMED MARKER SOMEWHERE ELSE IN THE SAME
FILE. camp-oolahwan.md cited an interview of 8 March 1980, published 1982, to
entry 26 -- which is a different article by the same author from December 1979.
The interview is entry 27, and entry 27 showed up here as uncited because the
marker that should have pointed at it had been typed one lower. verify_harness
saw nothing wrong: ^26 resolves. So when an entry is uncited, look for a
NEIGHBOURING number carrying a claim it does not support.

That cannot be automated. A check comparing a citing sentence against its source
entry was written on the model of citation_aim.py and DISCARDED the same hour:
516 findings, every sampled one a correct citation, because a source entry is
bibliographic and describes the document rather than what the document says.
citation_aim works only because a KB fact's claim restates the content. See
f_5567.

ADVISORY, ON THE PRECEDENT section_headings.py SET. The first whole-wiki run
found 136 uncited entries across 34 articles -- places-and-locations.md alone
has 28 entries and cites 9 of them. That is a backlog, and a blocking check
against a backlog trains everyone to ignore the output. Queued as p_484; make
this blocking when it clears. The first passes took it to 124 across 25, and the
2026-09-08 passes to 57 across 17: 35 of them Population A, 22 deliberate.

WHAT IT DOES CATCH TODAY is the number going UP, which means an edit stranded
something.

LIMIT, STATED SO IT IS NOT MISREAD: articles whose sources are lettered bullets
rather than numbered entries (programs-activities.md, coeducation-gender.md,
french-language-camping.md) have no numbered entries and are skipped entirely.
Their header reads "Sources: 0" by the same convention. This says nothing about
them either way.
"""
import json
import os
import re
import sys

BASELINE = 57           # whole-wiki count after the 2026-09-08 p_484 passes
#                         (was 136 when this check was written, the same day)


def sources_region(text):
    """(start, end) of the ## Sources section, bounded by the NEXT top-level
    heading. Bounding matters: directors-index.md has 81 lines matching a
    numbered-list pattern against 67 source entries, so an unbounded scan reads
    Open Questions and Research Notes as sources."""
    start = text.find('## Sources')
    if start < 0:
        return (-1, -1)
    nxt = re.search(r'^## ', text[start + len('## Sources'):], re.M)
    end = start + len('## Sources') + nxt.start() if nxt else len(text)
    return (start, end)


def main() -> int:
    with open('wiki/articles.json', encoding='utf-8') as fh:
        data = json.load(fh)
    registered = {a['article_id']
                  for a in (data['articles'] if isinstance(data, dict) else data)}

    rows = []
    for root, _dirs, files in os.walk('wiki'):
        for name in sorted(files):
            if not name.endswith('.md'):
                continue
            aid = name[:-3]
            if aid not in registered:
                continue
            with open(os.path.join(root, name), encoding='utf-8') as fh:
                text = fh.read()
            start, end = sources_region(text)
            if start < 0:
                continue
            entries = [int(m.group(1))
                       for m in re.finditer(r'^(\d+)\. ', text[start:end], re.M)]
            if not entries:                      # lettered-bullet sources
                continue
            body = text[:start] + text[end:]
            marks = {int(m.group(1)) for m in re.finditer(r'\^(\d+)', body)}
            uncited = [n for n in entries if n not in marks]
            if uncited:
                rows.append((len(uncited), aid, uncited))

    total = sum(r[0] for r in rows)
    print('=' * 70)
    print('UNCITED SOURCE ENTRIES (advisory)')
    print('=' * 70)
    if not rows:
        print('  PASS -- every numbered source entry is reached by a marker')
        return 0
    print('  %d entr(ies) across %d article(s) that no marker points at.' % (total, len(rows)))
    print('  Baseline at p_484 was %d. %s' % (
        BASELINE,
        'UP BY %d -- an edit has stranded something; look at the newest change first.' % (total - BASELINE)
        if total > BASELINE else 'Not above baseline.'))
    for count, aid, uncited in sorted(rows, reverse=True):
        shown = ', '.join(str(n) for n in uncited[:12])
        more = '' if len(uncited) <= 12 else ' …+%d' % (len(uncited) - 12)
        print('    %3d  %-38s %s%s' % (count, aid, shown, more))
    print('  Each is either a citation lost in an edit -- so a claim is now unsourced --')
    print('  or an entry added for a passage never written. Only reading tells them apart.')
    return 0


sys.exit(main())
