"""Find, and where possible DECIDE, near-miss name pairs in the plaque index.

p_298. build_index.py merges two names only when their normalised forms are
identical or the pair is in a hand-curated alias list. That is deliberately
conservative, so it SPLITS people whose name drifts across boards. The earlier
pass produced about thirty candidate pairs and stopped, because the matcher had
already been caught twice: it wanted to merge David and Dave Paltiel, a merge
this project had declined on reasoning, and to collapse Elissa and Melissa
Sukosd, who are more likely sisters.

The point of this script is to stop handing all of them to a person. One test
decides a large share of them mechanically:

  CO-OCCURRENCE. If both spellings appear on the SAME board, they are two
  people. A roster does not list one person twice under two spellings of their
  own name. This RULES OUT a merge; it never confirms one. (On the current
  index it rules out none: every near-miss pair sits on different boards, even
  the four that share a year.)

  ATTESTED ELSEWHERE. If one spelling appears in the knowledge base or the
  wiki from a source that is NOT the plaque album -- an annual report, a press
  notice, an article this project already wrote -- and the other appears
  nowhere, the attested spelling is the person's name and the other is very
  likely the board misread. This too suggests, and does not decide.

  LOW-CONFIDENCE READING. The audit recorded, per image, which names it was
  unsure of. If one spelling of a pair is flagged low-confidence on its board
  and the other is not, the flagged one is probably a misreading of the other
  -- the same shape as Sally Waff/Sally Watt and Matt Iviott/Matt Wiviott,
  both of which turned out to be reading errors this project had already
  resolved. This SUGGESTS a merge and its direction. It does not make one.

Nothing is decided by similarity alone, and the script writes no merges. The
directive from the earlier pass stands: the matcher has already been caught
twice, wanting to merge David and Dave Paltiel (declined on reasoning) and
Elissa with Melissa Sukosd (more likely sisters).

What survives that test is genuinely open, and the surviving list is short
enough to be read. Nothing is merged by this script -- it only writes
kb/plaque-audit/candidate-pairs.json for the human pass.
"""
import json, re, itertools, collections, os

def low_conf_index():
    """normalised name -> set of images where the audit flagged it uncertain."""
    out = collections.defaultdict(set)
    for line in io.open('kb/plaque-audit/audit.jsonl', encoding='utf-8'):
        r = json.loads(line)
        for nm in (r.get('low_conf') or []):
            base = re.split(r'\s*\(', nm)[0]
            out[norm(base)].add(r['image'])
    return out

import io

NICK = {
 'dave':'david','mike':'michael','matt':'matthew','steph':'stephanie','stephen':'steven',
 'chris':'christopher','tiff':'tiffany','andy':'andrew','dan':'daniel','danny':'daniel',
 'rob':'robert','bob':'robert','bobby':'robert','jen':'jennifer','jenny':'jennifer',
 'liz':'elizabeth','beth':'elizabeth','sam':'samuel','tom':'thomas','tommy':'thomas',
 'nick':'nicholas','pat':'patrick','ben':'benjamin','joe':'joseph','jon':'jonathan',
 'greg':'gregory','ted':'edward','ed':'edward','sue':'susan','kate':'katherine',
 'katie':'katherine','cathy':'catherine','pete':'peter','ric':'richard','rick':'richard',
 'zack':'zachary','zach':'zachary','alex':'alexander','ali':'alison','josh':'joshua',
}

def norm(s):
    s = re.sub(r"[^a-z0-9' -]", '', s.lower().strip())
    s = re.sub(r"^(sir|lady) ", '', s)
    return re.sub(r'\s+', ' ', s).strip()

def lev(a, b):
    if abs(len(a) - len(b)) > 2: return 9
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j-1] + 1, prev[j-1] + (ca != cb)))
        prev = cur
    return prev[-1]

def canon_given(g):
    g = g.strip('.').lower()
    return NICK.get(g, g)

def parts(n):
    p = n.split()
    return (p[0], ' '.join(p[1:])) if len(p) > 1 else (p[0], '')

def candidates(idx):
    keys = [k for k in idx if len(k.split()) > 1]
    by_sur = collections.defaultdict(list)
    for k in keys:
        by_sur[parts(k)[1]].append(k)
    out = []

    # same surname, given names that are variants of each other
    for sur, group in by_sur.items():
        for a, b in itertools.combinations(sorted(group), 2):
            ga, gb = canon_given(parts(a)[0]), canon_given(parts(b)[0])
            if ga == gb:
                out.append((a, b, 'same surname; given names are the same name'))
            elif len(ga) > 2 and len(gb) > 2 and lev(ga, gb) == 1:
                out.append((a, b, 'same surname; given names differ by one letter'))
            elif (ga.startswith(gb) or gb.startswith(ga)) and abs(len(ga) - len(gb)) >= 2:
                out.append((a, b, 'same surname; one given name is a prefix of the other'))

    # same given name, surnames one letter apart (plaque misreadings)
    by_giv = collections.defaultdict(list)
    for k in keys:
        by_giv[canon_given(parts(k)[0])].append(k)
    for giv, group in by_giv.items():
        for a, b in itertools.combinations(sorted(group), 2):
            sa, sb = parts(a)[1], parts(b)[1]
            if sa != sb and len(sa) > 3 and len(sb) > 3 and lev(sa, sb) == 1:
                out.append((a, b, 'same given name; surnames differ by one letter'))
    return out

def attestation():
    """A counter over text that is NOT itself derived from the plaques.

    The first version of this counted the whole of facts.json and found nothing,
    because p_292 folded the plaque transcriptions INTO the fact claims -- so
    every spelling was "attested elsewhere" and the test had no discrimination.
    Facts sourced to the Flickr album, and the folded-in roster text, are
    therefore excluded. A test whose corpus contains the thing it is testing
    will always pass, which is the same failure as a classifier reading the key
    instead of the board."""
    PLAQUE = 'src_flickr_kanawana_plaque_album'
    parts = []
    for f in json.load(open('kb/facts.json', encoding='utf-8'))['facts']:
        if PLAQUE in (f.get('sources') or []):
            continue
        parts.append(re.split(r'\|\| FULL ROSTER AS TRANSCRIBED', f['claim'])[0])
    for root, _, files in os.walk('wiki'):
        for fn in files:
            if fn.endswith('.md') and fn not in ('multi-year-index.md', 'plaque-audit.md'):
                parts.append(io.open(os.path.join(root, fn), encoding='utf-8').read())
    low = '\n'.join(parts).lower()
    return lambda display: low.count(re.sub(r"^(sir|lady) ", '', display, flags=re.I).lower())

def main():
    idx = json.load(open('kb/plaque-audit/person-index.json', encoding='utf-8'))
    lc = low_conf_index()
    att = attestation()
    rows = []
    for a, b, why in candidates(idx):
        ia, ib = set(x['image'] for x in idx[a]['appearances']), set(x['image'] for x in idx[b]['appearances'])
        shared = sorted(ia & ib)
        ya = sorted({x['year'] for x in idx[a]['appearances'] if x['year']})
        yb = sorted({x['year'] for x in idx[b]['appearances'] if x['year']})
        lca, lcb = bool(lc.get(a)), bool(lc.get(b))
        hint = ''
        if lca != lcb:
            flagged, clean = (idx[a]['display'], idx[b]['display']) if lca else (idx[b]['display'], idx[a]['display'])
            hint = 'the audit flagged "%s" as an uncertain reading and did not flag "%s"' % (flagged, clean)
        na, nb = att(idx[a]['display']), att(idx[b]['display'])
        att_hint = ''
        if (na > 0) != (nb > 0):
            seen, unseen = (idx[a]['display'], idx[b]['display']) if na else (idx[b]['display'], idx[a]['display'])
            att_hint = ('"%s" is attested %d time(s) elsewhere in the KB or wiki; "%s" appears nowhere else'
                        % (seen, max(na, nb), unseen))
        rows.append({
          'a': idx[a]['display'], 'b': idx[b]['display'], 'why': why,
          'low_conf_hint': hint, 'attested_hint': att_hint,
          'a_years': ya, 'b_years': yb,
          'a_boards': sorted(ia), 'b_boards': sorted(ib),
          'shared_boards': shared,
          'verdict': 'ruled_out' if shared else 'open',
          'reason': ('both names appear on %s -- a roster does not list one person twice'
                     % ', '.join(shared)) if shared else
                    'no board carries both spellings; nothing here decides it',
        })
    rows.sort(key=lambda r: (r['verdict'] != 'open', r['a'].lower()))
    os.makedirs('kb/plaque-audit', exist_ok=True)
    json.dump(rows, open('kb/plaque-audit/candidate-pairs.json', 'w'), indent=1, ensure_ascii=False)
    n_open = sum(1 for r in rows if r['verdict'] == 'open')
    print('candidate pairs :', len(rows))
    print('ruled out by co-occurrence :', len(rows) - n_open)
    print('still open :', n_open)
    ah = [r for r in rows if r['verdict'] == 'open' and r['attested_hint']]
    print('of the open ones, %d have one spelling attested outside the plaques and one not:' % len(ah))
    for r in ah:
        print('  %s' % r['attested_hint'])
    hinted = [r for r in rows if r['verdict'] == 'open' and r['low_conf_hint']]
    print('of the open ones, %d have a low-confidence reading on exactly one side:' % len(hinted))
    for r in hinted:
        print('  %-28s %-28s %s' % (r['a'], r['b'], r['low_conf_hint']))
    print('the rest, with no mechanical evidence either way:')
    for r in rows:
        if r['verdict'] == 'open' and not r['low_conf_hint'] and not r['attested_hint']:
            print('  %-28s %-28s %s | %s %s' % (r['a'], r['b'], r['why'], r['a_years'], r['b_years']))

main()
