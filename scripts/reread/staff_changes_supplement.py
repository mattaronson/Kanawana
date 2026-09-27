#!/usr/bin/env python3
"""Extract the staff-change passages the original p_490 sweep could not see.

WHY. kb/reread/ymca_annual_report_staff_changes.md was built by searching the
ninety-two cached Montreal YMCA annual reports for plain staff-change verbs --
appointed, resigned, succeeding, replaced, joined the staff. The OCR breaks words
at line ends, so "resign- ed" and "appoint- ed" match none of them, and neither
does a surname set as "Harold Pot- ter" or "Mr. Howard Lan- gille". Two of the
six names p_490 recorded as returning nothing from that aid are in the reports
(f_5747, f_5749). This finds what the plain pass missed rather than rebuilding
the aid, so the existing file stays the record of what was read from it.

Cite the report, never this file or the aid. Both are finding aids: the passages
are quoted mechanically and have not each been assessed.
"""
import re
import glob
import sys

VERBS = ['appointed', 'resigned', 'succeeded', 'succeeding', 'transferred',
         'replacing', 'replaced', 'retired', 'joined the staff',
         'leave of absence', 'elected']
WINDOW = 320


def tolerant(word: str) -> str:
    """Match a word across an OCR line break, boundaries at the two ends only."""
    parts = [re.escape(c) for c in word if not c.isspace()]
    body = r"\s*-?\s*".join(parts)
    if ' ' in word:                     # multi-word: allow a real space too
        body = r"\s*-?\s*".join(
            r"\s+".join(re.escape(c) for c in w) if False else
            r"\s*-?\s*".join(re.escape(c) for c in w)
            for w in word.split())
        body = r"\s+".join(
            r"\s*-?\s*".join(re.escape(c) for c in w) for w in word.split())
    return r"(?<![A-Za-z])" + body + r"(?![A-Za-z])"


def main() -> int:
    tol = re.compile('|'.join(tolerant(v) for v in VERBS), re.I)
    plain = re.compile('|'.join(re.escape(v) for v in VERBS), re.I)
    out = []
    for path in sorted(glob.glob('sources/cache/ymca-montreal-fonds/'
                                 'sgw-ymca-annual-report-*.txt')):
        text = re.sub(r'\s+', ' ',
                      open(path, encoding='utf-8', errors='replace').read())
        found = []
        for m in tol.finditer(text):
            if plain.fullmatch(m.group(0)):
                continue                      # the first sweep already had it
            lo = max(0, m.start() - WINDOW)
            found.append(f"- …{text[lo:m.end() + WINDOW]}…")
        if found:
            out.append((path.split('/')[-1], found))

    total = sum(len(f) for _, f in out)
    print("# Staff-change passages the plain sweep could not see\n")
    print("Extracted %d passages from %d reports by `scripts/reread/"
          "staff_changes_supplement.py`." % (total, len(out)))
    print("These are the hits where the staff-change verb itself is broken "
          "across a line by the\nOCR, so the search that built "
          "`ymca_annual_report_staff_changes.md` matched none of them.\n")
    print("**This is a finding aid, not a reading.** Cite the report.\n")
    for name, found in out:
        print("## %s\n" % name)
        for f in found:
            print(f + "\n")
    return 0


if __name__ == '__main__':
    sys.exit(main())
