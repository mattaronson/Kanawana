# Agent abc6c1a

**Task:** Perform an R3 VERIFY pass on the article at /home/user/Kanawana/wiki/places/the-kanawana-site.md.

**Tool uses:** 40

---

Now let me verify the source count. The articles.json says 12 sources_cited, the article header says "Sources: 14", and I count 15 footnotes in the Sources section (^1 through ^15). Let me also check the article's `sources_cited` list in articles.json against the actual sources in the article.

The articles.json `sources_cited` list is:
```
src_ymca_website, src_kanawana_facts, src_brochure_1921, src_brochure_1922, 
src_gas_bag_1923, src_green_triangle_1938, src_mcmorris_thesis, src_concordia_fonds, 
src_wikidata_lac_kanawana, src_lapresse_ymca_2018, src_weredale_camp, src_mysummercamps_kanawana
```

That's 12 sources. The article text has 15 footnotes but several reference the same underlying source (e.g., ^1, ^7, ^9 all reference the YMCA website). So 12 unique sources is correct, but the header says "Sources: 14" which is wrong -- it should say 12 or 15 depending on whether we count unique sources or footnotes.

Now let me also check for another issue I noticed -- on line 30, the article says Centre Camp has "small cabins without electricity or plumbing" (from f_0028, user_knowledge) and then immediately says "The camp has 12 cabins with electricity" (from f_0452, YMCA website). These are NOT contradictory -- f_0028 describes Centre Camp specifically, while f_0452 describes the Woodsmen and Pioneers sections which may be distinct from the "Centre Camp" of f_0028. But the placement under the Centre Camp heading is confusing -- the 12 cabins with electricity are in Woodsmen/Pioneers sections, which may or may not be in Centre Camp. Let me flag this as a clarity issue.

Here is the complete fix list.

---

## Complete Fix List for `/home/user/Kanawana/wiki/places/the-kanawana-site.md`

### FIX 1 — Distance from Montreal [MAJOR factual error]

**Line 8, exact text to change:**
```
approximately 70 km north of Montreal
```
**Change to:**
```
approximately 90 km north of Montreal
```
**Reason:** KB fact f_0022 (source: src_ymca_website, confidence: stated) says "approximately 90km north of Montreal." The article's "70 km" appears to be derived from the 1922 brochure's "45 miles" (f_0027), which is approximately 72 km by the historical railway route. The YMCA website's current figure is 90 km by road. These are different measurements and should not be conflated. The Overview should use the current authoritative figure.

---

### FIX 2 — Lake Wilson outpost camp misclassification [MAJOR factual error]

**Line 20, exact text to change:**
```
In 1923, Lake Wilson was an outpost camp destination.^6
```
**Change to:**
```
In 1923, Lac Wilson was among the hike destinations from camp.^6
```
**Reason:** KB fact f_0312 (source: src_gas_bag_1923, confidence: stated) says "Outpost camps in 1923 included Otoreke (senior camp) and Lake Marois." Lake Wilson is NOT listed. KB fact f_0313 (same source) lists "Lac Wilson" as a **hike destination**, not an outpost camp. Line 39 of the article itself correctly states the outpost camps were Otoreke and Lake Marois, making line 20 internally inconsistent as well.

---

### FIX 3 — Unsourced "45 minutes" driving time [MODERATE]

**Line 12, exact text to change:**
```
The camp is situated approximately 45 minutes north of Montreal by road, or about 45 miles (72 km) by the historical railway route.^4
```
**Change to:**
```
The camp is situated approximately 90 km north of Montreal by road,^1 or about 45 miles (72 km) by the historical railway route.^4
```
**Reason:** No KB fact establishes a driving time of "45 minutes." The "45 minutes" claim is unsourced and the footnote ^4 (1921 brochure) cannot be its source. Replacing it with the YMCA website's "90 km" figure (f_0022, cited as ^1) provides a sourced claim. The historical railway distance of 45 miles from f_0027 (src_brochure_1922, cited as ^5 not ^4) remains valid, but the footnote should be ^5 not ^4.

**Additionally**, the footnote on the railway distance should be ^5, not ^4:
```
by the historical railway route.^4
```
should be:
```
by the historical railway route.^5
```
because the 45-mile figure comes from the 1922 brochure (source ^5, f_0027), not the 1921 brochure (source ^4, f_0026).

---

### FIX 4 — Misattributed footnote on 1910 purchase [MODERATE]

**Line 8, exact text to change:**
```
The YMCA purchased the current site near Saint-Sauveur in 1910,^4
```
**Change to:**
```
The YMCA purchased the current site near Saint-Sauveur in 1910,^1
```
**Reason:** Footnote ^4 is the 1921 brochure (src_brochure_1921). The KB facts supporting the 1910 purchase date are f_0014 (src_ymca_website), f_0479 (src_kanawana_facts), and f_0004 (src_history_1935). None of them cite the 1921 brochure. The YMCA website (^1) is the strongest attribution since f_0014 directly states the date and source.

---

### FIX 5 — "1920s" should be "1923" [MINOR date imprecision]

**Line 12, exact text to change:**
```
Hike destinations from camp in the 1920s included
```
**Change to:**
```
Hike destinations from camp in 1923 included
```
**Reason:** KB facts f_0313 and f_0476 (both from src_gas_bag_1923) specify 1923. The footnote ^6 is the 1923 Gas Bag. The article should match the source's precision.

---

### FIX 6 — Missing "golf course" and "tents with wood floors" in Historical Facilities [MINOR omission]

**Line 69 (after "- Icehouse"), add two new list items:**
```
- Golf course
- Tents with wood floors
```
**Reason:** KB fact f_0031 (source: src_history_1935, confidence: stated) lists the full facility inventory as "2 pavilions, boats and canoes, 4 diving boards, a zinc slide, chapel, Council Ring, icehouse, **golf course**, and **tents with wood floors**." The article includes every other item from this list but omits these two.

---

### FIX 7 — Missing "Indian characters" on maps [MINOR omission]

**Line 71 (after the "Indian Grave" line), change:**
```
- An "Indian Grave" marking on the camp map
```
**to:**
```
- An "Indian Grave" marking on the camp map; Indian characters were also depicted on camp maps
```
**Reason:** KB fact f_0229 (source: src_mcmorris_thesis, confidence: stated) is in the article's kb_facts_used list but is not reflected in the text. Fact f_0228 (Indian Grave) and f_0229 (Indian characters) are separate facts from the same source.

---

### FIX 8 — Source count in header [MINOR metadata error]

**Line 3, exact text to change:**
```
*Status: draft | Sources: 14*
```
**Change to:**
```
*Status: draft | Sources: 15*
```
**Reason:** The article has 15 numbered footnotes in the Sources section (^1 through ^15). The header says 14. The articles.json lists 12 unique sources, but the article header should reflect the footnote count as displayed, which is 15. (Alternatively, if the convention is unique source count, change to 12, but 14 matches neither.)

---

### FIX 9 — Confusing placement of cabin inventory under Centre Camp [MINOR clarity]

**Line 30** mixes two different KB facts under the Centre Camp heading in a way that appears contradictory. The first sentence (from f_0028) says Centre Camp has "small cabins without electricity or plumbing." The second sentence (from f_0452) says "The camp has 12 cabins with electricity in the Woodsmen and Pioneers sections." This juxtaposition implies the electrified cabins are in Centre Camp, but f_0452 places them in Woodsmen/Pioneers sections, which are separate section names. Recommended fix:

**Line 30, change:**
```
Small cabins without electricity or plumbing, along with platform tents — the traditional camping experience.^1 The camp has 12 cabins with electricity in the Woodsmen and Pioneers sections, 14 prospector tents in the Coureurs des Bois and Pathfinders sections, and 3 rooms in the Rose des Vents Pavilion.^9
```
**to:**
```
Small cabins without electricity or plumbing, along with platform tents — the traditional camping experience.^1
```

Then add a new subsection after the Lake Wilson Area subsection (after line 36) and before Outpost Camps (line 38):

```
### Accommodation Summary
Across the full site, the camp has 12 cabins with electricity (in the Woodsmen and Pioneers sections), 14 prospector tents (in the Coureurs des Bois and Pathfinders sections), and 3 rooms in the Rose des Vents Pavilion.^9
```

**Reason:** This separates the Centre Camp description (f_0028) from the whole-camp accommodation inventory (f_0452) and avoids the false implication that Centre Camp cabins have electricity.

---

### FIX 10 — f_0098 and f_0338 in kb_facts_used but not in text [MINOR]

Two facts are listed in the articles.json `kb_facts_used` but have no corresponding text in the article:

- **f_0098**: "Carpenters worked for 2 months before the 1941 camp opening" (src_cfcf_1941)
- **f_0338**: "A 1913 Campers' reunion place mat/napkin is the earliest Kanawana artifact in Concordia archives" (src_concordia_fonds)

**Option A (preferred):** Add them to the article.
- Add to Historical Facilities after line 72: `- Extensive construction preceded the 1941 season, with carpenters working for two months before camp opened.^11`
- Add to the maps paragraph at line 74: `The earliest Kanawana artifact in the Concordia Archives is a 1913 Campers' reunion place mat or napkin.^13`

**Option B:** Remove f_0098 and f_0338 from the `kb_facts_used` list in articles.json if the content is deemed out of scope.

---

### kb_facts_used updates needed in articles.json

**Current list (39 facts):**
```
f_0022, f_0023, f_0024, f_0025, f_0026, f_0027, f_0028, f_0029, f_0030, f_0031,
f_0098, f_0141, f_0226, f_0227, f_0228, f_0229, f_0230, f_0301, f_0303, f_0312,
f_0313, f_0338, f_0340, f_0354, f_0442, f_0445, f_0449, f_0450, f_0451, f_0452,
f_0470, f_0471, f_0472, f_0473, f_0474, f_0475, f_0476, f_0477, f_0478
```

**Add these facts** (used in article text but missing from list):
| Fact ID | Claim | Why |
|---------|-------|-----|
| f_0233 | "A totem pole was added to the Council Ring in 1927 under Harold Cross" | Line 72 explicitly states "added 1927 under Harold Cross" -- this is f_0233, not f_0227 (which only says "1970s photo") |
| f_0013 | "The Page family sold the land for the current Saint-Sauveur site to the YMCA" | Line 8 says "acquiring it from the Page family" -- sourced from f_0013 |
| f_0014 | "The YMCA acquired the larger site from the Page family at Saint-Sauveur-des-Monts circa 1910" | Line 8, the 1910 purchase date. If Fix 4 is applied (changing footnote to ^1), this becomes the backing fact |
| f_0479 | "The YMCA purchased the current site near Saint-Sauveur, Quebec in 1910" | Corroborating fact for the 1910 date from src_kanawana_facts |

**Remove if not incorporated into text (per Fix 10 decision):**
| Fact ID | Claim | Why |
|---------|-------|-----|
| f_0098 | "Carpenters worked for 2 months before the 1941 camp opening" | Not in article text unless Fix 10 Option A is applied |
| f_0338 | "A 1913 Campers' reunion place mat/napkin is the earliest Kanawana artifact" | Not in article text unless Fix 10 Option A is applied |

**Final kb_facts_used list (assuming Fix 10 Option A -- all facts incorporated):**
```json
["f_0013", "f_0014", "f_0022", "f_0023", "f_0024", "f_0025", "f_0026", "f_0027", "f_0028", "f_0029", "f_0030", "f_0031", "f_0098", "f_0141", "f_0226", "f_0227", "f_0228", "f_0229", "f_0230", "f_0233", "f_0301", "f_0303", "f_0312", "f_0313", "f_0338", "f_0340", "f_0354", "f_0442", "f_0445", "f_0449", "f_0450", "f_0451", "f_0452", "f_0470", "f_0471", "f_0472", "f_0473", "f_0474", "f_0475", "f_0476", "f_0477", "f_0478", "f_0479"]
```

That is 43 facts (39 original + 4 additions).

---

### Summary by severity

| Severity | Fix # | Issue |
|----------|-------|-------|
| **MAJOR** | 1 | "70 km" should be "90 km" (line 8) |
| **MAJOR** | 2 | Lake Wilson called "outpost camp" but was a hike destination (line 20) |
| **MODERATE** | 3 | "45 minutes" driving time is unsourced; footnote on railway distance is wrong (line 12) |
| **MODERATE** | 4 | 1910 purchase footnote ^4 should be ^1 (line 8) |
| **MINOR** | 5 | "1920s" should be "1923" (line 12) |
| **MINOR** | 6 | Golf course and tents with wood floors omitted from f_0031 list (after line 69) |
| **MINOR** | 7 | f_0229 "Indian characters" not reflected in text (line 71) |
| **MINOR** | 8 | Source count "14" in header is incorrect (line 3) |
| **MINOR** | 9 | Cabin inventory placed confusingly under Centre Camp heading (line 30) |
| **MINOR** | 10 | f_0098 and f_0338 in kb_facts_used but not in text (need incorporation or removal) |

Fixes 1 through 4 must be applied before the article can advance to R3-verified. Fixes 5 through 10 are recommended but not blocking.
