"""Recompute the derived counts in wiki/articles.json from the articles themselves.

Three fields in that file are not data, they are measurements of something else:
word_count and open_questions measure the article markdown, and article_count
measures the records list. Until 2026-09-05 all three were written by hand. A
recompute that day found 54 of 104 records carrying a stale word_count or
open_questions, and article_count reading 93 against 104 records -- a figure
eleven articles out of date. A stale number is worse than no number, because
nothing distinguishes it from a current one (p_417).

So they are generated here and asserted by scripts/verify/data_integrity.py,
the same arrangement the plaque index already uses. Do not edit the three
fields by hand; run this script and commit what it writes. Every other field
in the file is hand-maintained and is passed through untouched.

DEFINITIONS -- each is a choice, and the point of writing them down is that the
number means the same thing in every record.

word_count
    len(text.split()) over the WHOLE markdown file, status header, headings,
    footnote markers, Related Articles and Sources list included. This is the
    definition the existing 104 values were computed under, so it is kept.
    Note it is NOT `wc -w`: Python splits on Unicode whitespace (U+00A0 and
    friends), the C locale does not, so the two disagree on articles carrying
    non-breaking spaces. Anyone quoting a figure from this field should say
    which definition it is; this project's own operator report was misled by
    the difference once already.

open_questions
    Numbered top-level entries under the `## Open Questions` heading that are
    still open. An entry is CLOSED, and not counted, when either:
      * its text begins with `~~` (struck through -- this wiki's convention
        for a question that has been answered in place), or
      * it opens with a bracket tag stating an unqualified resolution:
        [Resolved], [ANSWERED 2026-08-25], [Resolved editorially 2026-07-10].
    A qualified tag -- [Partially resolved], [Largely resolved], [Half
    resolved, half open] -- leaves the entry OPEN and counted, because a
    remainder is a remainder. An article with no Open Questions section
    counts 0.

article_count
    len(articles). It had drifted eleven behind.

Usage:  python3 scripts/wiki/build_article_counts.py [--check]
        --check exits 1 and prints the differences instead of writing.
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARTICLES = os.path.join(ROOT, 'wiki', 'articles.json')

OPEN_QUESTIONS = re.compile(r'^##\s+Open Questions\s*$(.*?)(?=^##\s|\Z)', re.M | re.S)
ENTRY = re.compile(r'^\d+\.[ \t]+', re.M)
# A resolution tag at the head of an entry. The qualifier group is what keeps
# "[Partially resolved]" open; it must be checked before the bare marker.
RESOLVED_TAG = re.compile(
    r'^\[(?P<qualifier>partial|partly|partially|half|largely|substantially|mostly)?'
    r'[^\]]*?\b(?:resolved|answered|closed)\b[^\]]*\]', re.I)


def count_open_questions(text, numbering=None):
    """Open entries under ## Open Questions. See the module docstring.

    If `numbering` is a list it collects the literal numbers written in the
    file, so the caller can report a list that does not read 1..n. Three
    articles carry duplicate or out-of-order numbers. The count here does not
    depend on them -- it counts entries, not labels -- and they are reported
    rather than renumbered, because other articles cite questions by number
    ("billy-ball Open Question #8") and silently shifting a number would
    re-point a citation at a different question.
    """
    section = OPEN_QUESTIONS.search(text)
    if not section:
        return 0
    body = section.group(1)
    if numbering is not None:
        numbering.extend(int(m.group(0).split('.')[0]) for m in ENTRY.finditer(body))
    starts = [m.end() for m in ENTRY.finditer(body)]
    bounds = [m.start() for m in ENTRY.finditer(body)][1:] + [len(body)]
    n = 0
    for start, end in zip(starts, bounds):
        entry = body[start:end].strip()
        if entry.startswith('~~'):
            continue
        tag = RESOLVED_TAG.match(entry)
        if tag and not tag.group('qualifier'):
            continue
        n += 1
    return n


def article_path(record):
    return os.path.join(ROOT, 'wiki', record['wiki_folder'], record['article_id'] + '.md')


def build():
    raw = io.open(ARTICLES, encoding='utf-8').read()
    data = json.loads(raw)
    changes = []
    warnings = []
    for record in data['articles']:
        path = article_path(record)
        if not os.path.exists(path):
            sys.stderr.write('missing article file for %s: %s\n'
                             % (record['article_id'], path))
            return None, None, None, 1
        text = io.open(path, encoding='utf-8').read()
        numbering = []
        for field, value in (('word_count', len(text.split())),
                             ('open_questions', count_open_questions(text, numbering))):
            if record.get(field) != value:
                changes.append('%s %s: %s -> %s'
                               % (record['article_id'], field, record.get(field), value))
            record[field] = value
        if numbering and numbering != list(range(1, len(numbering) + 1)):
            warnings.append('%s: Open Questions numbered %s, not 1..%d'
                            % (record['article_id'],
                               ','.join(str(n) for n in numbering), len(numbering)))
    if data.get('article_count') != len(data['articles']):
        changes.append('article_count: %s -> %d'
                       % (data.get('article_count'), len(data['articles'])))
    data['article_count'] = len(data['articles'])
    # Round-trips byte for byte against the committed file: 2-space indent,
    # Unicode kept as Unicode, no trailing newline.
    return json.dumps(data, indent=2, ensure_ascii=False), changes, warnings, 0


def main():
    out, changes, warnings, rc = build()
    if rc:
        return rc
    for w in warnings:
        print('  [note] %s' % w)
    check = '--check' in sys.argv[1:]
    if check:
        if changes:
            sys.stderr.write('wiki/articles.json derived counts are stale:\n')
            for c in changes:
                sys.stderr.write('  %s\n' % c)
            return 1
        print('wiki/articles.json: derived counts current')
        return 0
    io.open(ARTICLES, 'w', encoding='utf-8').write(out)
    print('wiki/articles.json: %d derived count(s) updated' % len(changes))
    for c in changes:
        print('  %s' % c)
    return 0


if __name__ == '__main__':
    sys.exit(main())
