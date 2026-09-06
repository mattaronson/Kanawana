# Session handoff prompt — Camp Kanawana wiki

Written 2026-09-05 (evening), with PR #10 open and green. Copy everything below the
line into a new session.

---

You are continuing the Camp Kanawana research-to-wiki project at `/home/user/Kanawana`
(GitHub: `mattaronson/Kanawana`). Read `CLAUDE.md` first — it is long, it is the
operating contract, and it has been amended twice.

## Where things stand

`origin/main` is at **`c5cbdd6`**. **PR #10** (`claude/kanawana-research-continue-spy7u9`)
is open as a draft with **19 commits**, green on every commit, mergeable clean, no review
threads. Its 247k insertions are almost entirely five cached Internet Archive volumes;
the wiki and data changes are small.

**All six verify scripts pass.** Two changed today:

```
python3 scripts/verify/data_integrity.py      # blocking — now also asserts articles.json
                                              #   against its builder, and type-checks fact fields
python3 scripts/verify/verify_harness.py      # blocking (A1/A2 classes)
python3 scripts/verify/consistency.py         # blocking — now has a third rule class, SPAN
python3 scripts/verify/citation_aim.py        # BLOCKING as of this PR (was advisory)
python3 scripts/verify/staleness.py           # advisory
python3 scripts/verify/restricted_guard.py    # blocking
```

Totals: **4,827 facts** (KB v6.38) · **63 conflicts** (32 open) · **1,580 sources** ·
**106 articles** (50 E1-reviewed, 9 R3-verified, 44 draft, 3 stub) ·
**133 pending priorities** of 420.

`scripts/wiki/build_article_counts.py` is new. Run it after every article edit;
`data_integrity.py` fails if `wiki/articles.json` differs from what it produces.
Do not hand-edit `word_count`, `open_questions` or `article_count`.

## The rules that actually govern the work

Not style preferences. Each exists because it was violated and cost something. The first
five carried over; four more were earned today, all by me, all in this PR.

1. **A negative result from a tool is a fact about the tool, not about the world.**
   A 403, a blocked domain, an empty search — record as an ACCESS FAILURE with the
   untried routes named. Never as "does not exist." *Today: the Quebec business registry
   returns 403 for excessive use, and the Know History 403 turned out to be hiding a
   podcast rather than an unreachable document.*
2. **"X appears nowhere in this project" is one grep, and must never be written without
   running it.**
3. **Where a document is known only from an image, "the document does not say X" must be
   written as "the image does not show X."**
4. **Corrections go in place and visibly.** Superseded facts are prefixed
   `[SUPERSEDED <date>: …]` and kept, never deleted.
5. **Oral history yields to documents only where they DIRECTLY conflict.**
6. **Read the page image, not the OCR, when one letter carries the claim.** Twice today
   the OCR was wrong in a way that mattered: `Y.W.C.A.` where a project had assumed
   YMCA, and `GUSHING` for Cushing. The route: fetch the item's `_djvu.xml`, find the
   word's coordinates and leaf, then `archive.org/download/<id>/page/n<leaf>_w2560.jpg`
   (the `page/nN` index can sit one behind the djvu leaf number) or the IIIF API with
   `/max/0/default.jpg` — *not* `/full/`, which returns "Invalid size". DjVu
   y-coordinates count from the bottom.
7. **Search the KB before reading a source, not after.** I read Shorgan's April 1965
   article and extracted it as `f_4863`, hours after this project had already extracted
   the same article as `f_3146`–`f_3149`. The duplicate is kept and cross-linked. The KB
   is the index to the corpus.
8. **When you settle a date, redo the arithmetic that sat beside it.** Camp Stephens's
   closure moved to 1918, its run was correctly re-dated to 1919–2019, and the count in
   front of it stayed "about 102". It is 101. `consistency.py`'s new SPAN rule now checks
   `N seasons, YYYY–YYYY` against `end − start + 1` — seasons and summers only, never
   "years", which are elapsed durations and correct as written.
9. **A string-matching coverage sweep lies in two directions.** It scored "Anne I. Vail"
   at zero articles while the wiki is full of Nan Vail and Ann Vail; and it reported
   "Elsie Palter" absent from a paragraph naming her, because the line wrapped between
   her given name and her surname. Normalise whitespace and search name variants before
   concluding anyone is absent.

## What this session did

**Infrastructure.** `articles.json`'s three derived fields are generated and asserted
(p_417 — 50 of 104 records were stale). `citation_aim.py` is blocking (p_401 — four
findings cleared, and it has since caught three real regressions, all mine).
`consistency.py` gained the SPAN rule. `data_integrity.py` now type-checks fact fields,
after a stray comma made a claim a tuple that passed data_integrity and crashed three
other checks.

**Research closed.** p_405 (Ottawa 1893 is a *YWCA* minute; the North American Year Books
1893–97 record no camp for Ottawa *or* Montreal, so the null cuts both ways) · c_061
(Camp Stephens closed in **1918**) · p_408 (the Know History "chapter" is a podcast;
transcribed locally, silent on the L&V Games) · p_403 (**twenty-three attendance seasons
filled**, none from a new source — the camp's own directors' reports were here all along;
then the plaque corpus and the L&V trophy closed everything from 1976 on; **1911, 1914
and 1920 remain**) · p_368 (Seton's *Book of Woodcraft* read: the council-ring chant is an
Omaha prayer collected by Alice Fletcher, and Blackstock's Mazinaw carving is Seton's
sentence with the tenses changed) · p_327 · p_336 · p_370 (stale, not open) · p_402
(nine orphaned movement figures folded in) · p_412's tail · p_414 (MacSween stub) ·
p_374 and p_375 blocked with routes named.

**New articles:** `people/jared-macsween.md` (stub), `people/tony-shorgan.md` (draft).

**New conflict:** **c_063** — Camp Stephens's own 125th-anniversary chapel service dates
its first *boys'* camp to 1911 and calls the first twenty years an adult and family Bible
camp. If that holds, Kanawana's boys' camp is seventeen years older than Stephens's. It
is **not** written up as a finding: it is a dramatised script, it contradicts itself, and
the reading flatters this project. The Winnipeg association's own annual reports would
settle it; the Year Books cannot, and c_063's notes say so.

## Highest-value open work

Only a human can do these — surface them to Matt, don't grind:

- **p_416** — recover Carol Skinner's blog from the Internet Archive. Still the only
  first-person long-form source for any Kanawana person. Blocked here, not for a browser.
- **p_413** — one Pip recipient unaccounted for; ask the committee.
- **p_419** (new) — Ottawa 1893 now needs the Ottawa YMCA's 1890s annual reports or the
  YWCA minute book Fraser read in 1954. City of Ottawa Archives. A letter, not a search.
- **p_420** (new) — three annual-report volumes (published 1912, 1915, 1921) would close
  the last three attendance seasons. Add to the p_282 Concordia letter.
- **p_421** (new) — ask the Taylor Statten Camps whether Eastaugh's 1973 "complete and
  detailed description of the rituals" survives. It is the version Kanawana's leaders
  were taught, between Seton's book and the camp's own script.

Research an agent can still do — **the queue is not exhausted**: 45 pending items at
weight ≥7 were never opened this session, and several are workable from the cached
*Canadian Camping* run alone (p_351, p_377, p_378, p_395, p_326). Do not assume from a
handoff that the top of the queue is archive-blocked; open them and look.

## Open questions for Matt

Carried forward, still unanswered: whether the Pip-committee work belongs in
`people/matt-aronson.md`; whether there is other framed correspondence at camp; and
Alexandra Olshefsky's staff years.

## Posture

Matt supplies documents and first-hand testimony mid-thread, and they frequently overturn
things. Check what he says against the record, in both directions. And check your own
work the same way: four defects in this PR were mine, and all four were caught by looking
again rather than by a script noticing.
