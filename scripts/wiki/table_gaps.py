"""Find years an article discusses in prose but leaves out of its own table.

Written 2026-09-07 after the third instance in one session of a fact sitting in
the wiki and missing from the place that needed it. The case that prompted it:
camp-perrot.md carried "177 boys and 87 girls in 1955, 207 boys and 104 girls in
1957" in a section rebutting a 1969 claim, while its attendance table skipped
1955, 1956 and 1957 entirely -- and the argument built on that table dated a
change three years late as a result.

WHAT THIS IS. A TARGETING TOOL, NOT A CHECK. It reports years that appear in an
article's prose near a bare number and do not appear in that article's
year-keyed table. Most hits are nothing: a year is mentioned for a hundred
reasons that have no business in a table. The output is a reading list ranked by
how much numeric weight sits beside the year, and every hit has to be read.

It cannot see the other two shapes of the same defect -- a fact written into one
article and contradicted in another, and a fact written into one article and
absent from the article whose subject it is. Nothing here detects those.
"""
import re, sys, glob, os
from collections import defaultdict

YEAR = re.compile(r'\b(1[89]\d\d|20[0-2]\d)\b')
NUM  = re.compile(r'(?<![\w.,$])\d{1,3}(?:,\d{3})*(?![\w%])')

def tables(lines):
    """Yield (start, end, years) for each pipe table whose first column holds years."""
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|[-: |]+\|\s*$', lines[i+1]):
            j = i + 2
            years = set()
            while j < len(lines) and lines[j].lstrip().startswith('|'):
                first = lines[j].split('|')[1] if lines[j].count('|') > 1 else ''
                years.update(int(m) for m in YEAR.findall(first))
                j += 1
            if len(years) >= 3:
                yield i, j, years
            i = j
        else:
            i += 1

def main(paths):
    rows = []
    for p in paths:
        text = open(p, encoding='utf-8').read()
        lines = text.split('\n')
        tbls = list(tables(lines))
        if not tbls:
            continue
        covered = set().union(*(t[2] for t in tbls))
        # Range is per table, not the union of all of them. An article with a
        # 1912-1921 table and a 1949-1959 table does not thereby claim to
        # tabulate 1930, and flagging 1930 as an omission is a false positive.
        spans = [(min(t[2]), max(t[2])) for t in tbls]
        in_table = set()
        for s, e, _ in tbls:
            in_table.update(range(s, e))
        hits = defaultdict(int)
        where = {}
        for n, line in enumerate(lines):
            if n in in_table or line.lstrip().startswith(('#', '|')):
                continue
            if re.match(r'^\d+\.\s', line.strip()):      # numbered source entries
                continue
            for m in YEAR.finditer(line):
                y = int(m.group(1))
                if y in covered or not any(a <= y <= b for a, b in spans):
                    continue
                near = line[max(0, m.start()-120):m.end()+120]
                weight = len(NUM.findall(near))
                if weight >= 2:
                    hits[y] += weight
                    where.setdefault(y, (n + 1, near.strip()[:150]))
        for y, w in sorted(hits.items(), key=lambda kv: -kv[1]):
            rows.append((w, p, y, where[y]))
    rows.sort(key=lambda r: -r[0])
    if not rows:
        print('No years found in prose with numeric weight and missing from a year-keyed table.')
        return
    print(f'{len(rows)} year(s) discussed in prose and absent from the article\'s own table.')
    print('A TARGETING LIST, NOT A FINDING. Read each one.\n')
    for w, p, y, (ln, ctx) in rows:
        print(f'  weight {w:2d}  {os.path.relpath(p, "wiki")}  year {y}  (line {ln})')
        print(f'            {ctx}')

if __name__ == '__main__':
    args = sys.argv[1:] or sorted(glob.glob('wiki/**/*.md', recursive=True))
    main(args)
