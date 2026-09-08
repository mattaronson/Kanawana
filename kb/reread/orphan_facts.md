# Orphan facts — content in the KB that no article reaches

Measured 2026-09-07 under p_492. A fact is listed here when **neither its fact_id nor any of its source
ids appears anywhere under `wiki/`**. That is a strict test and it is still only a PROXY: an article can
carry a fact's content while citing a different source, or citing a source by title with no id at all.
f_5608 is on this list and its content was written into `documents/kanawana-in-media.md` the same day —
the article's footnote 14 gives the Flickr URL without a `[src_]` bracket, so the measure cannot see it.
**Check each entry against the destination before treating it as missing.**

Counts: 5586 facts in all; 238 fully disconnected; 131 of those in method/meta/sources categories, which are
process records and belong nowhere in the wiki; **107 substantive**, listed below.

Null results are deliberately included: a recorded null is content, and an article that does not carry it
cannot tell a searched-and-empty question from an unasked one.

---

## Triage, added 2026-09-07 after working the list: this is not a queue of 107 jobs

**18 of the 107 are now cited; 89 are not.** Before working the rest, note that the list mixes at least
four kinds of record and **only one of them is an article's business**. Triage each entry into one of
these before spending time on it.

**1. Material an article should carry.** The real work. f_1727 (the c.1920s dining-hall photograph) and
f_2391 (the 1964 camper origins) were both this, and both are now in articles.

**2. Nulls about the world.** Keep including these, for exactly the reason above. "The Wikipedia articles
on Saint-Adolphe-d'Howard contain no mention of the YMCA" (f_2196) is a finding about the record, and an
article that omits it cannot distinguish a searched question from an unasked one.

**3. Nulls and notes about *this project's own process*.** These are **not** article material and never
will be. "p_457 worked the same day it was raised" (f_5228), "citation corrected via Crossref"
(f_2222), "a third independent research pass on…" (f_1924), "the near-miss name pairs are now generated
rather than listed" (f_2370). They exist so nobody repeats a search or an argument, and their home is
the priority queue and `logs/pipeline.log`. **The distinction from class 2 is the subject:** a null about
Saint-Adolphe's Wikipedia page is about the world; a null about whether p_457 was worked is about us.

**4. Metadata about the project's holdings.** Flickr photo counts, sub-series extents in centimetres,
finding-aid item titles (f_1475, f_1545, f_2260). These belong in **source records**, not in prose, and
an article that recited them would be describing the filing cabinet instead of the camp.

**A caution on measuring this mechanically.** A classifier keyed on opening phrases ("NULL RESULT",
"CORRECTION") was tried on 2026-09-07 and filed obvious class-3 records as class 1 — f_5116 opens "A
CLEAN NULL, RECORDED SO NOBODY READS IT AGAIN" and was scored a candidate. A scorer that checks whether
a fact's distinctive tokens appear anywhere under `wiki/` was also tried; it was right on the three
entries hand-checked, but a token appearing somewhere in 511,000 words is weak evidence that the *claim*
is there. **Neither number is trustworthy enough to publish, so neither is published here.** What is
published is the four classes and the instruction to sort by hand.

| fact | category | claim (opening) |
|---|---|---|
| `f_1320` | camping_movement | The 109-page university paper 'Mary S. Edgar's Contribution to the Canadian Camping Movement' in the Sundridge-Strong Digital Collection was authored … |
| `f_1321` | people | Mary Susanne Edgar (May 23, 1889 – September 17, 1973) was born in Sundridge, Ontario. She graduated from the National Training School of the YWCA in … |
| `f_1325` | institutional | The Association des camps du Québec (ACQ) was founded in 1961. The QCA (formed 1937 as a CCA provincial unit) and the ACQ appear to be the same organi… |
| `f_1365` | camps | Camp Dorval (P0145/12E, 1926-1928, 0.5cm records) was a short-lived YMCA day camp in Dorval, Quebec (West Island of Montreal). Only 0.5cm of archival … |
| `f_1367` | camps | Camp Perrot (P0145/12G) was a boys' camp operated by Montreal YMCA. A document 'Comparison of Two Boys Camps operated by Montreal YMCA' compares Camp … |
| `f_1371` | biography | Gabor Ivan Zinner, author of the 1973 McGill thesis on Noosphere, is now a lawyer in Calgary, Alberta (Zinner Law Office, 100-1100 8 Ave SW). He pract… |
| `f_1373` | media | Camp Kanawana has 4,416 photos on Flickr (flickr.com/photos/kanawana/) and an active Instagram account (@ymcakanawana, 1,835 followers, 573 posts as o… |
| `f_1413` | camping_movement | The QCA/CCA organized a formal Camping School at McGill University from 1937 to 1940 — one of the earliest camp leader training programs in Canada. A … |
| `f_1414` | camping_movement | McGill PE students attended a 'Camp School' at Camp Nominingue (founded 1925, north of Mont-Tremblant) as part of their curriculum, learning camping, … |
| `f_1415` | camping_movement | Arthur S. Lamb (1886-1958), 'father of modern physical education in Canada', was a former Vancouver YMCA PE director and Springfield College graduate … |
| `f_1420` | traditions | Kanawana's early English motto 'Each for all and all for each' was a shared YMCA camp tradition, not unique to Kanawana. At least two other YMCA camps… |
| `f_1421` | traditions | Camp Kanawana is the only YMCA camp or YMCA-affiliated organization in the world using the motto 'Non Nobis Solum'. The motto is also used by Lower Ca… |
| `f_1422` | traditions | The LCC school song 'Non Nobis Solum' was first sung at the 1936 return-to-school assembly at Lower Canada College. Lyrics by early alumni, melody fro… |
| `f_1423` | traditions | Charles Sanderson Fosbery, LCC founder (headmaster 1909-1935), held a BA in classics from Trinity College Dublin and arrived in Montreal in 1900 as ch… |
| `f_1426` | camping_movement | 'A Log of Canada's Centenary Journey' was published in 1971, likely containing the complete route, sections, and participant roster for the CCA Centen… |
| `f_1431` | geography | The Kanawana dam between Lake Kanawana and Lake Wilson does NOT appear in the CEHQ (Centre d'expertise hydrique du Québec) répertoire des barrages. Th… |
| `f_1432` | people | Joanna Hode/Houde (director 1995-2000 per oral history) has zero web presence connecting her to Camp Kanawana, YMCA, or any camp director role. 25+ di… |
| `f_1434` | people | Mabel C. Jamieson was NOT a founding member of the Ontario Camping Association (1933). OCA founding members included Ferna Halliday, A.L. Cochrane, H.… |
| `f_1435` | people | The 'Pupils College in Richmond' where Mabel C. Jamieson reportedly studied (completing 1918) is unidentifiable. St. Francis College in Richmond, Queb… |
| `f_1436` | people | The Comité des seize (Committee of Sixteen) in Montreal, of which Mabel C. Jamieson was a member, was founded in 1917 (not 1919 as sometimes reported)… |
| `f_1437` | people | Rev. John Tudor Harries (B.A., M.Div.) listed Camp Kanawana as an early career formative experience, alongside Manor Road United Church, Central Neigh… |
| `f_1438` | people | George Clouston (d. 2011) was described in his obituary as having been 'an enthusiastic volunteer and member' of the YMCA and its Kamp Kanawana 'as a … |
| `f_1439` | people | Douglas Warren Marston (c.1918-2011) attended Kamp Kanawana as a 'junior summer camp' participant. He died November 14, 2011 in his 94th year.… |
| `f_1452` | institutions | Pascale Audette was named President and CEO of the YMCAs of Québec effective January 6, 2025 — the first woman to hold this position in the organizati… |
| `f_1453` | people | Karen Louise Deterding (d. August 22, 2014, age 57, of pancreatic cancer) was described in her obituary as being deeply missed by 'friends from Kamp K… |
| `f_1454` | people | Mike Cohen, Montreal media personality, Côte Saint-Luc city councillor, and columnist for The Suburban newspaper, attended Camp Kanawana as a child an… |
| `f_1455` | people | Hedley S. Dimock created and directed Summer Camp Institutes from 1930 to 1948 at the George Williams College Lake Geneva campus, examining the role o… |
| `f_1457` | people | Raye Kass presented 'Leadership on a hot tin roof: Applications for Camp Professionals' at the 8th International Camping Congress, October 4-7, 2008, … |
| `f_1466` | media | The Montreal Gazette published an article about YMCA Summer Camp Kanawana on July 7, 1897, just three years after the camp's founding.… |
| `f_1467` | programs | In July 1913, detachments of Montreal YMCA boys left the city for Kamp Kanawana, with a programme for boys aged 3 to 17 that included instruction in a… |
| `f_1468` | programs | In July 1918, Camp Kanawana had the largest attendance in its history with 110 members in camp, and instruction included first aid work, basket-making… |
| `f_1469` | traditions | In August 1942, YMCA boys staged a parade and circus at Kanawana, with 'Games of Luck and Skill' entertaining campers at a week-end festival.… |
| `f_1470` | programs | In November 1962, citizenship training and educational programs for youth and young adults were planned at Kamp Kanawana.… |
| `f_1471` | people | Sean Day was the regional director of camps for YMCA Québec (as of 2021).… |
| `f_1472` | chronology | Camp YMCA Kanawana was closed for a second consecutive year in 2021 due to COVID-19. Sean Day said offering overnight services to more than 250 camper… |
| `f_1473` | chronology | Camp YMCA Kanawana held a 120th anniversary reunion on September 5, 2014, at Victoria Hall, where alumni (former campers and staff) assembled to celeb… |
| `f_1474` | chronology | Camp YMCA Kanawana held a 125th anniversary Family, Alumni, and Friends Weekend in 2019.… |
| `f_1475` | media | YMCA Camp Kanawana maintains a Flickr photostream with 4,416 photos documenting camp activities and history.… |
| `f_1477` | chronology | As of fall 2025, YMCA Québec will no longer offer day camps (including holiday and spring break camps), but Camp YMCA Kanawana summer camp continues t… |
| `f_1488` | people | A Globe and Mail arts piece ('Stuart McLean's bent vision,' c.2003) described McLean's time as a counsellor at Camp Kanawana in his 20s as 'at once ma… |
| `f_1492` | people | Kevin Slezak served as Assistant Director of Camp YMCA Kanawana, then as Sleep-Away Camp Director and Summer Camp Director at YMCA Quebec. As of 2025,… |
| `f_1494` | programs | EMSB (English Montreal School Board) schools including Vincent Massey Collegiate (Rosemount), John F. Kennedy High School (St. Michel), and École Seco… |
| `f_1495` | media | The 'Spirit of Kanawana' blog (kanawana.blogspot.com) is an alumni-run blog dedicated to sharing Kanawana history and traditions, inviting contributio… |
| `f_1496` | traditions | The Spirit of Kanawana blog reports that lost verses of a camp song were rediscovered in the Kanawana Archives at Concordia University in 2006, and th… |
| `f_1522` | people | The name 'Dawson' does not appear anywhere in the retrieved text of the Concordia YMCA of Montreal fonds finding aid, despite Ralph Dawson's authorshi… |
| `f_1523` | institutional | The Westmount Branch and North Branch of the Montreal YMCA both opened in 1912.… |
| `f_1525` | institutional | The 1976 Lovell's Directory lists the Kamp Kanawana office at 1441 Drummond, Montreal (H3G 1WS, tel. 849-5331), with a second location in Chateauguay … |
| `f_1526` | programs | The Sherbrooke Record (July 21, 1972) reported a three-day counsellor leader training program at Camp Kanawana.… |
| `f_1528` | programs | Le Droit (Ottawa), June 25, 1937, reported a first aid instructor going to Camp Kanawana on July 1.… |
| `f_1529` | programs | The Westmount Examiner (November 16, 1962) reported citizenship training planned at Kamp Kanawana.… |
| `f_1545` | documents | The official 'Kanawana' Flickr account holds 4,416 photos in 33 albums (joined 2010). A 'University Concordia Archives' album contains 34 digitized ar… |
| `f_1546` | documents | The Concordia Records Management/Archives Flickr holds two ca.1910 Kanawana photos: a flag-raising ceremony captioned 'FLAG RAISING KAMP KANAWANA / MO… |
| `f_1547` | people | FamilySearch record for Mabel Grace Jamieson (b. 8 Nov 1893, Canada; d. 9 Mar 1966, Osoyoos BC; married name Mooney; resided Megantic QC per 1911 cens… |
| `f_1551` | context | Tamaracouta Scout Reserve (founded 1912) claims to be the oldest continuously running Scout camp in the world — regional camping context for the Laure… |
| `f_1571` | people | A Concordia Archives photograph (captioned 'Pop Cameron and the Canoe Trippers') shows a group of boys and men with canoes and packs posed around a ca… |
| `f_1572` | geography | The 1941 hand-drawn Kanawana camp map (three near-identical copies in the archive) carries printed travel directions: 'Kanawana is situated about five… |
| `f_1573` | facilities | A Kamp Kanawana site map (dated by the archive to 1980-2001) labels facilities around Lac Kanawana including a Fitness Course, Ball Field, Hospital, L… |
| `f_1574` | founding | A 1982 print advertisement for Kamp Kanawana states: 'In 1894 the Y.M.C.A. pioneered camping in the Laurentians by opening the first boys camp in Cana… |
| `f_1575` | programs | A 1981 advertisement for 'Les Voyageurs de la Vérendrye' — described as 'excursions en canoë pour les jeunes de 13 à 17 ans' / 'extended wilderness ca… |
| `f_1576` | media | A handwritten 1970s ad-planning sheet for Kamp Kanawana reads: 'YMCA summer camp. Kamp kanawana for boys + girls age 7-15. Some places still available… |
| `f_1577` | events | A 1913 Kamp Kanawana reunion banquet menu card, dated 'Wednesday, Nov. 26th, 1913' and printed on autumn-leaf themed paper, is headed 'Kamp Kanawana K… |
| `f_1578` | events | A silkscreen printing film for a 'Kamp Kanawana Reunion, April 7th, 1989' marks the camp's founding-to-reunion span as '1894-1989' (i.e. a 95th-annive… |
| `f_1579` | facilities | A cyanotype architectural blueprint titled 'Proposed Service Wing to Dining Hall, KAMP KANAWANA Y.M.C.A.' is signed 'J.M. Venters, Architect, 1503 Mac… |
| `f_1580` | camp_culture | Camp staff produced hand-drawn t-shirt and silkscreen art across the 1980s-1990s with recurring motifs of Pacific Northwest Coast-style masks/totems (… |
| `f_1582` | traditions | A scrapbook page captioned 'Awards, Circa 1940' documents the camp's felt-badge award hierarchy in period handwriting: a maroon triangle with an embro… |
| `f_1583` | organizations | A felt badge reads 'KANAWANA OUTING CLUB' around a central YMCA triangle logo, evidencing a camp 'Outing Club' distinct from the main honour-award sys… |
| `f_1584` | traditions | A felt YMCA pennant reads 'Y.M.C.A.' in large vertical lettering with a shield crest bearing the banner text 'KAMPKANAWANA' (run together, no space) a… |
| `f_1727` | facilities | A Concordia Archives photograph of the interior of a long open-sided dining pavilion (dated c.1920s) shows a hanging banner reading 'KAMP KANAWANA' an… |
| `f_1776` | chronology | Alfred Sandham's 'History of the Montreal YMCA' (1873, covers 1851-1860) and the YMCA of Montreal's 1889-90 Annual Report both contain no references t… |
| `f_1924` | people | A third independent research pass on Joanna Hoad's post-Lower Canada College life and pre-Kanawana history (21 queries across WebSearch, WebFetch, Fac… |
| `f_2069` | people | UNCONFIRMED IDENTIFICATION: the "Advance Guard '63" dining-hall plaque names a "Rick Patten" alongside Julien Tasse, Wally Leemans, Rusty McKay, Buppy… |
| `f_2196` | site | NULL RESULT (p_263): the Wikipedia articles on Saint-Adolphe-d'Howard, in both English and French, contain NO mention of the YMCA, Camp Otoreke, Camp … |
| `f_2197` | site | Saint-Adolphe-d'Howard, the municipality containing the camp's ORIGINAL 1894-1909 site, is described as 'located on the shores of lake Saint-Joseph' a… |
| `f_2198` | site | Lac Kanawana is recorded at approximately 45.85 N, -74.20 to -74.19 W, in the MRC Les Pays-d'en-Haut, Quebec. A commercial nautical-chart aggregator g… |
| `f_2200` | traditions | NULL RESULT (p_263): the Camp Sloane YMCA Songbook (Lakeville, Connecticut) was downloaded and read in full -- 21,398 characters, 17 songs. It contain… |
| `f_2201` | traditions | STRUCTURAL COMPARATOR (p_263): Camp Sloane's 'Alma Mater' follows a lake-and-campfire anthem form -- 'Just beside Wanapakok / With her waves of blue /… |
| `f_2202` | traditions | NULL RESULT (p_263): 'The Song Book of the Y.W.C.A.', compiled by Imogene B. Ireland with the Music Committee of the National Board of the YWCA, 172 p… |
| `f_2206` | site | The QAHN photograph 'Camp Otoreke (YMCA Camp), Saint-Adolphe-d'Howard, 1944' is an old photographic postcard whose verso, transcribed by QAHN, reads: … |
| `f_2207` | site | QAHN's historical note on the Otoreke photograph, credited to the Concordia University Archives, records the site's post-1910 career: after the YMCA's… |
| `f_2211` | people | Stuart McLean arrived at Camp Kanawana as a counsellor in the summer of 1969 'in the Senior Boys Section' and worked there 'for five summers in the la… |
| `f_2216` | people | The Association des camps du Quebec reported on 14 March 2023 that 18 new English-language songs would be added to its 'Repere culturel' repertoire in… |
| `f_2217` | connections | Camp Weredale, a Montreal camp for children in care, was established in 1934 as a 'summer home away from home' for the orphaned or at-risk boys living… |
| `f_2219` | people | NULL RESULT (p_263), the whole Terry Mosher cluster: six sources -- Wikipedia, The Canadian Encyclopedia, the Canada Post stamp feature, the Concordia… |
| `f_2220` | people | CORRECTION TO A RESEARCH FLAG (p_263): a research agent, working without access to this wiki, flagged the Hamilton 'Ed Smee' of the Conserver Society … |
| `f_2221` | people | The Ed Smee Conserver Society Environmental Fund: the Conserver Society of Hamilton and District was established in 1983; its first Environmental Trus… |
| `f_2222` | people | CITATION CORRECTED AND COMPLETED via Crossref (tandfonline itself refuses automated clients): Twynam, G. David; Farrell, Jocelyn M.; Johnston, Margare… |
| `f_2223` | people | G. David Twynam's post-Kanawana academic career now has two fixed points: his 2002 co-authors place him at Lakehead University's School of Outdoor Rec… |
| `f_2224` | traditions | NULL RESULT (p_263), the 1967 Centennial Voyageur Canoe Pageant cluster: the Canadian History Ehx transcript, the Guysborough Journal feature, the Eri… |
| `f_2225` | connections | The 1967 Centennial Voyageur Canoe Pageant ran from Rocky Mountain House, Alberta on 24 May 1967 to Montreal on 4 September 1967 -- 104 days, 5,283 km… |
| `f_2229` | people | TWO DOCUMENTED-VS-DOCUMENTED DISCREPANCIES in Terry Mosher's public record, noted for accuracy but NOT raised as conflict records because neither touc… |
| `f_2231` | documents | MAJOR FIND (p_263): Trent University Archives holds a KANAWANA CAMP BROCHURE DATED 1940 -- Ontario Camps Association fonds, accession 72-007, Series 1… |
| `f_2232` | documents | Trent University Archives ALSO holds a Kanawana brochure from circa the 1970s -- Ontario Camping Association fonds, accession 78-006, Series F (Camp L… |
| `f_2241` | connections | NULL RESULT (p_263) with real adjacent content: Canadian Camping Magazine Vol 11 No 2 (February 1959) contains NO reference to Kanawana across 108KB o… |
| `f_2243` | traditions | SCOPE-LIMITED NULL (p_263): the Library of Congress Cooperative Recreation Service collection (AFC 2016/051, 1924-2011, donated by Bruce Greene) shows… |
| `f_2245` | history | THE 1918 SEASON IN DETAIL, from the Gazette of 27 July 1918 (recovered via Google Books after newspapers.com blocked access): 'At the Y.M.C.A. boys' c… |
| `f_2246` | people | TWO NEW 1918 STAFF NAMES from the same Gazette report: 'the camp cook is Mr. Harry Smith, from the Montreal High School, and being well acquainted wit… |
| `f_2260` | traditions | P145/12B07 (Kamp Kanawana - Program) lists the camp's own culture files, several earlier than anything this wiki currently cites: "Place mat or paper … |
| `f_2261` | history | P145/13B (Anniversaries) holds a file group headed "World Y 50th Jubilee, Montreal Y 50th" containing "Jubilees. - 1893, 1894, 1901", alongside "42nd … |
| `f_2370` | people | THE NEAR-MISS NAME PAIRS IN THE PLAQUE INDEX ARE NOW GENERATED AND EVIDENCED RATHER THAN LISTED (scripts/plaque/candidate_pairs.py, kb/plaque-audit/ca… |
| `f_5043` | organization | WHAT THE ASSOCIATION'S OTHER SUMMER LOOKED LIKE IN 1971, AND IT IS NOT A CAMP IN THE WOODS. 'Rapport ete 71, Projet La Petite Bourgogne, Camp de langu… |
| `f_5116` | institutional | A CLEAN NULL, RECORDED SO NOBODY READS IT AGAIN: 'SUBMISSION: THE MILE-END FRANCOPHONE PROJECT', MARCEL VEILLEUX, Director, April 1972. 'KANAWANA' OCC… |
| `f_5163` | founding | THE MUNICIPALITY OF SAINT-ADOLPHE-D'HOWARD DATES THE YMCA'S ARRIVAL ON THE ISLAND TO 1893, AND IT IS NOT EVIDENCE AGAINST 1894. Its 'Patrimoine' page:… |
| `f_5222` | site | THE AUTUMN 1978 WORKS AT KANAWANA, FROM THE NEWSLETTER THAT REPORTED THEM WHILE THEY WERE HAPPENING. Ka-News for October 1978: "at Kamp, we are in the… |
| `f_5223` | staff | THE CAMP TIGHTENED UP FOR 1979, AND SAID SO IN WRITING TO ITS OWN STAFF. Ka-News for December 1978 lists four changes: counsellor salary range increas… |
| `f_5228` | media | p_457 WORKED THE SAME DAY IT WAS RAISED. THE MAGAZINE IS ALMOST CERTAINLY 'OUTDOOR CANADA', NOT 'OUTDOORS CANADA'. Ka-News of December 1978 writes "'O… |
| `f_5244` | institutional | THE CAMPS WERE THEIR OWN FUNDRAISING UNITS IN THE NATIONAL YMCA'S OVERSEAS PROGRAMME. A sample of nine of the forty-seven unread texts was pulled to t… |
| `f_5608` | documents | THE CAMP'S FLICKR ACCOUNT LISTS TWENTY-FOUR ALBUMS, AND THE TWO THIS PROJECT WORKS FROM ARE NOT AMONG THEM. flickr.com/photos/kanawana/albums fetched … |
