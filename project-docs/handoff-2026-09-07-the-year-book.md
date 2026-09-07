# Handoff, 7 September 2026 — the Year Book, and a guess that was doing a finding's work

*Thirteen commits from `e0f1c79` to `4fb65ff`. KB v8.96 → **v9.09**, 5,224 → **5,267 facts**.
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
Kautz Family YMCA Archives. Two endpoints do everything:

```
ENUMERATE / FULL-TEXT SEARCH (page level, returns parentobject = the volume)
  .../digital/bl/dmwebservices/index.php?q=dmQuery/p16022coll351/<search>/title!dmrecord/nosort/<rows>/<start>/0/0/0/json
  <search> is 0, or FIELD^TERMS^MODE^OPERATOR:
      CISOSEARCHALL^Kanawana^all^and
      CISOSEARCHALL^Brooks, M. G.^exact^and     ← exact phrase works
READ ONE PAGE'S OCR
  .../index.php?q=dmGetItemInfo/p16022coll351/<page dmrecord>/json   → the "transc" field
```

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

## The technique that did most of the work

The alphabetical list of employed officers prints each man's **year of entry into Association
work** after his name, and **it does not change as he moves**. One two-digit figure follows one
man across forty years and separates him from others of the same name. These lists answer only
to the **inverted** form — `"Brooks, M. G."`, not "M. G. Brooks".

It produced, in one session: Brooks's forty years, Holliday's whole career and his missing
years, Forgie's career and his 1927 departure from Canada.

## What was found, in order of weight

**Harold C. Cross's career begins in Montreal, not Victoria.** His article asks in those words
"where was he between 1912 and 1919?" He was the **North Branch's boys' worker** through the
1911-12, 1912-13 and 1913-14 volumes and **General Secretary at Charlottetown** in 1914-15. The
man who came back in the mid-1920s to direct Kanawana was returning to the association he began
in.

**W. J. Holliday is Captain William J. Holliday**, and his going is bracketed to between 12
February and 1 June 1918 by two Canadian overseas lists a year apart. Every roster this project ever saw gave him as
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
  the camp. Do not read the earlier silence as evidence of anything.
- **1962** looked like a hole in that run. It is not: the volume is there and searchable, and
  Seaman is in it — the roster just prints his title as bare "Program" that year and drops the
  camp's name, while Otoreke's line on the next row keeps its own.
- **Geo. W. O. Matthews is in no roster at all.** The likely reason is that his tenure fell wholly
  between two annual editions — a hypothesis, not a finding. The established consequence:
  **an annual roster cannot see a man who came and went inside one year**, so the branch boys'
  line built from this series is incomplete by at least him.
- **Harold C. Cross is on neither war-service list**, though both name Holliday and Hollinshead —
  so the lists reach Montreal in the right years. It makes YMCA overseas service unlikely for him
  and says nothing about enlistment, which inverts the value of the CEF records: worth more for
  Cross than for Holliday.
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

**37. Name the list, never the volume.** *(Added after this handoff was first written, from an
error made an hour later.)* One Year Book volume holds an alphabetical list of paid officers, a
Directory of Associations, and in the war years several dated war-service lists under one running
head — **and they use different name forms**: "Holliday, W. J." in one, "Holliday, Capt. William
J." in another, full given names with no posting in a third. An exact-phrase search on one form
searches **one list**. This session twice wrote "absent from the volume" when it meant "absent
from the alphabetical list of paid officers," and Holliday turned out to be in both volumes it
had called him absent from. "Not in this list" is checkable; "not in the volume" is a claim about
a dozen lists at once.

## Where to go next

- **`p_475`** — Forgie's initials, from the Ebbs obituary or the Northway profile. Two documents
  this project cites and has never read in full. Cheapest high-value item on the board.
- **`p_474`** — the Canadian overseas list is Canada-wide and about a hundred names; only the
  Montreal ones have been taken. Read the rest against the people index. Also: does the 1917-18 or
  1919-20 volume carry an equivalent, since presence in 1919 but not 1918 dates a man's going?
  And the **symbol** prefixed to some names on the United States list — its key was not on any
  page read, and Hollinshead carries it. Settle what it means before anyone reads significance in.
- **`p_472`** — Holliday's overseas service and the **Sydney, Nova Scotia** posting, entirely
  untouched. With "William" in hand a genealogical search is newly possible.
- **`p_464`** — 1914 and 1915 in the Central boys' post are the last gap in the war-decade line.
- **`p_467`** — Cross, 1915-1918, with the CEF records now the sharper instrument.

**For the operator, unchanged and not to be ground on:** `c_067`, `c_068`, `p_442`, `p_443`,
`p_439`, the fifty-nine fonds images that need eyes rather than searches, and the eleven items in
`one-afternoon-with-a-browser.md`.
