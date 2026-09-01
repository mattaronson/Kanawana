"""p_292: fold the p_291 audit into kb/facts.json.

NON-DESTRUCTIVE. Existing claim text is preserved in full and the recovered
roster is APPENDED under a marked heading, so nothing an earlier reader
observed is lost to my transcription -- the same no-silent-overwrite rule the
conflict policy applies to contradictions, applied here to enrichment.
"""
import json, datetime

ROLE_ORDER = ['director','directors','directress','section_director','cit_director',
 'cit_program_director','coordinators','masters','capitaine','counsellor','counsellors',
 'staff','crew','tripper','trippers','wolf','therapist','guest','cit','cits','lit','lits',
 'jc','jcs','jcgs','jbc','campers','members','rangers','voyageurs','girls','boys','section',
 'roll','swimmers','recipients','namers','signatories','participants','confirmed_subset']
SKIP = {'title','object','form','device','devices','carved_devices','structure'}

def render(names):
    out=[]
    keys = [k for k in ROLE_ORDER if k in names] + [k for k in names if k not in ROLE_ORDER and k not in SKIP]
    for k in keys:
        v = names[k]
        if isinstance(v, str):
            out.append(f"{k.replace('_',' ')}: {v}")
        elif isinstance(v, list):
            if v and isinstance(v[0], list):   # [name, year] pairs
                out.append(f"{k.replace('_',' ')}: " + "; ".join(f"{a} ({b})" for a,b in v))
            else:
                out.append(f"{k.replace('_',' ')}: " + ", ".join(str(x) for x in v))
        elif isinstance(v, dict):
            inner = "; ".join(f"{kk}: {', '.join(vv) if isinstance(vv,list) else vv}" for kk,vv in v.items())
            out.append(f"{k.replace('_',' ')}: {inner}")
    return " | ".join(out)

rows = [json.loads(l) for l in open('kb/plaque-audit/audit.jsonl')]
fd = json.load(open('kb/facts.json'))
facts = {f['fact_id']: f for f in fd['facts']}
SRC = 'src_flickr_kanawana_plaque_album'
touched = 0

for r in rows:
    fid = r.get('fact_id')
    if not fid or fid not in facts: continue
    if r['verdict'] not in ('PARTIAL','TRANSCRIBED','COMPLETE'): continue
    body = render(r['names'])
    if not body: continue
    f = facts[fid]
    if 'FULL ROSTER AS TRANSCRIBED' in f['claim']: continue
    rec, act = r.get('recorded'), r.get('actual')
    gap = ''
    if isinstance(rec,int) and isinstance(act,int) and act > rec:
        gap = f" This fact previously carried {rec} of the {act} names on the object."
    lowc = ''
    if r.get('low_conf'):
        lowc = " READINGS HELD AT REDUCED CONFIDENCE: " + "; ".join(r['low_conf']) + "."
    f['claim'] = (f['claim'].rstrip() +
        f" || FULL ROSTER AS TRANSCRIBED FROM THE IMAGE (p_292, 2026-08-28, from {r['image']}): "
        + body + "." + gap + lowc +
        " The text before this marker is the original record and is preserved unchanged.")
    f['added_version'] = 'v5.67'
    if SRC not in f['sources']: f['sources'].append(SRC)
    touched += 1

fd['facts'] = list(facts.values())
fd['version'] = '5.67'; fd['kb_version'] = 'v5.67'; fd['fact_count'] = len(fd['facts'])
json.dump(fd, open('kb/facts.json','w'), indent=2, ensure_ascii=False)
print('facts enriched with full rosters:', touched)
