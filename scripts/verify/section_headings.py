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

BLOCKING SINCE 2026-09-07, when p_481 cleared. It shipped advisory because
fourteen pre-existing offenders would have failed every build until the backlog
was worked, which trains everyone to ignore the output; that was always meant to
end the day the backlog did, on the precedent data_integrity.py sets for
duplicate source ids. It now returns nonzero for any article missing a template
section, which is the case that produced it: a heading dropped by an edit.

The two articles in EXEMPT are NOT a residual backlog and do not fail the check.
They are printed every run anyway, because an exemption nobody sees is an
exemption nobody re-examines.
"""
import json
import os
import re
import sys

REQUIRED = ('## Overview', '## Open Questions', '## Related Articles', '## Sources')

# EXEMPT, not backlog. Two articles legitimately lack a section the template
# names, and the reasons are structural rather than editorial. Recorded here so
# nobody "fixes" them by bolting on an empty heading -- which would be the same
# error as an unrecorded null, in the other direction: a section that claims to
# hold something and holds nothing.
EXEMPT = {
    # An index OF sources. A "## Sources" section would either be empty or
    # duplicate the whole article.
    'sources-index':     ('Sources',),
    # Pure synthesis and navigation: ZERO citation markers in the file, because
    # every claim in it lives in the article it links to. A "## Sources" section
    # would have to list the entire wiki's sources or nothing.
    'timeline-overview': ('Sources',),
}

# The p_481 backlog, CLEARED 2026-09-07. Kept as an empty dict rather than
# deleted, so this file stays the record of what the backlog was and so a future
# regression has somewhere obvious to be listed. What the fourteen turned out to
# be: EIGHT were a naming inconsistency and nothing more -- the article called it
# "## Summary" where the template says "## Overview", and all eight were renamed
# (no inbound "#summary" anchors existed, checked first). FOUR had an unheaded
# opening paragraph that was already an overview, and got the heading.
# quebec-camp-landscape genuinely lacked "## Related Articles" and now has one.
# wartime-kanawana carried its questions in TWO places under two names -- a
# "## Research Gaps" section in the body and a "### Open Questions" list buried
# after the Sources inside the verification notes -- and they are consolidated,
# unchanged in substance, into one "## Open Questions" in the template position.
# The remaining two are in EXEMPT above.
KNOWN = {
}


def main() -> int:
    registered = set()
    with open('wiki/articles.json', encoding='utf-8') as fh:
        data = json.load(fh)
    for art in (data['articles'] if isinstance(data, dict) else data):
        registered.add(art['article_id'])

    new, known_still, exempt_seen = [], [], []
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
            if aid in EXEMPT and set(missing) <= set(EXEMPT[aid]):
                exempt_seen.append((aid, missing))
            elif aid in KNOWN and set(missing) <= set(KNOWN[aid]):
                known_still.append((aid, missing))
            else:
                new.append((aid, missing))

    print('=' * 70)
    print('SECTION HEADINGS')
    print('=' * 70)
    if exempt_seen:
        print('  [exempt] %d article(s) legitimately lack a template section; see '
              'EXEMPT in this file for why. Not a backlog.' % len(exempt_seen))
        for aid, miss in sorted(exempt_seen):
            print('               %-32s without: %s' % (aid, ', '.join(miss)))
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
        print('  Add the section, or add the article to EXEMPT in this file with a '
              'reason if it genuinely should not have one.')
    elif not known_still:
        print('  PASS -- every registered article carries Overview, Open Questions, '
              'Related Articles and Sources%s'
              % (', bar the exempt above' if exempt_seen else ''))
    else:
        print('  No new omissions.')
    return 1 if (new or known_still) else 0


sys.exit(main())
