STRUCTURE AUDIT -- 1 article(s) with a broken skeleton

  traditions/canoe-trips.md
      - ORPHAN: 19 '###' subsection(s) before the first '## ': ['What a ten-day canoe trip cost in 1926', '1945 to 1948: eight trips down the North River, and a circuit to Kingston and back', '1968: the Bahamas, France and Belgium', '...']

---

## What the first run found and fixed (2026-09-06)

Eight articles had a broken skeleton. Seven were repaired the same day; the eighth
is `traditions/canoe-trips.md`, deferred to p_453 because reordering it is not
mechanical.

**`site/council-ring.md` was the worst.** Its `## Sources` sat in the MIDDLE of the
article, and seven body sections came after it -- the whole Council of Tribes
Ceremony, some three thousand words including the Seton source text, a benediction
with two versions, and a YMCA director's account of cutting the ceremony back.
Anyone reading that article to its Sources would have stopped there and concluded
it was a short piece about a construction chronology. Sources moved to the end.

`traditions/lv-games.md` had three subsections hanging off the title with no
parent, and a resolved-conflict note stranded after Sources. `traditions/
order-of-owens.md` had a documented Who's Who finding -- an Owens who was a
Kanawana director in 1965 -- filed as a subsection of Open Questions, where it
read as a question rather than as the corroboration it is. `traditions/
section-names.md` had one orphan subsection. `history/wartime-kanawana.md` had no
`*Last Updated:*` line at all.

Two apparent findings were the checker's fault, not the wiki's, and both were fixed
in the checker. A first version flagged apparatus sections following one another --
Open Questions, then Related Articles, then Sources -- which is the template's own
order, and reported **all 114 articles** as broken. And the missing-Sources check
fired on two pages that cite nothing and on the source index itself, where adding
an empty `## Sources` to satisfy a checker would have been worse than the thing it
was checking for.
