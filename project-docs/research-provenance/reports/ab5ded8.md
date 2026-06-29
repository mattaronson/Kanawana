# Agent ab5ded8

**Task:** Research Lake Wilson at Camp Kanawana in Saint-Adolphe-d'Howard, Quebec. I need information about:

**Tool uses:** 85

---

Now I have enough information to compile a comprehensive research report. Let me compile the findings.

---

## RALPH Research Report: Lake Wilson at Camp Kanawana

### RETRIEVE Phase Summary

**Sources consulted:**
- YMCA Quebec official website (history, facilities, accommodations pages)
- Concordia University Archives -- YMCA of Montreal fonds (P0145), sub-series 12A, 12B
- Grace McMorris MA thesis metadata, Concordia Spectrum repository
- Internet Archive: "A History of Kamp Kanawana 1935" (YMCA of Montreal)
- Internet Archive: Gas Bag 1923 Re-union Number
- Commission de toponymie du Quebec (multiple Lac Wilson entries)
- Canadian Geographical Names Database (NRCan), multiple entries
- CRE Laurentides Atlas des lacs (Lac Wilson entry)
- Mapcarta geographic database (multiple Lac Wilson entries)
- AllTrails (Wilson Lake trail, Mille-Isles)
- Les Amis du Lac Wilson association records
- Existing Kanawana project KB (`/home/user/Kanawana/kb/facts.json`, `/home/user/Kanawana/wiki/places/the-kanawana-site.md`, `/home/user/Kanawana/wiki/chronology/founding-1894.md`)
- QAHN article on YMCA Camp in Saint-Adolphe-d'Howard
- BaladoDiscovery/BaladoDecouverte -- Saint-Adolphe-d'Howard history
- Various real estate and Waze/navigation listings

**Dead ends:**
- WebFetch tool returned 403 errors consistently (Spectrum PDF, Internet Archive, CRE Laurentides, Mapcarta, Concordia AtoM, kanawana.blogspot.com)
- McMorris thesis full text not accessible for keyword search
- No Commission de toponymie entry exists for the specific Lac Wilson at Camp Kanawana or in Saint-Adolphe-d'Howard
- "Spirit of Kanawana" blog not searchable
- No direct naming origin found for any Lac Wilson in the region

---

### ANALYZE Phase: Findings by Research Question

#### 1. Naming Origin of Lake Wilson -- Who Is It Named After?

**Finding: UNKNOWN. No source identified provides the naming origin.**

No publicly available source -- web, archival description, toponymic registry, camp publication, or thesis metadata -- provides the origin of the name "Lake Wilson" at Camp Kanawana or "Lac Wilson" in Saint-Adolphe-d'Howard. The key findings are:

- The 1935 History of Kamp Kanawana (`/home/user/Kanawana/sources/cache/green-triangle/1935-history.txt`, line 84-85) mentions the lake by name ("Lakes Kanawena and Whlson" -- OCR typos for Kanawana and Wilson) in the context of the dam ceremony, but provides no naming context.
- The 1923 Gas Bag (`/home/user/Kanawana/sources/cache/green-triangle/gas-bag-1923.txt`, line 112) lists "Lec Wilson" (OCR for Lac Wilson) as a hike destination alongside other locations like "Page's" and "Ste-Adolphe."
- The Commission de toponymie du Quebec has entries for other Lac Wilsons in Quebec with naming explanations (e.g., Brownsburg-Chatham's was "named after the family who owned the land at the beginning of the 20th century"; Saint-Theophile's was named because "a person named Wilson built a fishing camp there"), but has NO entry for the Saint-Adolphe-d'Howard or Kanawana Lac Wilson.
- The Concordia Archives reference a "Chaplain George S. Wilson" in a speech titled "The Young Adult: Citizen of a New Age" in the YMCA Montreal fonds, and a "Frank Wilson" in a 1911 Quebec City YMCA record. Neither has a demonstrated connection to the lake.
- The Concordia Archives also reference "Dr. Wilson Hume" in World Service records (1952). No connection to the lake.

**Hypothesis:** Given the pattern of other "Lac Wilson" names in Quebec (landowner surnames), the lake was very likely named after a Wilson family who owned or settled the land before the YMCA acquired it from the Page family circa 1910. The lake name would have predated the camp. This is a strong hypothesis but remains UNVERIFIED. The answer may reside in:
- The McMorris thesis full text (not accessible for keyword search)
- Concordia Archives sub-series P0145/12B03 (Land, facilities, equipment, supplies)
- The 1933 Ralph Dawson "History of Kamp Kanawana"
- The R.L. Charlton "Notes regarding Early Days" (1943)
- Cadastral/land registry records for the property before 1910

---

#### 2. Geography of Lake Wilson Relative to Camp Kanawana

**CRITICAL FINDING: There are TWO different lakes named "Lac Wilson" in this region.**

**A. Lac Wilson at Camp Kanawana (the camp's private lake)**
- Located within the 550-acre Camp Kanawana property
- Near coordinates 45.85N, 74.19W (approximate, based on Kanawana area coordinates)
- Administratively in or near Saint-Sauveur / Mille-Isles boundary
- Connected to Lake Kanawana by a dam (fact f_0024 in KB, sourced from 1935 History)
- One of three private lakes: Lake Kanawana, Lake Wilson, and Round Lake
- Mapcarta ID 24440254 places it near Lac-des-Becs-Scie and Mille-Isles, with Lac Kanawana, Lac Rond, and Lac Leonard as nearby features
- AllTrails lists "Wilson Lake via Yellow Trail [PRIVATE PROPERTY]" in Mille-Isles -- 3.2 mi trail, low-rated, marked as private property
- The existing wiki article (`/home/user/Kanawana/wiki/places/the-kanawana-site.md`, lines 19-20) describes it correctly as part of the camp's three lakes
- The founding article (`/home/user/Kanawana/wiki/chronology/founding-1894.md`, line 34) states: "A second lake, Lake Wilson, was within the property, with a dam controlling water levels between the two."

**B. Lac Wilson in Saint-Adolphe-d'Howard (a separate lake)**
- Located at approximately 45.94N, 74.41W (based on Chemin du Lac-Wilson Est geocoding)
- Administratively in Saint-Adolphe-d'Howard, MRC Les Pays-d'en-Haut
- CRE Laurentides lists it at coordinates 45 56'32"N, 74 24'45"W
- Has its own residents' association: Les Amis du Lac Wilson (est. August 12, 2002), headquartered at 124 ch. Parkview, Saint-Adolphe-d'Howard
- Has a road network around it: Chemin du Lac-Wilson Est and Chemin du Lac-Wilson Ouest
- Part of the Organisme de bassin versant de la riviere du Nord watershed
- This is approximately 20-30 km northwest of Camp Kanawana

**These are definitively two separate lakes.** The Lac Wilson in Saint-Adolphe-d'Howard is NOT the one at Camp Kanawana. The initial research question conflated them, which is understandable given that Camp Kanawana's founding history begins at Lake Saint-Joseph in the Township of Howard (now Saint-Adolphe-d'Howard) before moving to the Saint-Sauveur/Mille-Isles site circa 1910.

---

#### 3. Historical References to Lake Wilson in Camp Publications

Three historical references found in cached sources:

1. **1923 Gas Bag** (`/home/user/Kanawana/sources/cache/green-triangle/gas-bag-1923.txt`, line 112): "Commencement of Hike Week. Parties leave for Val Morin, Lac Hughes, Ste.Agathe, Sixteen Island Lake, Lec Wilson, and Page's" -- Lac Wilson listed as a hike destination, implying it was on the property or nearby but considered a destination rather than base camp.

2. **1935 History of Kamp Kanawana** (`/home/user/Kanawana/sources/cache/green-triangle/1935-history.txt`, lines 84-85): "During the afternoon, took the dam which had kept the water in Lakes Kanawena and Whlson at a desirable hieght was let out before the eyes of the assembled camperse" -- Describes the end-of-season dam opening ceremony, confirming the dam connecting Lake Kanawana and Lake Wilson was a camp tradition by 1935.

3. **YMCA Kanawana website (current)**: Lake Wilson described as "one of the most beautiful parts of the site" with "gorgeous views, amazing sunsets, and a great spot for stargazing." Private campsites available. Two-week campers have overnight camping excursions on Lake Wilson.

---

#### 4. Any "Wilson" Associated with YMCA Montreal or Camp Kanawana History

Three individuals named Wilson appear in the Concordia archival descriptions:

1. **Chaplain George S. Wilson** -- Gave a speech titled "The Young Adult: Citizen of a New Age" referenced in YMCA Montreal fonds sub-series 5E05 (Planning and Development Committee). No demonstrated connection to the lake or camp.

2. **Dr. Wilson Hume** -- Referenced in sub-series 14B (World Service), records from 1952. Listed among World Service speakers and correspondents. No demonstrated connection to the lake or camp.

3. **Frank Wilson** -- Referenced in sub-series 14H, associated with Quebec City YMCA and "Twice-Born Men" (1911). No demonstrated connection to the lake or camp.

4. **John Wilson McConnell** (1877-1963) -- Already in the Kanawana KB. A major YMCA Montreal benefactor, philanthropist, publisher of the Montreal Star. While his middle name was Wilson, he is always referred to as "J.W. McConnell" and there is no evidence the lake was named after him. His YMCA involvement dates to 1901 (rented a room at the YMCA), and his major fundraising role was from 1909 onward.

**No Wilson has been identified who has a direct, documented connection to the naming of Lake Wilson.**

---

#### 5. Saint-Adolphe-d'Howard Lake Naming History

- The Township of Howard was created in 1873, named after Frederick Howard, 5th Earl of Carlisle (Commissioner of the Colonies during the American Revolution).
- "Adolphe" refers to Adolphe Jodoin (1836-1891), Cure of Saint-Sauveur-des-Montagnes, who founded the Lac-Saint-Joseph Mission in 1878.
- The municipality has approximately 70-85 lakes in its territory.
- Lake naming in the region generally follows the Quebec pattern: most lakes are named after families who owned land adjacent to them, settlers, or individuals who built camps/cabins there. This is confirmed by Commission de toponymie entries for other Lac Wilsons in Quebec.
- No specific naming registry or comprehensive history of lake names in Saint-Adolphe-d'Howard was found.

---

### HYPOTHESIZE Phase: Follow-Up Research Threads

1. **Highest priority: Access the McMorris thesis full text** (`https://spectrum.library.concordia.ca/id/eprint/992763/1/McMorris_MA_F2023.pdf`). The thesis covers 1894-1967 Kanawana history and likely discusses the property acquisition and lake names. The WebFetch tool could not access it; a direct download should be attempted.

2. **Access the 1933 Ralph Dawson "History of Kamp Kanawana"** at Concordia Archives. This is separate from the 1935 document already cached and may contain earlier and more detailed naming information.

3. **Access Concordia Archives sub-series P0145/12B03** (Land, facilities, equipment, supplies). This sub-series explicitly covers property records and may contain deeds or maps naming the lakes and their origin.

4. **Search Quebec land registry / cadastral records** for the Kanawana property pre-1910 to identify whether a Wilson family owned any portion of the land before the Page family.

5. **Contact the oral history source** (src_oral_aronson in the KB) who is noted as covering "Lake Wilson/Desjardins" as a topic. This person may know the naming origin.

6. **Clarify the geographic distinction** between the two Lac Wilsons for the project wiki. The current Kanawana site article correctly treats Lake Wilson as part of the camp property, but the Saint-Adolphe-d'Howard lake should not be confused with it.

7. **Search for "Wilson" in the 1921 and 1922 brochures** already cached in the project. These early camp publications may mention the lake or a Wilson individual.

8. **Check the 1928 and 1962 Kanawana maps** analyzed in the McMorris thesis for lake naming details.

---

### Key Sources

- [YMCA Quebec - The Kanawana Story](https://www.ymcaquebec.org/en/summer-camp-kanawana/history)
- [YMCA Quebec - Camp Kanawana Facilities](https://www.ymcaquebec.org/en/summer-camp-kanawana/facilities)
- [YMCA Quebec - Camp Kanawana Accommodations](https://www.ymcaquebec.org/en/summer-camp-kanawana/lodging-equipment-rental)
- [MySummerCamps - YMCA Kamp Kanawana](https://www.mysummercamps.com/rentals/Detailed/YMCA_Kamp_Kanawana_L170.html)
- [McMorris Thesis - Concordia Spectrum](https://spectrum.library.concordia.ca/id/eprint/992763/)
- [A History of Kamp Kanawana 1935 - Internet Archive](https://archive.org/details/a-history-of-kamp-kanawana-1935)
- [CRE Laurentides - Lac Wilson](https://crelaurentides.org/lake/wilson/)
- [Concordia Archives - YMCA Fonds Sub-series 12A](https://www.concordia.ca/offices/archives/ymca-fonds-sub-series-12A.html)
- [Concordia Archives - Kamp Kanawana (AtoM)](https://concordia.accesstomemory.org/kamp-kanawana)
- [Commission de toponymie - Lac Wilson, Brownsburg-Chatham](https://toponymie.gouv.qc.ca/ct/ToposWeb/Fiche.aspx?no_seq=451695)
- [Commission de toponymie - Lac Wilson, Saint-Theophile](https://toponymie.gouv.qc.ca/ct/ToposWeb/Fiche.aspx?no_seq=67250)
- [Mapcarta - Lac Wilson (near Kanawana)](https://mapcarta.com/24440254)
- [AllTrails - Wilson Lake via Yellow Trail, Mille-Isles](https://www.alltrails.com/trail/canada/quebec/lac-wilson-via-sentier-jaune)
- [NRCan GeoNames - Lac Wilson](https://geonames.nrcan.gc.ca/search-place-names/unique?id=EJPBD)
- [Les Amis du Lac Wilson - Business Registry](https://b2bhint.com/en/company/ca-qc/les-amis-du-lac-wilson--3360965670)
- [BaladoDiscovery - Saint-Adolphe-d'Howard History](https://baladodiscovery.com/circuits/900/poi/10164/saint-adolphe-d-howard-history)
- [Concordia Archives - YMCA Fonds 5E05](http://www.concordia.ca/offices/archives/ymca-fonds-sub-sub-series-5E05.html)
