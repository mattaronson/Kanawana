# Session handoff prompt — Camp Kanawana wiki

Written 2026-09-06 (night), with PR #10 open, green, and 88 commits ahead of `main`. Copy everything
below the line into a new session.

---

You are continuing the Camp Kanawana research-to-wiki project at `/home/user/Kanawana`
(GitHub: `mattaronson/Kanawana`). Read `CLAUDE.md` first — it is long, it is the operating contract,
and it has been amended twice.

## Where things stand

`origin/main` is at **`c5cbdd6`**. **PR #10** (`claude/kanawana-research-continue-spy7u9`) is open as
a draft, **88 commits** ahead, green on every commit, mergeable clean, no review threads. Most of the
diff is cached source material; the wiki and data changes are small.

**All seven verify scripts pass, plus one new advisory.**

```
python3 scripts/verify/data_integrity.py      # blocking — asserts generated files, type-checks fact
                                              #   fields, FAILS on a dangling source_id
python3 scripts/verify/verify_harness.py      # blocking (A1/A2 classes)
python3 scripts/verify/consistency.py         # blocking — SPAN rule
python3 scripts/verify/citation_aim.py        # BLOCKING
python3 scripts/verify/restricted_guard.py    # blocking
python3 scripts/verify/staleness.py           # advisory
python3 scripts/verify/footnote_labels.py     # advisory
python3 scripts/verify/oq_kb_cross.py         # advisory, NEW — see rule 20
```

Totals: **4,923 facts** (KB v6.96) · **65 conflicts** (34 open) · **1,639 sources** ·
**106 articles** (52 E1-reviewed, 8 R3-verified, 43 draft, 3 stub) · **118 pending priorities** of 431.

`scripts/wiki/build_article_counts.py` generates `word_count`, `open_questions` and `article_count`.
Run it after every article edit; `data_integrity.py` fails if `wiki/articles.json` differs from what
it produces. Do not hand-edit those three fields. **Do not run `scripts/verify/seed_read_state.py`.**

## The capability that matters most

`https://openlibrary.org/search/inside.json?q=<phrase>` full-text searches the Internet Archive book
corpus **including lending-restricted and print-disabled items**, unauthenticated. It returns the
item identifier, the scan leaf, and a highlighted window of about twelve words. Searching the last
four words of one window returns the next; a paragraph takes six to ten queries. **Sleep 15 seconds
between calls; on a non-JSON reply wait 45-60 and retry; numeric-heavy queries need `--max-time 170`
because the backend is slow on them, not because it is refusing.** The contract is at `f_4933`.

**Page images on lending-restricted items return HTTP 403 with an HTML body**, even with the item's
own details page sent as `Referer`. Keep that distinct from the missing-Referer trap, which returns a
43-byte transparent GIF under HTTP 200. One means "not licensed"; the other means "you forgot a
header". Unrestricted items can be downloaded whole:
`https://archive.org/download/<id>/<id>_djvu.txt`.

## The rules that actually govern the work

Twenty now. Each exists because it was violated and cost something. Fifteen carried over; five were
earned on 2026-09-06.

1. **A negative result from a tool is a fact about the tool, not about the world.** Record it as an
   ACCESS FAILURE with the untried routes named. Never as "does not exist."
2. **"X appears nowhere in this project" is one grep, and must never be written without running it.**
3. **Where a document is known only from an image, "the document does not say X" must be written as
   "the image does not show X."**
4. **Corrections go in place and visibly.** Superseded facts are prefixed `[SUPERSEDED <date>: …]`
   and kept, never deleted.
5. **Oral history yields to documents only where they DIRECTLY conflict.**
6. **Read the page image, not the OCR, when one letter carries the claim.**
7. **Search the KB before reading a source** — and searching does not help when the KB does not know
   the name to search for.
8. **When you settle a date, redo the arithmetic that sat beside it — and check the other articles.**
9. **Locate by structure, not by first string match.**
10. **A string-matching coverage sweep lies in two directions.**
11. **Test a capability before spending a session on what it promises** — and **re-test a capability
    before trusting a dead end.**
12. **A silent failure that returns HTTP 200 is the worst kind.**
13. **When a priority's own closing sentence turns out to be wrong, correct the priority.**
14. **The pending count is not the work remaining.**
15. **Use the knowledge base as a test of the derived indexes, not only as a consumer of them.**
16. **(New) An enumeration is only as wide as the string it was run on.** p_430's item list was built
    from a bare `"Kanawana"` query — seventy-six items — by someone who had just learned that
    `"Camp Kanawana"` returns eight. `"Kamp Kanawana"` is a third string, returns thirteen, and **two
    of them are in neither list**: the Dictionary of Literary Biography's entry on Stuart McLean, and
    the American Camp Association's own textbook. The camp has spelled its name two ways for a
    century. Run both. (`"Kanawanna"`, `"Lac Kanawana"`, `"Lake Kanawana"` and `"Kanawana, Que"` are
    now swept and are nulls; do not re-run them.)
17. **(New) An index entry means what its heading says it means.** "Kanawana, PQ, see
    St-Sauveur-des-Monts, PQ" is an ordinary gazetteer cross-reference until you recover the heading
    — "**Post Offices in Canada** (Sub post offices and closed and renamed post offices appear in
    italics…)" — at which point it dates the end of the camp's post office. Wording, alphabetical
    neighbours and service codes look identical either way. The heading is not context for the entry;
    it is the entry's predicate, and a snippet search hands you the subject without it every time.
18. **(New) Do not read across a scrambled row. Query the field whose value is unique in the
    corpus.** Four column ambiguities have now been settled this way: Kanawyer, California in the UPU
    postal list; Lac Bâtiment in the Matawinie lake cluster; **D-U-N-S 20-765-0813** in the credit
    directories (which proved "Emp Here 55" belongs to the association and not the camp — a very
    attractive wrong number, since David Leduc's own account gives 75 staff); and **three telephone
    numbers** in a 1991 ski guide, where the straight reading puts Kanawana at Mont-Laurier. It took
    three controls there, because one would have been a coincidence.
19. **(New) A source in `sources.json` is not a source that has been read.** Janet Torge's *Dear Sam*
    sat in the citation slot of a live article for five months as a bookseller's listing while the
    same article asked, three screens further down, a question the book answers. `read_state` was
    honest — "derived:cited-by-fact" is what it said — and nobody looked.
20. **(New) Use the knowledge base as a test of the ARTICLES, and now do it with a script.**
    `canadian-camping-movement.md`'s Open Question 4 said "no named individual confirmed on both
    sides" of the Kanawana-to-Nominingue connection. `f_2641` and `f_3039` had made that join weeks
    earlier and **say so in their own text**. The question was not unanswered; it was unread.
    `scripts/verify/oq_kb_cross.py` is that check made routine — and run with
    `--since <fact number>` at the end of a research burst, it reports only what your own new facts
    may have answered. It caught a third case on its first run.

## What this session did (2026-09-06, night)

**p_430 is nearly finished.** Groups 1, 2, 3, 4 and 5 are complete and two of group 6's three
memoirs are read. What it produced:

- **The credit directories, 1993-2001** (f_4951) — Kamp Kanawana as a division of the YMCA de
  Montréal, and the address bracket that dates the move from 1441 to 1435 rue Drummond.
- **The Dictionary of Literary Biography** on Stuart McLean (f_4949) — July 2005 for the *Vinyl Cafe*
  show recorded at camp, and an **unpublished 19 May 2010 interview** held by its author David C.
  Greer, now an open question in `stuart-mclean.md`.
- **The American Camp Association's textbook** calling Kanawana Canada's first organizational camp
  (f_4950) — recorded, and argued down to what it is worth in the same paragraph.
- **A last-day naked swim called "the camp ritual"** (f_4952), from an American family's memoir of
  the late 1920s, and absent from every camp publication this project has read. *The absence of a
  tradition from the camp's own publications is not evidence it did not exist.*
- **Sam Lazarus a camper from 1986** (f_4953), from his mother's book.
- **The post office ends between about 1955 and the mid-1960s** (f_4954, and p_428 half-answered).
- **The Kanawana Outing Club run from a house in Châteauguay** in 1977 (f_4955), and the 1991 guide's
  scrambled row decoded (f_4956).
- **The Petit Futé's 2011-12 entry** (f_4957) — the fullest French description of the programme this
  project holds, and a date for the *Aventurier Extrême* programme.
- **Three of the directors index's men given day jobs** — F. H. Spinney a Montreal school principal
  who wrote a national column on teaching (f_4958); Hay Finlay McGill's gymnastics and soccer coach
  and co-founder of Camp Nominingue (f_4959); C. B. Powter a physical-training master, on a Montreal
  committee in 1912 with D. J. Evans, Kanawana's 1913 director (f_4960, f_4961). **The men the
  Montreal YMCA put in charge of its camps were schoolmasters** — which is also a search heuristic:
  for an unidentified early camp name, try school prospectuses, education journals and university
  athletic histories, not YMCA literature, which is already read to the end.
- **The 1898 camp leadership**, six named men, added to `directors-index.md` from facts that had been
  in the KB for a day (f_4908, f_4911, f_4913).

## Highest-value open work

**Agent-doable.** `p_430`'s remainder: group 6's last two memoirs, `atlasroutierduqu0000mapa`, and
**the name sweep proper — about fifty names still to run**, logged at
`sources/cache/name-sweep/2026-09-06-directors-index-name-sweep.txt`, which is the authoritative
record of what has been swept. Also **p_432** (the rest of *The School*'s run, 1912-1935, covering
every year of Spinney's camp service), **p_431** (was Kanawana a founding member of the ACQ?),
**p_426** (the rest of Fong's McConnell biography), **p_429** (the unnamed director in *Who's Who in
Canada 1965*), and the Henry Foss Hall lead inside p_430.

**Only a human can do these.** `p_422` the letter to the Commission de toponymie · `p_424` which
cache copy is canonical · `p_416` Carol Skinner's blog · `p_413` the Pip committee's list · `p_419`
Ottawa archives · `p_420` three annual-report volumes · `p_421` the Taylor Statten ceremony document
· `p_404` the Pine Crest history · `p_221`, which needs its scope re-confirmed. **`p_428`'s
remainder is now one query** in Library and Archives Canada's Post Offices and Postmasters database
— the exact closing date, the postmaster, and whether the office served the camp or a wider
settlement. LAC refuses this environment at the gateway. The same is true of **LAC fonds MG 28 (I
280)**, whose provenance is given as Johnston W. Abraham of DeWittville, Que. — Kanawana's Business
Manager from about 1914, if it is the same man.

## Open questions for Matt

Carried forward: whether the Pip-committee work belongs in `people/matt-aronson.md`; whether there is
other framed correspondence at camp; Alexandra Olshefsky's staff years. New: **did Kanawana ever run
a session for diabetic children?** And: **is the "Sam L" on the 2003 Junior Boys counsellors board
Sam Lazarus?** The dates fit and the board gives only an initial.

## Posture

Matt supplies documents and first-hand testimony mid-thread, and they frequently overturn things.
Check what he says against the record, in both directions. And check your own work the same way. Of
what this session fixed, the two best finds — Hay Finlay and the 1898 camp leadership — were **not
new research at all**. They were this project's own knowledge base, unread. Looking again is the
method, and it is now partly automated.
