#!/usr/bin/env python3
"""Rank the skimmed sources by how much of them is NOT already in the project.

WHY. p_441 -- "read the 729 skimmed sources" -- is the largest remaining body of
work here and it is all on disk. It is down to 394. The priority itself says how
to test an item before reading it: "pick strings DISTINCTIVE to that document --
unusual personal names, exact figures, a room, a place -- and grep those against
kb/facts.json." That is right and it is slow by hand. This does it mechanically
for every skimmed record at once, so the reading queue is RANKED rather than
alphabetical.

WHAT A SCORE MEANS, AND WHAT IT DOES NOT. A distinctive token PRESENT in the
project is weak evidence the passage around it was worked. A token ABSENT is a
specific, checkable place to look. So a high score means "many specific places to
look", not "this document is unread", and a low score means "little here that is
not already somewhere", not "this document is finished". THE SCORE RANKS; IT DOES
NOT DECIDE. Every item still has to be read before anything follows from it.

THE PROXY FAILURES THIS PROJECT HAS ALREADY PAID FOR, and how this avoids them:

  - char_count as a content measure. A web capture of 533,742 bytes held 2,148
    characters of text and passed every check. So this strips tags and scripts
    before measuring anything, and reports the STRIPPED length beside the score.
  - p_451's own reading list, ranked on cached file size, whose top entry was a
    paywall shell. Same fix.
  - A destination checked in the wrong language (f_5759). Tokens here are
    language-independent by construction: figures and proper names, never
    wording.
  - citation_aim's discarded sibling, which compared a citing sentence to a
    bibliographic source entry and produced 516 false findings because the two
    describe different things. This compares a document's tokens to the whole
    project text, which is the comparison that actually holds.

THE FIRST VERSION OF THIS FAILED CALIBRATION AND THE FAILURE IS KEPT HERE,
because it is the same failure in a new costume. It scored every skimmed source
on its total absent tokens, and the ranking came back led by 200KB issues of
Canadian Camping -- a corpus this project has ALREADY read word for word, 164 of
164, with a per-item ledger at kb/reread/cc_progress.jsonl. What it was actually
measuring was DOCUMENT LENGTH: a long periodical about camps all over Canada
carries hundreds of names that are absent from this project because they have
nothing to do with Kanawana. That is char_count wearing a hat, and it is the
fourth time this project has ranked a reading list on size by accident.

WHAT IT MEASURES NOW: absent tokens WITHIN A WINDOW OF A CAMP MENTION. A document
that never names the camp scores nothing, and a long document scores on the
paragraphs that concern the camp rather than on its length. The camp-mention
count is printed beside the score so a reader can see which it is.

CALIBRATION, run 2026-09-08 before this was trusted. src_history_1935 is the
control: p_487 read it end to end on 2026-09-07, listed eighteen distinctive
items and found seventeen of them already in the wiki, so a working instrument
must score it LOW. It scores 9 absent of 29 -- AND ALL NINE ARE OCR CORRUPTION:
"GREW TRIANGLE" for Green Triangle, "Seniob Director", "Lakes Kanawena",
"Shawbridge InvitationGenes", "Montevideog Uruguay". THAT IS THE NOISE FLOOR OF
THIS INSTRUMENT ON SCANNED TEXT, and it is high: expect roughly a third of the
tokens in an OCR'd document to be absent because they are damaged, not because
they are new. Read the ratio against that floor, not against zero.

WHEN INSPECTING ONE SOURCE it also prints the document's SECTION HEADINGS with
line numbers, and that is not decoration. On 2026-09-08 the 1975 director's
report took FIVE separate passes in one evening: Food Services, then Kampers and
Staff, then Hike & Trip, then the camper questionnaire, then the rest. The first
four each read the document for one thing and left the next -- the failure this
project has catalogued for weeks, committed four times against one file by the
person cataloguing it. The fifth pass began by listing the headings and working
them in order, and that is what finished it. So the instrument that sends you to
a document now hands you its map at the same time: a heading list is a checklist,
and a document read against one is finishable.

NOT A CHECK. No baseline, not in all.py, exits 0 always. Its output is a queue.
"""
import json
import os
import re
import sys

TAG = re.compile(r'<script.*?</script>|<style.*?</style>|<[^>]+>', re.S | re.I)
WS = re.compile(r'[ \t\xa0]+')

# A proper-name bigram: two capitalised words in a row. Single capitalised words
# are far too common in OCR'd headings to be distinctive.
NAME = re.compile(r"\b[A-Z][a-zA-Z'’-]{2,}\s+[A-Z][a-zA-Z'’-]{2,}\b")
# A figure worth checking: money, a percentage, or a number with a separator.
FIGURE = re.compile(r'\$\s?\d[\d, ]*\d|\b\d{1,3}(?:[, ]\d{3})+\b|\b\d+(?:\.\d+)?\s?%')

# A section heading in these documents: a short line, mostly capitals or title
# case, no sentence punctuation. Deliberately loose -- a heading list with a few
# false entries is still a map; a strict pattern that drops PROGRAM AREAS is not.
# ALL CAPS, or Title Case ending in a colon. A first version allowed any short
# capitalised line and returned the 1977 report's entire staff roster as
# "headings" -- ninety names, each a short Title Case line. Two words with no
# colon is a person, not a section.
HEADING = re.compile(r'^(?:[A-Z][A-Z0-9 &/\'.-]{3,44}|[A-Z][A-Za-z0-9 &/\'.-]{2,44}:)\s*$')

NOISE = re.compile(r'(YMCA|Camp|Kamp|Montreal|Montr|Quebec|Qu.bec|Internet Archive'
                   r'|Annual Report|Saint|St\.|Canada|Canadian)', re.I)

CAMP = re.compile(r'anawana|Kamp\b', re.I)
WINDOW_LINES = 12       # lines either side of a camp mention


def strip(text):
    return WS.sub(' ', TAG.sub(' ', text))


def haystack():
    """An INDEX, not a string. A substring scan of the whole project text per
    token is O(tokens x project) and took minutes on 388 sources; the tokens are
    themselves regular, so indexing the project with the same two patterns makes
    each lookup O(1). Figures are normalised so that "1,234" and "1 234" and
    "$1,234" all collapse to one key -- the separator is a typesetting choice and
    was producing false absences."""
    parts = []
    with open('kb/facts.json', encoding='utf-8') as fh:
        parts.append(fh.read())
    for root, _dirs, files in os.walk('wiki'):
        for name in files:
            if name.endswith('.md'):
                with open(os.path.join(root, name), encoding='utf-8') as fh:
                    parts.append(fh.read())
    text = WS.sub(' ', '\n'.join(parts))
    idx = set()
    for m in NAME.finditer(text):
        idx.add(' '.join(m.group(0).split()))
    for m in FIGURE.finditer(text):
        idx.add(norm_figure(m.group(0)))
    return idx


def norm_figure(s):
    return re.sub(r'[\s,$]', '', s)


def tokens(text):
    out = set()
    for m in NAME.finditer(text):
        t = ' '.join(m.group(0).split())
        if not NOISE.search(t):
            out.add(t)
    for m in FIGURE.finditer(text):
        out.add(' '.join(m.group(0).split()))
    return out


def main() -> int:
    # One positional argument. A source_id fragment inspects that record and
    # prints its absent tokens; a read_state word ("extracted", "partial",
    # "swept") scans that population instead of the default "skimmed". Added
    # 2026-09-08 after the 2026 parent guide -- read_state "extracted", cited in
    # the wiki as ^pg26 -- turned out to hold two whole passages nobody had
    # taken: the fifteen rivers of the trip programme and the camp's named
    # authority on homesickness. AN "EXTRACTED" STATE IS A CLAIM ABOUT WHAT WAS
    # TAKEN OUT OF A DOCUMENT, NOT ABOUT WHAT IS LEFT IN IT, which makes the
    # 720 extracted records a population worth the same treatment (p_451).
    STATES = {'skimmed', 'extracted', 'partial', 'swept', 'read', 'snippet', 'unread'}
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    state = arg if arg in STATES else 'skimmed'
    only = None if arg in STATES else arg
    limit = 40
    with open('sources/sources.json', encoding='utf-8') as fh:
        data = json.load(fh)
    srcs = data['sources'] if isinstance(data, dict) else data
    hay = haystack()

    rows = []
    for s in srcs:
        if only:
            if only not in s['source_id']:
                continue
        elif s.get('read_state') != state:
            continue
        cp = s.get('cache_path') or ''
        if not cp or not os.path.exists(cp) or os.path.isdir(cp):
            continue
        with open(cp, encoding='utf-8', errors='replace') as fh:
            raw = fh.read()
        text = strip(raw)
        if len(text) < 400:
            continue
        lines = strip(raw).split('\n') if '\n' in raw else raw.split('\n')
        lines = [WS.sub(' ', TAG.sub(' ', l)) for l in raw.split('\n')]
        hits = [i for i, l in enumerate(lines) if CAMP.search(l)]
        if not hits:
            continue
        keep = set()
        for i in hits:
            keep.update(range(max(0, i - WINDOW_LINES), min(len(lines), i + WINDOW_LINES + 1)))
        near = '\n'.join(lines[i] for i in sorted(keep))
        toks = tokens(near)
        if not toks:
            continue
        # A figure written "1,234" in one place and "1 234" in another is the
        # same figure; check both separators before calling it absent.
        absent = [t for t in toks
                  if (norm_figure(t) if any(c.isdigit() for c in t) else t) not in hay]
        rows.append((len(absent), len(toks), len(hits), len(text),
                     s['source_id'], cp, sorted(absent)))

    rows.sort(reverse=True)
    print('=' * 78)
    print('SKIMMED SOURCES, RANKED BY DISTINCTIVE TOKENS ABSENT FROM THE PROJECT')
    print('=' * 78)
    print('  read_state = %s' % state)
    print('  %d source(s) measured, of those that name the camp at all.\n  A token absent is a place to look, not a verdict; on scanned text expect about\n  a third to be absent through OCR damage alone (see the docstring).' % len(rows))
    print()
    print('  %-5s %-5s %-5s %-8s  %s' % ('ABSNT', 'TOKS', 'MENT', 'CHARS', 'source_id'))
    for absent, ntok, nment, nchar, sid, cp, alist in rows[:limit]:
        print('  %-5d %-5d %-5d %-8d  %s' % (absent, ntok, nment, nchar, sid))
        if only:
            for t in alist[:60]:
                print('          %s' % t)
            heads = [(n + 1, l.strip()) for n, l in enumerate(lines)
                     if HEADING.match(l.strip()) and len(l.strip().split()) <= 6]
            if heads:
                print()
                print('        SECTION HEADINGS -- read them in order, tick them off:')
                for n, h in heads[:60]:
                    print('        %6d  %s' % (n, h))
    if not only and len(rows) > limit:
        print('  … %d more below the top %d' % (len(rows) - limit, limit))
    return 0


sys.exit(main())
