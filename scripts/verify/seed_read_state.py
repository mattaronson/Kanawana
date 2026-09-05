#!/usr/bin/env python3
"""One-time seeding of the `read_state` field on sources.json (check H).

WHAT THIS IS ALLOWED TO INFER, AND WHAT IT IS NOT.

The whole point of read receipts is to stop the project asserting things it has
not established. A seeding script that guessed would defeat its own purpose, so
this one derives read_state ONLY from evidence already in the repo, and stamps
every value it writes with the basis it used:

  cited by >=1 fact in kb/facts.json
      -> read_state "extracted", basis "derived:cited-by-fact"
      Justification: a fact was extracted from it. That is direct evidence the
      source was opened and read closely enough to yield a claim.

  named in a wiki article but cited by no fact
      -> read_state "unknown", basis "derived:named-in-article-only"
      Justification: NOT evidence of reading. The p_218 sweep found citation
      markers pointing at whichever source sat nearest in the list rather than
      the one carrying the claim, so an appearance in a Sources section proves
      only that someone typed the id.

  neither
      -> read_state "unknown", basis "derived:dormant"

Two values this script will NEVER write: "unopened" and "unavailable". Both are
positive assertions about a check somebody performed -- that the item was looked
for and not read, or looked for and could not be reached. Neither can be
derived from the absence of a citation, and inventing them would recreate
exactly the confident-null problem the check exists to expose.

Re-running is safe: any source that already has a read_state whose basis is not
"derived:*" is left untouched, so hand-asserted receipts always win over
derived ones.
"""
import json, os, sys

ROOT = '/home/user/Kanawana'

sources_doc = json.load(open(os.path.join(ROOT, 'sources/sources.json')))
sources = sources_doc if isinstance(sources_doc, list) else sources_doc['sources']
facts = json.load(open(os.path.join(ROOT, 'kb/facts.json')))['facts']

cited_by_fact = set()
for f in facts:
    cited_by_fact |= set(f.get('sources', []))

wiki_text = ''
for root, _d, fnames in os.walk(os.path.join(ROOT, 'wiki')):
    for fn in fnames:
        if fn.endswith('.md'):
            wiki_text += open(os.path.join(root, fn), encoding='utf-8').read()

changed = 0
tally = {}
for s in sources:
    basis = s.get('read_state_basis', '')
    if s.get('read_state') and not basis.startswith('derived:'):
        continue                      # hand-asserted receipt: never overwrite
    if s['source_id'] in cited_by_fact:
        state, basis = 'extracted', 'derived:cited-by-fact'
    elif s['source_id'] in wiki_text:
        state, basis = 'unknown', 'derived:named-in-article-only'
    else:
        state, basis = 'unknown', 'derived:dormant'
    if s.get('read_state') != state or s.get('read_state_basis') != basis:
        changed += 1
    s['read_state'] = state
    s['read_state_basis'] = basis
    tally[basis] = tally.get(basis, 0) + 1

if '--dry-run' in sys.argv:
    print('DRY RUN -- nothing written')
else:
    json.dump(sources_doc, open(os.path.join(ROOT, 'sources/sources.json'), 'w'),
              indent=1, ensure_ascii=False)

print('sources: %d, updated: %d' % (len(sources), changed))
for k in sorted(tally):
    print('  %-38s %4d' % (k, tally[k]))
print('\nNote: no source was assigned "unopened" or "unavailable" -- neither is derivable.')
