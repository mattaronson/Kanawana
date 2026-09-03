"""Publication gate: restricted facts must never reach the wiki.

THE BOUNDARY IS THE WIKI, NOT THE REPOSITORY. The operator's decision, 2026-09-03:
the source archive is public already and the OCR corpus in this repo is fine
where it is. What is questionable is pushing named personal material into the
published wiki. So the knowledge base MAY hold restricted material -- that is the
point of holding it, so it is not lost -- and this script guards the one door
that matters.

A restricted fact is any record in kb/facts.json carrying:

    "publication": {"status": "restricted", "register_id": "r_NNNN",
                    "review_on": "YYYY-MM-DD", "basis": "...", "why": "..."}

Checks:

  1. Every restricted fact is registered: register_id resolves to a record in
     kb/restricted/register.jsonl, and that record points back at the fact.
  2. Every restricted fact carries a review_on date and a stated basis.
  3. NO PERSONAL NAME appearing only in restricted facts appears anywhere under
     wiki/. Names that also occur in unrestricted facts are ignored -- a person
     can be in the wiki for their job and restricted for an assessment of it.
  4. The register itself stays content-free: it indexes, it does not reproduce.

Violations name the fact and the register entry, never the person. Wire this into
any future publication step (scripts/build-content.ts) before the wiki goes up.

Exit 1 on any violation.
"""
import json, re, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG  = os.path.join(ROOT, 'kb/restricted/register.jsonl')

REG_ALLOWED = {'id','fact_ids','source_id','locator','category','subjects','reason',
               'withheld_by','withheld_at','embargo_basis','review_on',
               'release_conditions','what_was_published_instead','note',
               'released_on','released_because'}
REASON_MAX = 1200

# Role, place and institution words only. NEVER put a surname in here: while
# debugging noise I briefly added two of the surnames this gate exists to
# protect, which silently excused them from every check.
STOP = {'Kamp','Kanawana','Camp','Director','Directors','Montreal','Senior','Junior',
        'Waterfront','Report','Association','Voyageurs','Verendrye','Restricted','Context'}
# Match title case AND ALL CAPS, and compare case-insensitively. The first
# version of this matched only title case, so the very names it was written to
# protect -- which the restricted facts write in capitals for emphasis -- slid
# straight past it and the gate reported a clean pass. A guard that fails open
# is worse than no guard, because it is trusted. Caught by the regression test
# below, not by reading the code.
NAME = re.compile(r"\b([A-Z][A-Za-z'\u2019-]{2,})\s+([A-Z][A-Za-z'\u2019-]{2,})\b")

def names(text, common=frozenset()):
    """Personal names in a piece of text, lowercased for comparison.

    A capitalised pair is a name unless BOTH tokens are ordinary vocabulary.
    Rather than carry a dictionary, `common` is built from the corpus itself:
    any token that also occurs as a plain lowercase word in the unrestricted
    facts and the wiki is ordinary. "Without Naming" and "Any Future" have two
    common tokens and fall out; "Pierre Parizeau" keeps its surname even though
    "pierre" is an ordinary French word, because nobody writes "parizeau" in
    lowercase."""
    out = set()
    for a, b in NAME.findall(text):
        if a.title() in STOP or b.title() in STOP:
            continue
        # Keep the pair if EITHER token is uncommon. Requiring both to be
        # uncommon dropped "Pierre Parizeau", because "pierre" occurs as an
        # ordinary lowercase word in this French-and-English corpus. A given
        # name is often a word; a surname almost never is, and one uncommon
        # token is enough to make a pair worth checking.
        if a.lower() in common and b.lower() in common:
            continue
        out.add(('%s %s' % (a, b)).lower())
    return out

def common_words(texts):
    """Tokens that appear as plain lowercase words -- i.e. ordinary vocabulary."""
    words = set()
    for t in texts:
        words |= set(re.findall(r'\b[a-z]{3,}\b', t))
    return words

def wiki_text():
    parts = []
    for root, _, files in os.walk(os.path.join(ROOT, 'wiki')):
        for f in files:
            if f.endswith(('.md', '.json')):
                parts.append(io.open(os.path.join(root, f), encoding='utf-8').read())
    return '\n'.join(parts)

def main():
    facts = json.load(open(os.path.join(ROOT, 'kb/facts.json'), encoding='utf-8'))['facts']
    restricted = [f for f in facts if (f.get('publication') or {}).get('status') == 'restricted']
    if not restricted:
        print('no restricted facts; nothing to gate')
        return 0
    reg = {r['id']: r for r in
           (json.loads(l) for l in io.open(REG, encoding='utf-8') if l.strip())} \
          if os.path.exists(REG) else {}
    bad = []

    for f in restricted:
        pub = f['publication']
        rid = pub.get('register_id')
        if rid not in reg:
            bad.append('%s: publication.register_id %r is in no register record' % (f['fact_id'], rid))
        elif f['fact_id'] not in (reg[rid].get('fact_ids') or []):
            bad.append('%s: register record %s does not list this fact' % (f['fact_id'], rid))
        if not pub.get('review_on'):
            bad.append('%s: restricted with no review_on date' % f['fact_id'])
        if not pub.get('basis'):
            bad.append('%s: restricted with no stated embargo basis' % f['fact_id'])

    for r in reg.values():
        extra = sorted(set(r) - REG_ALLOWED)
        if extra:
            bad.append('%s: fields not permitted in the register: %s' % (r.get('id'), extra))
        if len(r.get('reason', '')) > REASON_MAX:
            bad.append('%s: `reason` is %d chars (max %d) -- long enough to be reproducing '
                       'the content the register exists to index' % (r.get('id'), len(r['reason']), REASON_MAX))

    wt_raw = wiki_text()
    unrestricted = [f['claim'] for f in facts
                    if (f.get('publication') or {}).get('status') != 'restricted']
    common = common_words(unrestricted + [wt_raw])
    open_names = set()
    for c in unrestricted:
        open_names |= names(c, common)
    wt = wt_raw.lower()
    for f in restricted:
        if (f.get('publication') or {}).get('released_on'):
            continue
        leaked = sorted(n for n in (names(f['claim'], common) - open_names) if n in wt)
        if leaked:
            bad.append('%s (register %s): %d restricted name(s) reach wiki/. Names not printed. '
                       'Read the fact and remove them from the article.'
                       % (f['fact_id'], f['publication'].get('register_id'), len(leaked)))

    print('=' * 70)
    print('PUBLICATION GATE -- %d restricted fact(s), %d register record(s)' % (len(restricted), len(reg)))
    print('=' * 70)
    if not bad:
        print('  all restricted facts registered and dated; none reaches wiki/')
        return 0
    for b in bad:
        print('  - %s' % b)
    return 1

sys.exit(main())
