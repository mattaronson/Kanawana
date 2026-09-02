"""Build the re-read worklist: one row per DOCUMENT, not per source record.

Operator directive 2026-09-02: re-read every word of every source. Three
separate occasions produced content from a source this project had marked read,
and the 1951 camp history -- nine facts quoting it, read_state "extracted" --
turned out never to have been read end to end. "Extracted" means somebody took
what they went looking for.

Deduped to documents because sources.json holds the same document more than
once: 1,310 records collapse to 1,189 documents, and reading a document twice
under two ids would burn budget for nothing.

Ranked by DEPENDENCY -- how many facts and how many wiki articles rest on the
source -- because that is where an unread document does the most damage. Ties
break toward the smaller file, so cheap documents clear early.
"""
import json, os, collections, re, io

def load():
    s = json.load(open('sources/sources.json', encoding='utf-8'))
    return s if isinstance(s, list) else s['sources']

def doc_key(r):
    cp = r.get('cache_path')
    if cp and os.path.isfile(cp):
        return 'cache:' + cp
    if r.get('origin_url'):
        return 'url:' + r['origin_url'].rstrip('/').split('#')[0]
    return 'id:' + r['source_id']

def main():
    rec = load()
    facts = json.load(open('kb/facts.json', encoding='utf-8'))['facts']

    fact_cites = collections.Counter()
    for f in facts:
        for sid in (f.get('sources') or []):
            fact_cites[sid] += 1

    art_cites = collections.Counter()
    arts = json.load(open('wiki/articles.json', encoding='utf-8'))
    arts = arts['articles'] if isinstance(arts, dict) and 'articles' in arts else arts
    for a in arts:
        for sid in set(a.get('sources_cited') or []):
            art_cites[sid] += 1

    groups = collections.defaultdict(list)
    for r in rec:
        groups[doc_key(r)].append(r)

    rows = []
    for k, rs in groups.items():
        ids = sorted(r['source_id'] for r in rs)
        kind, _, loc = k.partition(':')
        size = os.path.getsize(loc) if kind == 'cache' else 0
        rows.append({
            'doc_key': k,
            'kind': kind,                       # cache | url | id
            'location': loc,
            'source_ids': ids,
            'title': rs[0].get('title') or '',
            'date': rs[0].get('date') or '',
            'origin': rs[0].get('origin') or '',
            'reliability': rs[0].get('reliability') or '',
            'bytes': size,
            'facts_citing': sum(fact_cites[i] for i in ids),
            'articles_citing': sum(art_cites[i] for i in ids),
            'prior_read_state': rs[0].get('read_state'),
            'prior_basis': rs[0].get('read_state_basis'),
        })

    rows.sort(key=lambda r: (-r['articles_citing'], -r['facts_citing'], r['bytes'] or 10**9))
    for i, r in enumerate(rows, 1):
        r['rank'] = i

    json.dump(rows, open('kb/reread/queue.json', 'w'), indent=1, ensure_ascii=False)

    done = set()
    if os.path.exists('kb/reread/ledger.jsonl'):
        for line in io.open('kb/reread/ledger.jsonl', encoding='utf-8'):
            done.add(json.loads(line)['doc_key'])

    by_kind = collections.Counter(r['kind'] for r in rows)
    todo = [r for r in rows if r['doc_key'] not in done]
    print('source records      :', len(rec))
    print('distinct documents  :', len(rows))
    print('  cached text       :', by_kind['cache'],
          '(%.1f MB)' % (sum(r['bytes'] for r in rows) / 1e6))
    print('  URL only          :', by_kind['url'])
    print('  no text, no URL   :', by_kind['id'])
    print('already read        :', len(rows) - len(todo))
    print('REMAINING           :', len(todo))
    print()
    print('next 15 by dependency:')
    for r in todo[:15]:
        print('  #%-4d %-5s art=%-2d facts=%-3d %7s  %s' %
              (r['rank'], r['kind'], r['articles_citing'], r['facts_citing'],
               r['bytes'] or '-', (r['title'] or r['source_ids'][0])[:70]))

main()
