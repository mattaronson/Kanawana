#!/usr/bin/env python3
"""Mechanical VERIFY harness for p_218 -- the deterministic half of the R3-verified bar.

Checks per article:
  A1. header "Sources: N" == count of numbered Sources entries
  A2. articles.json sources_cited (as a SET) == set of [src_xxx] ids appearing in the article
      (numbered entries may legitimately repeat a source, so compare sets, not counts)
  B. every ^N citation marker resolves to a numbered Sources entry
  C. every numbered Sources entry is actually cited by some ^N marker (orphan sources)
  D. every [src_xxx] bracket resolves to a real sources.json record
  E. every [[wiki-link]] resolves to a real file
  F. header status line == articles.json status
  G. header "Last Updated" present

SCOPE NOTE (2026-08-14): checks A1/A2/B/C/D/E/F/G run over DRAFT articles only,
because they encode the R3-verified bar. But check B (do citation markers
resolve?) is a plain integrity property that every article should satisfy, and
restricting it to drafts hid a real defect: canoe-trips.md, an E1-REVIEWED
article, carried markers ^3-^7 against an unnumbered bullet source list, so
none of them resolved. It had been that way for months.

So a WHOLE-WIKI pass now runs check B over all articles regardless of status,
reported separately at the end. Do not narrow it back to drafts. The lesson
generalises: a checker scoped to the articles you are currently working on will
not tell you about the articles you are not.

SCOPE NOTE (2026-09-02): checks A1 and G were widened the same way, for the same
reason, and immediately found sixteen articles with broken source numbering --
including the-kanawana-site.md, at E1-reviewed, carrying TWO entries numbered 36.
Eleven of twelve wrong headers were too LOW, i.e. sources appended after the
article stopped being a draft, which is exactly the life-cycle stage a draft-only
scope cannot reach. See f_2365, f_2366 and scripts/verify/renumber_sources.py.

WHAT THIS HARNESS STILL CANNOT SEE: an article that disagrees with its own data.
It passed all six plaque-audit articles clean while one of them stated three
counts that its own index contradicted. That is scripts/verify/consistency.py
(p_301); run BOTH.

PROVENANCE CHECKS (2026-08-16, operator-requested). Everything above audits what
the wiki SAYS. These three audit what the project has actually READ -- a
different failure mode, and the one that caused every blocker cleared on
2026-08-14. Three of those four were resolved by reading material already on
disk: the c_024 passage was quoted in the conflict record itself, the 1966
shield was legible in a photograph already supplied, and the Concordia
catalogue was sitting in sources/cache/. The failure was not insufficient
searching. It was stopping once a claim fit, and then writing the stop into the
record as though it were a finding.

  H. READ RECEIPTS. Every source should carry a read_state saying whether it was
     actually opened, and on what basis. Without it, "read it, nothing there"
     and "never opened" are the same null -- which is precisely how 594 of 638
     corpus items sat unopened for five months while the wiki recorded confident
     nulls against them. H also cross-checks: a source marked unopened that is
     nevertheless cited by a fact is an inconsistency worth seeing.
  I. DORMANCY. Sources cited by no fact AND named in no article. Not
     necessarily a defect -- a genuine null result is dormant and should be --
     but a dormant source with read_state 'unknown' is unexamined material the
     project has forgotten it holds.
  L. ALIAS RECORDS. Two source records with DIFFERENT ids but the SAME origin_url
     are the same document registered twice. This is not the same defect as K
     (one id held by several records) and K cannot see it. It matters because an
     alias can be DORMANT while its twin is cited all over the wiki, which makes
     the dormancy report (I) overstate how much material is genuinely unexamined:
     8 of the 53 sources flagged dormant on 2026-08-18 turned out to be aliases
     of live sources, including the 1891-92 annual report whose "Out-door Work
     suffers from the disadvantage of not owning suitable grounds" is quoted in
     two articles under the twin id.
  J. CONFLICT PASSAGES. Every position in a conflict record must carry the FULL
     surrounding passage, not just the claim restated. c_024 was filed as an
     unresolvable human-decision-point on the strength of a quoted span; the
     sentence that dissolved it sat in the same paragraph, and the conflict
     stood for a day because nobody re-read around the quote. A passage that is
     no longer than its own claim is not a passage.
  M. CONFLICTS THE KB ALREADY ANSWERS. [THRESHOLD: >=2 shared subject terms. Set
     by replaying c_026, not guessed -- >=1 returned 177 facts (unreadable), >=2
     returned 37 including f_2127 (the fact that dissolved it), >=3 returned 8
     and lost f_2127, i.e. would have failed the case the check exists for.] A conflict record whose positions cite no
     facts at all, while the KB holds facts on the same subject, was probably
     raised without checking what was already known. c_026 is the case that
     forced this check: it was filed on 2026-08-18 as a bare 1974-vs-2017
     disagreement about acreage, with empty facts[] on both positions -- and
     f_2127, added eight versions earlier, already recorded the whole acreage
     series, the intervening 1964 purchase, and the report line ("no record
     found that showed the Kanawana site has ever been surveyed") that explains
     why the figures never agreed. Nothing in H-L could see this: those checks
     ask whether SOURCES were read, and here the source had been read and
     extracted. The unread thing was the KB itself. M is a weak signal by
     construction -- empty facts[] is a proxy, and a genuinely novel conflict
     can legitimately have one -- so it prints candidates, not defects.

These are deliberately NON-BLOCKING and print as a separate section. They
measure the project's reading discipline, not any article's correctness.
"""
import json, os, re
from collections import defaultdict

# Derived, not hardcoded: this runs on a CI runner as well as in the session
# container, and the old absolute path existed only in the latter.
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WIKI = os.path.join(ROOT, 'wiki')

arts = json.load(open(os.path.join(ROOT, 'wiki/articles.json')))['articles']
sources = json.load(open(os.path.join(ROOT, 'sources/sources.json')))['sources']
SRC_IDS = set(s['source_id'] for s in sources)

files = {}
for root, _dirs, fnames in os.walk(WIKI):
    for f in fnames:
        if f.endswith('.md'):
            rel = os.path.relpath(os.path.join(root, f), WIKI)
            files[rel[:-3]] = os.path.join(root, f)

DRAFTS = [a for a in arts if a['status'] == 'draft']

link_re    = re.compile(r'\[\[([^\]]+?)\]\]')
cite_re    = re.compile(r'\^(\d+)')
srcref_re  = re.compile(r'\bsrc_[A-Za-z0-9_]+')   # matches ids inside combined brackets too, e.g. [src_a, src_b]
hdr_src_re = re.compile(r'^\*Status:\s*([a-zA-Z0-9\-]+)\s*\|\s*Sources:\s*(\d+)', re.M)
srcline_re = re.compile(r'^(\d+)\.\s', re.M)

def article_path(a):
    return os.path.join(WIKI, a['wiki_folder'], a['article_id'] + '.md')

report = {}
for a in sorted(DRAFTS, key=lambda x: x['article_id']):
    path = article_path(a)
    issues = []
    if not os.path.exists(path):
        report[a['article_id']] = ['MISSING FILE: ' + path]
        continue
    text = open(path, encoding='utf-8').read()

    parts = re.split(r'^## Sources\s*$', text, flags=re.M)
    body = parts[0]
    srcsec = re.split(r'^## ', parts[1], flags=re.M)[0] if len(parts) > 1 else ''

    m = hdr_src_re.search(text)
    if not m:
        issues.append('F: no parseable "*Status: X | Sources: N*" header line')
        hdr_n = None
    else:
        hdr_status, hdr_n = m.group(1), int(m.group(2))
        if hdr_status != a['status']:
            issues.append('F: header status %r != articles.json status %r' % (hdr_status, a['status']))

    numbered = srcline_re.findall(srcsec)
    n_numbered = len(numbered)
    if hdr_n is not None and hdr_n != n_numbered:
        issues.append('A1: header "Sources: %d" != %d numbered entries' % (hdr_n, n_numbered))

    # A2: compare SETS of source ids, not counts
    in_article = set()
    for br in re.findall(r'\[([^\]]*src_[^\]]*)\]', text):
        in_article |= set(srcref_re.findall(br))
    in_json = set(a.get('sources_cited', []))
    missing_from_json = sorted(in_article - in_json)
    extra_in_json = sorted(in_json - in_article)
    if missing_from_json:
        issues.append('A2: cited in article but absent from articles.json sources_cited: %s' % missing_from_json)
    if extra_in_json:
        issues.append('A2: in articles.json sources_cited but never cited in article: %s' % extra_in_json)

    cited = set(int(x) for x in cite_re.findall(body))
    avail = set(int(x) for x in numbered)
    if sorted(cited - avail):
        issues.append('B: citation markers with no Sources entry: %s' % sorted(cited - avail))
    if sorted(avail - cited):
        issues.append('C: Sources entries never cited by a ^N marker: %s' % sorted(avail - cited))

    bad_src = sorted(s for s in in_article if s not in SRC_IDS)
    if bad_src:
        issues.append('D: [src_] refs not in sources.json: %s' % bad_src)

    bad_links = []
    for mm in link_re.finditer(text):
        tgt = re.split(r'\\\|', mm.group(1))[0].split('|')[0].strip()
        if tgt not in files:
            bad_links.append(tgt)
    if bad_links:
        issues.append('E: broken wiki-links: %s' % sorted(set(bad_links)))

    if not re.search(r'^\*Last Updated:', text, re.M):
        issues.append('G: no "*Last Updated:*" line')

    report[a['article_id']] = issues

# ---------------------------------------------------------------------------
# WHOLE-WIKI pass: citation markers must resolve, in EVERY article, any status.
# Articles whose Sources section is a bullet list (no "N." entries) legitimately
# use label-style markers (^mc, ^charron); those carry no digits and are skipped
# by cite_re, so a bullet-list article only fails here if it mixes the two --
# which is exactly the defect this pass exists to catch.
# ---------------------------------------------------------------------------
# Checks A1 and G run wide too, for the same reason. the-kanawana-site.md, at
# E1-REVIEWED, carried TWO source entries numbered 36 -- an oral-history entry
# appended with the number of the existing acreage entry -- so its ^36 marker
# resolved to whichever a reader hit first, and its header undercounted by one.
# A1 would have caught it on day one if A1 had been allowed to look. Restricting
# a check to drafts does not make the defect rarer, only invisible: an article
# is MOST likely to accumulate appended sources AFTER it stops being a draft.
wide = {}
wide_a1 = {}
wide_g = {}
for a in arts:
    p = article_path(a)
    if not os.path.exists(p):
        continue
    tx = open(p, encoding='utf-8').read()
    pp = re.split(r'^## Sources\s*$', tx, flags=re.M)
    if len(pp) < 2:
        continue
    srcsec_w = re.split(r'^## ', pp[1], flags=re.M)[0]
    numbered_list = [int(x) for x in srcline_re.findall(srcsec_w)]
    numbered_ids = set(numbered_list)
    used = set(int(x) for x in cite_re.findall(pp[0]))
    missing = sorted(used - numbered_ids)
    if missing:
        wide[a['article_id']] = (a['status'], missing)

    # G: a source NUMBER used twice, or the sequence broken. Either way a ^N
    # marker stops being a unique address, which is the whole point of it.
    if numbered_list:
        dupes = sorted({n for n in numbered_list if numbered_list.count(n) > 1})
        gaps = [n for n in range(1, max(numbered_list) + 1) if n not in numbered_ids]
        if dupes or gaps:
            wide_g[a['article_id']] = (a['status'], dupes, gaps)

    # A1 wide: header count against the entries actually present.
    mh = hdr_src_re.search(tx)
    if mh and int(mh.group(2)) != len(numbered_list) and numbered_list:
        wide_a1[a['article_id']] = (a['status'], int(mh.group(2)), len(numbered_list))

clean = [k for k, v in report.items() if not v]
dirty = {k: v for k, v in report.items() if v}

print('=' * 70)
print('MECHANICAL VERIFY -- %d draft articles' % len(DRAFTS))
print('=' * 70)
print('CLEAN (%d):' % len(clean))
for k in clean:
    print('    %s' % k)
print()
print('WITH ISSUES (%d):' % len(dirty))
for k in sorted(dirty):
    print('\n  %s' % k)
    for i in dirty[k]:
        print('    - %s' % i)

klass = defaultdict(int)
for v in dirty.values():
    for i in v:
        klass[i.split(':')[0]] += 1
print('\n' + '=' * 70)
print('ISSUE COUNTS BY CLASS:', dict(sorted(klass.items())))

print('\n' + '=' * 70)
print('WHOLE-WIKI: unresolvable ^N citation markers (%d article(s), all statuses)' % len(wide))
print('=' * 70)
if not wide:
    print('    none')
for k in sorted(wide):
    st, miss = wide[k]
    print('    %-32s [%s] markers with no Sources entry: %s' % (k, st, miss))

print('\n' + '=' * 70)
print('WHOLE-WIKI: header "Sources: N" != numbered entries (%d article(s), all statuses)' % len(wide_a1))
print('=' * 70)
if not wide_a1:
    print('    none')
for k in sorted(wide_a1):
    st, hdr, n = wide_a1[k]
    print('    %-32s [%s] header says %d, %d entries present' % (k, st, hdr, n))

print('\n' + '=' * 70)
print('WHOLE-WIKI: duplicate or missing source NUMBERS (%d article(s), all statuses)' % len(wide_g))
print('=' * 70)
if not wide_g:
    print('    none')
for k in sorted(wide_g):
    st, dupes, gaps = wide_g[k]
    bits = []
    if dupes: bits.append('numbers used twice: %s' % dupes)
    if gaps:  bits.append('numbers skipped: %s' % gaps)
    print('    %-32s [%s] %s' % (k, st, '; '.join(bits)))

# ===========================================================================
# PROVENANCE PASS -- checks H, I, J. Non-blocking; see the module docstring.
# ===========================================================================
facts = json.load(open(os.path.join(ROOT, 'kb/facts.json')))['facts']
conflicts_raw = json.load(open(os.path.join(ROOT, 'kb/conflicts.json')))
conflicts = conflicts_raw if isinstance(conflicts_raw, list) else conflicts_raw.get('conflicts', [])

VALID_READ_STATES = {'extracted', 'skimmed', 'unopened', 'unavailable', 'unknown'}

cited_by_fact = set()
for f in facts:
    cited_by_fact |= set(f.get('sources', []))

all_wiki_text = ''
for p in files.values():
    all_wiki_text += open(p, encoding='utf-8').read()
named_in_wiki = set(s['source_id'] for s in sources if s['source_id'] in all_wiki_text)

# --- H: read receipts -------------------------------------------------------
no_state, bad_state, contradictory = [], [], []
state_counts = defaultdict(int)
for s in sources:
    st = s.get('read_state')
    if st is None:
        no_state.append(s['source_id'])
        continue
    state_counts[st] += 1
    if st not in VALID_READ_STATES:
        bad_state.append((s['source_id'], st))
    if st == 'unopened' and s['source_id'] in cited_by_fact:
        contradictory.append(s['source_id'])

# H2: the legacy boolean `extracted` vs. the evidence. These are two independent
# claims about the same thing and they disagree, so neither can be trusted alone.
# extracted=False while facts cite it is the interesting direction: the flag was
# simply never flipped when the source was used.
flag_false_but_cited = [s['source_id'] for s in sources
                        if not s.get('extracted') and s['source_id'] in cited_by_fact]
flag_true_but_uncited = [s['source_id'] for s in sources
                         if s.get('extracted') and s['source_id'] not in cited_by_fact]

# --- I: dormancy ------------------------------------------------------------
dormant = [s for s in sources
           if s['source_id'] not in cited_by_fact and s['source_id'] not in named_in_wiki]

# --- J: conflict passages ---------------------------------------------------
# TWO SCHEMAS EXIST. c_023-c_025 use positions[{claim, source, facts}]; c_001-c_022
# use an older shape with values[] / fact_ids[]. The first version of this check
# only understood positions[] and so silently passed 22 of 25 conflicts -- the
# very "checker scoped to what you happen to be working on" failure the module
# docstring warns about, reproduced inside the check written to prevent it.
# Conflicts whose shape is not recognised are now REPORTED, never skipped.
thin_positions, unreadable = [], []
for c in conflicts:
    cid, st = c['conflict_id'], c.get('status', '?')
    if c.get('positions'):
        for i, pos in enumerate(c['positions']):
            passage = (pos.get('passage') or '').strip()
            claim = (pos.get('claim') or '').strip()
            if not passage:
                thin_positions.append((cid, st, 'position %d' % i, 'no passage field'))
            elif len(passage) <= len(claim):
                thin_positions.append((cid, st, 'position %d' % i,
                                       'passage (%d ch) not longer than claim (%d ch)'
                                       % (len(passage), len(claim))))
    elif c.get('values'):
        for i, v in enumerate(c['values'] if isinstance(c['values'], list) else [c['values']]):
            txt = json.dumps(v) if not isinstance(v, str) else v
            if 'passage' not in txt:
                thin_positions.append((cid, st, 'value %d' % i, 'legacy schema, no passage'))
    else:
        unreadable.append((cid, st, sorted(c.keys())))

print('\n' + '=' * 70)
print('PROVENANCE PASS (non-blocking) -- what has actually been READ')
print('=' * 70)

print('\nH. READ RECEIPTS -- %d sources' % len(sources))
if state_counts:
    for k in sorted(state_counts):
        print('     read_state=%-12s %4d' % (k, state_counts[k]))
print('     %-21s %4d   <-- cannot tell "read, empty" from "never opened"' % ('NO read_state:', len(no_state)))
if bad_state:
    print('     INVALID read_state values (%d): %s' % (len(bad_state), bad_state[:10]))
if contradictory:
    print('     CONTRADICTORY (%d): marked unopened but cited by a fact: %s'
          % (len(contradictory), contradictory[:10]))
print('     legacy flag `extracted` vs. evidence:')
print('       extracted=False yet cited by a fact: %4d  (flag never flipped; trust the citation)'
      % len(flag_false_but_cited))
print('       extracted=True  yet cited by nothing: %4d  (flag asserts a read the KB cannot show)'
      % len(flag_true_but_uncited))

print('\nI. DORMANT SOURCES -- %d of %d cited by no fact AND named in no article' % (len(dormant), len(sources)))
if not dormant:
    print('     none')
for s in sorted(dormant, key=lambda x: (x.get('read_state') or 'zzz', x['source_id'])):
    print('     %-46s [%s] %s' % (s['source_id'],
                                  s.get('read_state') or 'NO read_state',
                                  (s.get('title') or '')[:70]))

# --- L: alias records (same URL, different id) -------------------------------
byurl = defaultdict(list)
for s in sources:
    u = (s.get('origin_url') or '').strip().rstrip('/')
    if u:
        byurl[u].append(s['source_id'])
alias_groups = []
for u, ids in sorted(byurl.items()):
    uniq = sorted(set(ids))
    if len(uniq) > 1:
        live = lambda i: i in cited_by_fact or i in named_in_wiki
        marks = [(i, 'live' if live(i) else 'DORMANT') for i in uniq]
        shadowing = any(m == 'DORMANT' for _, m in marks) and any(m == 'live' for _, m in marks)
        alias_groups.append((u, marks, shadowing))
shadow_groups = [g for g in alias_groups if g[2]]

print('\nL. ALIAS RECORDS -- %d URL(s) registered under more than one source_id' % len(alias_groups))
print('     of those, %d have a DORMANT id shadowing a live one -- these are NOT' % len(shadow_groups))
print('     unexamined material, they are the same document counted twice:')
if not shadow_groups:
    print('     none')
for u, marks, _ in shadow_groups:
    print('     %s' % u[:92])
    for i, m in marks:
        print('        %-8s %s' % (m, i))

print('\nJ. CONFLICT PASSAGES -- %d position(s) across %d conflict(s) without a full passage'
      % (len(thin_positions), len(set(x[0] for x in thin_positions))))
if not thin_positions:
    print('     none')
for cid, st, where, why in thin_positions:
    print('     %-8s [%-21s] %-12s %s' % (cid, st, where, why))
if unreadable:
    print('     UNRECOGNISED SHAPE -- not inspected, do not read as passing (%d):' % len(unreadable))
    for cid, st, keys in unreadable:
        print('       %-8s [%-21s] keys=%s' % (cid, st, keys))

# --- K: duplicate source ids (integrity) ------------------------------------
id_counts = defaultdict(int)
for s in sources:
    id_counts[s['source_id']] += 1
dup_ids = sorted(k for k, v in id_counts.items() if v > 1)
print('\nK. DUPLICATE source_ids -- %d id(s) held by more than one record' % len(dup_ids))
if not dup_ids:
    print('     none')
else:
    print('     %d records / %d unique ids. A [src_x] citation pointing at a duplicated'
          % (len(sources), len(id_counts)))
    print('     id is ambiguous: it resolves to whichever record a reader happens to hit.')
    for k in dup_ids:
        print('     %-44s x%d' % (k, id_counts[k]))


# --- M: conflicts the KB may already answer ---------------------------------
# Proxy, not proof: a conflict whose positions cite NO facts, while facts on the
# same entity exist in the KB. See the module docstring for why this check is
# separate from H-L -- the unread thing here is kb/facts.json, not a source.
facts_doc = json.load(open(os.path.join(ROOT, 'kb/facts.json')))['facts']
conf_doc = json.load(open(os.path.join(ROOT, 'kb/conflicts.json')))
conflicts = conf_doc if isinstance(conf_doc, list) else conf_doc['conflicts']

def _cited_facts(c):
    out = []
    for pos in c.get('positions', []) or []:
        out += pos.get('facts', []) or []
    out += c.get('fact_ids', []) or []
    return [f for f in out if f]

# Matching had to be rebuilt after a self-test. The first version required the
# entity string and an attribute word to appear VERBATIM in the fact, and scored
# 0 hits when replayed against pre-resolution c_026 -- entity "Camp Kanawana
# site" against a fact whose entity is "Kamp Kanawana", attribute "acreage"
# against a fact that says "land area" and "acres". It would have passed the one
# conflict it was written for. So: normalise Kamp/Camp, match entity by token,
# and draw the subject vocabulary from the POSITION CLAIMS as well as the
# attribute field -- the claims are where the shared word ("acres") actually is.
_STOP = set('''about above across after against along among around because been
before being below between both camp during each从 from have into more most only
other over same since some such than that their them then there these they this
those through under until were what when where which while with would'''.split())

def _norm(t):
    return re.sub(r'\bkamp\b', 'camp', (t or '').lower())

def _subject_terms(c):
    text = ' '.join([c.get('attribute') or ''] +
                    [(p.get('claim') or '') for p in (c.get('positions') or [])])
    toks = set()
    for w in re.findall(r'[a-z]{5,}', _norm(text)):
        if w not in _STOP:
            toks.add(w[:4])          # crude stem: acreage/acres -> "acre"
    return toks

# Check J learned the hard way that a checker which only understands the schema
# in front of it will silently pass everything written in the other one. M is
# subject to the same trap: it keys on 'entity', which the c_001-c_022 shape does
# not have. Those are reported as un-inspected rather than skipped in silence.
candidates = []
m_unreadable = []
for c in conflicts:
    if c.get('status') != 'unresolved':
        continue
    if _cited_facts(c):
        continue
    ent = (c.get('entity') or '').strip()
    attr = (c.get('attribute') or '').strip()
    if not ent:
        m_unreadable.append((c.get('conflict_id', '?'), sorted(c.keys())))
        continue
    ent_toks = set(w for w in re.findall(r'[a-z]{4,}', _norm(ent)) if w not in _STOP)
    terms = _subject_terms(c)
    if not ent_toks or not terms:
        m_unreadable.append((c.get('conflict_id', '?'), sorted(c.keys())))
        continue
    hits = []
    for f in facts_doc:
        blob = _norm(f['claim'] + ' ' + ' '.join(f.get('entities', []) or []))
        if not any(re.search(r'\b' + re.escape(t), blob) for t in ent_toks):
            continue
        n = sum(1 for t in terms if re.search(r'\b' + re.escape(t), blob))
        if n >= 2:                    # see THRESHOLD note in the module docstring
            hits.append((n, f['fact_id']))
    if hits:
        hits.sort(reverse=True)
        candidates.append((c['conflict_id'], ent, attr, hits))

print('\nM. CONFLICTS THE KB MAY ALREADY ANSWER -- %d unresolved conflict(s) cite no' % len(candidates))
print('     facts while the KB holds facts on the same subject. Read these before')
print('     treating the conflict as open; empty facts[] is a proxy, not a defect:')
if not candidates:
    print('     none')
for cid, ent, attr, hits in candidates:
    print('     %-8s %s -- %s' % (cid, ent, attr))
    print('        %d KB fact(s) share >=2 subject terms; strongest first:' % len(hits))
    for n, fid in hits[:8]:
        print('          %s  (%d terms)' % (fid, n))
if m_unreadable:
    print('     NO entity FIELD -- not inspected, do not read as passing (%d):' % len(m_unreadable))
    for cid, keys in m_unreadable:
        print('       %-8s keys=%s' % (cid, keys))

# ===========================================================================
# EXIT CODE. Added 2026-09-03, when this harness was wired into CI and turned
# out to have no sys.exit at all: it reported everything and always exited 0,
# so nothing it found could ever fail a build.
#
# BLOCKING: A1, A2, B, D, E, F, G on drafts, and all three whole-wiki passes.
# These are integrity failures -- a marker that resolves nowhere, a source id
# that is not a source, a header that miscounts its own list.
#
# ADVISORY: C (a Sources entry no marker cites). A listed-but-uncited source is
# often deliberate -- a null result recorded so the ground is not re-covered --
# and failing a build on it would train people to ignore the build.
#
# The provenance passes H-M are advisory by design; see the docstring.
# ===========================================================================
BLOCKING_CLASSES = {'A1', 'A2', 'B', 'D', 'E', 'F', 'G'}
_blocking = sorted({k for v in dirty.values() for i in v
                    if (k := i.split(':')[0]) in BLOCKING_CLASSES})
_wide = len(wide) + len(wide_a1) + len(wide_g)

print('\n' + '=' * 70)
if _blocking or _wide:
    print('FAIL -- blocking issue classes present: %s' % (_blocking or 'none'))
    if _wide:
        print('       plus %d whole-wiki finding(s): %d unresolvable marker(s), '
              '%d header mismatch(es), %d numbering break(s)'
              % (_wide, len(wide), len(wide_a1), len(wide_g)))
    print('=' * 70)
    sys.exit(1)
print('PASS -- no blocking issue class, no whole-wiki finding')
print('       (advisory findings above, if any, do not fail the build)')
print('=' * 70)
sys.exit(0)
