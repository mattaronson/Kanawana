"""Embargo metadata check. Not a publication ban.

THE PRINCIPLE, set by the operator on 2026-09-03: the record comes first.
Publication policy is a decision for the wiki's UI layer, not for the collection
layer. "We're better off having the whole record and selecting from it now than
deleting material that ought to just be embargoed and potentially creating holes
in the record for future scholarly work."

So this script does NOT stop sensitive material reaching kb/facts.json or wiki/.
Both are working surfaces and both should be complete. What it enforces is that
embargoed material is *labelled* wherever it sits, so that a future web UI can
find it and decide what to do with it — redact, gate behind a login, show a
placeholder, or publish once the embargo lapses. An unlabelled passage is the
failure mode, because the UI cannot act on what it cannot see.

An embargoed fact in kb/facts.json carries:

    "publication": {"status": "embargoed", "register_id": "r_NNNN",
                    "review_on": "YYYY-MM-DD", "basis": "...", "why": "..."}

A wiki passage carrying embargoed material is wrapped:

    <!-- embargo:r_0001 -->
    ...the passage...
    <!-- /embargo:r_0001 -->

Checks:
  1. Every embargoed fact is registered, dated, and has a stated basis.
  2. Every register entry resolves to real facts and a readable source locator.
  3. Every embargo marker in wiki/ is well formed, paired, and names a register
     entry that exists.
  4. Any name that appears ONLY in embargoed facts and also appears in wiki/
     must sit inside an embargo block. Outside one, it is unlabelled and the UI
     would publish it unknowingly.

Exit 1 on any violation. Violations name the fact, the article and the register
entry — never the person.
"""
import json, re, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG  = os.path.join(ROOT, 'kb/restricted/register.jsonl')

REG_ALLOWED = {'id','fact_ids','source_id','locator','category','subjects','reason',
               'withheld_by','withheld_at','embargo_basis','review_on',
               'release_conditions','how_it_is_surfaced','note',
               'released_on','released_because'}

# Role, place and institution words only. NEVER put a surname here: while
# debugging noise an earlier version added two of the protected surnames, which
# silently excused them from every check.
STOP = {'Kamp','Kanawana','Camp','Director','Directors','Montreal','Senior','Junior',
        'Waterfront','Report','Association','Voyageurs','Verendrye','Restricted','Context'}

# Title case AND ALL CAPS. An earlier version matched only title case, so names
# written in capitals for emphasis passed straight through and the check
# reported a clean pass.
NAME  = re.compile(r"\b([A-Z][A-Za-z'’-]{2,})\s+([A-Z][A-Za-z'’-]{2,})\b")
OPEN  = re.compile(r'<!--\s*embargo:(r_\d+)\s*-->')
CLOSE = re.compile(r'<!--\s*/embargo:(r_\d+)\s*-->')

def names(text, common=frozenset()):
    """Personal names in text, lowercased. A capitalised pair is a name unless
    BOTH tokens are ordinary vocabulary -- requiring both to be uncommon dropped
    "Pierre Parizeau", since "pierre" is an ordinary French word here."""
    out = set()
    for a, b in NAME.findall(text):
        if a.title() in STOP or b.title() in STOP: continue
        if a.lower() in common and b.lower() in common: continue
        out.add(('%s %s' % (a, b)).lower())
    return out

def common_words(texts):
    w = set()
    for t in texts: w |= set(re.findall(r'\b[a-z]{3,}\b', t))
    return w

def wiki_files():
    for root, _, fs in os.walk(os.path.join(ROOT, 'wiki')):
        for f in fs:
            if f.endswith('.md'):
                p = os.path.join(root, f)
                yield os.path.relpath(p, ROOT), io.open(p, encoding='utf-8').read()

def blocks(text):
    """(register_id, span_text) for each well-formed embargo block."""
    out, errs = [], []
    pos = 0
    while True:
        m = OPEN.search(text, pos)
        if not m: break
        c = CLOSE.search(text, m.end())
        if not c:
            errs.append('unclosed embargo block for %s' % m.group(1)); break
        if c.group(1) != m.group(1):
            errs.append('embargo block opened as %s and closed as %s' % (m.group(1), c.group(1)))
        out.append((m.group(1), text[m.end():c.start()]))
        pos = c.end()
    for c in CLOSE.finditer(text):
        if not OPEN.search(text[:c.start()]):
            errs.append('embargo close tag %s with no opening tag' % c.group(1))
    return out, errs

def main():
    facts = json.load(open(os.path.join(ROOT, 'kb/facts.json'), encoding='utf-8'))['facts']
    emb = [f for f in facts if (f.get('publication') or {}).get('status') == 'embargoed']
    reg = {r['id']: r for r in (json.loads(l) for l in io.open(REG, encoding='utf-8') if l.strip())} \
          if os.path.exists(REG) else {}
    bad = []

    for f in emb:
        pub = f['publication']; rid = pub.get('register_id')
        if rid not in reg: bad.append('%s: register_id %r is in no register record' % (f['fact_id'], rid))
        elif f['fact_id'] not in (reg[rid].get('fact_ids') or []):
            bad.append('%s: register record %s does not list this fact' % (f['fact_id'], rid))
        if not pub.get('review_on'): bad.append('%s: embargoed with no review_on date' % f['fact_id'])
        if not pub.get('basis'):     bad.append('%s: embargoed with no stated basis' % f['fact_id'])

    known = {f['fact_id'] for f in facts}
    for r in reg.values():
        extra = sorted(set(r) - REG_ALLOWED)
        if extra: bad.append('%s: fields not permitted in the register: %s' % (r['id'], extra))
        for fid in (r.get('fact_ids') or []):
            if fid not in known: bad.append('%s: lists %s, which is not a fact' % (r['id'], fid))
        loc = r.get('locator') or {}
        if not (loc.get('file') and os.path.exists(os.path.join(ROOT, loc['file']))):
            bad.append('%s: locator does not resolve to a readable file' % r['id'])

    wiki = list(wiki_files())
    for path, text in wiki:
        bl, errs = blocks(text)
        for e in errs: bad.append('%s: %s' % (path, e))
        for rid, _ in bl:
            if rid not in reg: bad.append('%s: embargo block cites %s, which is in no register record' % (path, rid))

    unrestricted = [f['claim'] for f in facts if (f.get('publication') or {}).get('status') != 'embargoed']
    common = common_words(unrestricted + [t for _, t in wiki])
    open_names = set()
    for c in unrestricted: open_names |= names(c, common)

    for f in emb:
        if f['publication'].get('released_on'): continue
        want = names(f['claim'], common) - open_names
        if not want: continue
        for path, text in wiki:
            # Strip the embargo blocks out and search what is LEFT. Testing
            # whether a name appears inside some block was the wrong question:
            # a name that appears both inside a block and loose in the prose
            # passed, because it was findable inside one. What matters is
            # whether ANY occurrence sits outside.
            outside = OPEN.sub('\x00', text)
            outside = re.sub(r'\x00.*?<!--\s*/embargo:r_\d+\s*-->', ' ', outside, flags=re.S)
            outside = outside.lower()
            loose = sorted(n for n in want if n in outside)
            if loose:
                bad.append('%s: %d name(s) from %s (register %s) appear OUTSIDE an embargo block. '
                           'Names not printed. Wrap the passage in <!-- embargo:%s --> ... '
                           '<!-- /embargo:%s --> so the UI layer can act on it.'
                           % (path, len(loose), f['fact_id'], f['publication'].get('register_id'),
                              f['publication'].get('register_id'), f['publication'].get('register_id')))

    print('=' * 70)
    print('EMBARGO METADATA -- %d embargoed fact(s), %d register record(s), %d article(s) scanned'
          % (len(emb), len(reg), len(wiki)))
    print('=' * 70)
    if not bad:
        print('  every embargoed fact is registered and dated; every occurrence in wiki/ is labelled')
        return 0
    for b in bad: print('  - %s' % b)
    return 1

sys.exit(main())
