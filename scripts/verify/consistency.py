"""Check numbers ASSERTED in prose against the data they are drawn from.

p_301. The verify harness checks citation integrity: does every marker resolve,
does every source exist, does the header count match. It passed all six of the
plaque-audit articles clean while multi-year-index.md said 1,493 distinct names
and 149 traced people over an index holding 1,483 and 155, and printed a table
of 149 rows beneath a sentence claiming more. Every one of those numbers was
correct when written. They went stale because a later fix moved the data and
nobody walked back through the prose.

Two kinds of check, because the defect has two shapes.

DERIVED -- a number in prose against a value computed from a data file. These
need a registry: no parser can know that "distinct named individuals" means
len(person-index.json). Adding a rule is three lines and is the price of
letting an article state a number at all.

SPAN -- a season count against the year range printed beside it: "N seasons,
YYYY-YYYY" must satisfy N == end - start + 1. General, no registry. It exists
because on 2026-09-05 a closure year was settled, a run was correctly re-dated
from 1918-2019 to 1919-2019, and the count in front of it was left at "about
102". Seasons and summers only -- "37 years (1919-1956)" is an elapsed duration
and correct as written.

TABLE -- a number in prose against the number of rows in a table in the SAME
file. This one is general: it needs no registry, only a phrase that looks like
a count and a table below it. Three of the four live defects p_227 found were
this shape (f_2359), including "12 documented recipients" over eleven rows.

Exit 1 if anything disagrees.
"""
import json, re, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def path(*p): return os.path.join(ROOT, *p)

# --- the data the DERIVED rules draw on -------------------------------------
IDX = json.load(open(path('kb/plaque-audit/person-index.json'), encoding='utf-8'))
AUDIT = [json.loads(l) for l in io.open(path('kb/plaque-audit/audit.jsonl'), encoding='utf-8')]

STAFF = {'Staff','Counsellor','Tripper','Director','Directress','Section Director',
         'CIT Director','CIT Program Director','Co-ordinator','Master','Capitaine','Maintenance'}
NEUTRAL = {'Knight','Signatory','Award recipient','Guest','Therapist(joke)'}

def _multi():
    return {n: v for n, v in IDX.items() if len(v['years']) > 1 and not v['initial_only']}

def _progressions():
    n = 0
    for v in _multi().values():
        by = {}
        for a in v['appearances']:
            y = a['year']
            if y is None: continue
            if y not in by or (a['role'] in STAFF and by[y] not in STAFF): by[y] = a['role']
        jr = sorted(y for y, r in by.items() if r not in STAFF and r not in NEUTRAL)
        st = sorted(y for y, r in by.items() if r in STAFF)
        if jr and st and st[-1] > jr[0]: n += 1
    return n

def _names_transcribed():
    def count(x):
        if isinstance(x, str):  return 1
        if isinstance(x, list): return sum(count(i) for i in x)
        if isinstance(x, dict): return sum(count(v) for v in x.values())
        return 0
    # only the roster-bearing keys; a title or a note is not a name
    SKIP = {'title', 'note', 'epitaph', 'epigraph', 'motto', 'year'}
    t = 0
    for r in AUDIT:
        nm = r.get('names') or {}
        if isinstance(nm, dict):
            t += sum(count(v) for k, v in nm.items() if k not in SKIP)
    return t

# --- DERIVED rules ----------------------------------------------------------
# (file, regex with ONE capturing group holding the number, callable, label)
DERIVED = [
 ('wiki/people/multi-year-index.md',
  r'\*\*([\d,]+) distinct named individuals', lambda: len(IDX),
  'distinct named individuals in person-index.json'),
 ('wiki/people/multi-year-index.md',
  r'of whom ([\d,]+) appear in more than one year', lambda: len(_multi()),
  'people appearing in more than one year'),
 ('wiki/people/multi-year-index.md',
  r'\*\*([\d,]+) people can be traced from a junior position', _progressions,
  'documented junior-to-staff progressions'),
 ('wiki/meta/plaque-audit.md',
  r'all ([\d,]+) images \[src_', lambda: len(AUDIT), 'images in the audit'),
 ('wiki/site/named-places-and-camp-vocabulary.md',
  r'all ([\d,]+) images transcribed in the p_291 audit', lambda: len(AUDIT),
  'images in the audit'),
 ('wiki/traditions/plaque-culture.md',
  r'all ([\d,]+) images transcribed in the p_291 audit', lambda: len(AUDIT),
  'images in the audit'),
 ('wiki/meta/plaque-audit.md',
  r'\*\*(\d+)\*\* \|\s*\n\| Fact complete', lambda: sum(1 for r in AUDIT if r['verdict'] == 'PARTIAL'),
  'PARTIAL verdicts'),
]

# --- SPAN rule ---------------------------------------------------------------
# "N seasons, YYYY-YYYY" must satisfy N == end - start + 1. General, like the
# TABLE rule, and it needs no registry.
#
# Why it exists: on 2026-09-05 Camp Stephens's wartime closure was settled at
# 1918, its unbroken run was correctly re-dated from 1918-2019 to 1919-2019,
# and the count in front of it was left at "about 102". Settling a date and
# leaving the arithmetic alone is the exact failure this project keeps making,
# and no check could see it -- every number was internally consistent with the
# sentence it sat in, and wrong against the span beside it.
#
# SEASONS AND SUMMERS ONLY, never "years". A season count is inclusive of both
# ends; "37 years (1919-1956)" is an elapsed duration and correct as written.
# Both readings occur in this wiki and only the first is checkable.
#
# An approximation marker -- about, roughly, ~, approximately -- allows a
# tolerance of 2, since "about 87 seasons" over a span nobody has pinned to the
# year is an honest statement and not an arithmetic claim.
SPAN = re.compile(
    r'(?P<approx>about |roughly |~|approximately )?\*{0,2}(?P<n>\d{1,3})\*{0,2}\s+'
    r'(?:consecutive\s+|unbroken\s+)?(?P<unit>seasons|summers)\b[^\n]{0,40}?\(?'
    r'\b(?P<a>1[89]\d\d|20\d\d)\s*(?:-|\u2013|\u2014|to )\s*(?P<b>1[89]\d\d|20\d\d)\b', re.I)

def check_spans(rel):
    out = []
    text = io.open(path(rel), encoding='utf-8').read()
    for m in SPAN.finditer(text):
        n, a, b = int(m.group('n')), int(m.group('a')), int(m.group('b'))
        span = b - a + 1
        tol = 2 if m.group('approx') else 0
        if abs(n - span) > tol:
            line = text[:m.start()].count('\n') + 1
            out.append('%s:%d  "%s" -- %d %s stated, but %d to %d inclusive is %d'
                       % (rel, line, m.group(0).replace('\n', ' ')[:70], n,
                          m.group('unit'), a, b, span))
    return out

# --- TABLE rules ------------------------------------------------------------
# A sentence claiming a count, immediately above or below a markdown table.
# Deliberately narrow: only phrasings that name what is being counted, so that
# "over 300 people" in a capacity line is never mistaken for a row count.
# Every one of the first three hits this check produced was a false positive,
# which is the failure mode that gets a check switched off. Three rules came
# out of that. (1) "three names OF roughly one hundred" is a ratio, not a row
# count -- a trailing "of" disqualifies the phrase. (2) A table row that is an
# explicit placeholder is not an item: pip-alumni-award.md's 2010 row reads
# "-- | *No documented recipient* | --", so thirteen rows document twelve
# recipients and the prose was right. (3) A sentence may legitimately name a
# subset -- julien-tasse.md says four boards name him and a fifth thanks his
# family -- so an author can silence one line with <!-- count-ok: reason -->
# on the line above. Silencing requires writing the reason down, which is the
# point.
COUNT_PHRASE = re.compile(
    r'\b(?:only\s+)?(\d{1,4}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|'
    r'thirteen|fourteen|fifteen|twenty|twenty-nine|thirty)\s+'
    r'(?:documented\s+|surviving\s+|confirmed\s+|known\s+|named\s+)?'
    r'(recipients?|entries|rows|boards|plaques|people|names|knights|directors|winners)\b'
    r'(?!\s+of\b)',
    re.I)
def is_placeholder(line):
    """A row that records the ABSENCE of an item -- an empty year, a '*No
    documented recipient*' cell -- is not one of the things the prose counts."""
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if any(re.match(r'^\*\s*(no|none|not)\b.*\*$', c, re.I) for c in cells):
        return True
    rest = cells[1:]
    return bool(rest) and all(c in ('', '-', '\u2014', '\u2013') for c in rest)
WORDS = {w: i for i, w in enumerate(
    'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen '
    'fifteen sixteen seventeen eighteen nineteen twenty'.split())}
WORDS['twenty-nine'] = 29; WORDS['thirty'] = 30

def table_blocks(text):
    """Yield (start_line, end_line, n_rows) for each markdown table."""
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        if lines[i].startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:\-|]+\|\s*$', lines[i+1]):
            j = i + 2
            rows = 0
            while j < len(lines) and lines[j].startswith('|'):
                if not is_placeholder(lines[j]):
                    rows += 1
                j += 1
            yield (i, j, rows)
            i = j
        else:
            i += 1

def check_tables(rel):
    out = []
    text = io.open(path(rel), encoding='utf-8').read()
    lines = text.split('\n')
    for start, end, rows in table_blocks(text):
        # only the sentence that introduces the table, or the one just after it
        window = [k for k in range(max(0, start - 2), start)] + [k for k in range(end, min(len(lines), end + 2))]
        for k in window:
            if k > 0 and 'count-ok' in lines[k - 1]:
                continue
            for m in COUNT_PHRASE.finditer(lines[k]):
                raw = m.group(1).lower()
                n = WORDS[raw] if raw in WORDS else int(raw)
                if n != rows and abs(n - rows) <= max(4, rows // 3):
                    out.append('%s:%d  "%s" but the table beside it has %d rows'
                               % (rel, k + 1, m.group(0), rows))
    return out

def main():
    bad = []
    for rel, pat, fn, label in DERIVED:
        text = io.open(path(rel), encoding='utf-8').read()
        want = fn()
        hits = re.findall(pat, text, re.M)
        if not hits:
            bad.append('%s  RULE DID NOT MATCH -- the sentence it guards was reworded or '
                       'removed, so this number is now unchecked: %s' % (rel, label))
            continue
        for h in hits:
            got = int(str(h).replace(',', ''))
            if got != want:
                bad.append('%s  says %s, data says %d  (%s)' % (rel, h, want, label))

    for root, _, files in os.walk(path('wiki')):
        for f in files:
            if f.endswith('.md'):
                rel = os.path.relpath(os.path.join(root, f), ROOT)
                bad += check_tables(rel)
                bad += check_spans(rel)

    print('=' * 70)
    print('INTERNAL CONSISTENCY -- numbers in prose against the data behind them')
    print('=' * 70)
    print('  DERIVED rules: %d' % len(DERIVED))
    if not bad:
        print('  no disagreements')
        return 0
    for b in bad:
        print('  - %s' % b)
    return 1

sys.exit(main())
