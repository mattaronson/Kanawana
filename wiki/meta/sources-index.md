# Sources and Archives

*Status: E1-reviewed | Sources: 643 (this article catalogs the project's sources; see Source Statistics, below)*
*Last Updated: 2026-09-06 (p_387: the three structural breaks of 1974-1976 in the *Canadian Camping* run)*

## Summary

This article catalogs all sources consulted for the Kanawana Wiki Builder project. As of March 2026, the knowledge base drew on 138 source records; by 2026-07-09 this had grown to 580, spanning primary camp publications (1921–1980), archival finding aids, academic research, biographical references, and web sources -- including a substantial Phase 2 broad-net expansion into social media, review platforms, job postings, municipal/heritage registries, and Wayback-recovered predecessor-domain documents. The collection is anchored by Grace McMorris's 2023 Concordia MA thesis (now read in full, not just chapters 1-3 + conclusion), Internet Archive primary documents (including a newly mapped ymca-montreal-fonds collection of 25+ items), and Concordia University's YMCA of Montreal Fonds P145.

## Primary Sources (31)

### Camp Publications (Internet Archive)

| Source | Date | Type | Notes |
|--------|------|------|-------|
| Kamp Kanawana Brochure 1921 | 1921 | Brochure | Director G.D. Brandon. Fully extracted. |
| Kamp Kanawana Brochure 1922 | 1922 | Brochure | Director Ereaux. Staff, costs, facilities, badge system. 11,586 chars. |
| Kanawana: The YMCA Camp for Boys 12-17 (1923 Brochure) | 1923 | Brochure | Director Philip G. Paterson. Complete rebrand in tone from 1922. |
| The Gas Bag, 1923 Re-union Number | 1923-09-01 | Camp newsletter | 14th season chronicle, staff, badge winners, camp life. 23,900 chars. |
| A History of Kamp Kanawana (1935 Season Chronicle) | 1935-08-23 | Season chronicle | Anonymous. NOT Ralph Dawson 1933 history. 4,912 chars. |
| The Green Triangle, July 29, 1938 | 1938-07-29 | Camp newsletter | Fancy dress ball, staff names. 7,180 chars. |
| CFCF Radio Broadcast — YMCA Kamp Kanawana | 1941-06-26 | Radio transcript | 48th season broadcast. 7,846 chars. |
| Ka-News, May 1980 | 1980-05 | Staff newsletter | Director "Dave," 14+ staff names, programs. |

### Internet Archive: YMCA Montreal Fonds Collection (NEW — March 2026)

Concordia University's Records Management uploaded 25+ digitized items to Internet Archive (collection: ymca-montreal-fonds) starting September 2022. Newly identified items not yet extracted include:

| Source | Date | Notes |
|--------|------|-------|
| Alfred Sandham, *History of the Montreal YMCA* | 1873 | Earliest known YMCA Montreal history. |
| *Historical Sketch of the YMCA of the City of Montreal* (Jubilee) | 1901 | Covers 1851–1901, overlaps Camp Jubilee founding. HIGH PRIORITY. |
| YMCA Annual Report 1889–1890 | 1890 | Pre-camp-founding. |
| YMCA Annual Report 1891–1892 | 1892 | Immediately pre-founding. May document Cushing's 1892 trip. HIGH PRIORITY. NOTE: IA identifier uses '1991-1992' (metadata typo). |
| YMCA Annual Report 1966–67 | 1967 | IA identifier: sgw-ymca-annual-report-1966-67. Only known digitized annual report from the 1940s–1960s, filling a significant gap between the 1891–1892 and 1993 reports. HIGH PRIORITY. |
| SGW College Bulletin, September 1932 | 1932 | May contain YMCA/camp references. |
| YMCA News Release: Largest Sum (1965) | 1965-04-27 | Fundraising campaign. |
| YMCA News Release: Back in Pointe Saint-Charles (1980) | 1980-03-17 | Institutional context. |

### YMCA Official Documents

**Parent preparation guides — a source that silently supersedes itself.** The camp publishes an
annual parent preparation guide at ymcaquebec.org, and each year's edition replaces the previous one
at a *new* URL while the old file stays reachable. Three editions have been cached (2025, January
2026, and the current "Camp-Kanawana-GUIDE-Parent-EN_2026.pdf" / "-FR_2026.pdf" posted by 16 June
2026), and the current one follows the same 43-page structure as the 2025 guide, with the canoe-trip
complement embedded from page 29 rather than issued as a separate document.^pg These guides have
already supplied staff rosters, the site map legend, and programme detail found nowhere else, so the
supersession matters: a citation to "the preparation guide" without an edition year is ambiguous, and
any claim drawn from one should name the year. The June 2026 edition is cached but **not yet fully
extracted** — it is the most current primary document the project holds and the likeliest place for
2026-season facts.

| Source | Type | Notes |
|--------|------|-------|
| YMCA Kamp Kanawana Facts | Fact sheet | Official YMCA fact sheet. 644 chars. |
| Matt Aronson — Oral History | Ongoing oral history | Domain expert: personal timeline 1985–2002, Sean Day, L&V, 1894 founding, Pine Crest. |

### Concordia University Archives (YMCA of Montreal Fonds P145)

**Use the PDF finding aid, not the web pages.** Three different Concordia surfaces carry this fonds,
and they are not equivalent:

| Surface | What it is | Reachable? |
|---|---|---|
| **PDF finding aid** — `concordia.accesstomemory.org/downloads/ymca-of-montreal-fonds-2.pdf` | The authoritative document. 125 pages, generated 2023-11-24. **15 series, 173 sub-series and sub-sub-series units.** | **Yes** — `/downloads/` sits outside the browser challenge. Cached in this repo. |
| **Static HTML mirror** — `concordia.ca/offices/archives/ymca-fonds-*.html` | A hand-made subset on the university CMS. **95 pages.** Every one maps to a unit in the PDF; **78 units have no page here.** | Yes, but not crawlable — the fonds index renders its links in JavaScript, so the pages must be enumerated by pattern. |
| **AtoM catalogue** — `concordia.accesstomemory.org` | The live database. Holds item-level records and digital objects the other two do not, and is actively updated (films were posted in February 2026). | **No.** See below. |

The AtoM catalogue serves every request — including its own OAI-PMH endpoint, which exists solely
for machines — behind a JavaScript challenge that sets a cookie carrying `navigator.webdriver`. Its
`robots.txt` is `User-agent: * / Crawl-delay: 60`, so the site's published policy permits automated
access while the technical control does not. An honest declaration (`webdriver=true`) was sent and
refused. On 2026-08-25 the operator authorized asserting `false`; that was tried, under the
crawl-delay and with a descriptive contact User-Agent, and **was also refused** — the server checks
more than that flag.

**Escalation stopped there, and this is deliberate.** Going further would have meant
reverse-engineering an anti-bot control on someone else's server. Concordia is the only party who
can license that, the operator's authorization could not be traced to them, and the archive is a
collaborator this project may well need to write to. The catalogue is therefore recorded as
`read_state: unavailable`, not as a null.

**This costs less than it sounds.** The authoritative finding aid is the PDF above, which is not
behind the challenge and is already cached here. AtoM adds item-level records and digital objects on
top of it — worth having, and the way to get them is an operator-side fetch from a normal browser or
an email to `archives@concordia.ca`, who are in the business of answering exactly this question.

Note also that `archives.concordia.ca` is **not** the catalogue — it redirects to the CMS.

| Sub-series | Title | Notes |
|------------|-------|-------|
| P145 (main) | YMCA of Montreal Fonds | Box HA1874. 14 camping sub-series (12A–12N). |
| 1B | History | Harold Cross manuscript, correspondence 1939–1957, Murray Ross correspondence, chapter drafts. |
| 12A | Committees | Permanent Camp Committee minutes (1895-96!), 1895 St. Agathe scouting journal, Charlton/Dawson/Cushing histories (1933/1943), Boys Camps comparisons (1945-46, 1953-54), Outdoor Education report (1974). |
| 12B | Kamp Kanawana | 12B01 (admin: season reports, committee minutes, camp director correspondence, Dave Twynam correspondence), 12B02 (finance), 12B03 (land/facilities), 12B04 (communications: brochures from 1950, 1959, 1960s, 1964, 1965), 12B05 (staff), 12B06 (campers), 12B07 (program). |
| 12C | Camp Otoreke | Parallel sub-series to 12B for Camp Otoreke records. |
| 12D | Camp Becsies | Textual records 1929–1936, 1960–1971. Previously unknown YMCA camp. |
| 12E | Camp Dorval | Textual records 1926–1928. Short-lived YMCA camp. |
| 12F | Camp Weredale | YMCA planning documents related to Weredale (1977–1983). |
| 12G | Camp Perrot (see note below) | Boys'-and-girls' service camp compared against Kanawana in reports 1945–46, 1953–54; 11 of its own annual reports/brochures (1944/45-1969) are separately digitized on Internet Archive, not catalogued under this label — see [[site/camp-perrot|Camp Perrot]]. |
| 12H | Ski lodge | YMCA ski lodge records. |
| 12I | Camp Thunderbird | YMCA Camp Thunderbird records. |
| 12J | Wilderness Survival Camp | Wilderness Survival Camp program records. |
| 12K | Les Voyageurs de la Vérendrye | Canoe program est. 1958-59. Exploratory logs, Lac Landron lease (1962-63), brochures, camper records (1967-80), review (1982). |
| 12L | Lac St-Joseph / Camp Jubilee | 1893 camper lists, John Roy 1901 letters, 1898 photo; Box HA2312 holds an unread "Director's report (1908)," a specific lead for the undocumented 1901-1923 director gap. |
| 12M | Day camp | 1953-1989. Box HA2312 (admin: memos, promotion, policy, staff seminars) and Box HA1886 (resource materials: bilingual manuals, Olympic Day programming). No Kanawana-specific content confirmed. |
| 12N | Camping associations | 1929-1981. Four sub-sub-series: 12N01 American Camping Association (1937-59); 12N02 Canadian Camping Association (1936-81); 12N03 Quebec Section CCA / Quebec Camping Association (1929-70, incl. McGill camping-leadership courses); 12N04 QCA / Association des camps du Québec (1978-80). No Kanawana content by name in any box-level description. |
| 14D | National Council | Harold Cross Boys' Work file 1940–1945. 14D03: YMCA Montreal annual reports. 14D10: Nelson McEwen correspondence 1941–1945. |

**Note on "12G" (added 2026-07-10):** Concordia's full 125-page master finding-aid PDF shows that, unlike every sibling sub-series (12C-12F, 12H-12N, each with a full date-range and box-listing entry), "12G" has no descriptive entry at all in the finding aid's body — the structure jumps directly from 12F (Weredale) to 12H (Ski lodge). This appears to be a genuine cataloguing gap in Concordia's own finding aid (independently confirmed by two separate research passes the same day), not a wiki error. Camp Perrot material that *is* catalogued exists only as comparison documents within sub-series 12A.

**New research tool (2026-07-10):** the fonds' full 125-page master finding-aid PDF (`concordia.accesstomemory.org/downloads/ymca-of-montreal-fonds-2.pdf`) is directly downloadable via `curl` — unlike the bot-walled AtoM catalog interface — and readable via `pdftotext -layout`. This is a superior, reusable tool for future Concordia fonds research: it surfaced item-level detail (including several previously uncatalogued Kanawana audiovisual items — see below) that no static finding-aid page had captured, and confirms sub-sub-series 12B05 (Staff and counsellors) is explicitly access-restricted, explaining why static pages for 12B02/05/06 consistently 404 while 12B01/03/04/07 work.

**Newly surfaced Kanawana audiovisual items (2026-07-10, from the master PDF's item-level list, sub-series 09 moving images and 11 sound recordings):** *Camp Kanawana: Boating and Water Sports All Summer Long* (16mm, ~8 min); *News Documents and Kamp Kanawana* (VHS, 15 min); French and English *Kamp Kanawana* PSAs (December 1988 and March 1987, 1 min each); an undated *Kamp Kanawana* audio reel; a 1969 promotional audio tape; an August 24, 1962 audio interview with a "Woodsman" section member; an undated "Homesick tape"; and a 1963 recording titled "What is God? / Interview of Kamp Kanawana campers and staff." Only catalog metadata was retrieved, not transcripts or audio itself — these are potentially rich primary sources for a future session with audio-transcription capability.

### Newspaper Sources (BAnQ / Newspapers.com)

| Source | Date | Notes |
|--------|------|-------|
| Montreal Gazette — "YMCA Summer Camp Kanawana" | 1897-07-07 | Earliest known newspaper reference. |
| Montreal Gazette — "At Camp Kanawana" | 1918-07-11 | 110 members, detailed activities, Woodcraft League visit. |
| Montreal Gazette — "Youngsters Have Gay Time at Camp" | 1918-07-27 | Additional 1918 coverage. |
| Montreal Gazette — "YMCA Boys Leave for Kamp Kanawana" | 1913-07-07 | Two detachments, M.F. Furey, Dr. Hamilton. Behind paywall. |
| La Presse — Desjardins $1M donation | 2018-05-15 | New pavilion construction. |

### *Canadian Camping* Magazine, February 1949 – Winter 1988 (164 issues, read in full)

The largest single body of source material this project holds. The complete digitized run of the
national camping association's own magazine — 164 issues, Vol. 1 No. 1 (February 1949) to Vol. 39
No. 3 (Winter 1988) — cached from the Internet Archive and read word for word, page by page, in
2026. The copies scanned are Trent University's own deposit set: the mailing labels on the later
issues are addressed to the CCA archives and to individual camp directors who forwarded them there.

**Why the run stops in 1988.** It is not a gap in the digitization and should never be described as
one. Fitness Canada told the association at the end of November 1984 that it would no longer fund
the executive director's post, and that support for "all management aspects, re travel for meetings,
office functions, administrative assistance, would be reduced each year by 33-1/3% to terminate
completely in 1988" [f_4487]. The last issue says so in its own voice — "1988 is an historic year.
It is this year that the Canadian Camping Association is no longer receiving funding for its
operating expenses from the Federal Government through Fitness Canada. Will we survive?" — and
records that "there is no money left in the budget to produce this very C.C.A./A.C.C. Magazine you
now hold in your hands," the issue having been underwritten by a single camp, Camp Tawingo
[f_4722]. A member of the board who was present gives the reason as a jurisdictional
judgement rather than austerity: Fitness Canada's "thinking that camping is not within their
jurisdiction" [f_4525]. Every judgement this wiki makes about the thinness of the Canadian camping
record after 1988 has to carry that.

**Where the run begins, and what precedes it.** Charles F. Plewman's "The Canadian Camping Magazine
and How We Came By It" (Vol. 24 No. 1, Fall 1971) is the magazine's founding history written by its
founder [f_3564]. Drafted into the presidency of the Ontario Camping Association in the autumn of
1944 — the OCA having been formed eleven years before, in 1933 — he found an association that "was
an Ontario Camping Association but in name only," ninety per cent of its camps and all its officers
from Toronto, and concluded "we needed a magazine or bulletin of some kind to draw us closer
together" [f_3565]. The T. Eaton Company financed the first edition, "As an association we were poor
and just didn't have the money," and "Next I asked the one and only Mary Edgar to act as Editor and
she agreed" [f_3566]. The OCA "closed out the Ontario Bulletin in 1947 and threw its entire
resources behind 'Canadian Camping', a mimeographed bulletin published quarterly and edited as
before by Mary Edgar" [f_3569]. Then: "The first real Canadian Camping 'magazine' was published in
February of 1949 when for the first time it appeared in print" [f_3570] — which is exactly where
this project's cached run begins. **The run is therefore complete from the magazine's first printed
issue.** The mimeographed 1947–48 quarterly that preceded it is a separate, earlier body of material
this project does not hold and has never seen. The move into print "would not have been possible had
not Mr. Fred Haiblen of Toronto stepped in and assumed the financial responsibility"; Edgar edited
five more years and was succeeded by Mrs. G. W. Flynn [f_3571]. One caution: the Summer 1986
anniversary issue calls Mary S. Edgar "the Founder of Canadian Camping Magazine" [f_4589], which sits
beside Plewman's account of producing the first bulletin himself. The two may describe the same thing
from different angles; neither is preferred here.

**Three structural breaks, 1974–1976, and why none of them is a hole.** The run changes format twice
and stops once inside three years, and each break is explained in the magazine's own pages. Read them
before reading anything about content, because each one looks from the outside like missing material
[f_4930].

*February 1974 — publication suspended.* Vol. 26 No. 2 is a combined **Winter/Spring 1974** number and
nothing follows it until Vol. 27 No. 1 in **November 1974**, which opens by explaining the eight-month
silence: "In the last three years, the magazine was financially sliding downhill to the extent that an
unrealistic portion of the CCA budget was consumed to keep *Canadian Camping* coming off the press. As
a result of this situation, **the Board of Directors temporarily suspended publication of future
magazines effective in February 1974**." A Task Force reported to the Board in April 1974 and
recommended that a magazine format be kept, that it be bilingual as far as possible and self-supporting
— **and that the January issue become a "Directory Issue"** carrying a complete listing of every CCA
member camp in every province alongside the full editorial content, to widen circulation and attract
advertisers. That recommendation is the reason this project has the January 1975 and January 1976
directories at all, and with them Kanawana's capacity, its director, its activity list, and the
separate accreditation of [[traditions/canoe-trips|Les Voyageurs de la Vérendrye]]. **The camp's own
best-documented year in the national record is a byproduct of the national association's worst
financial one.**

*November 1975 — four pages, because of a postal strike.* Vol. 28 No. 1 is not a magazine but a
four-page newsletter, and the editor **Helen E. Stewart** says why on the first page: "Without any
doubt, the mail strike has brought its hardships and '*Canadian Camping*' is no exception.
Unfortunately, when the time for typesetting arrived, **we were lacking in advertisements and editorial
content which included resumes in French**. Recognizing we had a definite commitment to our reading
public, the decision was made to publish a four page Newsletter."

*June 1976 — announced as the last issue.* Vol. 28 No. 3 opens: "This issue of *Canadian Camping* is
its last. **The decision was made by the CCA Board at the recent meetings in Quebec City and was one
based wholely on financial considerations.**" Stewart adds that "The April and june issues were planned
when word reached me that there would be but one more issue," so accepted articles exist that were
never printed. The title then resumes in **October 1976** as Vol. 28 No. 4, a typewritten eight-page
newsletter from the association's new office at 102 Eglinton Ave. E., Toronto, whose own first
paragraph is a note to readers: "The format might be different… but the intent is still the same."
**So the depth of the source changes sharply here**, from a quarterly magazine to five or six short
newsletters a year, and any argument from silence about the later 1970s has to account for that before
it accounts for anything about camping.

One check on the third break, because the editor's sentence invites a wrong inference: **Vol. 28 is
numbered 1, 2, 3, 4 consecutively** — November 1975, January 1976, June 1976, October 1976 — so **no
number is absent from this project's cache**. Earlier volumes did carry an April number (Vol. 27 No. 3,
April 1975), which is what makes the missing April look like a gap. On the evidence of the numbering
the April 1976 issue was planned and not published, not printed and lost.

**Production, format and price, as the magazine states them.**

| Date | Change |
|------|--------|
| Feb 1949 | First printed issue, "the natural evolution of two years of mimeographed bulletins"; quarterly, 25 cents a copy [f_2475] |
| 1967 | Publisher change to Town Talk Publications; Eanswythe Flynn editing |
| Dec 1969 | Publisher change to Broydon Printers Ltd., Peterborough. Don Groff's summary: "From mimeograph to letterpress to offset; from stationery size to fold-over booklet, to display size" [f_3358] |
| Apr 1970 | Bilingual publication begins — masthead, editorial and articles in both languages, with French-only content that no English keyword search will ever surface [f_3385] |
| mid-1981 | Jay Haddad becomes editor, in a volunteer capacity [f_4558] |
| Winter 1986 | Haddad retires after four and a half years; the magazine passes to a group from Camp Tawingo, this issue being "a transitional issue" [f_4558, f_4559] |
| Winter 1988 | Final issue of the run, production underwritten by Camp Tawingo [f_4722] |

Subscription rates as printed: $3.00 a year and $8.00 for three years in 1970; a $2.00 staff rate
from 1971; $1.00 a single copy from Winter 1972; $6.00 a year with additional staff subscriptions at
$4.00 in 1984 [f_4410]; $8.00 a year and $2.00 an issue to 1987 [f_4616]; $10.00 and $3.00 from 1987,
when an ISSN appears for the first time, 0834325 [f_4684]. In Fall 1971 the magazine stated: "CANADIAN
CAMPING is a 100% Canadian magazine and is not subsidized in any way. It is supported solely by
advertisements" [f_3594] — which is worth setting against the federal operating grant that the
association itself depended on by the 1980s.

**Two warnings for anyone using the French text.** The Fall 1986 masthead carries a standing offer:
"If you would like to receive a complete English translation of any article in Canadian Camping
Magazine, send a stamped self addressed envelope," and the same in reverse for French [f_4616]. The
French-language material in this run was therefore *not* systematically translated, and the two
columns are not always the same text. Where they differ, the French is sometimes the sounder: the
Fall 1987 English rendering of the ACQ's report garbles a single Quebec ministry into two [f_4698].

**What the run contains about Kanawana, stated plainly.** Kanawana is named in 164 issues perhaps
two dozen times across thirty-nine years, almost always inside a directory listing, and exactly once
does one of its own people write in it — Jay Netherwood's "L'Étranger / The Stranger" in the final
issue, printed in both languages with the French set first [f_4708, f_4713]. The camp was a member of
the ACQ and through it of the CCA for the whole period, and the national magazine of its own movement
recorded that membership almost entirely as an absence. Everything of Quebec substance the run
yielded — the provincial association's competing founding dates, its accreditation régime, its
statistics, its French-language commission, its officers — came out of issues that never mention
Kanawana at all, which is the argument for reading a source in full rather than searching it for a
name [f_4738].

**Known defects in the scanned copies**, recorded so a later pass does not read a hole as an absence:
pages 6–7 of issue 149 (Winter 1984) and the whole of issue 145 are printed 180° rotated and were
recovered through a lossy decoder — every quotation from them is flagged as a reconstruction, and
four of its readings were later corrected against clean type [f_4465]; page 7 of the Spring 1987
issue and pages 13 and 19 of the Fall 1987 issue produced no machine-readable text at all
[f_4647, f_4690]; the 1983 national totals in the Summer 1984 statistics table do not add up and are
not usable, though the provincial columns are [f_4442]; and the foreign-counsellor table in the same
report has its columns broken in the OCR, so only its totals are extracted [f_4463]. A separate
absence is in the source rather than the tool: a postal strike, named by the editor, is why several
provinces are silent in the Fall 1987 issue [f_4689].

### The camp in other people's books

A full-text sweep of the Internet Archive's book corpus on 2026-09-06 found Kanawana named in books
that are not about it. Four are treated at length elsewhere — [[people/j-w-mcconnell|Fong's biography of
J.W. McConnell]], [[people/roy-locke|the Canadian Obituary Record]],
[[history/postwar-gap|Judy Abrams's memoir]] and [[traditions/programs-activities|Michael Kutz's]], plus
[[site/camp-otoreke|a 2016 Quebec history that gets the camp wrong]]. Three more add nothing about how
the camp ran and are worth recording anyway, because of what they show about the name — see the source note at the end of this section.

*Les Laurentides, peintures et paysage*, a travelling exhibition catalogue of **1977**, lists the ways
outsiders came to know the region: anglers, hunters, and "**les garçons installés dans des colonies de
vacances comme le camp Kanawana de la YMCA** [qui] sont venus dormir sous la tente et s'aventurer dans
des sorties en canoë."

Mike Gutwillig's *My Canada — Such a Mechiah!* (**1967**), on a Montreal childhood: "(and, if you were
really fortunate, getting **Camp Kanawana or Tameracouta** for two weeks)" — Kanawana and the Scout camp
as the two prizes of a summer.

L. Ian MacDonald's *Politics, People & Potpourri* (**2009**), collecting his *Gazette* columns: "Because
she recently went on a **five-day canoe trip at Camp Kanawana** in the Laurentians, she is the family
expert on proper canoeing technique…"

**What the three have in common is that none of them explains what Kanawana is.** In a Jewish memoir of
1967, an art catalogue of 1977 and a newspaper column collected in 2009, the name is used as though the
reader will know it — and in the first two it stands for camp-going in general rather than for itself.
That is a kind of evidence this project has almost none of: not what the camp did, but what its name
meant to somebody who was not there.


**Source note.** *Les Laurentides, peintures et paysage : exposition itinérante* (1977), Internet Archive scan leaf 106; Mike Gutwillig, *My Canada — Such a Mechiah!* (Prize Books, 1967), scan leaf 168; and L. Ian MacDonald, *Politics, People & Potpourri* (Montreal: published for *The Gazette* by McGill-Queen's University Press, 2009), scan leaf 354 [src_three_books_naming_kanawana_2026]. **One passage from each**, reconstructed 2026-09-06 from overlapping Open Library search-inside queries; all three are lending-restricted and none has been read, and the printed pages are unknown. The reconstructions and their queries are cached at `sources/cache/openlibrary-search-inside/2026-09-06-three-books-naming-kanawana.txt`. See [f_4940].

## Secondary Sources (37)

### Academic Works

| Source | Date | Type | Notes |
|--------|------|------|-------|
| McMorris, Grace. "An Experience That Lasts a Lifetime." MA thesis, Concordia University. | 2023 | Thesis | Central secondary source. Ch1–3 + Conclusion extracted, 78+ facts. Supervised by Peter Gossage, Professor of History, Concordia. Full PDF open-access on Concordia Spectrum (eprint 992763); also indexed on CORE.ac.uk. |
| Wall, Sharon. *The Nurture of Nature*. UBC Press. | 2009 | Monograph | Principal study of Ontario camping. Won 2010 Clio Prize. |
| Dean, Misao. "The Centennial Voyageur Canoe Pageant." *JCS* 40:3. | n.d. | Journal article | Nationalist symbolism of 1967 canoe pageant. |
| Ballantyne. *A Short History of the Canadian YMCA 1851–1944*. | 1944 | History | National YMCA history. 38,063 chars cached. Re-grepped in full 2026-07-10 for "camp," "Laurentian," "Saint-Sauveur," "St. Joseph," "Ball," "Cushing," "Kanawana" — zero Kanawana-specific mentions beyond one already-known national statistic. Confirmed dead end. |
| Cushing, James S. *The Genealogy of the Cushing Family*. Montreal: Perrault, 1905. | 1905 | Genealogy | 598 pages. Internet Archive. Key genealogical source. |

### YMCA Quebec Newsroom (Pip Alumni Award pages)

| Source | Year | Subject |
|--------|------|---------|
| YMCA Quebec — Carol Skinner Pip Award | 2016 | 9th recipient. Ceremony details. |
| YMCA Quebec — Terry Mosher Pip Award | 2015 | 8th recipient. Alumni committee noted. |
| YMCA Quebec — Chris Adam Pip Award | 2017 | Contains full year-by-year recipient list. |
| YMCA Quebec — Marina Sharpe Pip Award | 2018 | Selection criteria wording. |
| YMCA Quebec — James Orbinski Pip Award | 2024 | Most recent documented recipient. |

### Biographical and Organizational Sources

Selected highlights from 37 secondary sources:

- **Stuart McLean**: Samaritan Mag, OurKids.net, The Montrealer (2008), Westmount Magazine, CBC Fund article, CBC obituary, Concordia tribute, McMaster fonds, YMCA John Island Newsletter (2012 speech)
- **Caddell family**: CMAT memorial (Globe and Mail obituary), McGill News, Atwater Library bio (Andrew Caddell)
- **Camping movement**: CCA history, OCA history, Taylor Statten Camps, Pine Crest Encyclopedia
- **Cushing family**: DCB (Lemuel Sr.), Wikipedia (Lemuel Jr.), Beer Et Seq (Thomas/brewing)
- **1967 Centennial**: Wikipedia (Voyageur Pageant, Hodgins, Starkell, Ross), Manitoba Sports HOF, Canada Ehx
- **Hedley Dimock**: ACA Dimock Biography (PDF), Concordia Archives 12B05
- **Architecture**: CCA Ross & Macdonald fonds (Doctor's Cottage drawings)
- **Environment**: CREL Laurentides Lac Kanawana data
- **Heritage**: BaladoDecouverte Saint-Adolphe-d'Howard tour
- **Camping movement**: University of Minnesota Kautz Family YMCA Archives (YMCA in Canada records, 1851–1989). Includes records from the Montreal YMCA era when Canadian national administrative headquarters were located in Montreal, prior to formation of the National Council of YMCAs of Canada in 1912

## Tertiary Sources (12)

Wikipedia articles consulted for verification and context:

John Wilson McConnell, Lemuel Cushing Jr., Centennial Voyageur Canoe Pageant, Bruce Hodgins, Don Starkell, Murray G. Ross, Big Cove YMCA Camp, Mary Susanne Edgar, Richard Patten, John Cleghorn, Stuart McLean, Saint-Adolphe-d'Howard.

## Source Statistics

*Note: the category breakdown below (primary/secondary/tertiary/catalog split, extraction counts) was last hand-tallied in March 2026 and has not been recomputed against the current source list; only the total and KB Statistics figures below are current as of 2026-07-09. Recomputing the full breakdown is a future-work item.*

| Category | Count (March 2026) |
|----------|-------|
| Primary (camp publications, archives, oral history, newspapers) | 38 |
| Secondary (academic, organizational, biographical) | 56 |
| Tertiary (Wikipedia) | 16 |
| Catalog references | 16 |
| **Total (March 2026)** | **138** |
| **Total (current, 2026-07-10)** | **643** |
| Extracted (KB facts generated) | 98 (March 2026 tally, stale) |
| Unextracted (awaiting download or access) | 28 (March 2026 tally, stale) |
| With cached text on disk | 18 (March 2026 tally, stale) |

## KB Statistics

| Metric | Count |
|--------|-------|
| Total facts | 4700 |
| Fact categories | 83 |
| KB version | v6.06 |

Of those 4,700 facts, **2,264 came from the word-for-word read of the 164-issue *Canadian Camping*
run** described above — the single largest extraction this project has run, and the reason the fact
count roughly doubled between v5.07 and v6.06.

## Related Articles

- [[history/timeline-overview|Timeline Overview: Camp Kanawana Decade by Decade]]
- [[history/founding-1894|Founding of Camp Kanawana (1894)]]
- [[history/centennial-1967|Centennial Year (1967)]]
- [[connections/institutional-lineage/canadian-camping-movement|The Canadian Camping Movement]]
- [[documents/kanawana-in-media|Kanawana in Media]]
- [[people/harold-cross|Harold C. Cross]]
- [[traditions/pip-alumni-award|The Pip Alumni Award]]
- [[people/notable-alumni/stuart-mclean|Stuart McLean]]

## Open Questions

1. ~~[Critical] Can the McMorris thesis PDF be accessed for full text extraction (currently only chapters 1–3 + conclusion)?~~ [Resolved 2026-07-08/09] Yes — the thesis was read directly as a full 129-page PDF from spectrum.library.concordia.ca across Campaigns 30-31, superseding the earlier chapters-1-3-plus-conclusion extraction. Dozens of new facts and two article corrections (Ralph Dawson, the Pagé farm purchase date, the 1928/1962 camp maps) resulted.
2. [Important, substantially resolved 2026-07-10] What additional materials exist in Concordia Fonds P145 sub-series 12A–12K and 12M–12N? Mapped in detail via the master finding-aid PDF: 12M (day camp, 1953-89, no Kanawana content) and 12N (camping associations, 1929-81, four sub-sub-series, no Kanawana content) are now fully catalogued; several previously undocumented Kanawana-specific audiovisual items were surfaced (see the note above); the "12G | Camp Perrot" entry was found to be a cataloguing gap, not a real described sub-series.
3. ~~[Important] Are there Kanawana-specific records in the Trent University OCA/CCA fonds?~~ [Largely resolved] Yes — Derek Walsh's 1983 CCA Award of Excellence and his link to "Kamp Kanawana, YMCA, Montreal" are documented via the Trent University Ontario Camping Association fonds (see directors-index.md), among 30+ KB facts referencing Trent-held material. Trent also separately holds the Quebec Camping Association's own fonds (85-013, 1948-1982) — no Kanawana content by name found there either.
4. [Important, re-confirmed 2026-07-10] BAnQ digitized newspaper archive (numerique.banq.qc.ca) — systematic search for Kanawana mentions in Gazette, Montreal Star, La Presse, Le Devoir requires browser access. Now more precisely characterized: the block is a Radware "perfdrive.com" bot-validation redirect at both the search and article-detail level, confirmed on multiple distinct URLs — not a simple 403. Every article surfaced by site-restricted search was already in this KB; notably, no "Montreal Star" hit surfaced at all despite its partial digitization, unclear whether this reflects absence or incomplete coverage of that title.
5. ~~[Nice-to-have] Can the Ballantyne 1944 history yield any Montreal YMCA camping context?~~ [Confirmed dead end 2026-07-10] No — see the Academic Works table above.
6. [Nice-to-have, advanced 2026-07-10] Does BAnQ hold Quebec-specific camping records (provincial camping association, inspection records)? BAnQ numérique holds a digitized "Rapport annuel... Association des camps du Québec" entry (inaccessible due to the Radware block above). The more productive path turns out to be Concordia, not BAnQ: sub-series 12N holds the actual Quebec Section CCA/QCA correspondence, minutes, and constitutions (1929-1981) — see the fonds table above.
7. ~~[Nice-to-have] BAnQ Advitam Notice 519920 references YMCA Montreal archives received 1985 — what is the relationship to Concordia fonds?~~ [Clarified] These are two separate archival deposits, not the same holding: the BAnQ Advitam notice (f_0443) documents a distinct 1985 transfer to BAnQ, while Concordia's P145 fonds is the primary Kanawana-relevant collection used throughout this KB. No evidence the BAnQ material duplicates or supersedes the Concordia fonds; it remains a separate, unexplored lead in its own right.

---

[pg] Camp Kanawana parent preparation guides, 2025 and 2026 editions [src_kk_prep_guide_2025, src_kk_prep_guide_2026]. See [f_1828].
