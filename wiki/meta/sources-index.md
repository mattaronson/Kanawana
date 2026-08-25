# Sources and Archives

*Status: E1-reviewed | Sources: 643 (this article catalogs the project's sources; see Source Statistics, below)*
*Last Updated: 2026-07-10*

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
access; the technical control contradicts the policy. This project's position is recorded plainly:
the challenge can only be passed by asserting `webdriver=false`, and **an automated client will not
forge that flag**. An honest declaration was tried and refused. AtoM therefore requires an
operator-side fetch or a direct request to `archives@concordia.ca`.

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
| Total facts | 1941 |
| Fact categories | 77 (stale tally, not recomputed) |
| KB version | v5.07 |

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
