#!/usr/bin/env python3
"""Cross-check kb/reread/cc_findings.md against the magazine's own 1949-63
article catalogue. Prints catalogue entries whose distinctive words are largely
absent from the findings file -- i.e. articles this read may have passed over.

Not a proof of omission: the findings blocks paraphrase, and the catalogue OCR
is noisy. Treat the output as a worklist, and confirm each candidate against the
cached issue before patching a block.

    python3 scripts/reread/catalogue_check.py
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
cat = (ROOT / 'kb/reread/cc_catalogue_1949_1963.md').read_text(encoding='utf-8')
find = (ROOT / 'kb/reread/cc_findings.md').read_text(encoding='utf-8')
fw = set(re.sub(r'[^a-z0-9]', ' ', find.lower()).split())

DATE = re.compile(r'(Jan|Feb|Mar|Apr|May|June|Tune|July|Aug|Sept|Oct|Nov|Dec)\.?\s*(19[45][0-9]|196[0-3])\s*$')
STOP = set("with your that this from what will they have been when where about "
           "their there here into more than some very camp camps camping canadian".split())

entries, miss = [], []
for line in (l.strip() for l in cat.split('\n')):
    m = DATE.search(line)
    if not m:
        continue
    head = re.sub(r'[.\s]{3,}$', '', line[:m.start()]).strip(' .')
    if len(head) < 6:
        continue
    entries.append((m.group(2), m.group(1), head))

for yr, mon, head in entries:
    title = re.split(r'[—–]\s*(?=[A-Z])', head)[0]
    words = [w for w in re.sub(r'[^a-z0-9]', ' ', title.lower()).split()
             if len(w) > 4 and w not in STOP]
    if len(words) < 2:
        continue
    hits = sum(1 for w in words if w in fw)
    if hits < max(2, len(words) - 1):
        miss.append((yr, mon, head))

print(f"catalogue entries parsed: {len(entries)}")
print(f"candidates for review:    {len(miss)}\n")
for yr, mon, head in sorted(miss):
    print(f"{yr} {mon:5s} | {head}")
