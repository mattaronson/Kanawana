# p_218 VERIFY sweep — findings (2026-08-12)

**Scope:** all 28 articles stuck at `draft`, audited against the R3-verified bar
("every claim cited, dates checked against timeline, names checked against people index").
Five parallel read-only audit agents, one per cluster, plus a mechanical harness.

## Headline: p_218's own premise was wrong

The queue entry predicted VERIFY "should be fast per article" because these 28 were
WRITE-only syntheses of already-cited facts, with no new research. **The opposite is true.**
Synthesis is exactly what introduced the drift:

| Cluster | Articles | BLOCKING | MINOR |
|---|---|---|---|
| Two-Tier Era directors | 8 | 11 | 16 |
| Early/mid-era people | 7 | 8 | 18 |
| Notable alumni | 5 | 9 | 18 |
| Chronology eras | 5 | 12 | 15 |
| Programs/places/documents | 3 | 8 | 9 |
| **Total** | **28** | **48** | **76** |

**Zero of 28 articles pass clean.** One (`rob-braide.md`) required a privacy removal, already
applied and committed separately. This is a real result, not a bookkeeping artifact: the mechanical
harness found the articles almost spotless (all `^N` resolve, all `[src_]` resolve, 0 broken links),
which is precisely why the qualitative pass was necessary.

## The three drift signatures

Nearly every blocking finding is one of these, and all three are *specific to synthesis writing*:

1. **A number or qualifier lifted from the source article and re-attached to the wrong claim.**
   `between-centennials.md` took "within three years" — which the source attaches to the 1972
   all-female Voyageur trip — and re-attached it to the section restructuring, converting an
   explicitly *undocumented* date into a specific one. Also: "about 1950" moved off the
   tree-planting onto a directorship; the TELUS grant fused to the 2012 pavilion; 1994 relabelled
   "the camp's second Centennial."
2. **Citation markers pointing at whichever source was nearest, not the one carrying the claim.**
   `between-centennials.md` cites Peter Goddard's tenure to Concordia sub-series 12A, which holds
   nothing on him. `modern-era.md` cites the Grand Portage demolition and Clivus Multrum figures to
   the 2008 annual report, which supports none of it. `camp-pine-crest.md`'s single most important
   claim rests on a source it does not list at all.
3. **Documented uncertainty flattened into narrative continuity.** Garcia→Taylor presented as a
   clean handover when the index documents both an overlap and a *differently-named* successor
   (Kristen Whitelaw). Joanna Hoad's tenure — which the index flags as uncorroborated after two
   full research passes — restated as settled fact.

## BLOCKING findings by article

### Chronology (12 blocking) — weakest cluster
- **`modern-era.md:16`** — "closed overnight in 2021 … **then reopened in 2021**". Self-contradictory
  and false: `sean-day.md:44` documents a *second consecutive* closed season; the day-camp pivot went
  3 camps (2020) → 10 (2021). *The single most consequential fix in the sweep.*
- **`modern-era.md:8`** — "the camp's **second** Centennial (1994)". 1994 was Kanawana's first and only
  centennial. The phrase works in `timeline-overview.md` only because it sits in sequence after
  *Canada's* 1967 centennial; lifted out of that sequence it becomes a factual error.
- **`modern-era.md:8`** — "through **two pandemics'** worth of disruption". One pandemic, two closed seasons.
- **`modern-era.md:16`** — Garcia→Taylor false continuity (drift signature 3, above).
- **`modern-era.md:20`** — Grand Portage / Clivus Multrum / dry toilets all miscited to the 2008
  annual report; belong to the Clivus project page, Médiaterre 2009, and oral history.
- **`interwar-era.md:24`** — claims Charlton's 1943 manuscript "would corroborate and extend"
  Dawson's 1933 account. **Neither manuscript has ever been read by this project** (both are
  non-digitized, Box HA1881). No source can support this.
- **`interwar-era.md:16`** — incoherent inference: a 1923 brochure's silence cannot indicate the
  charter "postdates" a 1922 Council Ring. Source article reads it as "de-emphasized by 1923."
- **`postwar-gap.md:18`** — says Seaman moved to SGW faculty in 1963 "the same year he transitioned
  away from full-time camp directing"; `a-ross-seaman.md:22` says explicitly "**while still directing
  Kanawana**", and the same paragraph narrates an unbroken 1959–1967 directorship.
- **`postwar-gap.md` (whole)** — the **1963–1973 gap** documented at `directors-index.md:185` is
  surfaced nowhere: not in postwar-gap, not between-centennials, not the hub. The one genuine
  partition *gap*. (The index contradicts itself here, so this needs reconciliation, not insertion.)
- **`between-centennials.md:8`** — the "within three years" transposition (signature 1).
- **`between-centennials.md:22`** — Goddard miscited to Concordia 12A (signature 2).
- **`timeline-overview.md:23,57`** — 1980s row omits Bruce Netherwood (1988–1994, two seasons inside
  the decade) *and* claims the listed names are "the only documented directors" of it.

### Two-Tier Era directors (11 blocking)
- **Gary White tier conflation**, three articles + the index: `david-leduc.md:8` and
  `morgan-carter.md:8` credit White as Executive Director for years after his documented FY2001–2002
  tenure, contradicting **already-resolved conflict c_015**. `morgan-carter.md` contradicts *itself*
  (Overview says "under Gary White" for 2001–2003; line 12 says White had left by FY2002–2003).
  The honest answer for 2003–2004 appears to be "no Executive Director documented" — not a substitute name.
  **The same error is inherited in `directors-index.md:59`, which is E1-reviewed.**
- **`david-leduc.md:16`** — chronological impossibility: an Oxfam role (Mar 2000–Jun 2002) framed as
  "**After Kanawana**" when his directorship is 2004. Leftover from a superseded tenure estimate.
- **`morgan-carter.md:8`** — conflates Executive and on-site tiers into one succession line.
- **`morgan-carter.md:12`** — the 2003 plaque, the article's single most load-bearing corroboration,
  is uncited *and* absent from the source list.
- **`arleen-boyer.md:16`** — arithmetic: "five years after" should be three-to-four (tenure ended 2000;
  committee listing is FY2003–2004). The "five years" belongs to a different trace (2005 handbook).
- **`arleen-boyer.md:16`** — the 2005 Parent Handbook claim is uncited and its source is absent from
  the list, though `directors-index.md:295` carries it. Open Question 2 depends entirely on it.
- **`kate-taylor.md` / `nicolas-garcia.md`** — two people hold the single on-site Director role for
  2013–early 2014. Inherited from the index; **not resolvable from available sources** — needs a
  conflict record, not a guessed shortening of either range.
- **`kate-taylor.md:8`** — camp alias "Wawa" appears only in the uncited Overview.
- **`marie-pierre-lacasse.md:8`** — the 2007–2010 expeditions role and "13-year break" appear only in
  the uncited Overview; the body skips them entirely.

### Notable alumni (9 blocking)
- **`rob-braide.md:16-18`** — private-individual genealogy. **FIXED AND COMMITTED** (957862c).
- **`rob-braide.md:14`** vs **`centennial-1967.md:43`** — same 1967 trip, incompatible accounts
  (7 boys + 1 counsellor vs 6 boys + 2 counsellors; Saint-Sauveur→Ottawa vs Deep River→Britannia
  Beach) and internally self-contradictory in the same sentence. Knock-on: `centennial-1967.md:63`
  Open Question 1 is marked "confirmed dead end — who were the six boys and two counsellors" but
  `f_1825` now **names one of them**. That OQ is stale.
- **`rob-braide.md:8`** vs **`directors-index.md:169`** — conflicting job titles for a living person
  (GM, Standard Broadcasting vs President of Standard Broadcasting Corporation), two documented
  sources, no conflict record.
- **`sam-lazarus.md:18`** vs **`pip-alumni-award.md:64`** — SAM JAM totals: $260,000/70 children
  (CBC, 2015) vs $230,000/50 children ("17+ years", i.e. *later*). A lower figure at a later date;
  no KB fact supports the $230,000/50 pair.
- **`sam-lazarus.md:8,12`** — full name and exact birth/death dates are drawn from `f_0611`, the very
  fact the article's own research note declares unusable (mis-sourced to an unrelated 1913 Gazette
  piece), then attributed to sources that may not carry them. Right instinct, incomplete execution.
- **`sam-lazarus.md:16`** — book citation swapped to a 2014 article that cannot support it; the real
  source (Bookshop.org) was dropped in the split.
- **`james-orbinski.md`** — split integrity: `notable-alumni.md:50-54` still carries the **full
  biography**, never trimmed to a pointer, contradicting that file's own Revision History.
- **Folder placement, needs operator decision:** `chris-adam` (camp staff who built a camp program,
  plus a documented 1988–89 camp committee role — reads as core `people/`) and `sam-lazarus`
  (fails the "notable even if Kanawana never existed" test outright; his significance *is* the
  camp's own fund and SAM JAM). Agent explicitly did not move either.

### Early/mid-era people (8 blocking)
- **`ross-bannerman.md:8`** — "Camp Pascobac and Camp Stephens **in Manitoba**"; no KB fact locates
  Pascobac, and McEwen recruited Bannerman in Saint John, NB. The article's own body gets it right.
- **`ross-bannerman.md:16`** vs **`richard-patten.md:16`** — Bannerman "CEO of the Montreal YMCA in
  the late 1970s" vs Patten "Executive Director of the YMCA in Montreal (1976–79)". Plausibly the
  same office, same years, neither flagged, no conflict record. Bannerman's claim is also cited to a
  Concordia finding aid for a 1969 camp report.
- **`greig-macdiarmid.md:23`** — Open Question 2 says "no source before or after this window has been
  found"; **`f_1841` contradicts this** — the 1934 Annual Report names W.H. Spearman as director for
  the 1933 season, bracketing Macdiarmid's start to 1934–35. *Wider: `directors-index.md` has no
  W.H. Spearman row at all — a documented director missing from the people index.*
- **`rl-charlton.md:22`** — wholly uncited claim that Charlton is named in Joyce Oliver's
  "Book of Remembrance" project. `f_1913` names **D.A. Budge**, not Charlton, and says
  "Contents not yet read."
- **`rl-charlton.md:22`** — cited source contradicts the claim: article says sub-series 12L, cites a
  source (`f_1151`) that says 12A. Two KB facts disagree; the article silently picks one and cites
  the other.
- **`rl-charlton.md:16,28`** — "five-surface search" then enumerates four (twice). `f_1985` lists four.
- **`richard-patten.md:8,12`** — states as fact that an "Advance Guard '63" plaque names *this*
  Richard Patten. The source records only a "Rick Patten"; nothing in the KB links them, and
  `directors-index.md:157` independently records his camp years as **day camps**, not residential.
- **Cross-file:** `directors-index.md:144` and `postwar-gap.md:14` both say McEwen was "by then
  National Council Boys' Work Secretary" in 1951. Per the KB he held that role 1941–45 and was
  General Secretary, Saint John YMCA 1947–51. **Both cluster articles get it right; fix the two
  reference files.**

### Programs / places / documents (8 blocking)
- **`camp-pine-crest.md:8`** — "**is the direct origin**" of the L&V Games: uncited, and hardens
  `f_1299`'s documented "inspired by" into causation. Peer `lv-games.md` says "drew on". The
  supporting source (`src_ymca_kanawana_history`) is **not in this article's source list**.
  `quebec-camp-landscape.md:30,92` carries the same hardening; its L107 runs the *opposite* way,
  still asserting a reading `lv-games.md` formally retracted 2026-07-09.
- **`camp-pine-crest.md:18,20`** — three substantive claims uncited, two resting on sources absent
  from the list.
- **`camp-pine-crest.md:18`** — "three days rather than two" stated as settled; `lv-games.md:50`
  treats the modern format as an open question resting on "weak modern-format leads only".
- **`green-triangle.md:20`** vs **`:33`** — "**None of the 38 issues checked**" vs "the **three**
  issues examined so far". Neither is right: the source record shows **six** read in full.
- **`green-triangle.md:18`** — "Benny **Leshley**" vs `directors-index.md:124` "Benny **Lashley**",
  same source. The KB carries both spellings unflagged (`f_0086` / `f_0550`).
- **`cit-lit-program.md:8`** — "run **continuously** for over six decades"; the body claims only
  three and a half decades, and there is no CIT evidence between 1960 and 1975 (a 15-year hole).
- **`cit-lit-program.md:14`** — entire second body paragraph uncited.
- **`cit-lit-program.md:22`** — Trailblazers age 16–17 vs `section-names.md` age 16; and the two
  articles disagree on whether Trailblazers is the CIT or the LIT program. *cit-lit is correct on
  the age* (its source is titled "Trailblazers CIT (Ages 16-17)") — the error is in `section-names.md`.

## Defects found in already-E1-reviewed articles

The sweep was scoped to the 28 drafts, but repeatedly surfaced errors in their *reference* articles —
which are E1-reviewed, the top status tier. **E1-reviewed is therefore not error-free**, and these
were only found because something downstream leaned on them:
- `directors-index.md:59` — inherits the Gary White tier-conflation error.
- `directors-index.md:144` — McEwen's 1951 title wrong (see above).
- `directors-index.md:185` — 1963–1973 "gap" contradicts its own Camp Directors table.
- `directors-index.md` — no W.H. Spearman row despite `f_1841` documenting him for 1933.
- `directors-index.md:35,159` — Netherwood's title still the oral-history form, not the documented one.
- `pip-alumni-award.md:48` (and `f_1235`) — arithmetic: says "12 documented recipients through 2018",
  the table lists 11; 11+3=14 makes Orbinski the 15th, which is what everything else says.
- `pip-alumni-award.md:64` — SAM JAM totals (see above).
- `section-names.md:12,44` — Trailblazers age range.
- `quebec-camp-landscape.md:107` — stale, contradicts its own L30/L92 and a retracted reading.
- `centennial-1967.md:63` — Open Question 1 stale; `f_1825` names one of the participants.

## KB-level defects to fix at source (feeds p_220)
- **Duplicate source records** inflating counts and producing redundant markers: one YMCA-GTA blog
  post under **three** ids (`src_ymcagta_pine_crest_games`, `src_ymca_gta_blog_games`,
  `src_ymcagta_pinecrest_games`); one Orbinski press release under **three**; one Reader's Digest
  article under two; `src_wikipedia_john_cleghorn` and `src_myjewishlearning_lazarus` each listed twice
  within one article.
- `f_0086` / `f_0550` — Lashley/Leshley split, unflagged.
- `f_1968` — enumerates three items while claiming four.
- `f_0611` — mis-sourced to an unrelated 1913 Gazette article (already flagged in `sam-lazarus.md`).
- `f_1416` vs `f_0611` — Lazarus birth year 1979 vs 1978.
- `f_1866` — orphan fact (Chris Adam on the 1988–89 camp committee) that partly answers a live
  Open Question.

## Mechanical findings (see also scratchpad `mechanical-findings.md`)
- 9 articles have wrong "Sources: N" header counts. Convention confirmed empirically against the
  3 R3-verified articles (3/3), not assumed.
- 2 orphan Sources entries: `between-centennials` #7, `postwar-gap` #8 (a duplicate of #7).
- **18 of 25 draft Overviews assert dates with no citation at all**, against 15% for E1-reviewed —
  a systematic gap against "every claim cited", and the mechanical counterpart of the qualitative
  "uncited Overview" findings above.
- Name-variant scan across all 88 wiki files: **clean**. Every variant ("Arlene Boyle",
  "Johanna A.A. Hoade", "Nicholas Garcia") occurs only inside deliberate correction narratives.
  Independently corroborated by the directors agent.

## Method note
Two of my own mechanical checks produced false positives and were corrected rather than acted on:
comparing `sources_cited` **counts** (must be sets — numbered entries may repeat a source), and a
citation-propagation script that broke because house style places `^N` *after* the sentence period.
Any future mechanical citation analysis here must treat a trailing `^N` as belonging to the
preceding sentence.
