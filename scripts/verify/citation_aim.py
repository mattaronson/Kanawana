"""Check that a [f_NNNN] citation points at a fact that is ABOUT what it cites.

p_401. The existing harness checks that every citation RESOLVES: f_9999 with no
such fact fails the build. It has nothing to say about f_0412 cited beside a
sentence about Camp Keewaydin, because f_0412 is a real fact and the marker is
well formed. That defect passed every check for months, and three more of the
same shape were introduced in one session of writing -- each caught only by a
human re-reading the claim afterwards. A wrong-but-real id is invisible to a
resolver and reads as authority to everyone downstream.

The check is deliberately crude, because the precise version needs semantics.
It compares the DISTINCTIVE tokens of the citing sentence against those of the
fact it cites -- capitalised names, four-digit years, and numbers -- and flags a
citation that shares NONE of them. That is a weak test on purpose: a citation
sharing one proper noun passes, so the false-positive rate stays near zero and
the check keeps its credibility. It catches the shape that actually occurs,
which is a citation aimed at an entirely different subject.

Known-safe patterns are exempt rather than silenced one by one:
  - a sentence citing three or more facts at once (a summary line, where any
    one fact may cover only part of it)
  - a bare footnote line -- "See [f_2248]." carries no prose of its own to
    compare against, so there is nothing to test and testing it produces only
    noise. The check needs a citing sentence with at least two distinctive
    tokens of its own before it will judge the aim of anything.
  - NOT a fact flagged SUPERSEDED. That exemption was written first and then
    removed: it exempted f_0412, the very citation this check exists to catch.
    An amended fact is compared on what it CLAIMS, with the bracketed editorial
    note stripped, which is the right comparison anyway.
  - an explicit  <!-- aim-ok: reason -->  on the line above, which requires
    writing the reason down.

Advisory by design: prints findings and exits 0. Promote to blocking once the
back catalogue is clean.
"""
import json, re, io, os, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def path(*p): return os.path.join(ROOT, *p)

FACTS = {f['fact_id']: f for f in
         json.load(io.open(path('kb', 'facts.json'), encoding='utf-8'))['facts']}

CITE = re.compile(r'\[(?:f_\d{4,}[^\]]*)\](?:\s*,?\s*\[(?:f_\d{4,}[^\]]*)\])*')
FID = re.compile(r'f_\d{4,}')
# Distinctive = any word of four or more letters, or any number. NOT restricted
# to capitalised words: "the camp had an archery range" cited to a fact reading
# "Kanawana had an archery range and a lacrosse field" is a correct citation
# that a capitals-only tokenizer cannot see, because the shared words are common
# nouns. Case is folded and the frequency stop-list below removes the words that
# are too common in this corpus to discriminate.
TOKEN = re.compile(r"\b(?:[a-zA-ZÀ-ɏ'-]{4,}|\d{2,4})\b")

# A trailing editorial annotation added when a fact was flagged or superseded.
ANNOT = re.compile(r'\[(?:SUPERSEDED|Flagged)\b[^\]]*\]', re.S)

# Non-distinctive tokens are DERIVED from the corpus, not guessed at. A word
# that appears in a large share of all fact claims -- Quebec, Montreal, YMCA,
# Association -- tells you nothing about whether a citation is aimed correctly,
# and treating it as a match is how f_0413 (Mary Edgar at Camp Oolahwan) slipped
# past this check when cited beside a sentence about Kanawana's founding date:
# the only word they shared was "Quebec". Hand-maintaining that list would rot;
# a frequency threshold maintains itself as the KB grows.
def _fold(s):
    """Strip accents. The run is bilingual and the same name is spelled both
    ways within it -- "L'Etranger" in an OCR'd claim against "L'Étranger" in
    prose -- which read as a mis-citation when it was simply an accent."""
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

DF_CUTOFF = 0.02          # in >2% of fact claims == not distinctive here

def _corpus_stop():
    seen = {}
    for f in FACTS.values():
        for t in {x.lower() for x in TOKEN.findall(_fold(f['claim']))}:
            seen[t] = seen.get(t, 0) + 1
    n = max(len(FACTS), 1)
    # Never frequency-stop a number. A year is discriminating even when it is
    # common: "these section names date to 1959" cited to a fact about the 1959
    # renaming is a correct citation, and stopping 1959 as frequent turned four
    # correct citations into findings. Only WORDS can be too common to matter.
    return {t for t, c in seen.items()
            if c / n > DF_CUTOFF and not t.isdigit()}

GRAMMAR = {'this', 'that', 'these', 'those', 'when', 'where', 'while', 'what',
           'which', 'there', 'their', 'they', 'then', 'both', 'every', 'only',
           'from', 'with', 'under', 'after', 'before', 'also', 'here', 'have',
           'been', 'were', 'would', 'could', 'should', 'about', 'other',
           'than', 'them', 'some', 'such', 'into', 'over', 'more', 'most',
           'same', 'said', 'says', 'says.', 'which,', 'because', 'between'}
STOP = GRAMMAR | _corpus_stop()

def toks(s):
    return {t.lower() for t in TOKEN.findall(_fold(s))} - STOP

# A line that opens a footnote, list item or numbered note. Prose paragraphs in
# this wiki are hard-wrapped, so the citing sentence often starts on an earlier
# line -- but a footnote block is a stack of unrelated one-line entries and must
# never be joined up. These markers are where a block stops.
BLOCK_START = re.compile(r'^\s*(?:[-*+]\s|\d+\.\s|\|\s|>|#{1,6}\s|\[[a-z]{1,3}\]|See \[)')

def sentence_around(text, pos):
    """The citing sentence, bounded by its own hard-wrapped block.

    Two failure modes were traded off here, both observed on this corpus.
    Clipping to a single LINE let the check fire on every citation that landed
    on a continuation line, whose fragment carries no subject. Letting the
    sentence run freely across newlines pulled footnote definitions -- a stack
    of unrelated one-liners -- into the comparison and produced sixty findings,
    none of them real. So: walk back over wrapped prose lines, but stop at a
    blank line or at anything that opens a new block.
    """
    lines = text.split('\n')
    ln = text.count('\n', 0, pos)
    start = ln
    while start > 0:
        prev = lines[start - 1]
        if not prev.strip() or BLOCK_START.match(prev):
            break
        start -= 1
    end = ln
    while end + 1 < len(lines):
        nxt = lines[end + 1]
        if not nxt.strip() or BLOCK_START.match(nxt):
            break
        end += 1
    block = ' '.join(lines[start:end + 1])
    off = sum(len(lines[i]) + 1 for i in range(start, ln)) + (pos - (text.rfind('\n', 0, pos) + 1))
    a = block.rfind('. ', 0, off) + 1
    b = block.find('. ', off)
    b = len(block) if b < 0 else b + 1
    return block[a:b]

def check(rel):
    text = io.open(path(rel), encoding='utf-8').read()
    lines = text.split('\n')
    out = []
    for m in CITE.finditer(text):
        # A run of adjacent markers -- "See [f_2272], [f_2273], [f_2274]" -- is
        # ONE citation group. Judging each id separately flagged the two that
        # covered half the sentence each, which is how such a group is meant to
        # be written.
        ids = FID.findall(m.group(0))
        if len(ids) >= 3:
            continue      # a summary line; any one fact may cover only part
        line_no = text.count('\n', 0, m.start())
        if line_no > 0 and 'aim-ok:' in lines[line_no - 1]:
            continue
        sent = sentence_around(text, m.start())
        st = toks(CITE.sub('', sent))
        if len(st) < 2:
            continue    # nothing substantive to judge against. Two is enough:
                        # "Camp Keewaydin ... founded in 1893" is judgeable on
                        # {Keewaydin, 1893} alone, and a threshold of three
                        # silently exempted exactly that citation. The guard is
                        # only here to skip bare "See [f_0123]." footnote lines,
                        # which have no distinctive tokens at all.
        # The group passes if ANY of its facts is on topic. Adjacent markers
        # are written to cover a sentence between them; requiring each one to
        # match on its own flags the normal case.
        cited = [FACTS[i] for i in ids if i in FACTS]   # dangling: not our job
        if not cited:
            continue
        bare = {f['fact_id']: ANNOT.sub('', f['claim']) for f in cited}
        # Compare against the claim itself, not an editorial note appended
        # later: "[SUPERSEDED 2026-09-05 ... see c_031]" carries names and years
        # of its own that would mask a bad aim.
        if any(st & (toks(bare[f['fact_id']]) | toks(' '.join(f.get('entities') or [])))
               for f in cited):
            continue
        out.append('%s:%d  %s shares no name, year or number with the sentence citing it\n'
                   '        sentence: %s\n        %s'
                   % (rel, line_no + 1, ', '.join(ids), sent.strip()[:150],
                      '\n        '.join('%s says: %s' % (f['fact_id'], f['claim'][:130])
                                        for f in cited)))
    return out

def main():
    bad = []
    for root, _, files in os.walk(path('wiki')):
        for f in sorted(files):
            if f.endswith('.md'):
                bad += check(os.path.relpath(os.path.join(root, f), ROOT))
    print('=' * 70)
    print('CITATION AIM -- does a resolving [f_NNNN] point at a relevant fact?')
    print('=' * 70)
    if not bad:
        print('  every checked citation shares a name, year or number with its fact')
        return 0
    print('  [BLOCKING] %d citation(s) share nothing distinctive with the fact cited.' % len(bad))
    print('  The back catalogue was cleared on 2026-09-05 (p_401), so this now fails the')
    print('  build. Fix by citing the fact that carries the claim, or by rewording the')
    print('  sentence to say what the cited fact says. If the aim is right and the check')
    print('  simply cannot see it -- the distinctive name sits in the sentence before --')
    print('  put the name back in the citing sentence: a sentence carrying a citation')
    print('  should be checkable on its own.')
    for b in bad:
        print('  - %s' % b)
    return 1

sys.exit(main())
