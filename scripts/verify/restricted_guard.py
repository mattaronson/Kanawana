"""Enforce the boundary between the restricted register and the published layer.

kb/restricted/register.jsonl records that certain material is withheld. It must
never record the material. This checks both halves of that:

  1. NO CONTENT IN THE REGISTER. A register record may describe a category and a
     reason; it may not carry the withheld text or the names it concerns. Any
     field outside the permitted set fails, as does a `reason` long enough to be
     smuggling a quotation.

  2. NO LEAKAGE INTO THE INDEXED LAYER. For each record, the guard opens the
     source at the line range in its `locator`, extracts the personal names in
     that span AT RUNTIME, and fails if any appear in kb/facts.json or wiki/.

The names are never stored anywhere. They are derived from the source on each
run and discarded, which is what lets this register live in a public repository
alongside the thing it is protecting.

Exit 1 on any violation.
"""
import json, re, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG  = os.path.join(ROOT, 'kb/restricted/register.jsonl')

ALLOWED = {'id','source_id','locator','category','subjects','reason','withheld_by',
           'withheld_at','embargo_basis','review_on','release_conditions',
           'what_was_published_instead','note','released_on','released_because'}
REASON_MAX = 1200

# Words that look like names but are not people, in this corpus.
STOP = {'Do','All','He','She','However','Considers','Recommendations','Cont',
        'Kamp','Kanawana','Camp','Director','Montreal','YMCA','Office','Branch',
        'Spell','Send','Have','Get','Kitchen','With','This','The','Their','His',
        'Her','Not','And','For','But','Also','Should','Would','Could','Rick',
        'Medicare','Canadian','Canoe','School','Junior','Senior','Business','Manager'}
NAME = re.compile(r'\b([A-Z][a-z]{2,})\s+([A-Z][a-z]{2,})\b')

def names_in(path, lo, hi):
    """Personal names appearing in a span of the source. Derived, never stored."""
    lines = io.open(os.path.join(ROOT, path), encoding='utf-8', errors='ignore').read().split('\n')
    span = '\n'.join(lines[lo-1:hi])
    out = set()
    for a, b in NAME.findall(span):
        if a in STOP or b in STOP:
            continue
        out.add('%s %s' % (a, b))
    return out

def published_text():
    parts = [io.open(os.path.join(ROOT, 'kb/facts.json'), encoding='utf-8').read()]
    for root, _, files in os.walk(os.path.join(ROOT, 'wiki')):
        for f in files:
            if f.endswith(('.md', '.json')):
                parts.append(io.open(os.path.join(root, f), encoding='utf-8').read())
    return '\n'.join(parts)

def main():
    if not os.path.exists(REG):
        print('no restricted register; nothing to check')
        return 0
    recs = [json.loads(l) for l in io.open(REG, encoding='utf-8') if l.strip()]
    bad = []

    for r in recs:
        extra = sorted(set(r) - ALLOWED)
        if extra:
            bad.append('%s: fields not permitted in the register: %s' % (r.get('id'), extra))
        if len(r.get('reason', '')) > REASON_MAX:
            bad.append('%s: `reason` is %d chars (max %d) -- a reason this long is '
                       'probably carrying the content it is meant to withhold'
                       % (r.get('id'), len(r['reason']), REASON_MAX))

    pub = published_text()
    for r in recs:
        if r.get('released_on'):
            continue
        loc = r.get('locator') or {}
        f, rng = loc.get('file'), loc.get('lines')
        if not (f and rng and os.path.exists(os.path.join(ROOT, f))):
            bad.append('%s: locator does not resolve to a readable file and line range' % r.get('id'))
            continue
        leaked = sorted(n for n in names_in(f, rng[0], rng[1]) if n in pub)
        if leaked:
            bad.append('%s: %d name(s) from the restricted span appear in the published layer '
                       '(kb/facts.json or wiki/). Not printed here. Re-read the span at %s:%d-%d '
                       'and remove them.' % (r.get('id'), len(leaked), f, rng[0], rng[1]))

    print('=' * 70)
    print('RESTRICTED REGISTER GUARD -- %d record(s)' % len(recs))
    print('=' * 70)
    if not bad:
        print('  register carries no content; no restricted name reaches the published layer')
        return 0
    for b in bad:
        print('  - %s' % b)
    return 1

sys.exit(main())
