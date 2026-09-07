# Handoff, 7 September 2026 — the Year Book, and a guess that was doing a finding's work

*Twenty-nine commits from `e0f1c79` to `17122f0`. KB v8.96 → **v9.23**, 5,224 → **5,287 facts**.
Priorities 468 → **476**, of which 125 pending. 117 articles, ~419,000 words.
`scripts/verify/all.py` green on every commit but one — `b17ce6b` went red and is the subject of rule 39.*
Priorities 468 → **474**. `scripts/verify/all.py` green on every commit; CI green on every head.*

## The one thing to read first

Yesterday's finding aid listed four routes to the *YMCA Year Book* volumes for 1901-1905 and
1910-1920 — years this project had recorded as unreachable. Three were tested and shut. The
fourth read:

> the Kautz Family YMCA Archives, University of Minnesota, **which holds the series in print**

That last clause was an assumption written down as though it were a finding, and it closed the
route off for a day. Minnesota holds the series **digitally** too, open and full-text searchable.
Everything below came out of that.

**The rule this session would add: an untested qualifier attached to a route is not a finding
about the route, and it will stop anyone from trying it.** Yesterday's note did everything right
except notice that "holds it in print" was a guess. Three of the four routes were shut with
evidence; the fourth was shut with a phrase.

*(The three tested routes are still shut, retried today: Google Books returns 429 naming the
**same consumer project number** as yesterday, so it is a shared key exhausted by other traffic
and "retry tomorrow" was never the fix; both Google search routes 302 to `/sorry/`; HathiTrust is
still Cloudflare.)*

## The route, so nobody has to find it again

University of Minnesota Libraries, **ContentDM collection `p16022coll351`** on
`cdm16022.contentdm.oclc.org` — "YMCA Yearbooks, Directories, and Proceedings", 173 items,
Kautz Family YMCA Archives. **It does not stop in 1982**, as this handoff first said: it also holds
the modern US **YMCA Directories for at least 1996, 2000, 2001 and 2002**, which is how Bruce
Netherwood's Massachusetts years got dated. Two endpoints do everything:

```
ENUMERATE / FULL-TEXT SEARCH (page level, returns parentobject = the volume)
  .../digital/bl/dmwebservices/index.php?q=dmQuery/p16022coll351/<search>/title!dmrecord/nosort/<rows>/<start>/0/0/0/json
  <search> is 0, or FIELD^TERMS^MODE^OPERATOR:
      CISOSEARCHALL^Kanawana^all^and
      CISOSEARCHALL^Brooks, M. G.^exact^and     ← exact phrase works
READ ONE PAGE'S OCR
  .../index.php?q=dmGetItemInfo/p16022coll351/<page dmrecord>/json   → the "transc" field
```

**The endpoint does wildcards** — `CISOSEARCHALL^Kanaw*^all^and` works. That is the tool rule 37a
asks for when OCR might have mangled a name, and it was not known here until the end of the day.

**Three traps, each of which cost something today.**
1. `cdmhasocr` reads **0** on pages that plainly carry OCR in `transc`. Never use it to decide
   readability. Read `transc`.
2. UMedia's own `search.json` answers but **silently ignores** `set_spec` and `facets` — it
   returned Social Work Year Books and Minnesota county maps for collection-scoped queries. Go to
   ContentDM directly.
3. The Montreal block is printed **twice** in each early volume — an international-committee
   membership list and the Directory of Associations — and a search for "D. A. Budge" returns
   both. Searching **"J. E. Merritt"** lands on the directory page directly.

**Full-text coverage was controlled before any null was trusted**: "Montreal" returns 2,742 pages
across 124 volumes and reaches every target volume.

## The technique that did most of the work — it settled four identities

The alphabetical list of employed officers prints each man's **year of entry into Association
work** after his name, and **it does not change as he moves**. One two-digit figure follows one
man across forty years and separates him from others of the same name. These lists answer only
to the **inverted** form — `"Brooks, M. G."`, not "M. G. Brooks".

It produced, in one session: Brooks's forty years; Holliday's whole career, his missing years and
his given name; Forgie's career and his 1927 departure from Canada; **Ronald Hanagan's given name**,
where the 1941 and 1943 volumes print the same post spelled out in the branch directory and
abbreviated in the alphabetical list; and **Oscar L. Pearson as one man from 1912**, which joined a
1919 overseas captain to Montreal Central's physical director of 1941-43.

## What was found, in order of weight

**Harold C. Cross's whole 1912-1919 gap is filled, and his career begins in Montreal.** His
article asks in those words "where was he between 1912 and 1919?" He was the **North Branch's
boys' worker** through the 1911-12, 1912-13 and 1913-14 volumes, **General Secretary at
Charlottetown** in 1914-15, and then **Overseas Representative of the National Council of
Canada** in the 1915-16 and 1916-17 volumes before Victoria. *That last one was found only after
this session had twice written him up as absent* — see the corrections below.

**W. J. Holliday is Captain William J. Holliday**, and the association wrote his whole career out
when he retired: "**retired after over 41 years** … joined the staff of the Montreal Y.M.C.A. in
**1906** and, excluding periods of service overseas in **World War I and again in World War II**,
and **two years on the Sydney, N.S. staff**, has worked throughout his career in this Association."
Every piece assembled from the rosters is in that sentence, in the same order. He went overseas
early in **1940**, returned late in **1945**, and retired in **January 1948**.

**Four men who ran Montreal's camps were overseas at once** — Macdiarmid, Spearman, McGerrigle and
Holliday, four eras of the camp's leadership, named in one paragraph of the 1942 report. That is
why the camp's own record thins in exactly these years. Every roster this project ever saw gave him as
"W. J." The 1918-19 volume's *Overseas Secretaries, Canadian National Council, June 1, 1919* —
"released from regular Y. M. C. A. work for this special service" — gives the name and the rank.
He did **not** recover the Boys' Work directorship; he was a membership assistant in 1909-10 and
a branch secretary to 1917. Montreal's own 1918 report says he "resigned for overseas service",
and the roster then finds him at **Sydney, Nova Scotia** in 1919-20 and 1920-21.

**Six more Montreal men are on that overseas list**, including **Miller, Capt. Thomas Hicks**, who
had charge of the Kanawana season in July 1915. The 1917-18 and 1918-19 gaps in Montreal's roster
are a department's absence, not one man's.

**W. H. Ball left between the 1901 and 1902 volumes**, not somewhere across five years — and the
**1889** volume, which the Archive does not hold, puts "Wm. H. Ball, Jr." at the **Association
Training School, Springfield**, corroborating from outside Montreal the account Montreal gave of
him three years later.

**Harold C. Cross has a career and a retirement date.** Westmount Branch Secretary in 1927-28;
**Acting Secretary of the Metropolitan association in 1945**, the senior professional post of the
whole Montreal YMCA; **Program Secretary of the Metropolitan Board in 1948, 1950 and 1951**, which
is what he was while writing the centennial history; **retired 1 March 1953**; and in the *Retired
Secretaries* list down to **1969**, which is independent evidence he lived that long. Entry 1912 to
retirement 1953 implies a birth about 1885-1892 — the first age estimate this project has had for
him.

**R. H. Hanagan is Ronald Hanagan**, proved by one publication printing the same post spelled out
in the branch directory and abbreviated in the alphabetical list of the same volume.

**Oscar L. Pearson is one man from 1912** — Toronto, Ottawa, Toronto, and Montreal Central in
1941-43 — which joins the 1919 overseas captain to Kanawana's own association.

**M. G. Brooks is Murray Brooks**, Strathcona Hall's own former secretary, sent out by the student
association he had served; Colombo 1910-1923, Toronto 1934, **Burma** 1938, retired 11 March 1945.

**C. M. Daggett** was to run the **1904** camp — the first name in the director gap between John
Roy (1901) and Holliday (1908) — and the same issue says the camp "has now been in operation for
ten years."

**The 1906 Montreal roster has one line more than this project transcribed**, and it is the Boys'
Work Director, **W. A. Maclaren**. Holliday does not appear from nowhere in 1907; he was
Maclaren's assistant, and the two trade places twice.

**The camp's director and Central Branch's boys' worker were the same man, 1916-1919** —
J. G. MacKinnon, in two publications with no view of each other.

**"A. W. Forgie" is almost certainly the Commodore.** See `canadian-camping-movement.md`. The
decisive point is that he leaves Canada for India at **precisely 1927**, the year this project
already held for the end of Wallace Forgie's Canadian influence from the Ebbs obituary and the
Northway profile. **Not tightened past the initials** — that is now `p_475`, and it is a reading
job on two documents this project already cites.

## Nulls worth as much as the finds, all controlled

- **Kanawana appears in this series only 1957-1968.** That is the roster's practice changing, not
  the camp. **Tested three ways** after rule 37a cost a wrong conclusion elsewhere: the exact name;
  the wildcard stem `Kanaw*`, whose 386 hits across 69 volumes are all *Kanawha*, West Virginia;
  and the place names, where "Lac Wilson", "Lake Wilson" and "Laurentian" return **zero pages in
  the whole series** and all nine "Sauveur" hits are in the Ardèche or Belgium. The camp is not
  there under its name, a mangling of its name, or where it is.
- **1962** looked like a hole in that run. It is not: the volume is there and searchable, and
  Seaman is in it — the roster just prints his title as bare "Program" that year and drops the
  camp's name, while Otoreke's line on the next row keeps its own.
- **Geo. W. O. Matthews is in no roster at all.** The likely reason is that his tenure fell wholly
  between two annual editions — a hypothesis, not a finding. The established consequence:
  **an annual roster cannot see a man who came and went inside one year**, so the branch boys'
  line built from this series is incomplete by at least him.
- ~~**Harold C. Cross is on neither war-service list**, so YMCA overseas service is unlikely for
  him.~~ **This was the strongest negative of the session and it was wrong.** The control was
  sound — those lists do name Holliday and Hollinshead — but *two lists naming his colleagues does
  not make two lists exhaustive*, and the **Overseas Representative** run in the Canada section is
  a third list nobody here knew existed. He is in it for 1915-16 and 1916-17. What hid him was the
  typesetting: the entry reads "**H.C.Cross**" with no spaces, so every exact-phrase form missed
  it and only a loose single-token search found him.
- **Open Library search-inside is the wrong instrument for a common name.** "Brooks, M. G.",
  "M. G. Brooks" and "Murray Brooks" return 934, 346 and 190 hits of noise.

## My own corrections this session, all in place

1. **The big one.** I claimed Harold Cross at the 1913 camp season as something "no source in this
   project had said." It is in the table at the top of `directors-index.md` and was in the KB. I
   grepped the **cache** for that name and never grepped the **wiki** — half of a rule I had
   written an hour earlier. What is actually true is smaller and still worth having: the material
   was filed correctly in one article and never carried across to the man's own biography or the
   season's own row.
2. I dated 48 residence campsites and other things well, but wrote **"eight names"** beside a
   twelve-row table. `consistency.py` caught it against the table itself.
3. I typed a footnote marker **before** running `add_source_note.py`, which then allocated the
   next number and left one skipped. `verify_harness` caught it.
4. I called the Forgie identification "a suggestion and not an identification" and had to
   **supersede my own fact within the hour** once the career trace made it far stronger.
5. The 1904 source record was titled and typed as an annual report. It is the June 1904 issue of
   ***Men of Montreal***, the association's monthly, mastheaded the Summer Camp Number — which
   matters, because its camp passages are **future-tense announcements**, not reports on a season.

## Rules this session would add, numbered on from 32

**33. An untested qualifier attached to a route is not a finding about the route.** "Holds the
series in print" shut a door for a day. Write what was tested; mark what was assumed.

**34. A name you do not have is a search you cannot run.** Every finding in the fourth pass came
from annual reports **already in this repo**, in files marked read. Hollinshead, Daggett and
Murray Brooks were unfindable because nobody could grep for a name they did not have. The
corollary is uncomfortable: **a document marked "extracted" has been read for the questions
somebody had at the time.**

**35. Grep the destination AND the cache. Both halves, every time.** Running one half is how the
same passage got written up twice, the second time as a discovery.

**36. The outside source's job is often to make the question precise enough to search the inside
source with.** Holliday's "overseas service" was in this repo the whole time. What the Year Book
supplied was a two-year window that made the sentence findable.

**37a. A negative about a person needs a loose single-token search before it is recorded**,
however many exact forms have been tried — every exact form shares the assumption that the source
spaces a name the way you do. "H.C.Cross" defeated three of them. *(This project already had
rule 22, "a multi-word grep returning zero may be a fact about the whitespace." It cost a wrong
conclusion anyway.)*

**37. Name the list, never the volume.** *(Added after this handoff was first written, from an
error made an hour later.)* One Year Book volume holds an alphabetical list of paid officers, a
Directory of Associations, and in the war years several dated war-service lists under one running
head — **and they use different name forms**: "Holliday, W. J." in one, "Holliday, Capt. William
J." in another, full given names with no posting in a third. An exact-phrase search on one form
searches **one list**. This session twice wrote "absent from the volume" when it meant "absent
from the alphabetical list of paid officers," and Holliday turned out to be in both volumes it
had called him absent from. "Not in this list" is checkable; "not in the volume" is a claim about
a dozen lists at once.

**38. A citation resting on one ordinary shared word is fragile by construction.**
`citation_aim` builds its stopword list **by document frequency across the whole KB**, so its
standard tightens as the KB grows. This session wrote twenty-odd facts about the *Year Book*,
nearly all saying "volume," and **"volume" crossed the cutoff** — which broke two citations in
`canoe-trips.md` and `camp-perrot.md` that had been passing on that word alone. Neither article
was edited; the knowledge base moved under them. Put a name, a year or a number in the citing
sentence.

**39. Run `scripts/verify/all.py` in its own tool call, read it, *then* write the commit.**
*(Added after pushing a red build.)* Putting the check and the commit in one call means the
check's failure cannot stop the commit — and piping its output to `tail` makes the call exit zero
whatever the check says. This project already had rule 25, "a claim about a check is a claim."
This is its sibling: **a check that cannot stop the commit is decoration, not a gate.**

**39a. Run `add_source_note.py` FIRST and use the number it hands back.** *(CLAUDE.md already says
this; I broke it twice today, so here is why.)* The temptation is to write the prose and its `^N`
in one edit and add the note afterwards — but the script allocates the next free number by
scanning what is already there, so a marker you typed in advance makes it skip past you, leaving
your marker dangling and its entry unreferenced. `verify_harness` catches it every time, which is
the only reason it cost nothing.

**40. An exact search assumes the source spells a name the way you do — and a wildcard on the
stem does not save you when the error is *inside* the word.** Three costs today: `H.C.Cross` run
together with no spaces defeated three exact forms; `Otereke` with an E hid two years of
McGerrigle's directorship and briefly convinced me the camp entered this series in 1958;
`Holliday, Capt. William J.` did not match `Holliday, W. J.`

## The most expensive mistake of the session, in three moves

**Infer → withdraw → restore, and the middle move was the wrong one.**

1. A dagger against W. J. Holliday's name in the 1941 roster, plus the page footer's pointer to
   a war-services list, suggested he served in the Second World War as he had the First.
2. An hour later the war-services material turned up — the **National Y.M.C.A. War Services
   Executive Committee** — with Beaton in it and Holliday not. I **withdrew** the suggestion.
3. Montreal's own annual reports, in this cache the whole time, say he served: *"C. J. McGerrigle
   and W. J. Holliday are also serving in the War Services overseas"* (1942); *"went overseas
   early in 1940, returned to Canada late in 1945"* (1946); and the 1948 retirement paragraph.

**The test was the error, not the inference.** That committee is a governing body of about a
dozen men, not a roster of everyone serving — Beaton is on it because he *ran* it. **Absence from
a committee is not absence from service.**

**Rule 41: before treating a null as refutation, ask whether the list you searched is one the
claim would have put the man ON.** A null in a list that could not have held him refutes nothing,
and is more dangerous than no test at all, because it feels like diligence.

## The thing left unsettled, settled — and it went both ways

*(Written an hour after the section below, which is kept because the reasoning in it was sound
and the outcome still split.)* The war-services material **was** found: the **National Y.M.C.A.
War Services Executive Committee**, printed in the Canadian National Council section, with
**John W. Beaton as its Secretary** — Montreal's own General Secretary running the national war
executive. So Cross's four years acting in his place are now explained by **a named post rather
than by a symbol**, which is a better fact than the one it replaces.

**But Holliday is not in it**, and a loose search returns him on the two roster pages and nowhere
else in the volume. The suggestion that he served in the second war as he had the first is
**withdrawn**. The dagger against his name is simply unexplained.

**One symbol, two men, and the evidence resolved one and refuted the other.** A shared mark is
not a shared fact — which is the general form of the error the section below was guarding against,
and the reason it was worth guarding against.

## The reasoning that guarded it, kept

Two facts (`f_5319`, `f_5320`) rest on the reading that **a dagger in the 1940s Roster of Employed
Officers marks a man in Y.M.C.A. War Services**. It matters: it is what puts General Secretary
John W. Beaton at the war, and so explains Harold Cross's four years acting in his place, and it
is what suggests W. J. Holliday served in the **second** war as well as the first, at about sixty.

The evidence is good and is **not a legend**. The Montreal page's footer says "See alphabetical
list of those in Y.M.C.A. War services following alphabetical Roster of Employed Officers, page
258," and the dagger is **selective** — "†\*Holliday, W. J., Montreal, Que., Unemployment, 06"
carries both marks where most names on the page carry the asterisk alone. But the key line itself
was not found, so both facts say so in their own text. **Do not quietly upgrade this.** `p_477`
carries the route: a third list in name-and-home-address format begins around record 38425 in the
volume catalogued 1941, and checking whether Beaton or Holliday is in it would settle it.

## Where to go next

**Everything the Year Book could answer, it has.** `p_464`, `p_465`, `p_466`, `p_467`, `p_468`,
`p_469`, `p_470`, `p_472`, `p_473`, `p_474`, `p_476` and `p_477` are all closed. What is left in
this seam is optional: what Holliday actually *did* at Sydney; a genealogical search on **William
J. Holliday**, now that the given name, the 1906 start and the January 1948 retirement are all in
hand; and the full 1915 annual report, which this project does not hold and which is the only
route to the **summer of 1914** — the one camp season in the war decade still unnamed.

~~- **`p_475`** — Forgie's initials.~~ **Closed, and the initials were never needed.** J. Harry
  Ebbs's obituary — "Wallace Forgie, International Camper, 1883-1967," *Canadian Camping Magazine*
  Winter 1968, headline OCR'd "WALLACE FOKBIE" — **was in the cache**, and it narrates in order the
  exact career the roster gives: Canada 1908-1927, **five years overseas in the First World War
  with the Y.M.C.A.**, **boys' work in Western Canada** with canoe trips into the north-west as an
  associate of Hedley Dimock, then **India**, where in 1935 he built **Camp Tonakela near Madras**,
  opened by Mr. and Mrs. Taylor Statten. Every point matches the roster and nothing conflicts. Two
  independent records narrate one life. *He gave thirty-two years to the orphaned and street
  children of Madras, who called him "Tah-Tah."*

**Nothing on this board is now reachable from here.** What is left needs a person: the fifty-nine
fonds images, the eleven browser items, and the operator's own conflicts.

**For the operator:** `c_067`, `c_068`, `p_442`, `p_443`, the fifty-nine fonds images that need
eyes rather than searches, and the eleven items in `one-afternoon-with-a-browser.md`.

***`p_439` was on that list and should not have been.*** It asks a person to read the 1901-1905
and 1910-1920 volumes on HathiTrust — **which this session read the same day**, at Minnesota. It
stayed marked pending, and I repeated it under "for the operator" in report after report. So did
**`p_433`**, the **highest-weighted pending item in the whole queue**, which is a year-by-year
sweep of that very series. Both are closed now.

**Rule 42: check the queue before describing the state of the board.** A priority is a claim about
what remains to be done, and a long session going well is exactly what makes it stale. When a
session closes a seam, re-read the pending queue for anything the seam has quietly answered —
*before* writing the summary that tells someone else what is left for them.

## The shape of the day, in one line

**The Year Book's real contribution was not its own content but the names and dates that made
this project's own cache searchable.** Cross's overseas years, Holliday's war service and
retirement, Brooks's departure for Ceylon, Pearson's whole identity, the 1913 camp staff — all of
it was already in this repo, in annual reports marked read, unfindable until an outside source
made the question precise enough to ask.
