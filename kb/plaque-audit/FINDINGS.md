# p_291 — Plaque transcription audit: findings

All **151** images in `assets/images/plaques/` read against their KB facts.
Per-image records in `audit.jsonl`. **1,825 names** transcribed.

## Verdicts

| Verdict | Count | Meaning |
|---|---|---|
| PARTIAL | 83 | The fact under-records what the image shows |
| COMPLETE | 37 | Fact carries everything on the object |
| NO-NAMES | 13 | Object genuinely carries no roster; fact correct |
| ILLEGIBLE | 8 | Names present but not recoverable at this resolution |
| TRANSCRIBED | 6 | Read in full; fact text not compared line-by-line |
| UNREAD | 4 | No fact in the KB describes the object at all |

**Better than half the collection was under-recorded.** The worst ratios:
`staff-1997` 3 names of ~100 · `staff-1990` 5 of ~102 · `staff-2002` 6 of ~94 ·
Knights of Kanawana 3 of 29 · `staff-1979` 4 of 59 · `cit-1999-2` 5 of 25.

## Five objects with no fact at all

`cit-1999` (a second 1999 CIT board, distinct from f_1618's) ·
`junior-boys-councellors-2006` (painted over an earlier "Woodsmen 2006" sign) ·
`basin-trip-2010` · `dsc-0554` (fully legible, five names, undated but datable to 2002) ·
`dsc-0684` (effaced).

## Substantive findings beyond name counts

1. **John Cleghorn is on the Rangers 1956 plaque** — `f_1670` was COMPLETE and still
   failed, because nothing carried it to `john-cleghorn.md`, which asked as an
   [Important] open question which years he attended. **A correct fact can fail by
   never reaching the article that needs it.** Fixed.
2. **Dave Twynam is on the Staff of '79 plaque** — first-party confirmation of a Camp
   Director previously evidenced only by dated correspondence.
3. **The Knights of Kanawana** is a complete 29-person honour roll, 1980–2009, with
   citation and crest. No article; the Order of Owens has one on weaker evidence.
4. **"Wolf" is a real 2009 staff role** (Yak Trip and Talahassee boards), unknown here.
   **"May the Sanctum R.I.P."** records a camp structure that ended in 2007; `site/`
   has no Sanctum. **"The Suez Bridge"** is another unrecorded place-name.
5. **International staffing is documented.** The Pathfinder paddle lists six origins —
   Australia, England, Holland, Cape Breton, France, Virginia — and the 2009
   Talahassee board calls itself the "International Tent."
6. **`f_1663` says the 1994 Nature Trip board has no names.** It carries ~15 lines of
   effaced script. 1994 is the only year in the 1992–2001 run without a CIT plaque,
   making this the sole surviving roster from that season. **Top re-photography target.**
7. **Coeducation, in the campers' own words:** "The 1st Ladies of the Barracks" (2007),
   "To the women that filled the Lookout with love and friendship" (2008), and an
   all-female Voyageur crew in 2010 that the board does not remark on at all.
8. **Culture the roster facts dropped:** a Robert Frost epigraph (1984), thirteen
   catchphrases (1985), a dated setlist of pop covers (2006), Kanawoodstock across
   1993/95, 2000 and 2009, and a cabin-naming record (Zodiac, 2000).
9. **Raku was a dog** — the 1995 all-camp board is cut as a bone and painted with a paw.
10. **Cohort continuity runs throughout**, unrecorded: ≥12 of the 29 CITs of 1995 on the
    1997 staff plaque; 7 of the 2008 LITs as 2009 JCs; all 8 girls of one 2000 tent
    still at camp years later; the Tassés across 1963–1990.

## Errors found in existing facts

- **Three wrong attributions**, all among the undated `dsc-` files: `f_1629` puts the
  Pathfinder paddle's country column on the wrong board; `f_1627` cites `dsc-0559` as
  showing the bus plaque (it does not); `f_1667`/`f_1681` describe two faces of one
  birdhouse as separate objects, and the second calls it undated when the first has
  the year.
- **Name corrections:** Mia Dantono (not Mike Cantono) · Kertland (not Hertland) ·
  Tarczynski (not Tanczarski) · Ratchelous, Woshke · Demers (not Dennis) Stoddart ·
  Hassoun (not Hassan) · Wati (not Watt).
- **Role corrections:** Eric Bilodeau and D'Arcy are Trippers, not campers.

## Errors of mine, caught by later plaques

Recorded because the audit's value depends on them being visible: "Sassim" was
**Saddam** · "Waff" was **Watt** · a 1944 dating guess was **1999** · two boards I
called uncatalogued were objects the KB already had, seen obliquely · my Aurelie
Tanguy lead gained a better same-year competitor in Charles-Eric Tanguay · my
"Caroline Noble" reading on the Knights roll is unsettled against Caroline Poole.

## Method notes for anyone re-reading these boards

- **Alphabetical order is a tendency, not a rule.** Late additions get appended out of
  sequence at column feet. Ordering may *suggest* a faint name; it must never *exclude*
  one. (An earlier version of this task said the opposite and was wrong.)
- **Shape is evidence.** A bone with a paw print, a guitar pick, a birdhouse, a drum
  head, a route map, a moose antler — several objects carry their meaning in their form.
- **Check whether a central device is a divider or a spine.** The Roosties board splits
  given names left and surnames right; read as two lists it is nonsense.
- **Record what the paint says and what a person says in separate fields.**
- **"No names" and "names unreadable" are different claims.** The first closes a
  question; the second keeps it open.

## Re-photography priority

1. `nature-trip-1994` — the only 1994 roster in existence
2. `staff-2000` — ~60–70 names, half illegible
3. `cit-1999` — a whole uncatalogued board
4. `malibu-trip-2001` — blocked by conduit, not by wear; trivially fixable
5. `dsc-0684`, `voyageurs-1998-3` — likely past saving
