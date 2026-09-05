"""Regenerate the multi-year table in wiki/people/multi-year-index.md.

Written after the article's stated counts (1,493 names / 149 traced people /
44 progressions) were found to disagree with the index behind them. The table
had been assembled by hand, so every later fix to build_index.py -- the staff
column classifier, the Sir/Lady strip, the Julien Tasse pin -- moved the index
without moving the article. This script makes the table a FUNCTION of the
index, so that class of drift cannot recur silently. Run it after any
build_index.py change.

The star marks a documented junior-to-staff progression: a person whose
earliest board carries a junior or leadership-track role and who appears on a
later board in a staff-grade one. Roles that say nothing about rank -- Knight,
Signatory, Award recipient, Guest -- are NEUTRAL and prove a progression
neither way; they are printed in the trajectory but never trigger a star or
satisfy its junior half.
"""
import json, re, io, sys

STAFF_GRADE = {'Staff','Counsellor','Tripper','Director','Directress',
               'Section Director','CIT Director','CIT Program Director',
               'Co-ordinator','Master','Capitaine','Maintenance'}
NEUTRAL     = {'Knight','Signatory','Award recipient','Guest','Therapist(joke)'}

d = json.load(open('kb/plaque-audit/person-index.json'))
multi = {n: v for n, v in d.items() if len(v['years']) > 1 and not v['initial_only']}

def year_roles(v):
    """One role per year: the highest-standing role recorded for that year."""
    by = {}
    for a in v['appearances']:
        y = a['year']
        if y is None: continue
        cur = by.get(y)
        if cur is None or (a['role'] in STAFF_GRADE and cur not in STAFF_GRADE):
            by[y] = a['role']
    return by

def is_progression(by):
    junior = sorted(y for y, r in by.items() if r not in STAFF_GRADE and r not in NEUTRAL)
    staff  = sorted(y for y, r in by.items() if r in STAFF_GRADE)
    return bool(junior and staff and staff[-1] > junior[0])

rows = []
for n, v in multi.items():
    by = year_roles(v)
    yrs = sorted(by)
    traj = ' → '.join(f'{y} {by[y]}' for y in yrs)
    star = is_progression(by)
    disp = re.sub(r'\s*\(.*\)$', '', v['display']).strip()
    rows.append((v['span'], disp.lower(), disp, yrs, traj, star))

rows.sort(key=lambda r: (-r[0], r[1]))
prog = sum(1 for r in rows if r[5])

body = ['| Name as painted | Years | Span | Trajectory |', '|---|---|---|---|']
for span, _, disp, yrs, traj, star in rows:
    body.append(f'| {disp} | {yrs[0]}–{yrs[-1]} | {span} | {traj}{" ★" if star else ""} |')
table = '\n'.join(body)

path = 'wiki/people/multi-year-index.md'
s = io.open(path, encoding='utf-8').read()
m = re.search(r'\| Name as painted \|.*?(?=\n\n)', s, re.S)
if not m:
    sys.exit('table block not found')
io.open(path, 'w', encoding='utf-8').write(s[:m.start()] + table + s[m.end():])

print('traced people :', len(rows))
print('progressions  :', prog)
print('distinct names:', len(d))
