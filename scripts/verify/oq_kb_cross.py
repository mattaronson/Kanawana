#!/usr/bin/env python3
"""
oq_kb_cross.py -- ADVISORY. Cross-check every article's Open Questions against the knowledge base.

WHY THIS EXISTS
---------------
On 2026-09-06 `canadian-camping-movement.md`'s Open Question 4 still read "no named individual
confirmed on both sides of the connection" between Kanawana and Camp Nominingue. The knowledge base
had held the answer for weeks, in f_2641 and f_3039, both of which SAY IN THEIR OWN TEXT that the KB
already held Hay Finlay as Kanawana's 1922 section director. The question was not unanswered. It was
unread -- nobody had run the article and the KB against each other.

That was the second such case in two days; the first was the seventh split in the plaque index,
found by testing the index against the KB rather than reading it. This script is that test, made
routine.

WHAT IT DOES
------------
For each article with an "## Open Questions" section, it extracts proper-noun phrases from that
section, counts the KB facts whose claim contains each phrase, and reports the phrases where facts
EXIST and the article cites NONE of them by fact id. High fact counts on a phrase inside an open
question are the signal: the project knows a lot about a thing it is still asking about.

WHAT IT IS NOT
--------------
It is advisory and it is noisy. A phrase can appear in an open question incidentally ("no mention in
Le Devoir"), and a well-maintained article often incorporates facts without citing their ids. Expect
most rows to be nothing. The Camp Nominingue row -- 35 facts, none cited -- is what a real one looks
like.

HOW TO USE IT WELL
------------------
Run it bare after a research burst and read the top twenty. Better, run it with `--since`, which
drops every fact whose id is below a number you give: after adding f_4900 onwards, `--since 4900`
reports only the open questions that the facts you have JUST ADDED may have answered. That is the
sharp version of the check and the one worth making routine.

Usage:  python3 scripts/verify/oq_kb_cross.py [--min N] [--top N] [--since NNNN]
"""
import json, re, os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Words that make a phrase generic rather than a subject. A phrase whose every word is here is
# dropped; these are the project's own furniture, not things it asks questions about.
STOP = set("""The A An In On At Of For And Or But It Is Was Were Are Be Been This That These Those
Who What When Where Why How Did Does Do Has Have Had Not No Yes If Then Than So As By With From
Important Nice Resolved Partially Open Question Questions Critical New Confirmed Unknown None
Kanawana Camp Kamp YMCA Y.M.C.A Montreal Quebec Canada Canadian CLAUDE KB Concordia Archives
Archive Internet Wayback LinkedIn Facebook McGill Trent Library Nice-to-have Annual Report Reports
Director Directors Camping Association Google Books""".split())

# Phrases that are institutional furniture: they occur in hundreds of facts and in every second
# open question, and flagging them buries the signal. Kept explicit rather than tuned by threshold,
# because a threshold would also have hidden Camp Nominingue.
NOISE = {
    "Canadian Camping", "Canadian Camping Association", "Canadian Camping Association's",
    "Camp Director", "Camp Directors", "Quebec Camping Association", "Ontario Camping Association",
    "Annual Report", "Annual Reports", "Google Books", "Green Triangle", "Summer Camp",
    "Camp Jubilee", "Council Ring", "Pip Award", "The Pip Award", "Junior Department",
}

def phrases(text):
    out = set()
    for x in re.findall(r"\b([A-Z][a-zA-Z.'\-]+(?: [A-Z][a-zA-Z.'\-]+){1,3})\b", text):
        if len(x) < 8:
            continue
        if x in NOISE:
            continue
        if all(w.rstrip('.') in STOP for w in x.split()):
            continue
        out.add(x)
    return out

def main():
    argv = sys.argv[1:]
    minf = int(argv[argv.index('--min') + 1]) if '--min' in argv else 3
    top  = int(argv[argv.index('--top') + 1]) if '--top' in argv else 40
    since = int(argv[argv.index('--since') + 1]) if '--since' in argv else 0

    facts = json.load(open(os.path.join(ROOT, 'kb', 'facts.json')))['facts']
    claims = [(f['fact_id'], f['claim']) for f in facts]
    if since:
        claims = [(i, c) for i, c in claims
                  if i.startswith('f_') and i[2:].isdigit() and int(i[2:]) >= since]

    rows = []
    for path in sorted(glob.glob(os.path.join(ROOT, 'wiki', '**', '*.md'), recursive=True)):
        text = open(path).read()
        m = re.search(r'\n## Open Questions\n(.*?)(\n## |\Z)', text, re.S)
        if not m:
            continue
        # An article about Camp Ouareau naturally names Camp Ouareau in its own open questions,
        # and the KB naturally has fifty facts about it. Self-reference is not the signal; a
        # question about something the article is NOT about is.
        slug = os.path.basename(path)[:-3].replace('-', ' ').lower()
        for phrase in sorted(phrases(m.group(1))):
            key = phrase.lower().replace('.', '').replace("'s", '')
            if key in slug or all(w in slug for w in key.split()):
                continue
            hits = [fid for fid, claim in claims if phrase in claim]
            if len(hits) < minf:
                continue
            if any(h in text for h in hits):
                continue
            rows.append((len(hits), os.path.relpath(path, ROOT), phrase, hits[:5]))

    rows.sort(key=lambda r: -r[0])
    print('=' * 70)
    print('OPEN QUESTIONS vs THE KNOWLEDGE BASE -- advisory')
    print('=' * 70)
    scope = (' (facts from %s onwards only)' % ('f_%04d' % since)) if since else ''
    print('  %d phrase(s) named in an open question have >= %d KB facts and no cited fact id%s.'
          % (len(rows), minf, scope))
    print('  Most of these are nothing. Read the top of the list, not the whole of it.\n')
    for n, path, phrase, hits in rows[:top]:
        print('  %3d facts  %-38s %s' % (n, phrase, path))
        print('             %s' % ', '.join(hits))
    if len(rows) > top:
        print('\n  ... %d more below the cut; re-run with --top to see them.' % (len(rows) - top))
    print('\n  Advisory: this never fails a build. It says where to look.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
