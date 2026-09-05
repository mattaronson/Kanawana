#!/usr/bin/env python3
"""Cross-check W. E. Yard's 1949-1963 catalogue of articles against the blocks in
cc_findings.md.

The December 1963 issue printed the magazine's own cumulative subject index. Every
article it lists for an issue this pass has read should be traceable in that issue's
block; anything that is not is a candidate hole. This is a mechanical screen, not a
verdict: OCR noise in the index, and the fact that a block may cover an article under a
different form of words, both produce false positives. Read the report, do not trust it.

Usage: catalogue_check.py [max_issue]
"""
import re, io, sys, unicodedata

MAXN = int(sys.argv[1]) if len(sys.argv) > 1 else 60

MONTHS = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'june':6,'jul':7,'july':7,
          'aug':8,'sep':9,'sept':9,'oct':10,'nov':11,'dec':12}

def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = s.replace('’', "'").replace('‘', "'")
    s = re.sub(r'[^a-z0-9 ]+', ' ', s.lower())
    return re.sub(r'\s+', ' ', s).strip()

# --- issue blocks, and the (year, month) each covers -------------------------
src = io.open('kb/reread/cc_findings.md', encoding='utf-8').read()
heads = [(int(m.group(1)), m.start(), m.group(0)) for m in re.finditer(r'(?m)^## (\d+)\b.*$', src)]
heads.append((10**9, len(src), ''))
blocks, dates = {}, {}
for i, (n, st, head) in enumerate(heads[:-1]):
    blocks[n] = norm(src[st:heads[i+1][1]])
    m = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', head)
    if m:
        dates[n] = (int(m.group(2)), MONTHS[m.group(1)[:3].lower()])
by_date = {v: k for k, v in dates.items()}

# --- catalogue entries -------------------------------------------------------
cat = io.open('kb/reread/cc_catalogue_1949_1963.md', encoding='utf-8').read()
ENTRY = re.compile(r'^(.*?)[.\s!]*((?:Jan|Feb|Mar|Apr|May|June?|July?|Aug|Sept?|Oct|Nov|Dec)[a-z]*)[.!\s]*(\d{4})\s*$')

missing, checked, undated = [], 0, 0
for raw in cat.splitlines():
    line = raw.strip()
    if not line or line.startswith('#') or line.startswith('---'):
        continue
    m = ENTRY.match(line)
    if not m:
        continue
    title_author, mon, yr = m.group(1), m.group(2), int(m.group(3))
    key = (yr, MONTHS[mon[:3].lower()])
    n = by_date.get(key)
    if n is None or n > MAXN:
        undated += 1
        continue
    # split title from author on the em dash the index uses
    parts = re.split(r'[—–-]{1,2}', title_author)
    title = norm(parts[0])
    author = norm(parts[-1]) if len(parts) > 1 else ''
    words = [w for w in title.split() if len(w) > 3]
    if len(words) < 2:
        continue
    checked += 1
    block = blocks[n]
    # a hit is: any two of the title's longer words adjacent-ish in the block, or
    # three of them present anywhere, or the author surname present.
    present = [w for w in words if w in block]
    surname = author.split()[-1] if author else ''
    hit = (len(present) >= max(2, len(words) - 1)) or (len(surname) > 4 and surname in block)
    if not hit:
        missing.append((n, key, title_author.strip(), len(present), len(words)))

print('catalogue cross-check, issues 1-%d' % MAXN)
print('  %d dated entries fell inside the range and were checked; %d fell outside it' % (checked, undated))
print('  %d entries did not match their block:' % len(missing))
for n, key, t, p, w in sorted(missing):
    print('    issue %3d (%d-%02d)  %-70s  [%d/%d title words present]' % (n, key[0], key[1], t[:70], p, w))
