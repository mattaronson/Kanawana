#!/usr/bin/env python3
"""Check that every wiki article carries the sections CLAUDE.md's template names.

WHY THIS EXISTS. On 2026-09-07 a spinout silently dropped the "## Sources"
heading from traditions/canoe-trips.md. The article kept all twenty-eight of its
numbered source entries and every citation marker resolved, so EVERY EXISTING
CHECK PASSED -- the harness counts entries and markers, and nothing looked at
headings. The article sat with a bare numbered list under "Related Articles" for
two hours, and was found only because scripts/wiki/add_source_note.py refuses to
run on a file with no "## Sources" heading to insert into.

The audit that followed found fifteen articles missing template sections,
fourteen of them E1-reviewed. That is queued as p_481, with the reasoning: an
article with no Open Questions section makes no claim about what it does not
know, so a reader cannot tell a closed subject from an unexamined one -- the same
failure as an unrecorded null, at the article level.

ADVISORY, NOT BLOCKING, AND ON PURPOSE. Fourteen pre-existing offenders would
fail every build from now until p_481 clears, which would train everyone to
ignore the output. This follows the precedent data_integrity.py already sets for
duplicate source ids and p_303: report it every run, block on it once the
backlog is gone. WHAT IT DOES CATCH TODAY is a NEW omission -- a heading dropped
by an edit, which is the case that produced it.

Exit code is 0 by design. all.py still honours it, so if this ever starts
returning nonzero that is news.
"""
import json
import os
import re
import sys

REQUIRED = ('## Overview', '## Open Questions', '## Related Articles', '## Sources')

# Known at the time of writing and queued as p_481. Listed so the output shows
# only what is NEW, and so this file is the record of what the backlog was.
KNOWN = {
    'wartime-kanawana':          ('Overview', 'Open Questions'),
    'sources-index':             ('Overview', 'Sources'),
    'section-names':             ('Overview',),
    'quebec-camp-landscape':     ('Related Articles',),
    'lv-games':                  ('Overview',),
    'founding-1894':             ('Overview',),
    'directors-index':           ('Overview',),
    'da-budge':                  ('Overview',),
    'cushing-family':            ('Overview',),
    'council-ring':              ('Overview',),
    'centennial-1967':           ('Overview',),
    'canadian-camping-movement': ('Overview',),
    'billy-ball':                ('Overview',),
    'timeline-overview':         ('Sources',),
}


def main() -> int:
    registered = set()
    with open('wiki/articles.json', encoding='utf-8') as fh:
        data = json.load(fh)
    for art in (data['articles'] if isinstance(data, dict) else data):
        registered.add(art['article_id'])

    new, known_still = [], []
    for root, _dirs, files in os.walk('wiki'):
        for name in sorted(files):
            if not name.endswith('.md'):
                continue
            aid = name[:-3]
            if aid not in registered:      # README and other unregistered pages
                continue
            with open(os.path.join(root, name), encoding='utf-8') as fh:
                text = fh.read()
            missing = tuple(h[3:] for h in REQUIRED
                            if not re.search('^' + re.escape(h), text, re.M))
            if not missing:
                continue
            if aid in KNOWN and set(missing) <= set(KNOWN[aid]):
                known_still.append((aid, missing))
            else:
                new.append((aid, missing))

    print('=' * 70)
    print('SECTION HEADINGS (advisory)')
    print('=' * 70)
    if known_still:
        print('  [advisory] %d article(s) missing template sections, known and queued '
              'as p_481 -- advisory until that clears, then make this blocking.'
              % len(known_still))
        for aid, miss in sorted(known_still):
            print('               %-32s missing: %s' % (aid, ', '.join(miss)))
    if new:
        print('  NEW -- not in the p_481 backlog, so an edit dropped these:')
        for aid, miss in sorted(new):
            print('    - %-32s missing: %s' % (aid, ', '.join(miss)))
        print('  Add the section, or add the article to KNOWN in this file with a '
              'reason if it genuinely should not have one.')
    elif not known_still:
        print('  PASS -- every registered article carries Overview, Open Questions, '
              'Related Articles and Sources')
    else:
        print('  No new omissions.')
    return 0


sys.exit(main())
