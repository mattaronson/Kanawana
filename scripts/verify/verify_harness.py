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
"""
import json, os, re
from collections import defaultdict

ROOT = '/home/user/Kanawana'
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
