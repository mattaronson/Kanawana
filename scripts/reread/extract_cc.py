"""Pull every passage in the Canadian Camping run that touches this project.

164 issues, 14.1 MB. Reading all of it word for word would cost roughly 3.5M
tokens to find a few hundred relevant paragraphs, most of the rest being other
provinces and other camps.

So every file is examined mechanically -- nothing is skipped -- and each
paragraph containing a term of interest is pulled with its neighbours for
context. WITH ONE CAVEAT STATED UP FRONT: a term list is a classifier that reads
structure instead of meaning, which is the exact failure this project has hit
twice (the staff-column bug, f_2335; the 1935 chronicle's dropped names,
f_2378). It can only find what someone thought to look for. The mitigation is
to read a sample of whole issues alongside the extract, and the sample is part
of the task, not an optional extra.
"""
import re, io, os, sys, json, collections

SRC = 'sources/cache/canadian-camping'

TERMS = [
    # the camps
    'kanawana', 'otoreke', 'weredale', 'becsies', 'camp perrot', 'tamaracouta',
    # the association and its people, in both languages
    'quebec camping', 'quebec section', "association des camps", 'q.c.a.',
    'montreal ymca', 'ymca of montreal', 'montreal y.m.c.a',
    # people with a documented Kanawana role
    'dimock', 'ross seaman', 'a. ross seaman', 'roy locke', 'roy d. locke',
    'derek walsh', 'robitaille', 'netherwood', 'geoff anderson', 'tom potts',
    'ben hannan', 'ben hannah', 'norrey owens', 'o. n. h. owens', 'harold cross',
    'harold c. cross', 'stuart mclean', 'james turner', 'j. h. turner',
    'wasilewski', 'mischook', 'olshansky', 'robert wilkinson', 'dr. wilkinson',
    'keith farquharson', 'rix rogers', 'edgar smee', 'ed smee',
]
RX = re.compile('|'.join(re.escape(t) for t in TERMS), re.I)

def paragraphs(text):
    """Blank-line-separated blocks; OCR of a magazine has plenty."""
    return re.split(r'\n\s*\n', text)

def main():
    out, per_issue = [], collections.Counter()
    files = sorted(f for f in os.listdir(SRC) if f.endswith('.txt'))
    for fn in files:
        text = io.open(os.path.join(SRC, fn), encoding='utf-8', errors='ignore').read()
        paras = paragraphs(text)
        for i, p in enumerate(paras):
            if not RX.search(p):
                continue
            ctx = '\n\n'.join(paras[max(0, i-1):i+2])
            ctx = re.sub(r'[ \t]+', ' ', ctx).strip()
            if len(ctx) < 40:
                continue
            hits = sorted({m.group(0).lower() for m in RX.finditer(p)})
            out.append({'issue': fn, 'para': i, 'terms': hits, 'text': ctx[:2600]})
            per_issue[fn] += 1

    json.dump(out, open('/tmp/claude-0/cc_extract.json', 'w'), indent=1, ensure_ascii=False)
    print('files scanned      :', len(files))
    print('passages extracted :', len(out))
    print('issues with a hit  :', len(per_issue), '(of %d)' % len(files))
    print('extract size       : %.2f MB (from 14.1 MB)'
          % (sum(len(o['text']) for o in out) / 1e6))
    print()
    tc = collections.Counter(t for o in out for t in o['terms'])
    print('by term:')
    for t, n in tc.most_common(24):
        print('   %-28s %4d' % (t, n))
    print()
    print('densest issues:')
    for f, n in per_issue.most_common(12):
        print('   %-52s %3d' % (f.replace('canadiancampingmagazine_', ''), n))

main()
