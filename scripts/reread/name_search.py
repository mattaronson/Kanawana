#!/usr/bin/env python3
"""Search the cached documents for a person's name, tolerating OCR line-break
hyphenation.

WHY THIS EXISTS. p_490 built a finding aid of 358 staff-change passages out of
ninety-two Montreal YMCA annual reports and then worked it by grepping the aid
for each camp person's name. On 2026-09-08 that method produced two false nulls
in one hour. The priority's own text records "Ball, Dawson, Cushing, POTTER,
Charlton and LANGILLE all return ZERO from the sweep" -- and both Potter and
Langille are in the reports. The OCR sets a name broken across a line as
"Harold Pot- ter" and "Mr. Howard Lan- gille", so a plain search for the surname
matches neither, and the sweep that built the finding aid was itself a plain
search, so the passages were never extracted into it either. Reading them
answered howie-langille.md's Open Question 1 in both halves -- his first name and
where he went -- and produced a lead on Harold H. Potter's whole YMCA career.
See f_5747.

A NULL FROM A PLAIN GREP OVER OCR TEXT IS A FACT ABOUT THE GREP. This searches
for the name with an optional hyphen and any whitespace permitted between every
pair of letters, which is loose enough to catch every break the scanner makes and
tight enough that a false positive is obvious on sight -- the match is printed
with its context so it can be read rather than counted.

Usage:
    python scripts/reread/name_search.py Langille
    python scripts/reread/name_search.py "Van Wagner" --glob 'sources/cache/**/*.txt'
    python scripts/reread/name_search.py Potter --hyphen-only   # only the hits a
                                                                # plain grep misses
"""
import argparse
import glob as globmod
import re
import sys

DEFAULT_GLOB = "sources/cache/ymca-montreal-fonds/*.txt"


def loose(name: str) -> re.Pattern:
    """A pattern matching the name across any OCR line break or hyphenation."""
    parts = [re.escape(c) for c in name if not c.isspace()]
    # Word boundaries matter more than they look. Without them "Ball" matches
    # inside "basketball", "football" and "Ballantyne", and the first run of this
    # tool reported 1,253 hits for it across ninety-two reports (f_5749). \b is
    # no good here because a hyphenated break puts a non-word character inside
    # the name, so the boundary is asserted only at the two ends.
    return re.compile(r"(?<![A-Za-z])" + r"\s*-?\s*".join(parts) + r"(?![A-Za-z])",
                      re.I)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--glob", default=DEFAULT_GLOB)
    ap.add_argument("--context", type=int, default=260)
    ap.add_argument("--hyphen-only", action="store_true",
                    help="print only matches a plain search would miss")
    args = ap.parse_args()

    rx = loose(args.name)
    plain = re.compile(re.escape(args.name), re.I)
    found = 0
    for path in sorted(globmod.glob(args.glob, recursive=True)):
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = re.sub(r"\s+", " ", fh.read())
        for m in rx.finditer(text):
            if args.hyphen_only and plain.fullmatch(m.group(0)):
                continue
            found += 1
            lo = max(0, m.start() - args.context)
            print(f"[{path.split('/')[-1]}] …{text[lo:m.end() + args.context]}…\n")
    if not found:
        print(f'No match for "{args.name}" in {args.glob}.')
        print("That is now a fact about the corpus rather than about the pattern.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
