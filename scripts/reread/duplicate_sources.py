#!/usr/bin/env python3
"""Report source records that describe the same document, by CACHE PATH.

WHY THIS EXISTS. On 2026-09-06 the 1928 Camp Dorval report was found carrying two
source records -- one marked 'extracted', one marked 'unread', neither pointing at
the other. The first count of how widespread that was (f_5006) compared record
NAMES either side of the src_cache_ prefix and found 69 pairs. That method cannot
see a pair whose names differ by more than the prefix, and there is at least one:
src_cache_the_lookout_vol_1_no_3 and src_ia_the_lookout_1993 are the same single
digitized newsletter issue (f_5012). Both point into the same cached file, so a
path comparison catches what a name comparison misses.

WHAT DOES NOT WORK, ESTABLISHED BY RUNNING IT. The path comparison this script was
first written to do finds almost nothing: 16 shared paths across 1,668 records, and
only one group disagreeing about read_state. It does NOT catch the Lookout pair, and
the reason is the shape of the pairs themselves -- in every case checked, the
substantive record has NO cache_path at all and the src_cache_ record has the path.
Two records for one document, and they never both name the file. So the comparison
that works is between the FILENAME STEM of the record that has a path and the TITLE
of the record that does not: "1928-report-on-camp-dorval" against "Report on Camp
Dorval - Season 1928", "the-lookout-vol-1-no-3" against "The Lookout, Vol. 1 No. 3".
That is what --stems does, and it is the mode to use.

This reports; it does not merge. Two records for one document may carry different
provenance -- one hand-written when the document was read, one generated from the
cache directory -- and the no-silent-overwrite rule applies to source records as
much as to facts. Merging is an operator decision (p_442).

Read the output with the legitimate case in mind: a COLLECTION-level record plus
its ITEM-level records will share a path or a directory quite properly. The broken
case looks identical until you check read_state -- two records for one document
that disagree about whether it has been read. The report flags that disagreement
separately, and that is the column to act on.

Usage:
    python scripts/reread/duplicate_sources.py            # summary
    python scripts/reread/duplicate_sources.py --full     # every group
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
READ_ORDER = {"unread": 0, "skimmed": 1, "read": 2, "extracted": 3}


def norm(path: str) -> str:
    """Normalise a cache_path for comparison: strip, lowercase, drop ./ prefix."""
    p = (path or "").strip().replace("\\", "/")
    p = re.sub(r"^\./", "", p)
    return p.lower().rstrip("/")


def slug(title: str) -> str:
    """Compare titles loosely: lowercase, alphanumerics only."""
    return re.sub(r"[^a-z0-9]+", "", (title or "").lower())


def load():
    return json.loads((ROOT / "sources" / "sources.json").read_text())["sources"]


# Fraction of a cache filename's tokens that must appear in a title for the pair
# to be reported. 1.0 is strict containment, which is what this script did until
# 2026-09-06 and which misses the "sgw" case described at the match site below.
MIN_OVERLAP = 0.75

STOP = {"the", "a", "of", "on", "in", "and", "for", "to", "no", "vol", "pt",
        "txt", "pdf", "report", "season", "s"}

# A date is written one way in a filename and another in a title, and that alone
# hid a pair: "the-green-triangle-1933-07-08" against "The Green Triangle, July 8,
# 1933". The stem carries 07 and 08; the title carries "july" and "8". So month
# names are folded to their zero-padded number and leading zeros are stripped
# from every numeric token, which makes 07 and july agree and 08 and 8 agree.
MONTHS = {"january": "1", "february": "2", "march": "3", "april": "4",
          "may": "5", "june": "6", "july": "7", "august": "8",
          "september": "9", "october": "10", "november": "11", "december": "12",
          "jan": "1", "feb": "2", "mar": "3", "apr": "4", "jun": "6", "jul": "7",
          "aug": "8", "sep": "9", "sept": "9", "oct": "10", "nov": "11", "dec": "12"}


def fold(w: str) -> str:
    """One token, normalised: month names to numbers, numbers without padding."""
    if w in MONTHS:
        return MONTHS[w]
    if w.isdigit():
        return str(int(w))
    return w


def tokens(text: str) -> set:
    raw = {w for w in re.split(r"[^a-z0-9]+", (text or "").lower()) if w} - STOP
    return {fold(w) for w in raw}


def report_stems(records) -> int:
    """Match cache filename stems against titles of records lacking a cache_path."""
    pathless = [r for r in records if not r.get("cache_path") and r.get("title")]
    hits, seen = [], set()
    for r in records:
        cp = r.get("cache_path")
        if not cp:
            continue
        stem = tokens(Path(cp).stem)
        if len(stem) < 2:
            continue
        for other in pathless:
            if other["source_id"] == r["source_id"]:
                continue
            title = tokens(other["title"])
            # Strict containment misses a pair whose FILENAME carries a token the
            # title does not. Found 2026-09-06: the stem
            # "sgw-ymca-annual-report-1966-67" against the title "YMCA Montreal
            # Annual Report 1966-67" -- the filename says "sgw", the title says
            # "montreal", and neither is a subset of the other, so a real duplicate
            # went unreported and the volume was read as if unread. Requiring most
            # of the stem rather than all of it catches that shape.
            overlap = (len(stem & title) / len(stem)) if stem else 0.0
            if stem and (stem <= title or overlap >= MIN_OVERLAP):
                key = tuple(sorted((r["source_id"], other["source_id"])))
                if key not in seen:
                    seen.add(key)
                    hits.append((r, other))

    print("CACHE FILENAME STEM CONTAINED IN ANOTHER RECORD'S TITLE")
    print("-" * 70)
    print(f"{len(hits)} candidate pairs. A pair whose two records DISAGREE about")
    print("read_state is the broken case; a pair that agrees is redundant but honest.")
    print()
    for r, other in sorted(hits, key=lambda h: h[0]["source_id"]):
        flag = "  <-- DISAGREE" if r.get("read_state") != other.get("read_state") else ""
        print(f"{Path(r['cache_path']).name}{flag}")
        print(f"    {r['source_id']:<58} {r.get('read_state'):<10} has path")
        print(f"    {other['source_id']:<58} {other.get('read_state'):<10} "
              f"{other['title'][:60]}")
        print()
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="print every group, not a sample")
    ap.add_argument("--stems", action="store_true",
                    help="match cache FILENAME STEMS against the titles of records "
                         "that have no cache_path -- the mode that actually works")
    args = ap.parse_args()

    records = load()
    by_path = defaultdict(list)
    for r in records:
        if r.get("cache_path"):
            by_path[norm(r["cache_path"])].append(r)

    groups = {p: rs for p, rs in by_path.items() if len(rs) > 1}
    disagreeing = {
        p: rs for p, rs in groups.items()
        if len({r.get("read_state") for r in rs}) > 1
    }

    # Records with no cache_path whose title matches one that has a path.
    titled = defaultdict(list)
    for r in records:
        titled[slug(r.get("title", ""))].append(r)
    orphan_pairs = []
    for s, rs in titled.items():
        if not s or len(rs) < 2:
            continue
        with_path = [r for r in rs if r.get("cache_path")]
        without = [r for r in rs if not r.get("cache_path")]
        if with_path and without:
            orphan_pairs.append((s, rs))

    print(f"{len(records)} source records")
    print(f"{len(groups)} cache paths carry more than one record "
          f"({sum(len(v) for v in groups.values())} records)")
    print(f"{len(disagreeing)} of those groups DISAGREE about read_state -- "
          f"that is the broken case")
    print(f"{len(orphan_pairs)} exact title matches pair a record having a cache_path "
          f"with one having none")
    print()

    if args.stems:
        return report_stems(records)

    shown = disagreeing if not args.full else groups
    label = "DISAGREEING" if not args.full else "ALL"
    print(f"{label} GROUPS")
    print("-" * 70)
    for p, rs in sorted(shown.items()):
        print(p)
        for r in sorted(rs, key=lambda r: READ_ORDER.get(r.get("read_state"), -1)):
            print(f"    {r['source_id']:<62} {r.get('read_state')}")
        print()

    if orphan_pairs:
        print("TITLE MATCHES ACROSS THE CACHE_PATH BOUNDARY")
        print("-" * 70)
        for s, rs in sorted(orphan_pairs)[: None if args.full else 20]:
            print(rs[0].get("title"))
            for r in rs:
                print(f"    {r['source_id']:<62} "
                      f"{r.get('read_state'):<10} "
                      f"{'path' if r.get('cache_path') else 'NO PATH'}")
            print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
