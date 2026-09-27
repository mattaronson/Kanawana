#!/usr/bin/env python3
"""Classify the cached Montreal YMCA news releases by whether they mention the camps.

WHY. About 170 Montreal YMCA news releases (1962-1980) are cached and carry read_state
"skimmed" or "unread". Reading each one to find that it is about a downtown residence
fitness class is waste. But leaving them all "skimmed" is worse: a later pass cannot
tell the difference between "nobody looked" and "somebody looked and there was nothing",
and reads them again.

WHAT THIS IS AND IS NOT. It is a keyword classification. A file this script calls
NULL is a file in which these patterns do not appear -- that is a fact about the
patterns and this OCR, not about the document (handoff rule 33). The scans render
"Kanawana" as "Kanewana" in at least one file, so the pattern list carries variants and
should grow whenever another is found. A NULL record's basis must say so.

Usage:
    python3 scripts/reread/sweep_news_releases.py            # report only
    python3 scripts/reread/sweep_news_releases.py --write    # update sources.json
"""
import argparse
import json
import re
from pathlib import Path

CACHE = Path("sources/cache/ymca-montreal-fonds")
SOURCES = Path("sources/sources.json")

# Kanawana and its OCR variants, plus the association's other camps and the
# generic camping words that would make a release worth a human read.
CAMP = re.compile(
    r"kan[ae]w[ae]n+a|kanawa\b|otoreke|otereke|perrot|voyageur|becs?c?ies|"
    r"weredale|thunderbird|christieville|day camp|summer camp|camping",
    re.I,
)
KANAWANA_ONLY = re.compile(r"kan[ae]w[ae]n+a|kanawa\b", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    files = sorted(p for p in CACHE.glob("*news-release-*.txt"))
    if not files:
        raise SystemExit("no news-release files under %s" % CACHE)

    data = json.load(open(SOURCES))
    records = data["sources"] if isinstance(data, dict) else data
    by_path = {}
    for r in records:
        cp = r.get("cache_path")
        if cp:
            by_path.setdefault(Path(cp).name, []).append(r)

    kan, camp, null, unrecorded = [], [], [], []
    for f in files:
        text = f.read_text(errors="replace")
        if KANAWANA_ONLY.search(text):
            kan.append(f.name)
        elif CAMP.search(text):
            camp.append(f.name)
        else:
            null.append(f.name)
        if f.name not in by_path:
            unrecorded.append(f.name)

    print("%d cached news releases" % len(files))
    print("  %3d name Kanawana (or an OCR variant)" % len(kan))
    print("  %3d name another camp or camping generally, but not Kanawana" % len(camp))
    print("  %3d match no camp pattern at all" % len(null))
    if unrecorded:
        print("  %3d have NO source record -- catalogue these before sweeping" % len(unrecorded))
        for n in unrecorded[:10]:
            print("      " + n)

    if not args.write:
        print("\nreport only; pass --write to set read_state on the no-match files")
        return

    basis = (
        "swept 2026-09-06 under p_451 by scripts/reread/sweep_news_releases.py: NO CAMP "
        "PATTERN MATCHES IN THIS FILE. The pattern covers Kanawana and its OCR variants, "
        "Otoreke, Perrot, Voyageurs, Becsies, Weredale, Thunderbird, Christieville and the "
        "phrases day camp / summer camp / camping. THIS IS A FACT ABOUT THAT PATTERN AND "
        "THIS OCR, NOT ABOUT THE DOCUMENT -- the release was not read. It is recorded so a "
        "later pass can tell 'swept and nothing matched' from 'nobody looked'. If a camp "
        "name is ever found spelled some other way, add it to the pattern and re-run."
    )
    n = 0
    for name in null:
        for r in by_path.get(name, []):
            if r.get("read_state") in (None, "unread", "skimmed"):
                r["read_state"] = "swept"
                r["read_state_basis"] = basis
                n += 1
    out = json.dumps(data, indent=2, ensure_ascii=False)
    SOURCES.write_text(out)
    print("\n%d source record(s) set to read_state 'swept'" % n)


if __name__ == "__main__":
    main()
