#!/usr/bin/env python3
"""Append extracted facts to kb/facts.json and mark the extraction ledger.

Usage: append_facts.py <facts.json batch file> <issue numbers, comma separated>

The batch file is a JSON list of fact objects WITHOUT fact_id; ids are assigned
here from the current maximum so a re-run can never collide. Updates fact_count
and the per-issue ledger row in one pass, so the two cannot drift apart.
"""
import json, re, sys, collections

FACTS = 'kb/facts.json'
LEDGER = 'kb/reread/cc_extract_progress.jsonl'
VERSION = '6.06'

def main(batch_path, issues):
    batch = json.load(open(batch_path, encoding='utf-8'))
    d = json.load(open(FACTS, encoding='utf-8'))
    facts = d['facts']
    nxt = max(int(re.sub(r'\D', '', f['fact_id'])) for f in facts) + 1

    seen = {f['claim'][:120] for f in facts}
    added, skipped = [], []
    for f in batch:
        if f['claim'][:120] in seen:
            skipped.append(f['claim'][:80]); continue
        f = dict(f)
        f.setdefault('sources', ['src_ia_canadian_camping_collection'])
        f.setdefault('confidence', 'stated')
        f.setdefault('entities', [])
        f.setdefault('date_ref', None)
        f.setdefault('conflicts_with', [])
        f['added_version'] = VERSION
        f['added_by'] = 'reread_extraction'
        f = {'fact_id': 'f_%04d' % nxt, **f}
        nxt += 1
        facts.append(f); added.append(f['fact_id']); seen.add(f['claim'][:120])

    ids = [f['fact_id'] for f in facts]
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    if dup:
        sys.exit('ABORT: duplicate fact_id(s) %s -- nothing written' % dup[:5])
    d['fact_count'] = len(facts)
    d['version'] = d['kb_version'] = VERSION
    json.dump(d, open(FACTS, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

    want = {int(x) for x in issues.split(',') if x.strip()}
    rows = [json.loads(l) for l in open(LEDGER, encoding='utf-8') if l.strip()]
    per = collections.Counter(f.get('issue') for f in batch)
    for r in rows:
        if r['n'] in want:
            r['status'] = 'extracted'
            r['facts'] = per.get(r['n'], 0)
    with open(LEDGER, 'w', encoding='utf-8') as fh:
        for r in rows: fh.write(json.dumps(r, ensure_ascii=False) + '\n')

    done = sum(1 for r in rows if r['status'] == 'extracted')
    print('added %d facts (%s..%s); skipped %d duplicate claim(s)'
          % (len(added), added[0] if added else '-', added[-1] if added else '-', len(skipped)))
    for s in skipped[:5]: print('   skip:', s)
    print('facts.json now %d facts; ledger %d of %d issues extracted' % (len(facts), done, len(rows)))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
