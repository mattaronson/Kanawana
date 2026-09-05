#!/usr/bin/env python3
"""Stale-state check: has a later finding left an earlier record behind?

The rest of the harness asks whether the build is INTERNALLY CONSISTENT right
now. This asks a different question: whether some part of it is still carrying
a claim that a later pass superseded somewhere else. That failure mode is
invisible to every other check, because each individual file is well formed --
it is the DISAGREEMENT BETWEEN them that is the defect.

It exists because of two real cases found on 2026-09-05:

  * c_001 sat at "resolved_editorially" with a July phased reading of the
    coeducation date while the article had superseded it in August on
    documentary grounds. Both files were valid; together they said two things.
  * A February R1 review comment inside canadian-camping-movement.md still
    called the second-oldest ranking "well-supported" eleven lines below a
    Summary that withdraws it.

Advisory. It reports disagreements, and a human decides which side is right --
this script must never guess, because the newer record is not automatically
the correct one.
"""
import json, io, os, re, sys

RESOLVED = {'resolved', 'resolved_editorially'}
# 'likely_resolved' and 'partially_resolved' are deliberately NOT here: by their
# own names those conflicts are not settled, so a fact under one is correctly
# still disputed and reporting it would be noise.
DATE = re.compile(r'(20\d\d-\d\d-\d\d)')
# A withdrawal marker is a whole-fact one only at the START of a claim. Inline
# "CORRECTED:" is the opposite: a fact carrying its own correction, which is
# the convention working, not failing. Do not report those.
DEAD_PREFIX = re.compile(r'^\s*\[(SUPERSEDED|WITHDRAWN|RETRACTED)\b')


def load(p):
    return json.load(io.open(p, encoding='utf-8'))


def articles():
    out = {}
    for root, _, files in os.walk('wiki'):
        for fn in files:
            if fn.endswith('.md'):
                p = os.path.join(root, fn)
                out[os.path.splitext(fn)[0]] = (p, io.open(p, encoding='utf-8').read())
    return out


def main():
    facts = load('kb/facts.json')['facts']
    by = {f['fact_id']: f for f in facts}
    cd = load('kb/conflicts.json')
    conflicts = cd['conflicts'] if isinstance(cd, dict) and 'conflicts' in cd else cd
    arts = articles()
    findings = []

    # A. A conflict record older than the resolution its own article records.
    #
    #    A later date alone is NOT the defect -- an article routinely strikes
    #    its open question a day or two after the conflict is settled, and
    #    c_007 does exactly that ("confirming the original 1979 dating").
    #    The defect is a later passage that OVERTURNS rather than corroborates,
    #    so the two records now say different things. Distinguish on the
    #    article's own language, not on the dates:
    OVERTURNS = re.compile(
        r'supersed|withdraw|no longer|simply wrong|was wrong|in error|not a second|'
        r'reversed|retract|overturn|does not hold|abandon', re.I)
    CORROBORATES = re.compile(r'confirm|corroborat|consistent with|bears out|upholds', re.I)
    for c in conflicts:
        ra = (c.get('resolved_at') or '')[:10]
        if not ra:
            continue
        for slug in c.get('affects_articles') or []:
            if slug not in arts:
                continue
            path, s = arts[slug]
            for m in re.finditer(r'\*{0,2}\[?Resolved[^\n\]]{0,400}', s):
                seg = m.group(0)
                if not OVERTURNS.search(seg):
                    continue
                if CORROBORATES.search(seg) and not OVERTURNS.search(seg[:80]):
                    continue
                for dt in DATE.findall(seg):
                    if dt > ra:
                        findings.append(
                            ('A', f'{c["conflict_id"]} resolved_at {ra} ({c.get("status")}), but '
                                  f'{path} records a LATER resolution dated {dt} in overturning '
                                  f'language -- the two records may no longer agree'))

    # B. A superseded fact still cited by an article.
    dead = {fid for fid, f in by.items() if DEAD_PREFIX.match(f['claim'])}
    for slug, (path, s) in arts.items():
        for fid in set(re.findall(r'\[(f_\d+)\]', s)):
            if fid in dead:
                findings.append(('B', f'{path} cites {fid}, which is marked superseded'))

    # C. A fact still "disputed" whose every linked conflict is resolved.
    cst = {c['conflict_id']: c.get('status') for c in conflicts}
    for f in facts:
        if f.get('confidence') != 'disputed':
            continue
        cws = [x for x in (f.get('conflicts_with') or []) if x.startswith('c_')]
        if cws and all(cst.get(x) in RESOLVED for x in cws):
            findings.append(('C', f'{f["fact_id"]} is still confidence=disputed, but {cws} '
                                  f'{[cst.get(x) for x in cws]}'))

    # D. A review comment contradicting the article it sits in. Only the
    #    phrases this project has actually withdrawn -- a generic contradiction
    #    detector would be noise.
    WITHDRAWN = [
        (r'second[- ]oldest', r'withdraw|no longer assert|STALE'),
    ]
    for slug, (path, s) in arts.items():
        for m in re.finditer(r'<!--.*?-->', s, re.S):
            body = m.group(0)
            for claim, exempt in WITHDRAWN:
                if re.search(claim, body, re.I) and not re.search(exempt, body, re.I):
                    findings.append(('D', f'{path}: a review comment asserts a withdrawn claim '
                                          f'(/{claim}/) without marking it stale'))

    # E. Disputed facts with no conflict record at all. Structural, reported as
    #    a count -- CLAUDE.md asks for a conflict record, and fact-to-fact
    #    links alone leave kb-conflicts undercounting.
    dis = [f for f in facts if f.get('confidence') == 'disputed']
    noc = [f for f in dis if not [x for x in (f.get('conflicts_with') or []) if x.startswith('c_')]]

    print('=' * 70)
    print('STALENESS -- has a later finding left an earlier record behind?')
    print('=' * 70)
    if findings:
        for cls, msg in sorted(set(findings)):
            print(f'  [{cls}] {msg}')
    else:
        print('  no disagreement between conflicts, facts and articles')
    print(f'  note: {len(noc)} of {len(dis)} disputed facts carry no c_ conflict record (p_412)')
    print('  Advisory: this reports disagreements, it does not adjudicate them.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
