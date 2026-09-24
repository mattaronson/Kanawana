# Session handoff prompt — Camp Kanawana wiki

Written 2026-09-06 (evening), with PR #10 open, green, and 142 commits deep. Copy everything below
the line into a new session.

---

You are continuing the Camp Kanawana research-to-wiki project at `/home/user/Kanawana`
(GitHub: `mattaronson/Kanawana`). Read `CLAUDE.md` first — it is long, it is the operating
contract, and it has been amended twice.

## Where things stand

`origin/main` is at **`c5cbdd6`**. **PR #10** (`claude/kanawana-research-continue-spy7u9`) is open as a
draft with **142 commits**, green on every commit, mergeable clean, no review threads. Most of the diff
is cached source material; the wiki and data changes are small.

**All seven verify scripts pass.**

```
python3 scripts/verify/data_integrity.py      # blocking — asserts generated files, type-checks fact
                                              #   fields, FAILS on a dangling source_id
python3 scripts/verify/verify_harness.py      # blocking (A1/A2 classes)
python3 scripts/verify/consistency.py         # blocking — SPAN rule
python3 scripts/verify/citation_aim.py        # BLOCKING
python3 scripts/verify/staleness.py           # advisory
python3 scripts/verify/restricted_guard.py    # blocking
python3 scripts/verify/footnote_labels.py     # advisory
```

Totals: **4,905 facts** (KB v6.78) · **64 conflicts** (33 open) · **1,619 sources** ·
**106 articles** (52 E1-reviewed, 8 R3-verified, 43 draft, 3 stub) · **116 pending priorities** of 429.

Run `scripts/wiki/build_article_counts.py` after every article edit, and
`scripts/plaque/build_index.py` then `build_table.py` after touching the plaque alias list.
`data_integrity.py` fails if either output differs from its builder. Do not hand-edit those outputs.
Do not run `scripts/verify/seed_read_state.py`.

## The capability that matters most

**`https://openlibrary.org/search/inside.json?q=<phrase>` full-text searches the Internet Archive's
book corpus, including lending-restricted and print-disabled books, unauthenticated.** It returns the
item identifier, the scan leaf, and a highlighted window of about a dozen words. **Overlapping phrase
queries walk the text outwards** — search the last four words of a window and the next window comes
back; a paragraph takes six to ten queries. Sleep ~2s between calls; a non-JSON reply is a rate limit,
not an absence. The full contract, and the four IA routes that still fail, are at **`f_4933`**.

This closed a dead end this project had recorded as confirmed on 2026-07-09 and believed for fourteen
months. In one session it produced: the Lake Wilson renaming from outside the institution and dated to
1912 (`f_4934`); Roy Locke's obituary, which settled an identification this wiki had explicitly declined
(`f_4935`); Kanawana as a Dominion summer post office from 1915 to about 1955 (`f_4936`); diabetic
children at the camp (`f_4938`); a camper's letters home in the 1950s (`f_4937`); Stuart McLean's own
published prose about the camp (`f_4941`); the Outing Club in a 1976 city guidebook (`f_4942`); and
Harold Cross's 1936 office (`f_4943`).

**The two queries that found the most were not about Kanawana.** "Kanawana" + "Sir George Williams"
produced both McLean and the Outing Club; a query on Harold C. Cross produced the 1936 yearbook.
**`p_430`** is the standing priority for the name sweep, and it is the highest-value agent-doable item
in the queue.

Three limits, learned by hitting them: OCR breakage defeats phrase matching (`"director of Camp
Kanawana"` returns nothing because the scan reads `"di¬ rector"`); a query pairing a term with a book's
own title is not a test of the book; and every reconstruction is a reconstruction — cache it with the
queries that produced it and a statement of what was **not** recovered, as the files in
`sources/cache/openlibrary-search-inside/` do.

## The rules that actually govern the work

Not style preferences. Each exists because it was violated and cost something. Thirteen carried over;
two more were earned on 2026-09-06.

1. **A negative result from a tool is a fact about the tool, not about the world.** Record it as an
   ACCESS FAILURE with the untried routes named. Never as "does not exist."
2. **"X appears nowhere in this project" is one grep, and must never be written without running it.**
3. **Where a document is known only from an image, "the document does not say X" must be written as
   "the image does not show X."** The search-inside corollary: where a book is known only from
   snippets, say so in the article, not only in the cache file.
4. **Corrections go in place and visibly.** Superseded facts are prefixed `[SUPERSEDED <date>: …]` and
   kept. A fact that is accurate but was misread gets `[NOTE …]`; one that was short rather than wrong
   gets extended in place, as `f_4936` was.
5. **Oral history yields to documents only where they DIRECTLY conflict.**
6. **Read the page image, not the OCR, when one letter carries the claim.**
7. **Search the KB before reading a source** — and the harder form: searching the KB does not help when
   the KB does not know the name to search for.
8. **When you settle a date, redo the arithmetic that sat beside it — and check the other articles.**
   `j-w-mcconnell.md` was still calling the Lake Wilson naming unverified four days after
   `lake-wilson.md` recorded the answer.
9. **Locate by structure, not by first string match.**
10. **A string-matching coverage sweep lies in two directions.** Proved again: a sweep built to find
    stale priorities scored archive-request items highest and missed the genuinely stale one.
11. **Test a capability before spending a session on what it promises** — *and its other half, earned
    2026-09-06: **re-test a capability before trusting a dead end.***
12. **A silent failure that returns HTTP 200 is the worst kind.**
13. **When a priority's own closing sentence turns out to be wrong, correct the priority.**
14. **(New) The pending count is not the work remaining.** Three of the first four priorities opened
    this session were already done and never marked. Check the article before working the priority.
15. **(New) Use the knowledge base as a test of the derived indexes, not only as a consumer of them.**
    `f_2340` said seven of the 2008 LITs became JCs; the plaque index could show six; the difference
    was a real split, one person in two rows, and that is the seventh such split found.

## What this session did (2026-09-06, second half)

**Priorities closed:** p_328 (Seaman's 1962-63 secretaryship was **national**, not provincial) ·
p_357 (the 1971 regional restructuring — and the CCA's national office turns out to be two years older
than the association's own 1985 account of itself, raised as **c_064**) · p_387 (the three structural
breaks of 1974-76, and the discovery that the January Directory Issue — this project's source for
Kanawana's 1975 and 1976 particulars — exists *because* of the 1974 financial crisis) · p_386 (the 1976
YMCA-to-RLSS lifesaving changeover) · p_367 (the movement's "Threat to Camping" frame, and the 1972
unemployment-insurance change that raised the camp's payroll cost by an amount set in Ottawa) · p_297
(cohorts, not careers) · p_427 (all six books that name Kanawana) · p_342 and p_381 and p_385, all
already done and unmarked · p_349 and p_428 partially.

**Conflicts:** `c_006` resolved (Lake Desjardins is real, and is Lake Wilson before 1912).
`c_064` raised (the national office's own dates).

**New priorities:** `p_426` read the rest of Fong · `p_427` (closed same day) · `p_428` the post
office's exact dates, which need Library and Archives Canada · `p_429` the unnamed Kanawana director in
*Who's Who in Canada 1965* · **`p_430` the name sweep, which is the one to pick up.**

## Highest-value open work

Only a human can do these — surface them, don't grind:

- **p_422** the letter to the Commission de toponymie · **p_424** which cache copy is canonical ·
  **p_416** Carol Skinner's blog · **p_413** the Pip committee's list · **p_419** Ottawa archives ·
  **p_420** three annual-report volumes · **p_421** the Taylor Statten ceremony document · **p_404**
  the Pine Crest history · **p_221**, which needs its scope re-confirmed before fourteen plaque-only
  stubs are rewritten, and is not an agent's call.
- **p_282**, the standing Concordia letter, now carries seven requests.

Research an agent can do: **p_430** first, then `p_426`, then the ordinary queue. **Do not read the
pending count as work remaining** — see rule 14.

## Open questions for Matt

Carried forward, still unanswered: whether the Pip-committee work belongs in `people/matt-aronson.md`;
whether there is other framed correspondence at camp; and Alexandra Olshefsky's staff years.

**New, and worth asking:** did Kanawana ever run a session for **diabetic children**? A Montreal
memoir says a Knights of Pythias lodge paid for "diabetic children from Camp Kanawana" at a December
party, and nothing in this project's own records mentions them (`f_4938`).

## Posture

Matt supplies documents and first-hand testimony mid-thread, and they frequently overturn things. Check
what he says against the record, in both directions. And check your own work the same way: of the
defects fixed on 2026-09-06, the largest was a dead end this project had written down as final, and the
second largest was an article that had not noticed its own project answering its own question four days
earlier.
