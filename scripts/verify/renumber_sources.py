"""Renumber an article's Sources list so every ^N marker has exactly one target.

Written for p_302, after the verify harness's A1 and G checks were widened past
drafts and found sixteen articles whose source numbering had drifted: headers
that undercounted, numbers used twice, numbers skipped, and Sources sections
that mix a bullet list with numbered entries so that the numbers refer to
positions in a list half of whose items have no position.

The rule this enforces: an entry's IDENTITY is its position in the list, not
the digits printed in front of it. So entries keep their order and their text,
get consecutive numbers 1..N, and every ^N marker in the body is rewritten
through the old->new map. Label markers (^mc, ^cr) are folded into the same
sequence via --label, because a mixed list is what caused the drift.

Dry run by default. Pass --write to apply.
"""
import sys, re, io, argparse

ENTRY_NUM   = re.compile(r'^(\d+)\.\s+(.*)$', re.S)
ENTRY_BULL  = re.compile(r'^-\s+(.*)$', re.S)
ENTRY_LABEL = re.compile(r'^\^([0-9A-Za-z_]+):?\s+(.*)$', re.S)

def split(text):
    m = re.search(r'^## Sources\s*$', text, re.M)
    if not m:
        sys.exit('no "## Sources" heading')
    start = m.end()
    n = re.search(r'^## ', text[start:], re.M)
    end = start + (n.start() if n else len(text[start:]))
    return text[:m.start()], text[m.start():start], text[start:end], text[end:]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('--label', action='append', default=[],
                    help='LABEL=ENTRYINDEX (1-based position in the list) for a ^label marker')
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()

    text = io.open(a.path, encoding='utf-8').read()
    body, head, src, rest = split(text)

    entries, mapping = [], {}
    for line in src.split('\n'):
        s = line.strip()
        if not s:
            entries.append(None)
            continue
        m = ENTRY_NUM.match(s)
        if m:
            entries.append(('num', int(m.group(1)), m.group(2))); continue
        m = ENTRY_LABEL.match(s)
        if m:
            entries.append(('label', m.group(1), m.group(2))); continue
        m = ENTRY_BULL.match(s)
        if m:
            entries.append(('bull', None, m.group(1))); continue
        entries.append(('raw', None, s))

    out, k = [], 0
    for e in entries:
        if e is None:
            out.append(''); continue
        kind, old, txt = e
        if kind == 'raw':
            out.append(txt); continue
        k += 1
        if kind == 'num':
            if old in mapping:
                print('  !! source number %d appears twice; the SECOND is now %d' % (old, k))
            mapping[old] = k
        elif kind == 'label':
            mapping['^' + old] = k
        out.append('%d. %s' % (k, txt))

    for spec in a.label:
        lab, idx = spec.split('=')
        mapping['^' + lab] = int(idx)

    def sub(m):
        n = int(m.group(1))
        return '^%d' % mapping[n] if n in mapping else m.group(0)
    new_body = re.sub(r'\^(\d+)', sub, body)
    for key, val in mapping.items():
        if isinstance(key, str) and key.startswith('^'):
            new_body = re.sub(re.escape(key) + r'(?![0-9A-Za-z_])', '^%d' % val, new_body)

    new_body = re.sub(r'(\*Status: [A-Za-z0-9\-]+ \| Sources: )[^*]*\*',
                      r'\g<1>%d*' % k, new_body, count=1)

    changed = sorted((o, n) for o, n in mapping.items() if isinstance(o, int) and o != n)
    print('%s: %d entries' % (a.path, k))
    print('  renumbered:', changed or 'none')
    print('  labels    :', {kk: vv for kk, vv in mapping.items() if isinstance(kk, str)} or 'none')
    if a.write:
        io.open(a.path, 'w', encoding='utf-8').write(new_body + head + '\n'.join(out) + rest)
        print('  WRITTEN')

main()
