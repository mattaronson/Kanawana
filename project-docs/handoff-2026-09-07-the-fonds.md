# Handoff, 2026-09-07: a surface nobody had opened

*Written after thirty-four commits between roughly 23:00 and 01:30 UTC. Everything below is in
`kb/facts.json` and in articles; this file exists so the next session does not have to reconstruct
the shape of it from commit messages.*

## The one thing to read first

**The Montreal YMCA fonds on the Internet Archive is a collection, and it holds 1,120 items.** This
project had read or cited 653 of them. Of the 467 it had not, **435 are photographs and 32 are
texts** — and those 32 are now read-and-empty rather than unread. The whole text side of that fonds
is finished. See `p_462` and the finding aid at
`sources/cache/ymca-montreal-fonds/2026-09-07-ia-fonds-enumeration-what-is-unread.txt`, which
carries the item lists, the corrections, and the traps.

**Three traps in it, each of which cost something tonight:**

1. **Use the collection, not a phrase.** `q="ymca of montreal"` returns 942 items. `q=collection:ymca-montreal-fonds` returns 1,120. The phrase misses 181, mostly news releases catalogued by their own headline (f_5259).
2. **The plain-text file is named after the item's TITLE, not its identifier.** `<identifier>_djvu.txt` returns HTTP 404 with a 146-byte body. Read the file list from `archive.org/metadata/<identifier>` (f_5243).
3. **A catalogue year is worthless, and I proved it again.** `the-quarterly-reporter-1856-01` is a **June 1944** periodical reproducing an **1858** front page published from **Cincinnati**. I had called it "the association's earliest periodical, 1856" on the catalogue's word, in the same week this project's own Year Book inventory said never to do that (f_5243, corrected).

## And the limit that qualifies every enumeration this project has run

**`advancedsearch.php` is metadata-only and says so.** `sin=TXT` returns
`UNSUPPORTED_VALUE`. So "the Internet Archive has been enumerated for Kanawana" means **its
catalogue has**. A document that names the camp only in its text is invisible to it (f_5260).

**And the one full-text route that works here does not reach these items.** Open Library's
`search/inside.json` indexes the Archive's **book** corpus and nothing else. Tested with a control:
a distinctive phrase from *A History of Kamp Kanawana 1935* — an Internet Archive item — returns
**zero**, while an ordinary phrase returns nineteen book hits in the same minute; "the Green
Triangle" returns 2,118 hits and not one is a Green Triangle issue (f_5261).

**The consequence has a name: `p_463`.** 341 issues of *The Georgian* and the *McGill Daily* run sit
on the Archive, `sgw-concordia-connection.md` has asked since July whether either covered the camp,
and neither can be searched from here. It is item 10 in `one-afternoon-with-a-browser.md`.

## What the fonds gave, in order of weight

**The Canadian Camping Association did not exist in April 1936.** The Montreal *News Bulletin* of
May 1936 reports the Institute for Camp Leaders — 200 leaders at Toronto Central, 4-5 April, under
Hendry, Blatz, Edwards and Statten — whose stated outcome was a committee under Statten "to make
plans for **another gathering at which organization of a Canadian Camping Association might be
definitely considered**." Every other source in `association-founding-dates.md` is 1980s
recollection. It explains the 1936 date without endorsing it, reconciles the association's "fifty
years in 1986" with Adele Ebbs's 1938, and corroborates her supper club from outside her memory.
**`c_029` narrowed, not closed** (f_5247).

**Kanawana's own association gave Canadian primacy to Nova Scotia in 1944** — "the first organized
camp in Canada was conducted in 1889 at Chance Harbour" — forty-five years before the 1989
concession the wiki already had, and without its hedge (f_5249).

**"Camps would then be laboratories for the training of leaders in boys' work"** — the national
Boys' Work Committee, January 1931, thirty-four years before Kanawana ran one. An antecedent, not a
cause (f_5250).

**They ran Planned Group Development on the staff in 1959**, a year before the camper-facing
tent-group programme this KB dates to 1960. Two applications of one name, not a contradiction
(f_5256).

**Also:** Montreal Central's **indoor camps** for the boys who could not leave the city, the
national example in 1936 (f_5248); a 1932 camp-leader syllabus with "Indian Lore — simple Indian
ceremonies, making head bands, Indian dances" in the practicum, which is the transmission mechanism
this wiki had only as a lineage of individuals (f_5251); **48 residence campsites nationally in
1964**, giving `p_406` two comparable points at last (f_5252); the **Expo 67** explanation for a
1967 attendance dip the series had recorded without a reason (f_5253); the June 1946 statement of
what camping is for (f_5254); **F. William Halliday** from Calgary in 1962 (f_5245); "So-Ed Youth
Cultural Exchange, Otoreke", July 1967 (f_5246); and the **1874** annual report, where the
association's boys' work is a Friday prayer meeting that "commenced with a few school boys", with
Budge as secretary and a Cushing on the board (f_5255).

## Two corrections of mine besides the 1856 one

- I dated 48 campsites to **1965**; the same figures are printed for **1964** with a comparison the later printing drops. The camp numbers repeat across two years while the swimming numbers do not, so they are firm for 1964 and provisional for 1965 (f_5252, corrected in place).
- An orphan-label counter written with an **unescaped caret** made `^8ac` a start-of-line anchor and returned zero for every label. Acting on it would have deleted nine still-cited source entries. **A measurement that returns all zeros deserves one impossible case checked against it** (f_5235).

## Rules this session would add

**29. Enumerate the collection, not a phrase.** A denominator built from a phrase search is not a denominator.
**30. Say which layer you enumerated.** Catalogue and contents are different things, and "we have searched the Internet Archive" is false if you searched its metadata.
**31. Control every null that a broken endpoint could explain.** The Open Library result was worth having only because an ordinary phrase came back with nineteen hits in the same minute.
**32. After a spinout, grep the CHILD for pointing phrases** — "recorded above", "from this issue", "this article". Three broke tonight and nothing else would have caught them.

## Where things stand

`p_452` had three more cuts — `cca-director-certification`, `french-language-camping-national`,
`movement-archive-turn` — and the movement article is **17,889 words from 36,649**. `p_462`'s text
side is closed and its image half is narrowed to **fifty-nine title-suggestive candidates** that need
eyes. New: `p_458` (a 1986 ACQ visitation report should exist), **`p_459`** (every camp in Canada
was asked *in writing* to write its own history in 1985 and again in 1986 — did Kanawana?), `p_460`,
`p_461`, `p_462`, `p_463`.

**For a person:** `c_067` and `c_068` still need a decision. `c_068` is Arthur Ney's Otoreke
photograph, whose "1947" cannot be right because he reached Canada in 1948; only the book's photo
insert settles it.
