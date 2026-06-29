# Agent a743e0adae1ab0b55

**Task:** You are researching archival materials for the Kanawana Wiki project. Your task is to search Concordia Univers

**Tool uses:** 74

---

Good - both YouTube videos are already tracked. Now I have a comprehensive picture. Here is my final report.

---

## Concordia University Library Systems Research Report: YMCA of Montreal Fonds (P0145) and Camp Kanawana Materials

### 1. Concordia Library Main Catalog

- **URL attempted**: `https://library.concordia.ca/find/search.php?q=kanawana`
- **Result**: HTTP 403 Forbidden. The Concordia library search interface blocks automated web fetches. Not accessible via WebFetch.
- **Alternative**: The library's Special Collections page at `https://library.concordia.ca/find/special-collections/archival-fonds.php` lists the YMCA of Montreal fonds. Physical consultation is available at the Vanier Library Special Collections Reading Room on the Loyola Campus (514-848-2424 ext. 7762, spec-coll@concordia.ca).

### 2. Spectrum (Concordia's Institutional Repository)

- **URL attempted**: `https://spectrum.library.concordia.ca/id/eprint/992763/`
- **Result**: HTTP 403 Forbidden. Direct fetch blocked.
- **However**, web search confirmed the thesis exists and is cataloged:
  - **Title**: "An Experience That Lasts a Lifetime: Building Modernity, Man, and Nation at the YMCA of Montreal's Kamp Kanawana, 1894-1967"
  - **Author**: Grace McMorris
  - **Date**: 2023 (Fall)
  - **Supervisor**: Dr. Peter Gossage
  - **Committee**: Dr. Elena Razlogova (chair), Dr. Gavin Taylor, Dr. Theresa Ventura
  - **Abstract**: Explores summer camps as sites of masculine and national identity construction through three thematic chapters: active Christian citizenship, playing Indian, and the myth of the voyageur. Covers 1894-1967.
  - **Already in project**: Yes, as `src_mcmorris_thesis` with 185,000 chars, fully extracted (148 facts).
  - **Also indexed on**: CORE (`https://core.ac.uk/outputs/591919397/`) and Erudit.

### 3. Concordia Archives / Access to Memory (AtoM) Database

- **URLs attempted**: `https://concordia.accesstomemory.org/` and various sub-pages
- **Result**: All returned HTTP 403 Forbidden via WebFetch. However, web search extracted substantial catalog information.

#### Fonds Structure (Series 12 - Camps)

The YMCA of Montreal fonds (P0145) Series 12 contains these camp-related sub-series:

| Sub-series | Description |
|---|---|
| P0145/12A | Camping - Committees (general camp administration) |
| P0145/12B | **Kamp Kanawana** (the primary target) |
| P0145/12C | Camp Otoreke |
| P0145/12F | Camp Weredale |
| P0145/12G | Camp Perrot |
| P0145/12L | Lac St-Joseph / Camp Jubilee (earliest camp, 1893) |

#### Kamp Kanawana Sub-series (P0145/12B) Structure

| Sub-sub-series | Description |
|---|---|
| P0145/12B01 | General administration |
| P0145/12B02 | Financial administration |
| P0145/12B03 | Land, facilities, equipment, supplies |
| P0145/12B04 | **Communications** (brochures, newsletters, photographs, AV) |
| P0145/12B05 | Staff, counsellors |
| P0145/12B06 | Campers |
| P0145/12B07 | Program |

#### Key Materials Identified in P0145/12B04 (Communications)

From the finding aid (via search results, not direct page access):

**Camp Newsletters/Publications**:
- "The Gas Bag" - K.K.'s official paper, 1923
- "The Green Triangle" - Kamp Kanawana Kampers' newsletter, 1932-1940
- "Ka-News" - staff newsletter, 1976-1982

**Camp Brochures** (dates confirmed in finding aid): 1921, 1922, 1923, 1928, 1929, 1931, 1935, 1938, 1939, 1941, 1942, 1943, 1945, 1946

**Audiovisual**:
- "Kamp Kanawana: The Experience that Lasts a Lifetime" - colour VHS, 9 min (1993, directed by Cathy Reeves)
- "News and Kamp Kanawana" - VHS videocassette, 15 min
- Kanawana promotional audiovisual materials (videocassettes and audio cassettes)
- Film reel: 1960s silent camp footage (P0145-09-0087)

**Photographs**: Kanawana photographs (approx. 1936 and undated)

**Other Documents**:
- "Kamp Kanawana Facts-timeline 1894-1998"
- "Report of First Year of Camp" (1910)
- "Annual Report-Kamp Kanawana for Season 1921"
- "Report of Junior Camp" (1909)
- "History of Kamp Kanawana, by Ralph Dawson, 1933"
- "Comparison-Kamp Kanawana and Camp Perrot" (1953-1954)
- "Proposed two-site operation-Kanawana and Weredale" (1977)
- Situation reports profiling Kanawana, Camp Otoreke, and Camp Weredale
- YMCA Camping Research Project (1960) - "Interpretation of Score for Counselors"
- Kanawana orienteering map (6 photocopies, 1974)
- Tear sheets from local newspapers with Kanawana advertisements

#### AtoM Browse Interface
- `https://concordia.accesstomemory.org/informationobject/browse?repos=399&sortDir=desc&sort=alphabetic&media=print` shows 202 results with print media in the YMCA fonds
- `https://concordia.accesstomemory.org/kamp-kanawana` - direct landing page for Kanawana sub-series
- `https://concordia.accesstomemory.org/ymca-of-montreal-fonds-2;rad` - full fonds description in RAD format

### 4. Internet Archive - Digitized P0145 Materials

The following items from the `ymca-montreal-fonds` and `rma-concordia-publications` collections on Internet Archive are confirmed accessible. Items marked "NEW" are not yet in the project's `sources.json`.

#### Already Tracked in Project

| Item | IA Identifier | Upload Date | Status |
|---|---|---|---|
| A History of Kamp Kanawana 1935 | `a-history-of-kamp-kanawana-1935` | 2024-04-25 | Extracted |
| Kamp Kanawana Brochure 1921 | `1921-kamp-kanawana-brochure` | N/A | Extracted |
| Kamp Kanawana Brochure 1922 | `1922-kamp-kanawana-brochure` | N/A | Extracted |
| Kanawana: The YMCA Camp for Boys 12-17 (1923) | `1923-kanawana-the-ymca-camp-for-boys-12-17-in-the-laurentians-brochure` | 2024-04-26 | Extracted |
| The Green Triangle, July 29, 1938 | `the-green-triangle-1938-07-29` | 2024-04-25 | Extracted |
| YMCA Kamp Kanawana Broadcast - CFCF (1941) | `1941-06-26-ymca-kamp-kanawana-broadcast-station-cfcf` | 2024-04-29 | Extracted |
| Ka-News, May 1980 | `ka-news-1980-05` | N/A | Extracted |
| A Short History of Canadian YMCA 1851-1944 | `1851-1944-a-brief-history-of-the-canadian-ymca` | 2025-01-08 | Extracted |
| YMCA Kamp Kanawana Facts | `ymca-kamp-kanawana-facts` | N/A | Extracted |
| The Gas Bag, 1923 | `the-gas-bag-1923-09-01` | N/A | Extracted |
| Historical Sketch of YMCA Montreal 1901 | `historical-sketch-ymca-of-montreal-1901` | N/A | Tracked |
| History of Montreal YMCA (1873) | `ymca-history-1873` | N/A | Tracked |
| YMCA Annual Report 1889-1890 | `sgw-ymca-annual-report-1889-1890` | N/A | Tracked |
| YMCA Annual Report 1891-1892 | `sgw-ymca-annual-report-1991-1992` | N/A | Tracked |

#### NEW - Not Yet in Project Sources

| Item | IA Identifier | Upload Date | Priority |
|---|---|---|---|
| **YMCA Annual Report 1856** | `sgw-ymca-annual-report-1856` | N/A | Low (pre-camp era, but institutional context) |
| **YMCA Annual Report 1876** | `sgw-ymca-annual-report-1876` | N/A | Medium (may contain early outdoor program references) |
| **YMCA Annual Report 1993** | `sgw-ymca-annual-report-1993` | N/A | **HIGH** (centennial year! May contain 1994 centennial planning, camp status) |
| **Volleyball** (photograph) | `P0145-02-1487` | N/A | Low (general YMCA, not camp-specific) |
| **YMCA Swimming Pool** (photograph) | `P0145-02-0036` | 2024-06-18 | Low (general YMCA building photo) |
| **Basketball** (photograph) | `P0145-02-2745` | N/A | Low (general YMCA) |
| **YMCA Course** (photograph) | `P0145-02-1333` | 2024-07-05 | Low (general YMCA) |
| **Senior Gym Class** (photograph) | `P0145-02-2301` | 2025-01-27 | Low (general YMCA) |
| **Gym** (photograph) | `P0145-02-2098` | 2025-01-27 | Low (general YMCA) |
| **Wrestling** (photograph) | `P0145-02-2547` | 2025-02-05 | Low (general YMCA) |
| **Badminton** (photograph) | `P0145-02-2494` | N/A | Low (general YMCA) |
| **Gramophone Concert in Parlors** (photograph) | `P0145-02-0035` | 2024-06-18 | Low (general YMCA) |

### 5. YouTube Videos (from Concordia Archives)

Both already tracked in the project:
- "YMCA: Kamp Kanawana (no sound)" - 1960s silent film, `https://www.youtube.com/watch?v=ZrUuQ1SU7q8`
- "YMCA Kamp Kanawana: The Experience that lasts a lifetime" - 1993 documentary, `https://www.youtube.com/watch?v=_bznoSFg3MU`

### 6. Key Findings and Recommendations

**Most Actionable New Source**: The **YMCA Annual Report 1993** (`sgw-ymca-annual-report-1993`) is the highest-priority new discovery. This is from the centennial planning period and could contain significant information about Kanawana's status, the upcoming 1994 centennial celebration, institutional structure, and contemporary programming. It should be ingested and extracted immediately.

**Digitization is Ongoing**: Concordia's Records Management and Archives has been actively uploading materials to Internet Archive throughout 2024-2025. Items uploaded as recently as February 2025 (photographs). More camp-specific materials may appear in future uploads.

**Physical-Only Materials**: The vast majority of P0145/12B materials (camp administration, financial records, staff/counsellor records, camper records, program documentation) remain physical-only, accessible only at the Vanier Library Special Collections Reading Room. Key undigitized items include:
- Ralph Dawson's "History of Kamp Kanawana, 1933" (distinct from the 1935 document on IA)
- The 1953-1954 Kanawana/Camp Perrot comparison
- The 1977 two-site operation proposal
- The 1960 camping research project materials
- Staff and camper records
- The full run of The Green Triangle (1932-1940, only one issue digitized)
- The full run of Ka-News (1976-1982, only one issue digitized)

**Access Barrier**: Both the Concordia library catalog (`library.concordia.ca`) and the AtoM database (`concordia.accesstomemory.org`) blocked all WebFetch attempts with 403 errors. These sites appear to have bot-protection that prevents automated access. The finding aid content was only recoverable via web search result snippets.
