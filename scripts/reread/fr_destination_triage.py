#!/usr/bin/env python3
"""Triage the French-edition sources: which of their camp passages have no
English destination in the wiki?

WHY. Twenty-five source records carry read_state_basis "asserted:" and a French
cache file. Reading each end to end is expensive and, as 2026-09-08 showed
repeatedly, mostly wasted: the association published both editions of most
reports, an earlier pass usually worked the English one, and the French edition
duplicates it. The 2011 and 2012 community reports were read that day and every
item in them -- the girls' Boot Camp weekend, the open house, Tremplin Sante,
Laurie's testimonial -- was already in modern-era.md from the English.

But a French edition is worth checking because OCR damage falls differently
(f_5747: two years of the Social Audit table survive in French and not in
English), and because a French-only phrase can be the only surviving print of a
fact.

WHAT IT DOES. For each candidate source, take the lines around every mention of
the camp, pull out DISTINCTIVE TOKENS -- numbers with a separator or a percent
sign, and capitalised words that are not French function words -- and ask
whether each appears anywhere in wiki/. A token present is not proof the passage
was worked; a token ABSENT is a specific place to look.

THE RULE IT ENFORCES, which cost this project a retraction (f_5759): THE
DESTINATION IS CHECKED IN THE WIKI'S OWN LANGUAGE. The wiki writes English.
Grepping it for a French phrase returns a null that means nothing at all. So
this never searches for French wording; it searches for the language-independent
part -- figures, proper names, years.

NOT A CHECK. This is a reading aid, not a verify script. It does not run in
all.py and has no baseline. Its output is a queue, and every line of it needs a
person or a model to read the passage before anything follows.
"""
import json
import os
import re
import sys

STOP = set('''le la les un une des du de au aux et ou en dans pour par sur avec sans
sous vers chez ce cet cette ces son sa ses leur leurs notre nos votre vos qui que
quoi dont ou si ne pas plus moins tres bien tout tous toute toutes meme aussi
ainsi alors donc car mais or ni comme quand depuis pendant avant apres entre
Le La Les Un Une Des Du De Au Aux Et Ou En Dans Pour Par Sur Avec Sans Sous Vers
Ce Cet Cette Ces Son Sa Ses Leur Leurs Notre Nos Votre Vos Qui Que Dont Si Ne Pas
Plus Moins Tres Bien Tout Tous Toute Toutes Meme Aussi Ainsi Alors Donc Car Mais
Ni Comme Quand Depuis Pendant Avant Apres Entre Il Elle Ils Elles Nous Vous On
YMCA Kanawana Camp Kamp Y Les Des Du'''.split())

NUM = re.compile(r'\b\d{1,3}(?:[  ,]\d{3})+\b|\b\d+(?:[.,]\d+)?\s*%|\b\d{4,}\b')
CAP = re.compile(r'\b[A-ZÉÈÀÂÎÔÛÇ][A-Za-zÉÈÀÂÎÔÛÇéèàâîôûç\'-]{3,}\b')


def wiki_text():
    out = []
    for root, _dirs, files in os.walk('wiki'):
        for name in files:
            if name.endswith('.md'):
                with open(os.path.join(root, name), encoding='utf-8') as fh:
                    out.append(fh.read())
    return '\n'.join(out)


def main() -> int:
    only = sys.argv[1] if len(sys.argv) > 1 else None
    with open('sources/sources.json', encoding='utf-8') as fh:
        data = json.load(fh)
    srcs = data['sources'] if isinstance(data, dict) else data
    wiki = wiki_text()

    for s in srcs:
        cp = s.get('cache_path') or ''
        basis = s.get('read_state_basis') or ''
        if not cp.endswith('-fr.txt') or not basis.startswith('asserted:'):
            continue
        if only and only not in s['source_id']:
            continue
        if not os.path.exists(cp):
            continue
        with open(cp, encoding='utf-8', errors='replace') as fh:
            lines = fh.read().split('\n')
        hits = [i for i, l in enumerate(lines) if 'anawana' in l]
        if not hits:
            continue
        toks = {}
        for i in hits:
            window = '\n'.join(lines[max(0, i - 4):i + 9])
            for m in list(NUM.finditer(window)) + list(CAP.finditer(window)):
                t = m.group(0).strip()
                if t in STOP or t.isdigit() and len(t) == 4 and t.startswith(('19', '20')):
                    continue
                toks.setdefault(t, i + 1)
        missing = sorted((ln, t) for t, ln in toks.items()
                         if t.replace(' ', ' ') not in wiki
                         and t.replace(' ', ',') not in wiki
                         and t.replace(' ', ' ') not in wiki)
        print('=' * 70)
        print('%s  (%d camp mentions, %d distinctive tokens, %d absent from wiki/)'
              % (s['source_id'], len(hits), len(toks), len(missing)))
        for ln, t in missing[:30]:
            print('    line %-6d %s' % (ln, t))
    return 0


sys.exit(main())
