# Kanawana Wiki Builder — Operating Instructions

## Project Structure

```
project/
├── config.yaml              # Drive folder IDs, model preferences
├── sources/
│   ├── sources.json          # Source index/manifest
│   └── cache/                # Raw cached source texts
├── kb/
│   ├── facts.json            # All facts with provenance
│   ├── conflicts.json        # Unresolved conflicts
│   └── versions/             # KB version snapshots
├── wiki/
│   ├── README.md             # Hub page: Kanawana's core identity, entry point to the wiki
│   ├── articles.json         # Article status tracker
│   ├── history/ site/ traditions/ people/ documents/ meta/   # core, 1 click from the hub
│   ├── people/notable-alumni/                                # spoke, 2 clicks
│   └── connections/institutional-lineage/ connections/related-camps/  # spokes, 2 clicks
├── queue/
│   └── priorities.json       # Research priority queue
└── logs/
    └── pipeline.log          # Timestamped action log
```

## Execution Model

Run this loop indefinitely:

```
Pick top priority → Execute → Save state → Pick next priority → Execute → ...
```

**Stop only for:**
1. Human decision required (conflict resolution, editorial review, empty queue)
2. Context limit approaching — finish current atomic unit, save state, print: `Context limit reached. State saved. Run "continue" in a new session.`
3. Human interrupts — finish atomic unit, respond, resume

**Never ask "what should I work on next?"** unless `priorities.json` is empty or all items need human input.

### State Saves

Save after every completed atomic unit:
- One completed RALPH loop (all five phases)
- One article status change
- One source ingestion
- One KB extraction batch

Write affected JSON files immediately after each atomic unit.

### Human Decision Points (DO pause)

1. Editorial review — article ready for accept/edit/reject
2. Conflict resolution — sources disagree, affects current article
3. Empty queue — no actionable items remain

### NOT Pause Points (keep going)

- Completing an article task type
- Discovering a new source
- Finding a new stub-worthy entity
- Finishing a RALPH loop
- Encountering a non-blocking conflict

### Drive Sync

Push to Drive after every 5 atomic units, or when pausing for human, or at context limit. Backup only — not a workflow gate.

### Logging

Log every atomic unit to `pipeline.log`: what ran, what changed, timestamp.

## RALPH Research Methodology

Five-phase iterative research cycle: **Retrieve → Analyze → Loop-decide → Process → Hypothesize**

### R: RETRIEVE
- Check source cache first (avoid redundant fetches)
- Execute web searches, archive queries, Drive searches
- Log every source checked and found, including dead ends
- Output: sources consulted, new sources discovered, raw data cached

### A: ANALYZE
- Extract facts with source citation and confidence level (high/medium/low)
- Flag contradictions against existing KB
- Check whether newly discovered entities warrant new article stubs
- Output: candidate facts, contradiction flags, stub candidates

### L: LOOP DECISION
- **CONTINUE**: Not saturated, refine queries, loop back to R
- **ADVANCE**: Good coverage on subtopic, move to related subtopic, loop back to R
- **CONCLUDE**: Sufficient material, exit to P

### P: PROCESS
- Add verified facts to KB
- Update article draft if in a WRITE task
- Flag items needing independent verification

### H: HYPOTHESIZE
- Propose follow-up queries and research threads
- Identify archive leads
- Register new article stubs into priority queue

### Formal vs Informal RALPH

**Formal RALPH required for:**
- People stubs and biographies
- Founding-era articles
- Any article advancing stub → draft

**Informal RALPH acceptable for:**
- Adding facts from known cached source to existing draft
- Minor updates and cross-reference additions
- E1 review passes on already-verified articles

**Mandatory:** No article advances to drafting or review without at least one full RALPH cycle.

## Article Pipeline

### Status Progression

| Status | Requirements |
|--------|-------------|
| **stub** | Title, 1+ fact, 1+ source, research questions listed |
| **draft** | Summary, 2+ sections, 3+ sources, structure complete. Requires RESEARCH + RALPH. |
| **R3-verified** | VERIFY complete: every claim cited, dates checked against timeline, names checked against people index |
| **E1-reviewed** | REVIEW complete: cross-links verified, encyclopedic quality, no unsourced speculation, Open Questions actionable |

No skipping stages.

### Task Types

**RESEARCH**: Discover and extract information. Invokes RALPH loops. Output: KB facts, cached sources, stub/draft updated.

**VERIFY**: Cross-reference claims against independent sources. Check cited source accuracy, find corroborating/contradicting sources, check dates and names. Output: corrections, confidence adjustments, conflict records.

**WRITE**: Draft/revise article from verified facts. Only after RALPH concludes with sufficient material. Encyclopedic tone, neutral voice, inline citations. Output: article markdown.

**REVIEW**: Systematic fact-check. Every claim reviewed for source grounding, accuracy, tone, cross-links. Output: review notes, corrections, status advanced if passing.

### Article Template

```markdown
# [Article Title]

*Status: [stub|draft|R3-verified|E1-reviewed] | Sources: [count]*
*Last Updated: [date]*

## Overview
[2-3 paragraph summary]

## [Chronological or thematic sections]
[Prose with inline source references]

## Open Questions
[Numbered list of specific, actionable research questions]

## Sources
[Full citation list with URLs where available]
```

### Article Spawning Thresholds

Create stubs for newly discovered entities matching:
- Named person who held a camp role
- Recurring event or tradition
- Physical structure or location with its own history
- Publication or media
- Program or activity with structure and evolution

### Wiki Folder Placement — Hub and Spoke

Folders encode distance from Kanawana's own core identity, not just topic. Core categories sit at the wiki root (one click from `wiki/README.md`); spoke content gets an extra folder level (two clicks), in proportion to how far it actually is from Kanawana itself:

- **Core (`history/`, `site/`, `traditions/`, `people/`, `documents/`, `meta/`)** — the subject IS Kanawana: its own timeline, its own physical site, its own programming/culture, the people who built and ran it, its own media/documents. This includes articles that examine Kanawana through a wider social lens (e.g. coeducation, environmental education, land history) as long as Kanawana itself is the subject, not the wider phenomenon.
- **`people/notable-alumni/`** — a person had real contact with camp (camper, brief staff role) but their enduring, defining biography is a life lived mostly *outside and after* Kanawana. Test: would this person have a Wikipedia-notable article even if Kanawana never existed? If yes, they belong here, not in core `people/`.
- **`connections/institutional-lineage/`** — a parent or affiliated *institution* whose own history is much bigger than Kanawana's (e.g. YMCA of Montreal overall, Concordia/SGW, the national Canadian Camping Movement). Kanawana is one chapter in their story, not the reverse.
- **`connections/related-camps/`** — a sibling *camp* operated by a genuinely separate organization (different YMCA branch, YWCA, independent foundation) that intersected with Kanawana's history. Camps operated by the same institution as Kanawana (e.g. an earlier or overflow YMCA of Montreal site) are core `site/`, not a related camp.

When spawning a new stub, classify it into one of these five buckets before writing `wiki_folder`, and add it to the correct index page (`people/directors-index.md`, `people/notable-alumni/notable-alumni.md`, `connections/related-camps/quebec-camp-landscape.md`, etc.) so it's discoverable from the hub.

### Article Status Schema

```json
{
  "article_id": "string",
  "title": "string",
  "wiki_folder": "history|site|traditions|people|people/notable-alumni|connections/institutional-lineage|connections/related-camps|documents|meta",
  "status": "stub|draft|R3-verified|E1-reviewed",
  "status_history": [{"status": "", "at": "ISO8601", "by": "auto|human", "task": "RESEARCH|VERIFY|WRITE|REVIEW"}],
  "ralph_loops_completed": 0,
  "kb_facts_used": [],
  "sources_cited": [],
  "open_questions": 0,
  "cross_links": [],
  "file_id": "drive_file_id or null",
  "word_count": 0
}
```

## Source Discovery & KB Engine

### Source Record Schema

```json
{
  "source_id": "string",
  "type": "periodical|web|thesis|report|oral_history|catalog_reference",
  "title": "string",
  "date": "string",
  "date_precision": "exact|year|decade|approximate",
  "origin": "internet_archive|web|user_provided|concordia_archives",
  "origin_url": "string or null",
  "cache_path": "string or null",
  "char_count": 0,
  "ingested_at": "ISO8601",
  "extracted": false,
  "extraction_version": "string or null",
  "reliability": "primary|secondary|tertiary",
  "notes": "string"
}
```

### KB Extraction Constraints

- Extract only claims the source actually makes. No inference beyond what's stated.
- Preserve exact dates, names, and numbers.
- Flag uncertainty in the source itself.
- Never combine information from multiple sources in a single fact.
- Confidence reflects source ambiguity.

### Fact Schema

```json
{
  "fact_id": "string",
  "claim": "string",
  "sources": [],
  "confidence": "stated|inferred|user_knowledge|disputed",
  "category": "string",
  "entities": [],
  "date_ref": "string or null",
  "conflicts_with": [],
  "added_version": "string",
  "added_by": "auto_extraction|manual|ralph_loop"
}
```

### Conflict Handling

When a new fact contradicts an existing one (same entity + same attribute + different value):
1. Do NOT silently overwrite
2. Create conflict record linking both facts
3. Flag for human review
4. Preserve both facts until resolved

**Default resolution direction (operator directive, 2026-07-07):** oral history always yields to documented facts when the two directly conflict. When a conflict record pits an oral-history-sourced fact (`confidence: user_knowledge` or an oral-history source) against a documented source (primary or secondary — annual report, archival record, LinkedIn, press coverage, etc.), resolve in favor of the documented source without waiting for further human review. Mark the conflict `resolved`, note the resolution and date, and update affected wiki articles accordingly. The superseded oral-history fact is still preserved per the no-silent-overwrite rule — it is not deleted, only marked superseded. This directive applies only where the two sources actually conflict on the same claim; an undocumented span that no source covers (e.g., an oral-history date range partially outside any document's coverage window) is not "resolved" by this rule, since there is nothing documented to prefer — it remains open, flagged as unconfirmed. Genuine human-decision-point conflicts (two documented sources disagreeing with each other, or ambiguity about what a document actually means) still require human review as before.

## Wiki Manager

### Coverage Analysis

Compare KB facts against published articles to find:
- Orphan facts (not cited by any article)
- Thin articles (few facts or sources)
- Coverage gaps (KB categories with no article)
- Stale articles (cited sources updated since last edit)

### Priority Queue

Ranked list in `priorities.json`:
- New articles from orphan facts or Open Questions
- Sources worth ingesting
- KB conflicts awaiting resolution
- Articles ready for next task type

Priority factors: available sources, related KB facts, cross-links, human-assigned weight.

## Commands Reference

### Article
- `article new <topic>` — Create stub, run RESEARCH with RALPH
- `article advance <article_id>` — Run next required task type
- `article run-full <article_id>` — Run all task types through E1-reviewed
- `article status` — Show all articles and pipeline positions
- `article review <article_id>` — Present for human review

### Source
- `discover <topic>` — Search for new sources
- `ingest <url>` — Download and cache a source
- `ingest-batch <source_list>` — Batch download
- `catalog-scan` — Parse archive catalog pages

### KB
- `extract <source_id>` — Run fact extraction on cached source
- `extract-all-new` — Extract from unprocessed sources
- `kb-search <query>` — Semantic search across facts
- `kb-conflicts` — List unresolved conflicts
- `kb-stats` — Counts by category, confidence, coverage
- `kb-export` — Export KB as markdown or JSON

### Wiki
- `wiki status` — Dashboard: articles by status, KB stats, top priorities
- `wiki gaps` — Coverage analysis
- `wiki graph` — Cross-reference visualization
- `wiki plan <n>` — Suggest next N actions
- `wiki export` — Export wiki as markdown folder

---

# CLAUDE.md — Phase 2 Amendment: Wide-Net Research
*Effective: 2026-03-14. Supersedes the "stop and wait" instruction when the priority queue is blocked.*

## What Has Changed

Phase 1 exhausted all priorities achievable through structured web research on known sources.
Phase 2 expands the search mandate significantly. The operator does not have time to supply
content manually. The agent must find its own way forward using wider and deeper search.

## Standing Order When Queue Is Empty or Fully Blocked

Do not stop. Generate new priorities autonomously from the tasks below, add them to the queue,
and work them in priority order. Stop only for true dead-ends requiring physical archive access
or oral history from the operator.

---

## Phase 2 Research Mandate

### 1. Open Questions — Systematic Pursuit

Work through the ~35 Critical open questions one at a time. For each:
- Generate 5–10 distinct search queries across different search strategies (name variants,
  associated institutions, date ranges, related people)
- Try Google, Google News Archive, Google Books, HathiTrust, Internet Archive full-text search,
  Newspapers.com public access, and BAnQ public catalog
- If a person's name appears (e.g. "Billy Ball," "Harold Cross"), do full biographical research
  before concluding "unknown" — obituary databases, family tree sites (Ancestry public trees,
  FamilySearch, Généalogie Québec), LinkedIn, university alumni records, YMCA organizational
  histories
- Log every search attempted and its result (even null results) so the same ground is not
  re-covered

### 2. People — Biographical Research

For every named individual in the KB who lacks a standalone article and has ≥3 facts, assess
whether a biography is warranted. Priority targets:

- All directors in the 1947–2003 gap (find names first via YMCA annual reports, newspaper
  coverage, alumni materials)
- Billy Ball — full name, YMCA role, dates
- Harold C. Cross — birth/death, biography
- W.E. Cushing / Dr. Cushing disambiguation
- Ralph Dawson — role and biographical detail (rewrite lost article)
- Any new names surfaced during research

For each, search: obituaries (Gazette archive public access, Legacy.com, Find A Grave),
university records, YMCA Montreal historical mentions, Lower Canada College archives mentions,
McGill and Concordia yearbooks (many digitized on Internet Archive).

### 3. Cultural Elements — Songs, Cheers, Traditions, Stories

**Songs:** Search lyrics databases, folk music archives, YMCA song collections on Internet
Archive, sheet music databases (IMSLP, Library of Congress), and camp music scholarship.
The "Alabama Jubilee" connection already found is a model — look for similar origins for other
known songs. Search specifically for Richard Kerr as a composer in YMCA or camp contexts.

**Cheers and section names:** Search for other YMCA camps with similar section systems
(Scouts, Colonists, Rovers, etc.) — the naming conventions may have a common origin in the
camping movement literature.

**The Chopsy legend:** Search for "Chopsy" + camp, Quebec camps ghost stories, YMCA camp
legends. Check if any camp memoir or published oral history mentions it.

**Traditions generally:** Search Google Books and HathiTrust for "Camp Kanawana" (exact phrase),
"Kanawana" + YMCA + tradition/ritual/ceremony. Check if any academic work on summer camp culture
in Canada references Kanawana traditions.

### 4. Visual and Material Culture

**Photos and film:**
- Flickr: search "Camp Kanawana," "Kanawana," "YMCA camp Saint-Sauveur," "Lake Wilson Quebec"
- Google Images with date filters
- Internet Archive moving image collection: search "Kanawana" and "YMCA Montreal camp"
- YouTube: search "Camp Kanawana," "Kanawana 1993 documentary," "Stuart McLean Kanawana"
- Library and Archives Canada photo database (collectionscanada.gc.ca)
- McCord Museum digital collection (musee-mccord.qc.ca)

**Maps:**
- NRCan historical topographic maps (toporama.ca and geogratis.gc.ca) — Saint-Sauveur quad
  maps from different eras
- BAnQ cartographic collection
- Library and Archives Canada cartographic collection

**Merchandise and paraphernalia:**
- eBay: search "Camp Kanawana," "Kanawana pennant," "Kanawana badge," "YMCA camp Quebec pennant"
- Etsy vintage camp memorabilia searches
- WorthPoint and similar collectibles databases
- Document any items found: description, date estimate, seller/location — existence and
  description is factual record even if not purchasable

**Architecture:**
- CCA online collection: fetch the full Ross & Macdonald finding aid page and document all
  Kanawana-related drawings by title, date, medium, and dimensions
- Search Bibliothèque nationale for any published architectural documentation

### 5. Inter-Camp and Institutional Connections

**Other YMCA camps:** Research Camp Weredale, Camp Ouareau, and other Quebec YMCA camps —
shared staff, programming traditions, history with Kanawana, mentions in their own histories.

**Lower Canada College:** Search LCC archives mentions, LCC alumni publications, "Lower Canada
College" + "Kanawana" combinations.

**McGill and Concordia:** Search digital collections and student newspaper archives (McGill Daily
and Georgian are partially digitized) for Kanawana mentions, camp advertisements, alumni references.

**Canadian camping movement:** Search Ontario Camping Association archives, Canadian Camping
Association publications, and academic work on organized camping in Canada for Kanawana references.

**The YMCA internationally:** Search YMCA USA and international publications for references to
Montreal YMCA camps, particularly 1890–1930.

### 6. Newspaper Research — Expanded

- **Montreal Star** (1869–1979): BAnQ numerique — fetch search results pages even if full
  articles are blocked
- **The Standard** (Montreal): some issues digitized
- **La Presse** and **Le Devoir** BAnQ public access pages
- **Google News Archive** (news.google.com/newspapers): "Kanawana," "Camp Kanawana,"
  "YMCA camp Montreal"
- **Chronicling America** (LOC): U.S. papers sometimes covered the Canadian YMCA camp movement
- Saint-Sauveur and Laurentians local historical press

For each hit: extract who/what/when/where facts, add to KB with source, update relevant articles.

### 7. Social Media and Alumni Networks

Search public content only:
- **Facebook:** "Camp Kanawana" public posts, groups, pages — document existence of alumni
  groups, note any historical photos or facts mentioned publicly
- **Reddit:** r/montreal, r/Quebec, r/camping searches for "Kanawana"
- **Instagram/TikTok:** hashtags #campkanawana, #kanawana
- **LinkedIn:** "Camp Kanawana" in experience field — may surface staff names from undocumented periods

Do not extract personal information about living private individuals. Extract only institutional
facts, historical information, and information about public figures.

**Amendment, 2026-09-03 — record everything; embargo is metadata.** The rule above was being
followed by not writing the material down, which loses it: a later pass cannot tell the
difference between "the source says nothing" and "someone decided not to write it down," and
reads the same document to the same dead end. A hole in the record looks exactly like an absence
of evidence, which is a serious thing to manufacture for anyone who later relies on this
research.

**Publication policy belongs to the wiki's UI layer, not to collection.** For collecting data and
writing articles, the repo and the wiki are both fine and both should be COMPLETE. So:

1. **Extract it.** Sensitive material goes into `kb/facts.json` like any other fact, carrying a
   `publication` block: `{"status": "embargoed", "register_id": "r_NNNN", "review_on":
   "YYYY-MM-DD", "basis": "...", "why": "..."}`.
2. **Write it where it belongs** in the article, wrapped in `<!-- embargo:r_NNNN -->` …
   `<!-- /embargo:r_NNNN -->`, with a one-line note saying what it is and when it reviews.
3. **Register it** in `kb/restricted/register.jsonl` — which facts, which document and lines,
   what kind, why, the basis, the review date. See `kb/restricted/README.md`.
4. **Say something about it.** Material like this usually needs context a reader fifty years on
   will not have — who was judging whom, at what age, in what kind of document. Supply it
   outside the block.

Default embargo for personal assessments of identifiable private individuals: the later of
record date + 75 years and estimated birth + 100, released earlier on consent or confirmed
death. `review_on` is a date to look again, never a date to publish automatically.

`scripts/verify/restricted_guard.py` checks the labelling, not the content: every embargoed fact
registered and dated, every marker paired, and no name occurring only in embargoed facts
appearing in an article outside a block. **Unlabelled is the failure, not present.**

The default embargo for personal assessments of identifiable private individuals is the later of
record date + 75 years and estimated birth + 100, released earlier only on consent or confirmed
death. `review_on` is a date to look again, never a date to publish automatically.

### 8. Autonomous Article Spawning

Spawn new article stubs for any of the following once ≥5 facts exist:
- The 1994 Centennial
- Camp Weredale and its relationship to Kanawana
- YMCA Montreal institutional history as it relates to camp
- Notable Alumni (collective article, or individual stubs if warranted)
- The Physical Plant and Infrastructure
- Environmental and Ecological History
- Winter Programming (if evidence found)
- Indigenous Place Names and Land History

---

## What "Exhausted" Means in Phase 2

A search topic is exhausted only when:
1. At least 8 distinct queries have been attempted across at least 3 different search surfaces
2. All results have been read and any facts extracted
3. The null result is logged in the source record

Do not declare a person or topic "unknown" after 2–3 searches. Phase 1 found the Alabama
Jubilee connection, the Ross & Macdonald drawings, and the Hedley Dimock father-son story —
all from non-obvious sources. Phase 2 requires the same persistence.

---

## Output: Ongoing

Continue saving state, updating KB and articles, and pushing to Drive on the same schedule.
Add a `research-log.md` in `project-docs/` recording each Phase 2 search campaign: topic,
queries tried, surfaces searched, results.

---

## Pending Priority — Oral History Interview Protocol

Add to the priority queue: **DRAFT_ORAL_HISTORY_INSTRUMENT** (status: pending, blocked on
Phase 2 research completion).

When blocked items p_045 (Chopsy legend), p_048 (songs and cheers), and p_051 (Grand Portage
and Longhouse) are ready to action, draft a structured oral history interview document for the
operator before requesting any input. Do not ask ad hoc questions — prepare the full interview
instrument first, then present it in a single session request.
