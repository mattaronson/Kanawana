#!/usr/bin/env python3
"""Wiki-wide person-name variant detector.

This project has had real name-corruption incidents (Arlene Boyle -> Arleen Boyer;
Joanna/Johanna Hoad/Hoade; Nicolas/Nicholas Garcia). This finds near-duplicate person
names across ALL wiki articles so a VERIFY pass can spot a variant that drifted into
one file but not another.

Method: harvest capitalised First(+Middle) Last sequences, group by surname-ish last
token, then report groups whose full forms differ. Also does an explicit check on the
known-risky names.
"""
import os, re, json
from collections import defaultdict
from difflib import SequenceMatcher

ROOT = '/home/user/Kanawana'
WIKI = os.path.join(ROOT, 'wiki')

# Capitalised name sequences: "Arleen Boyer", "Joanna A.A. Hoad", "R.L. Charlton"
name_re = re.compile(r'\b((?:[A-Z][a-z]+|[A-Z]\.(?:[A-Z]\.)*)(?:\s+(?:[A-Z][a-z]+|[A-Z]\.(?:[A-Z]\.)*)){1,3})\b')

STOP = set('''The A An And Or But For In On At To From With By Of As It He She They We You I This That These Those
Camp Kanawana Kamp YMCA Montreal Quebec Canada Canadian Concordia University Archives Sources Overview
Open Questions Related Articles Research Notes Status Last Updated Director Directors Executive Chief
Internet Archive Wayback Machine Annual Report Green Triangle Council Ring Lake Wilson Saint Sauveur
Two Tier Era Pip Award Notable Alumni'''.split())

occurrences = defaultdict(set)   # full name -> set of files
for root, _d, fnames in os.walk(WIKI):
    for f in fnames:
        if not f.endswith('.md'):
            continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, WIKI)
        text = re.sub(r'<!--.*?-->', '', open(path, encoding='utf-8').read(), flags=re.S)
        text = re.sub(r'\[\[[^\]]*\]\]', ' ', text)          # drop wiki-links
        text = re.sub(r'\[src_[^\]]*\]', ' ', text)          # drop source refs
        for m in name_re.finditer(text):
            nm = ' '.join(m.group(1).split())
            toks = nm.split()
            if any(t.strip('.') in STOP for t in toks):
                continue
            if len(toks) < 2:
                continue
            occurrences[nm].add(rel)

# group by last token (surname-ish), lowercased & de-punctuated
groups = defaultdict(list)
for nm in occurrences:
    groups[nm.split()[-1].lower().strip('.')].append(nm)

print('=' * 72)
print('NEAR-DUPLICATE NAME GROUPS (same surname, differing full form)')
print('=' * 72)
found = 0
for surname, names in sorted(groups.items()):
    if len(names) < 2:
        continue
    # only interesting if the forms are similar (likely same person), not e.g. two real siblings
    interesting = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            r = SequenceMatcher(None, names[i].lower(), names[j].lower()).ratio()
            if r >= 0.72:
                interesting.append((names[i], names[j], r))
    if interesting:
        found += 1
        print('\n  surname "%s":' % surname)
        for nm in sorted(names):
            print('     %-28s  %s' % (nm, ', '.join(sorted(occurrences[nm])[:4])))
print('\n  groups reported: %d' % found)

print('\n' + '=' * 72)
print('EXPLICIT CHECK on known-risky names')
print('=' * 72)
RISKY = ['Boyer', 'Boyle', 'Hoad', 'Hoade', 'Garcia', 'Macdiarmid', 'MacDiarmid',
         'McEwen', 'Netherwood', 'Caldwell', 'Slezak', 'Lacasse', 'Charlton']
for key in RISKY:
    hits = {nm: fs for nm, fs in occurrences.items() if key.lower() in nm.lower()}
    if hits:
        print('\n  "%s":' % key)
        for nm, fs in sorted(hits.items()):
            print('     %-28s (%d files) %s' % (nm, len(fs), ', '.join(sorted(fs)[:3])))
