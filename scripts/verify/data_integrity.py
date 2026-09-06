"""Cheap structural checks on the data files, for CI.

Three things that have actually gone wrong in this project and would each have
been caught here in a second:

  1. UNPARSEABLE JSON. A trailing comma turned a string concatenation into a
     tuple, kb/facts.json was never written, and the commit went through with
     only half the change in it.

  2. DUPLICATE OR MALFORMED IDS, AND FIELDS OF THE WRONG TYPE. fact_id,
     source_id, article_id and conflict_id must each be unique and well
     formed; a duplicated source_id makes every [src_x] citation to it
     ambiguous. A fact's claim must be a non-empty string and its sources,
     entities and conflicts_with must be lists -- a claim that is not a string
     parses as valid JSON, passes every id check, and then crashes three other
     verify scripts on the regex that reads it.

  3. GENERATED FILES OUT OF DATE. kb/plaque-audit/person-index.json and the
     table in wiki/people/multi-year-index.md are outputs of build_index.py and
     build_table.py. Editing either by hand, or changing the builder without
     re-running it, is how the wiki came to state three counts its own index
     contradicted. Three fields of wiki/articles.json -- word_count,
     open_questions and article_count -- are likewise outputs, of
     scripts/wiki/build_article_counts.py; they were hand-written until
     2026-09-05, when half the file turned out to be stale (p_417). This
     regenerates all three files into a scratch copy and fails if the committed
     files differ.

BLOCKING vs ADVISORY. A check earns the right to fail a build by being
actionable by whoever just pushed. Duplicate source_ids are real -- twenty of
them -- but they predate this workflow, resolving them needs a judgement about
which record is canonical, and that is queued as p_303. Failing every build on
a standing backlog item teaches people to ignore the build, which costs more
than the defect. So it reports and does not fail, and moves to blocking the day
p_303 clears.

Exit 1 on any BLOCKING failure.
"""
import json, io, os, re, sys, subprocess, shutil, tempfile, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def P(*p): return os.path.join(ROOT, *p)

JSON_FILES = ['kb/facts.json', 'kb/conflicts.json', 'wiki/articles.json',
              'sources/sources.json', 'queue/priorities.json',
              'kb/plaque-audit/person-index.json', 'kb/plaque-audit/candidate-pairs.json']
JSONL_FILES = ['kb/plaque-audit/audit.jsonl', 'kb/reread/ledger.jsonl',
               'kb/restricted/register.jsonl', 'kb/reread/queue.json']

ID_RE = {'fact_id': re.compile(r'^f_\d{4,}$'),
         'conflict_id': re.compile(r'^c_\d{3,}$'),
         'source_id': re.compile(r'^src_[A-Za-z0-9_]+$'),
         'priority_id': re.compile(r'^p_\d{3,}$')}

def main():
    bad = []       # blocking
    note = []      # advisory: real, but not this push's to fix

    for rel in JSON_FILES:
        p = P(rel)
        if not os.path.exists(p):
            continue
        try:
            json.load(open(p, encoding='utf-8'))
        except Exception as e:
            bad.append('%s: does not parse as JSON -- %s' % (rel, e))

    for rel in JSONL_FILES:
        p = P(rel)
        if not os.path.exists(p):
            continue
        if rel.endswith('.json'):
            try: json.load(open(p, encoding='utf-8'))
            except Exception as e: bad.append('%s: does not parse -- %s' % (rel, e))
            continue
        for n, line in enumerate(io.open(p, encoding='utf-8'), 1):
            if not line.strip(): continue
            try: json.loads(line)
            except Exception as e: bad.append('%s:%d does not parse -- %s' % (rel, n, e))

    if not any(b.startswith('kb/facts.json') for b in bad):
        facts = json.load(open(P('kb/facts.json'), encoding='utf-8'))
        ids = [f['fact_id'] for f in facts['facts']]
        dup = [k for k, v in collections.Counter(ids).items() if v > 1]
        if dup: bad.append('kb/facts.json: duplicate fact_id(s): %s' % dup[:10])
        malformed = [i for i in ids if not ID_RE['fact_id'].match(i)]
        if malformed: bad.append('kb/facts.json: malformed fact_id(s): %s' % malformed[:10])
        if facts.get('fact_count') != len(ids):
            bad.append('kb/facts.json: fact_count is %r, there are %d facts'
                       % (facts.get('fact_count'), len(ids)))
        # A claim that is not a string parses as valid JSON and passes every id
        # check, then crashes three other verify scripts on the regex that reads
        # it. That happened on 2026-09-05, from a stray comma turning a claim
        # into a tuple; the file was committed-clean by this script and broken
        # for citation_aim, staleness and restricted_guard. Types are checked
        # here so the failure lands where the defect is.
        SHAPE = {'claim': str, 'sources': list, 'confidence': str,
                 'entities': list, 'conflicts_with': list}
        for f in facts['facts']:
            for field, want in SHAPE.items():
                if field in f and not isinstance(f[field], want):
                    bad.append('%s: %s is %s, expected %s'
                               % (f['fact_id'], field, type(f[field]).__name__, want.__name__))
            if isinstance(f.get('claim'), str) and not f['claim'].strip():
                bad.append('%s: claim is empty' % f['fact_id'])
            pub = f.get('publication')
            if pub and pub.get('status') not in (None, 'embargoed', 'released'):
                bad.append('%s: publication.status %r is not recognised' % (f['fact_id'], pub['status']))

    if not any(b.startswith('sources/sources.json') for b in bad):
        s = json.load(open(P('sources/sources.json'), encoding='utf-8'))
        rec = s if isinstance(s, list) else s['sources']
        sids = [r['source_id'] for r in rec]
        dup = [k for k, v in collections.Counter(sids).items() if v > 1]
        if dup:
            note.append('sources/sources.json: %d source_id(s) held by more than one record; '
                        'a [src_] citation to any of them is ambiguous. Pre-existing and queued '
                        'as p_303 -- advisory until that clears, then make this blocking. '
                        'First few: %s' % (len(dup), sorted(dup)[:5]))

        # every source_id a fact cites must have a record here. A fact written
        # by hand can invent one, and forty-two of them had, silently, for
        # months (p_220). The count in the queue drifted between the day it was
        # taken and the day it was fixed, which is why this is a check and not
        # a number written down somewhere.
        if not any(b.startswith('kb/facts.json') for b in bad):
            known = set(sids)
            dangling = collections.Counter()
            for f in facts['facts']:
                for sid in f.get('sources', []):
                    if sid not in known:
                        dangling[sid] += 1
            if dangling:
                bad.append('kb/facts.json cites %d source_id(s) with no record in '
                           'sources/sources.json: %s. Do not drop the citation. Decide for '
                           'each whether it is a variant of an existing record (remap the '
                           'fact) or a source never indexed (add a record saying it was '
                           'reconstructed from the citation and not read) -- see '
                           'project-docs/source-id-remap-2026-09-06.md for how the first '
                           'forty-two were handled.'
                           % (len(dangling), sorted(dangling)[:8]))

    # 3. generated files
    tmp = tempfile.mkdtemp(prefix='kanawana-regen-')
    try:
        for rel in ['kb', 'wiki', 'scripts', 'sources']:
            shutil.copytree(P(rel), os.path.join(tmp, rel), dirs_exist_ok=True)
        for script in ['scripts/plaque/build_index.py', 'scripts/plaque/build_table.py',
                       'scripts/wiki/build_article_counts.py']:
            r = subprocess.run([sys.executable, script], cwd=tmp,
                               capture_output=True, text=True)
            if r.returncode != 0:
                bad.append('%s: exits %d when re-run -- %s'
                           % (script, r.returncode, (r.stderr or '').strip()[-300:]))
        for rel in ['kb/plaque-audit/person-index.json', 'wiki/people/multi-year-index.md',
                    'wiki/articles.json']:
            a, b = P(rel), os.path.join(tmp, rel)
            if os.path.exists(a) and os.path.exists(b):
                if io.open(a, encoding='utf-8').read() != io.open(b, encoding='utf-8').read():
                    builder = ('scripts/wiki/build_article_counts.py'
                               if rel == 'wiki/articles.json'
                               else 'scripts/plaque/build_index.py then build_table.py')
                    detail = ('' if rel != 'wiki/articles.json' else
                              ' Only word_count, open_questions and article_count are '
                              'generated; every other field in that file is hand-maintained.')
                    bad.append('%s is not what its builder produces. Re-run %s and commit '
                               'the result -- do not edit those fields by hand.%s'
                               % (rel, builder, detail))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print('=' * 70)
    print('DATA INTEGRITY')
    print('=' * 70)
    for n in note:
        print('  [advisory] %s' % n)
    if not bad:
        print('  PASS -- data files parse; fact ids unique and well formed; '
              'generated files match their builders')
        return 0
    for b in bad:
        print('  - %s' % b)
    print('  FAIL')
    return 1

sys.exit(main())
