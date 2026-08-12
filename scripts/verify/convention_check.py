#!/usr/bin/env python3
"""Learn the header 'Sources: N' convention from the 50 E1-reviewed articles (the gold standard),
instead of assuming it. Compares header N against three candidate conventions:
   (a) count of numbered entries in the Sources section
   (b) count of unique [src_xxx] ids in the article
   (c) len(articles.json sources_cited)
"""
import json, os, re
from collections import Counter

ROOT = '/home/user/Kanawana'
WIKI = os.path.join(ROOT, 'wiki')
arts = json.load(open(os.path.join(ROOT, 'wiki/articles.json')))['articles']

hdr_re = re.compile(r'^\*Status:\s*([a-zA-Z0-9\-]+)\s*\|\s*Sources:\s*(\d+)', re.M)
srcline_re = re.compile(r'^(\d+)\.\s', re.M)
srcref_re = re.compile(r'\[(src_[A-Za-z0-9_]+)\]')

def path_of(a):
    return os.path.join(WIKI, a['wiki_folder'], a['article_id'] + '.md')

for status in ('E1-reviewed', 'R3-verified'):
    tally = Counter()
    mismatch_examples = {'a': [], 'b': [], 'c': []}
    n = 0
    for a in arts:
        if a['status'] != status:
            continue
        p = path_of(a)
        if not os.path.exists(p):
            continue
        text = open(p, encoding='utf-8').read()
        m = hdr_re.search(text)
        if not m:
            tally['NO_HEADER'] += 1
            continue
        hdr_n = int(m.group(2))
        parts = re.split(r'^## Sources\s*$', text, flags=re.M)
        srcsec = re.split(r'^## ', parts[1], flags=re.M)[0] if len(parts) > 1 else ''
        a_val = len(srcline_re.findall(srcsec))
        b_val = len(set(srcref_re.findall(text)))
        c_val = len(a.get('sources_cited', []))
        n += 1
        for key, val in (('a', a_val), ('b', b_val), ('c', c_val)):
            if hdr_n == val:
                tally['matches_' + key] += 1
            elif len(mismatch_examples[key]) < 3:
                mismatch_examples[key].append('%s: hdr=%d %s=%d' % (a['article_id'], hdr_n, key, val))

    print('=' * 68)
    print('%s  (%d articles with a parseable header)' % (status, n))
    print('  (a) header == numbered Sources entries : %d/%d' % (tally['matches_a'], n))
    print('  (b) header == unique [src_] ids        : %d/%d' % (tally['matches_b'], n))
    print('  (c) header == articles.json sources_cited: %d/%d' % (tally['matches_c'], n))
    if tally['NO_HEADER']:
        print('  no parseable header: %d' % tally['NO_HEADER'])
    for k in ('a', 'b', 'c'):
        if mismatch_examples[k]:
            print('  sample %s-mismatches: %s' % (k, '; '.join(mismatch_examples[k])))
