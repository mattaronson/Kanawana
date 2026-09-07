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
# The DAY IS NOT MATCHED AT ALL. Requiring digits for it is what kept
# "FOR THE YEAR ENDING MARCH 3lst, 1946" unread -- the OCR sets an ell for the one, and
# only the month and year are reported anyway. Anything non-numeric between the month and
# the four-digit year is skipped, bounded tightly so a distant year cannot be captured.
_DAY = r"[^0-9]{0,4}\d{0,2}[^0-9]{0,6}"
PATTERNS = [
    re.compile(r"year\s+end(?:ing|ed)\s*,?\s*(" + MONTHS + r")" + _DAY + r"(\d{4})", re.I),
    re.compile(r"as\s+at\s+(" + MONTHS + r")" + _DAY + r"(\d{4})", re.I),
    # A bare span with no "year ending" phrase at all: "JUNE I, 196k = MAY 31, 1965", where
    # the opening year is OCR'd to nonsense but the closing one is clean. The year-end is
    # the SECOND date. These are the 1960s volumes, which are the ones where getting the
    # season wrong matters most, since that is where the association changed its year-end.
    re.compile(r"(?:" + MONTHS + r")[^0-9]{0,4}\d{0,2}[^0-9]{0,8}[\dOoIikl]{4}\s*[-=–—]\s*("
               + MONTHS + r")" + _DAY + r"(\d{4})", re.I),
]
# The scans render 3 as 4, 1 as I or l, and drop characters, so the day is not trusted;
# only the month and year are reported.

# FRENCH EDITIONS, added 2026-09-06. Nineteen of the volumes this script reported UNREAD
# are the French-language editions, and they state the year-end as plainly as the English
# ones do -- "Bilan au 31 mai 1983", "l'exercice terminé à cette date". The null was a fact
# about an English-only regex, which is exactly what the docstring warns about and exactly
# what a reader of the output would otherwise have taken for a defective volume.
# The OCR mangles the accents and sometimes the month itself ("31 maiï 1983"), so the month
# alternatives are matched loosely.
MOIS = {
    "janvier": "January", "fevrier": "February", "février": "February", "mars": "March",
    "avril": "April", "mai": "May", "juin": "June", "juillet": "July", "aout": "August",
    "août": "August", "septembre": "September", "octobre": "October",
    "novembre": "November", "decembre": "December", "décembre": "December",
}
MOIS_RE = "|".join(sorted(MOIS, key=len, reverse=True))
# Three further failure modes, all found 2026-09-06 by looking at the volumes the first
# French patterns still missed, and all defects in the regex rather than the volume:
#   "Bilan au \n Ÿ 31 mai 1984"        -- a line break and a stray OCR glyph inside the phrase
#   "L'exercice FINANCIER terminé le"  -- a word between "exercice" and "terminé"
#   a volume stating its year-end past the 20,000-character window
# The first two are handled here; the third by widening the window in main().
# Any run of non-digits: the stray glyph in "Bilan au \n Ÿ 31 mai 1984" is a WORD
# character to Python, so neither \\s nor \\W matched it and the volume stayed UNREAD.
_GAP = r"[^0-9]{0,8}"
PATTERNS_FR = [
    re.compile(r"(?:bilan|exercice(?:\s+\w+){0,2}\s+termin\w*)" + _GAP + r"(?:au|le)" + _GAP
               + r"(\d{1,2})\s*(?:er)?" + _GAP + r"(" + MOIS_RE + r")\w{0,2}" + _GAP + r"(\d{4})", re.I),
    re.compile(r"\bau" + _GAP + r"(\d{1,2})\s*(?:er)?\s*(" + MOIS_RE + r")\w{0,2}\s*(\d{4})", re.I),
]

# Camp-level reports are a different document class and do not follow the association's
# year-end at all: a "Camp Perrot annual report" or a "Kamp Kanawana annual report" covers
# one season and is named for it. Running them through this scan produced twelve nulls that
# looked like unreadable volumes and were nothing of the kind.
CAMP_LEVEL = re.compile(r"(camp-perrot|kamp-kanawana|point-saint-charles|les-voyageurs)", re.I)


# Widened from 20,000 on 2026-09-06: several volumes state their year-end only in the
# auditors' report, which in the later editions sits well past the first 20,000 characters.
WINDOW = 120000


# The scans break words across lines with a hyphen -- "for the year ending Dec-\nember"
# in the 1959, 1960 and 1961 volumes, which are three of the four December-regime reports
# where getting the season right matters most. Joining those back up before matching is a
# one-line fix that was worth four volumes.
DEHYPHEN = re.compile(r"[-~\u2010-\u2015]\s*\n\s*")


def year_end(text):
    """The year-end statement nearest the START of the document.

    Not "the first pattern that matches anywhere", which is what this did until
    2026-09-06 and which broke the moment the search window was widened: the 1989
    report came back as May 1988, because a later-in-the-document match of an
    earlier-in-the-list pattern beat the title page. Position in the document is
    the thing that carries authority here -- the title page and the auditors'
    report state the volume's own year-end, and a date deep inside it is as likely
    to be a comparative column.
    """
    best = None
    for pat in PATTERNS:
        m = pat.search(text)
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), m.group(1).title(), m.group(2))
    for pat in PATTERNS_FR:
        m = pat.search(text)
        if m and m.group(2).lower() in MOIS and (best is None or m.start() < best[0]):
            best = (m.start(), MOIS[m.group(2).lower()], m.group(3))
    return (best[1], best[2]) if best else None


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
    camp_level = []
    for f in files:
        if CAMP_LEVEL.search(f.name):
            print("%-52s %-18s %s" % (f.name, "n/a", "-- camp-level report, one season, named for it"))
            camp_level.append(f.name)
            continue
        head = DEHYPHEN.sub("", f.read_text(errors="replace")[:WINDOW])
        got = year_end(head)
        if got:
            month, yr = got
            print("%-52s %-18s %d" % (f.name, "%s %s" % (month, yr), season(month, yr)))
        else:
            print("%-52s %-18s %s" % (f.name, "UNREAD", "-- read the title page by eye"))
            unread.append(f.name)
    assoc = len(files) - len(camp_level)
    print()
    print("%d of %d ASSOCIATION volumes state a year-end in their first %d characters."
          % (assoc - len(unread), assoc, WINDOW))
    print("%d further file(s) are camp-level reports, excluded: a Camp Perrot or Kamp Kanawana"
          % len(camp_level))
    print("annual report covers ONE SEASON and is named for it, so the association's year-end")
    print("question does not arise. Scanning them produced nulls that read as unreadable volumes.")
    if unread:
        print()
        print("UNREAD is a fact about this regex and this OCR, not about the volume.")


if __name__ == "__main__":
    main()
