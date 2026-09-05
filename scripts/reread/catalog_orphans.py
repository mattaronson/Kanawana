"""Catalogue cached text files that no source record points at.

Found 2026-09-02 while answering "are these all OCR'd and cached?". They are --
40.3 MB of OCR'd text sits in sources/cache -- but 300 of the 904 files, 25.8 MB,
belong to no source record. The pipeline fetched them and never wired them up,
so every downstream step that asks "what sources do we have" has never seen them.
The largest block is 164 issues of Canadian Camping Magazine, 1949-1988, against
18 source records for the whole run.

A file with no record cannot be read, cited, or counted as unread. This makes
records for them so they enter the re-read queue like everything else.
"""
import json, os, re, hashlib, collections

def load():
    s = json.load(open('sources/sources.json', encoding='utf-8'))
    return (s, s if isinstance(s, list) else s['sources'])

ORIGIN = {'canadian-camping':'internet_archive', 'ymca-montreal-fonds':'internet_archive',
          'green-triangle':'internet_archive', 'web-pages':'web',
          'concordia-findingaid':'concordia_archives', 'brochures':'internet_archive',
          'theses':'web', 'concordia-mirror':'concordia_archives', 'parent-guides':'web'}

def title_for(folder, base):
    n = base.rsplit('.', 1)[0]
    m = re.match(r'canadiancampingmagazine_vol(\d+)[_ ]?no?(\d+)_(.*)$', n, re.I)
    if m:
        return 'Canadian Camping Magazine, Vol. %s No. %s (%s)' % (m.group(1), m.group(2), m.group(3))
    return n.replace('-', ' ').replace('_', ' ').strip()

def date_for(base):
    m = re.search(r'(1[89]\d\d|20\d\d)[-_]?(\d{2})?[-_]?(\d{2})?', base)
    if not m: return '', 'unknown'
    y, mo, d = m.group(1), m.group(2), m.group(3)
    if y and mo and d: return '%s-%s-%s' % (y, mo, d), 'exact'
    if y and mo:       return '%s-%s' % (y, mo), 'month'
    return y, 'year'

def main():
    doc, rec = load()
    ref = {r['cache_path'] for r in rec if r.get('cache_path')}
    ids = {r['source_id'] for r in rec}

    # green-triangle/ duplicates the fonds copies byte for byte; skip those.
    seen_hash = {}
    for r in rec:
        cp = r.get('cache_path')
        if cp and os.path.isfile(cp):
            seen_hash[hashlib.md5(open(cp, 'rb').read()).hexdigest()] = r['source_id']

    added, dupes = [], []
    for root, _, files in os.walk('sources/cache'):
        for f in sorted(files):
            p = os.path.join(root, f)
            if p in ref or os.path.getsize(p) == 0 or f.startswith('.'):
                continue
            h = hashlib.md5(open(p, 'rb').read()).hexdigest()
            if h in seen_hash:
                dupes.append((p, seen_hash[h])); continue
            folder = os.path.basename(root)
            base = re.sub(r'[^a-z0-9]+', '_', f.rsplit('.', 1)[0].lower()).strip('_')[:70]
            sid = 'src_cache_%s' % base
            k = 2
            while sid in ids:
                sid = 'src_cache_%s_%d' % (base, k); k += 1
            ids.add(sid)
            date, prec = date_for(f)
            r = {'source_id': sid, 'type': 'periodical' if 'magazine' in f.lower() or 'triangle' in f.lower() else 'report',
                 'title': title_for(folder, f), 'date': date, 'date_precision': prec,
                 'origin': ORIGIN.get(folder, 'web'), 'origin_url': None, 'cache_path': p,
                 'char_count': os.path.getsize(p), 'ingested_at': '2026-09-02T00:00:00Z',
                 'extracted': False, 'extraction_version': None,
                 'reliability': 'primary' if folder in ('ymca-montreal-fonds', 'green-triangle', 'concordia-findingaid') else 'secondary',
                 'read_state': 'unread',
                 'read_state_basis': 'none: catalogued 2026-09-02 from a cached file that belonged to no source record',
                 'notes': 'Text was already OCR\'d and on disk in %s; no record pointed at it, so nothing downstream could see it. Catalogued by scripts/reread/catalog_orphans.py for the p_304 re-read.' % folder}
            rec.append(r); added.append(r)
            seen_hash[h] = sid

    if isinstance(doc, dict):
        doc['sources'] = rec
    json.dump(doc, open('sources/sources.json', 'w'), indent=2, ensure_ascii=False)

    by = collections.Counter(os.path.basename(os.path.dirname(r['cache_path'])) for r in added)
    print('catalogued %d new source records (%.1f MB of text)'
          % (len(added), sum(r['char_count'] for r in added) / 1e6))
    for k, v in by.most_common(): print('   %-22s %4d' % (k, v))
    print('skipped %d byte-identical duplicates of files already catalogued' % len(dupes))

main()
