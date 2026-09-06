#!/usr/bin/env python3
"""Read every cached YMCA of Montreal annual report and report the year-end it states.

Why this exists: f_5039 established that a report "for the year ending March 31st" has the
PREVIOUS summer inside it, and the project cited that as though it held for the whole run.
It does not. The association used 31 March through its 99th report, then 31 December, then
31 May. A December-era report describes the SAME summer as its cover year. Getting this
wrong moves a camping season by a year, silently.

The cache filenames are not a guide either: the file named 1963 is the report for the year
ended 31 May 1964, while the file named 1984 is for the year ended 31 May 1984.

Usage: python3 scripts/reread/annual_report_year_ends.py [--dir DIR]

The OCR is poor, so a null here means "no year-end statement matched", never "the report
does not state one". Volumes that come back UNREAD need a human eye on the title page.
"""
import argparse
import pathlib
import re

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
# "for the year ending March 31st, 1949" / "as at December 31, 1962" / "YEAR ENDED MAY 31, 1982"
PATTERNS = [
    re.compile(r"year\s+end(?:ing|ed)\s*,?\s*(" + MONTHS + r")\s*(\d{1,2})\s*(?:st|nd|rd|th)?\s*,?\s*(\d{4})", re.I),
    re.compile(r"as\s+at\s+(" + MONTHS + r")\s*(\d{1,2})\s*(?:st|nd|rd|th)?\s*,?\s*(\d{4})", re.I),
]
# The scans render 3 as 4, 1 as I or l, and drop characters, so the day is not trusted;
# only the month and year are reported.


def year_end(text):
    for pat in PATTERNS:
        m = pat.search(text)
        if m:
            return m.group(1).title(), m.group(3)
    return None


def season(month, end_year):
    """Which summer a year ending in `month` `end_year` contains."""
    n = ["January", "February", "March", "April", "May", "June", "July", "August",
         "September", "October", "November", "December"].index(month) + 1
    # A year ending before the summer (Jan-May) contains the previous summer;
    # one ending after it (Jun-Dec) contains its own year's.
    return int(end_year) - 1 if n <= 5 else int(end_year)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="sources/cache/ymca-montreal-fonds")
    args = ap.parse_args()
    files = sorted(pathlib.Path(args.dir).glob("*annual-report*.txt"))
    if not files:
        raise SystemExit("no annual-report files under %s" % args.dir)
    unread = []
    print("%-52s %-18s %s" % ("file", "year end (stated)", "camping season"))
    print("-" * 92)
    for f in files:
        head = f.read_text(errors="replace")[:20000]
        got = year_end(head)
        if got:
            month, yr = got
            print("%-52s %-18s %d" % (f.name, "%s %s" % (month, yr), season(month, yr)))
        else:
            print("%-52s %-18s %s" % (f.name, "UNREAD", "-- read the title page by eye"))
            unread.append(f.name)
    print()
    print("%d of %d volumes state a year-end in their first 20,000 characters." % (len(files) - len(unread), len(files)))
    if unread:
        print("UNREAD is a fact about this regex and this OCR, not about the volume.")


if __name__ == "__main__":
    main()
