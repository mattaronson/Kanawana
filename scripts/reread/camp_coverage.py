#!/usr/bin/env python3
"""How much of what the annual reports say about each camp has reached its article.

WHY. The p_441 campaign read eighty-one documents FOR KANAWANA CONTENT. That was the
right scope for its question, and it means every other camp the association ran was read
past rather than read. The gap is measurable with two counts and nothing cleverer:

    how many cached annual reports NAME the camp
    how many of those the camp's article CITES

On 2026-09-06 that arithmetic said 55 and 8 for Camp Otoreke. Reading two of the
forty-seven uncited volumes produced three seasons of registration figures, the season
dates, the metropolitan share, the canoe-trip programme, and a counting convention in
which a married couple is two people (f_5139, f_5140).

WHAT THIS IS NOT. A mention is not a fact: many will be a camp's name in a list of
association properties. The count ranks where to look, it does not say what is there.
And a high citation count does not mean a camp is well covered -- an article can cite a
report for one sentence and miss the page.

TWO COLUMNS, AND THE SECOND IS THE HONEST ONE FOR KANAWANA. The first version of this
script compared each camp only against its own article, and reported Kanawana as 114
reports naming it against 5 cited -- which is nonsense, because Kanawana's content is
spread across forty-odd articles and site/the-kanawana-site.md is only one of them. A
sibling camp concentrates in a single article; the subject of the whole wiki does not.
So the report now also counts citations ANYWHERE IN THE WIKI, and for Kanawana that is
the number to read.

"CITED NOWHERE" MEANS NO SOURCE ID NAMES IT, NOT THAT NOBODY HAS READ IT. The 2007
annual report came top of the uncited list on 2026-09-06 and had been read in July from
the Wayback Machine, its content sitting in traditions/environmental-history.md under a
source note that names no source id at all (f_5142). Reading it again was still worth it
-- it produced four things the July extraction had missed, and surfaced a duplicate pair
-- but treat a high uncited count as a place to look, never as a claim that nobody has.

EVERY FACT TAKEN FROM ONE OF THESE MUST CARRY THE YEAR-END MAPPING from
project-docs/annual-report-year-ends.md. An April, March or May year-end report describes
the PREVIOUS summer; a December one describes its own. Getting that wrong moves a season
by a year, silently, which is what f_5039 was about.

Usage: python3 scripts/reread/camp_coverage.py
"""
import json
import pathlib
import re

CAMPS = {
    "Camp Otoreke": ("otoreke", "wiki/site/camp-otoreke.md"),
    "Camp Perrot": ("perrot", "wiki/site/camp-perrot.md"),
    "Camp Becscies": (r"becs?c?ies", "wiki/site/camp-becsies.md"),
    "Camp Weredale": ("weredale", "wiki/connections/related-camps/camp-weredale.md"),
    "Kamp Kanawana": ("kan[ae]w[ae]n+a", "wiki/site/the-kanawana-site.md"),
    "Camp Thunderbird": ("thunderbird", "wiki/site/camp-thunderbird.md"),
}
REPORTS = sorted(pathlib.Path("sources/cache/ymca-montreal-fonds").glob("sgw-ymca-annual-report-*.txt"))


def main():
    srcs = json.load(open("sources/sources.json"))
    recs = srcs["sources"] if isinstance(srcs, dict) else srcs
    by_path = {r.get("cache_path"): r.get("source_id") for r in recs if r.get("cache_path")}

    print("HOW MUCH OF THE ANNUAL REPORTS HAS REACHED EACH CAMP'S ARTICLE\n")
    print("A mention is not a fact, and the count ranks where to look rather than saying")
    print("what is there. Read the module docstring, and the year-end mapping, first.\n")
    for camp, (pat, artpath) in sorted(CAMPS.items()):
        art = pathlib.Path(artpath)
        if not art.exists():
            print("%-18s ARTICLE MISSING: %s" % (camp, artpath))
            continue
        cited = set(re.findall(r"src_[a-z0-9_]+", art.read_text(encoding="utf-8")))
        wiki_cited = set()
        for f in pathlib.Path("wiki").rglob("*.md"):
            wiki_cited |= set(re.findall(r"src_[a-z0-9_]+", f.read_text(encoding="utf-8")))
        rx = re.compile(pat, re.I)
        rows = []
        for p in REPORTS:
            n = len(rx.findall(p.read_text(errors="replace")))
            if n:
                sid = by_path.get(str(p), "(unregistered)")
                rows.append((n, p.name, sid in cited, sid in wiki_cited))
        rows.sort(reverse=True)
        un = [r for r in rows if not r[3]]
        in_art = sum(1 for r in rows if r[2])
        print("%-18s %3d report(s) name it | %3d cited by its own article | %3d cited ANYWHERE in the wiki | %3d cited nowhere"
              % (camp, len(rows), in_art, len(rows) - len(un), len(un)))
        for n, f, _, _w in un[:8]:
            print("      %3d mentions  %s" % (n, f))
        if len(un) > 8:
            print("      ... and %d more uncited" % (len(un) - 8))
        print()


if __name__ == "__main__":
    main()
