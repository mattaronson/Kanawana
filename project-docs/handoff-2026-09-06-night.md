# Session handoff prompt — Camp Kanawana wiki

Written 2026-09-06 (night), revised the same night, with PR #10 open, green, and 93 commits ahead of `main`. Copy everything
below the line into a new session.

---

You are continuing the Camp Kanawana research-to-wiki project at `/home/user/Kanawana`
(GitHub: `mattaronson/Kanawana`). Read `CLAUDE.md` first — it is long, it is the operating contract,
and it has been amended twice.

## Where things stand

`origin/main` is at **`c5cbdd6`**. **PR #10** (`claude/kanawana-research-continue-spy7u9`) is open as
a draft, **93 commits** ahead, green on every commit, mergeable clean, no review threads. Most of the
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

Totals: **4,928 facts** (KB v6.99) · **65 conflicts** (34 open) · **1,642 sources** ·
**106 articles** (52 E1-reviewed, 8 R3-verified, 43 draft, 3 stub) · **119 pending priorities** of 432.

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

Twenty-one now. Each exists because it was violated and cost something. Fifteen carried over; six
were earned on 2026-09-06.

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

21. **(New) A source marked READ is read FOR SOMETHING.** Five volumes of the *YMCA Year Book and
    Official Roster* — 1893 to 1897, the camp's founding years — were downloaded, cached in this
    repo and marked `read_state: read` on 2026-09-05. Their basis line is honest and specific: the
    provincial narrative reports were read, and the volumes were searched for "camp", "tent" and
    "Ottawa". **None of those strings reaches a line that reads "Phys. Director, W. H. Ball, Jr."**
    The Montreal association's complete founding-era staff sat unread in a file marked read for a
    day. `read_state` records what was read; nothing records the question that had not been asked
    yet. **A cache of read files is not a cache of exhausted files** — so before searching the world
    for a name, grep the cache for it.
    *And the failure that produced this rule was mine and worse than that:* I wrote that the series
    was "unknown to this project" in two facts, a priority, a cache file, an article and a commit
    message, without running the one grep rule 2 requires. All of it is corrected in place.

## The capability that opened this evening

**The `YMCA Year Book and Official Roster` series, and it is on the Internet Archive unrestricted.**
Annual, continent-wide, published by Association Press. For every YMCA in the United States and
Canada it prints **the complete named paid staff, branch by branch**, and an **Alphabetical List of
Employed Officers** giving every man's post and, by its own printed legend, **his year of entry into
Association work**.

Nineteen items, enumerated via `archive.org/services/search/v1/scrape?q=identifier:ymcayearbook*`
and written into **p_433**. The catalogue's `year` field is **wrong** — it reads 1890 for all ten
University of Toronto scans; the year is in the identifier and should be confirmed inside the volume.

Read so far: **1893-97** (already in this repo; rosters read 2026-09-06, f_4966) and **1921**
(f_4964, f_4965). Unread: 1891, 1892, **1906, 1907, 1908**, 1922, four Google scans, and 1936.
**Take 1906-1908 next** — they would name W. H. Ball Jr.'s successor as Montreal's Physical Director
after his 1901/02 departure, and they sit either side of the camp's move to Saint-Sauveur.

**Know the limit before starting.** "Kanawana" occurs zero times in the 1921 volume, and so do
"summer camp" and "boys' camp". The series rosters associations and their staff, not their
programmes. **It will never name the camp. It names the men**, which is the thing missing for the
camp's first forty years. And the men it does *not* name are informative too: Spinney, Powter,
Ereaux, Charlton and Owens are absent from the 1921 employed-officers list, consistent with the
camp's educational and section staff being schoolmasters and seasonal hires rather than association
secretaries.

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
- **The founding-era staff of the YMCA of Montreal, 1893-1897, year by year** (f_4966) — including
  "**W. H. Ball, Jr.**" in all five volumes, which gives the camp's founder a father of the same name
  and `billy-ball.md` the first genealogical handle it has ever had; **W. F. Chapman** as Assistant
  Secretary for four years before the 1898 junior camp; and **C. B. Powter** as Ball's Assistant
  Physical Director from 1896, closing a career built from four sources in one day.
- **Harold C. Cross documented as Boys' Work Secretary at Victoria, B.C.**, where the article said
  "likely", and his entry into YMCA work dated to **1912**, seven years earlier than anything held
  here — which opens a new question: where was he from 1912 to 1919? (f_4965)
- **Henry Foss Hall's *The Georgian Spirit* closed as a null.** Six pairings return zero, with a
  control pairing proving the AND works. The Montreal YMCA's own historian supplied the research for
  Sir George Williams University's official history and the camp is nowhere in it.
- **`scripts/verify/oq_kb_cross.py`**, and it caught three real cases — one from weeks ago, one from
  the previous day, and two of this session's own omissions when run with `--since`.

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

## Three more rules, from the morning of 2026-09-06

**22. A multi-word grep that returns zero may be a fact about the whitespace.** These scans' OCR
routinely puts two or more spaces between words. `FREDERICK H. SPINNEY` with single spaces returns
ZERO across ten volumes of *The School*; the double-spaced form returns fourteen. This project
recorded "his first name is not in any source found" for a day on the strength of that query, in a
KB fact, an article and a cache file. Match on the surname alone and read the context, or put
`[[:space:]]\+` between the parts. Never grep a multi-word name with single spaces and then write
the zero down as a fact about the world.

**23. A source searched in one section is searched in one section.** The YMCA *Year Book* lists the
same staff twice, in an alphabetical list of paid officers and in a branch directory by city. The
1900 volume's alphabetical list is OCR-ruined; its branch directory is fine. Searching the first,
finding it unreadable, and writing "the 1900 roster cannot be read" put a false access failure into
a fact, a source record, a cache file, two articles and a priority — all committed, all corrected
within the hour. This is rule 21's twin: rule 21 says a source marked READ was read for something,
and this one says the same about a source marked UNREADABLE. Before recording that a document does
not yield, ask what *part* of it you actually looked at.

**24. An endpoint that returns results may be returning someone else's query.**
`archive.org/services/search/v1/scrape` was observed returning the result set of a *previous* query
while reporting it as the answer to the current one — eleven volumes of *The School* came back for
`identifier:ymcayearbookoffi*`, and for a quoted query naming a single known identifier. Adding
`year` to its `fields` list returns items unrelated to the query outright. A failure announces
itself; a stale success does not. Use
`advancedsearch.php?q=...&fl[]=identifier&fl[]=title&rows=N&page=1&output=json` — the `output=json`
is required, and omitting it produces an HTML page that looks like the endpoint refusing JSON. See
f_4978. And keep a control in every enumeration session: query something whose answer you already
know, and check that you get it.

## Two more, from later the same morning

**25. A catalogue year is worthless, a title page beats it, and a volume's own contents beat its
title page's OCR.** Three terms, in that order. The Internet Archive's `year` field for the YMCA
*Year Book* is wrong by two years on one item and names only the first of five bound volumes on
another, so title pages were made the authority — and then a title page reading "FOR THE YEAR
1898" turned out to be the 1893 volume, because these scans confuse 3 and 8 (the same OCR renders
F. S. Morrison's year of entry, 93, as "SS"). Its contents said 1892 and early 1893 throughout.
An hour's work, a fact, a cache file, two articles and a commit were built on the misread digit,
including a manufactured "tension" against an existing fact. **Where two items hold the same year,
read both — their disagreement is what exposes this.** And when a correction lands, check whether
anything else was read the same way: the Archibald McKellar identification came off a different
scan's "1898" volume and had to be re-verified before the correction could be written. It held.

**26. Five errors in one morning, all mine, none caught by a verify script.** Worth stating as a
rule because the pattern is one thing, not five: *a query that fails is not a fact about the
world.* A grep with single spaces against double-spaced OCR ("his first name is in no source
found"). A section searched and the volume declared unreadable ("the 1900 roster cannot be read").
A phrase-grep for "Charles Cushing" against a table that writes him as a row headed by the surname
("occurs nowhere in this project"). A title-page pattern that could not match an association-year
date, and one that could not match "FOB THE YEAR". And a misread digit taken for a document.

Every one was caught by going back to the source after writing the claim down, and every one had
already been committed. **Write the claim, then read the source again as though someone else had
written the claim.** The verify scripts check structure, citations and labelling; they cannot tell
you that your query was the wrong shape. Only the source can.

## 27, and it invalidates work rather than merely adding to it

**A count is not a list, and the search-inside API pages.** `openlibrary.org/search/inside.json`
reports a `total` and returns **twenty**. The parameter is `&page=N`; `&from=` and `&offset=` are
accepted and silently ignored, which is worse than being rejected. This project has carried
"Kanawana returns seventy-six" since the capability was found and had been working from the first
page of it for the whole time.

The 76 are now enumerated in full, and the reassuring half is that every item among them actually
about the camp was already registered — the first page had the substance. **The unreassuring half
is the name sweep.** Every name run through this API before 2026-09-06 was checked against at most
twenty hits. A name logged as "243 hits, none of them him" was checked against eight per cent of
them; that name was W. J. Holliday, who was in this repo's own cache all along. **The high-count
names in that log are sampled, not swept**, and the nulls recorded against them do not mean what
they say. A caveat to that effect is now at the top of the sweep log's advice section.

Two smaller things from the same hour. Each hit's `identifier` field is **a list, not a string**,
so `str(fields['identifier'])` never matches a bare identifier and yields a false null — extract
with `[0]`. And when a hit looks like a find, check the word rather than the string: of the 76,
one large cluster is **the Tapirapé term for thunder**, one is **Kiri Te Kanawa**, one is the
**Kanawha River**, one is a Japanese word in Hepburn's dictionary, and one is **Kanawa Magazine**
of the Canadian Recreational Canoeing Association behind an OCR'd second "na".

## 28. Two quoted phrases are ANDed across the whole book, not near each other

The sweep log advised pairing a common name with "Montreal", "Y.M.C.A." or "Kanawana" to cut the
noise. **Tested, and it does not work for the first two.** `"W. J. Holliday" "Montreal"` returns
134 hits, and every one is still the Indianapolis art collector who swamped the bare-name search —
"Montreal" is matching in a bibliography of Canadiana somewhere else in the same volume. The
pairing narrowed 243 to 134 and changed nothing about whose hits they are.

Pairing with **"Kanawana"** is worth doing: the word is rare enough that co-occurrence in one book
means something. Pairing with a common word is nearly worthless.

**For a common name, the two honest options are to page the whole result set and read it, or to
find a source where the man is likely to be indexed and search that instead.** Both of today's
biographical wins came from the second: Harold C. Cross turned up by running his name against the
International Council of Religious Education's *Yearbook* series, and W. J. Holliday was in this
repo's own cache. Neither came from a cleverer query against the whole corpus.

The one good by-product is that the Holliday null now stands on a method that can support it: the
Montreal YMCA's W. J. Holliday is not in that book corpus under that name.

## 29. Facts here cite the COLLECTION, not the item — so "is this source cited?" is not a readable test

Roughly 734 source records carry `read_state: skimmed` under one blanket note saying they were
keyword-swept for six terms and never read closely. Asking whether their `source_id` appears in
`facts.json` returns **no for all of them** — because facts drawn from that collection cite
`src_ia_ymca_montreal_fonds_collection`, the collection-level id, not the item-level `src_ymf_*`
ones. I built a claim about half the corpus on that answer and committed it. It took fifteen
minutes to disprove.

**What is actually true, on the items checked properly: they are partially extracted, one theme at
a time.** The 1938 *Voice of Youth* radio script is labelled skimmed, and its music — set list,
song leader, singing venues — is fully in the KB. Its skit, its cast of five named boys, its
rehearsal room, its letterhead and a Sunday crowd of "over 250 campers and visitors" were all
still sitting in it. That is **rule 21 at the scale of half the corpus**: read for something, and
the something was songs.

**The test that works is per-document and takes a minute.** Pick strings distinctive to the item —
unusual names, exact figures, a room, a place — and grep those. Not the source_id, and not common
capitalised phrases (a second attempt matched "New York" and "Park Avenue"). *Voice of Youth* was
diagnosed by grepping `Morry Cross`, `Willingdon Room` and `John Houseman`, absent, against
`Farewell Rock` and `Sandy Spence`, present.

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

The morning of the 6th added a second half to that. Of the four errors it caught, **three were its
own, made and committed within the hour** — a first name declared missing when a bad query had
hidden it, a volume declared unreadable when only one of its two rosters was, and a man placed in
the wrong volume of a book already open on the desk. None was caught by a verify script. They were
caught by going back to the scan and reading the thing again after writing the claim down. Write the
claim, then check it against the source as though someone else had written it.
