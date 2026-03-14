# Camp Kanawana Wiki Project — Briefing for Strategic Review

*Prepared: 2026-03-14*
*Purpose: Provide a comprehensive project status report and request revised instructions for the next phase of work.*

---

## 1. What This Project Is

We are building a source-grounded research wiki on **Camp Kanawana**, a YMCA summer camp near Saint-Sauveur, Quebec, operating continuously since 1894 — the second-oldest camp in Canada. The wiki is constructed by an AI agent (Claude, running in Claude Code) that executes an autonomous research-to-publication pipeline governed by a structured methodology called RALPH (Retrieve → Analyze → Loop-decide → Process → Hypothesize).

The project lives in a git repository with this structure:

```
├── CLAUDE.md              # Operating instructions for the AI agent
├── config.yaml            # Model preferences, Drive folder IDs
├── sources/
│   ├── sources.json       # 135 indexed sources
│   └── cache/             # Raw cached source texts
├── kb/
│   ├── facts.json         # 724 facts with provenance
│   └── conflicts.json     # 1 unresolved conflict
├── wiki/
│   ├── articles.json      # 28 articles tracked
│   ├── context/ programs/ people/ places/ chronology/ documents/ meta/
├── queue/
│   └── priorities.json    # 64 priorities (47 completed, 16 blocked, 1 stale)
└── logs/
    └── pipeline.log       # Timestamped action log
```

The AI agent picks up the top priority, executes it, saves state, and picks up the next one. It pauses only when it needs a human decision, runs out of context, or the queue is empty/fully blocked.

---

## 2. Current State — By the Numbers

### Knowledge Base
| Metric | Value |
|--------|-------|
| Total facts | 724 (f_0001–f_0724) |
| Confidence: stated | 665 (92%) |
| Confidence: user_knowledge | 43 (6%) |
| Confidence: inferred | 14 (2%) |
| Confidence: disputed | 2 (<1%) |
| Added by: auto_extraction | 365 |
| Added by: ralph_loop | 280 |
| Added by: ralph_mcmorris_full | 62 |
| Added by: ralph_r1_dimock | 17 |
| Unresolved conflicts | 1 (coeducation start date: 1968 vs 1969) |
| Orphan facts (not cited by any article) | 0 |

Top fact categories: people (142), staff (57), traditions (56), programs (54), camping_movement (34), centennial (30), facilities (28), directors (27), founding (25).

### Sources
| Metric | Value |
|--------|-------|
| Total sources indexed | 135 |
| By type: web | 82 |
| By type: catalog_reference | 19 |
| By type: periodical | 14 |
| By type: report | 12 |
| By type: thesis | 6 |
| By type: oral_history | 2 |
| Reliability: primary | 54 |
| Reliability: secondary | 63 |
| Reliability: tertiary | 18 |
| Extracted (facts pulled) | 99 |
| Not yet extracted | 36 |

The 36 unextracted sources are either behind paywalls, proxy-blocked, require physical access, or are audio/video.

### Wiki Articles
| Metric | Value |
|--------|-------|
| Total articles | 28 |
| E1-reviewed (highest status) | 27 |
| Draft (incomplete) | 1 (ralph-dawson — lost content, 0 words) |
| Total word count | ~39,400 words |
| Total open questions across all articles | ~185 |
| Articles with Critical open questions | 18 of 27 |

### Article Inventory

| Article | Folder | Status | Words | Sources | Facts | Open Qs |
|---------|--------|--------|-------|---------|-------|---------|
| Founding of Camp Kanawana (1894) | chronology | E1 | 2,200 | 7 | 49 | 6 |
| D.A. Budge | people | E1 | 1,100 | 5 | 11 | 4 |
| Canoe Tripping at Kanawana | programs | E1 | 650 | 5 | 12 | 3 |
| The Council Ring | places | E1 | 600 | 4 | 8 | 3 |
| L&V Games | programs | E1 | 750 | 4 | 13 | 4 |
| Wartime Kanawana | chronology | E1 | 1,800 | 5 | 29 | 3 |
| Section Names and Age Groups | context | E1 | 900 | 3 | 14 | 3 |
| Coeducation and Gender | context | E1 | 2,100 | 6 | 23 | 8 |
| Programs and Activities | programs | E1 | 2,100 | 10 | 91 | 8 |
| Ralph Dawson | people | draft | 0 | 2 | 0 | 3 |
| Directors and Staff | people | E1 | 2,400 | 19 | 109 | 7 |
| Sources and Archives | meta | E1 | 1,200 | 0 | 23 | 7 |
| Harold C. Cross | people | E1 | 750 | 5 | 14 | 6 |
| The 1967 Centennial | chronology | E1 | 1,200 | 10 | 50 | 6 |
| Canadian Camping Movement | context | E1 | 1,100 | 11 | 39 | 5 |
| Billy Ball | people | E1 | 700 | 5 | 9 | 7 |
| The Cushing Family | people | E1 | 1,200 | 7 | 19 | 5 |
| Traditions and Culture | programs | E1 | 1,800 | 17 | 68 | 6 |
| The Kanawana Site | places | E1 | 1,600 | 12 | 47 | 6 |
| Camp Otoreke | places | E1 | 900 | 10 | 22 | 7 |
| Stuart McLean | people | E1 | 1,400 | 13 | 38 | 6 |
| Pip Alumni Award | programs | E1 | 1,500 | 11 | 33 | 6 |
| J.W. McConnell | people | E1 | 750 | 5 | 16 | 6 |
| Lake Wilson | places | E1 | 650 | 5 | 8 | 6 |
| Myths and Legends | context | E1 | 2,811 | 19 | 38 | 8 |
| Camp Songs and Cheers | programs | E1 | 2,200 | 15 | 22 | 9 |
| Places and Locations | places | E1 | 2,950 | 15 | 36 | 13 |
| Hedley Dimock | people | E1 | 2,100 | 14 | 36 | 5 |

### Priority Queue
| Status | Count |
|--------|-------|
| Completed | 47 |
| Blocked | 16 |
| Pending | 0 |
| In-progress | 0 |

**All non-blocked priorities have been completed.** The queue is effectively empty of actionable work.

---

## 3. What Has Been Accomplished

Over approximately 10 sessions spanning 2026-02-10 to 2026-03-14:

1. **Bootstrapped the entire project** — created all data schemas, directory structure, pipeline logic, and the RALPH research framework.
2. **Ingested and extracted 99 sources** — web pages, theses, archival catalog entries, periodicals, reports, and two oral history records.
3. **Built a 724-fact knowledge base** with full provenance, cross-referencing, and conflict detection.
4. **Wrote 28 wiki articles** (27 at the highest quality tier, E1-reviewed) totaling ~39,400 words.
5. **Executed 47 research priorities** including formal RALPH loops, verification passes, editorial reviews, and cross-linking sweeps.
6. **Achieved zero orphan facts** — every fact in the KB is cited by at least one article.
7. **Discovered and documented** previously unknown connections: Ross & Macdonald architectural drawings at the CCA, Stuart McLean's camp years, the Alabama Jubilee origin of the camp marching song, the Hedley Dimock father-son story, and more.

---

## 4. What Is Blocked

The 16 blocked priorities fall into four categories:

### 4a. User Must Download (6 items — highest impact)

These are freely available sources behind a proxy that blocks the AI agent. The human operator can download them and provide the text.

| ID | Source | Why It Matters |
|----|--------|----------------|
| p_054 | Historical Sketch of the YMCA of Montreal (1901), Internet Archive | Covers 1851–1901, overlaps Camp Jubilee founding. Likely contains camp origin details. |
| p_055 | YMCA Annual Report 1891–1892, Internet Archive | Immediately pre-founding. May document Cushing's 1892 Lake St. Joseph trip. |
| p_056 | Alfred Sandham, History of the Montreal YMCA (1873), Internet Archive | Earliest known YMCA Montreal history. |
| p_057 | Concordia AtoM finding aid PDF | Complete archival finding aid — may reveal file-level descriptions missing from web catalog. |
| p_060 | CCA Ross & Macdonald architectural drawings page | Major architectural firm designed a camp building. |
| p_064 | Remaining IA collection items (YMCA Annual Reports 1856, 1876, 1889–1890, 1993; News Releases 1965, 1980; SGW College Bulletin 1932) | Mixed value; some could fill gap periods. |

### 4b. Oral History Needed (3 items)

These require input from the project owner (Matt Aronson) or other alumni. No online documentation exists.

| ID | Topic |
|----|-------|
| p_045 | The "Chopsy" ghost story — full narrative, origin period, telling context |
| p_048 | Camp songs and cheers — section cheers, Grace text, campfire repertoire, marching song full lyrics |
| p_051 | Grand Portage and Longhouse building identification, named cabin inventory |

### 4c. Paywalled / Restricted Access (4 items)

| ID | Source | Access Required |
|----|--------|-----------------|
| p_030 | BAnQ digitized newspapers (Gazette, Montreal Star, La Presse, Le Devoir) | Browser session at numerique.banq.qc.ca |
| p_031 | Gazette 1897 & 1918 full articles | Newspapers.com subscription |
| p_058 | Gazette July 7, 1913 article | Newspapers.com subscription |
| p_005 | Green Triangle newsletter issues 1932–1940 | Physical Concordia Archives visit |

### 4d. Other Human Action (3 items)

| ID | Need |
|----|------|
| p_040 | Restore ralph-dawson.md content (lost during context compaction) |
| p_062 | Listen to Stuart McLean "A Letter from Camp" audio and transcribe camp facts |
| p_063 | Search YouTube for 1993 Kanawana documentary film |

---

## 5. Open Questions — The Critical Ones

Across 27 articles, there are ~185 open questions. Here are the ones tagged [Critical] — the questions whose answers would most significantly improve the wiki:

### People
- **Billy Ball**: What was his full name? What was his role within the YMCA? (Only "Billy Ball" appears in any source.)
- **Cushing Family**: Which Cushing led the 1892 trip? Was W.E. Cushing (1943 historian) the same as Dr. Cushing (1946 medical advisor)?
- **Harold Cross**: Birth and death dates unknown. No biographical record found despite extensive search.
- **Directors 1947–2003**: A 56-year gap in the director list. Spans the coeducation transition, site changes, and 1994 centennial.
- **Ralph Dawson**: Was he a director or just a historian/alumnus? Article content was lost.

### Places
- **Grand Portage and Longhouse**: What are/were these buildings? Known only from oral tradition.
- **Historical buildings**: Which 1920s structures (Lakeside Pavilion, Hospital, Icehouse, Chapel) still exist?
- **The Kanawana Site**: Who was the Page family who sold/donated the land?

### Traditions
- **"Chopsy" legend**: Full narrative unknown. Completely undocumented outside oral tradition.
- **Camp songs**: Lyrics to "On My Way to Kanawana" by Richard Kerr unknown. Full marching song lyrics unknown. Section cheers unknown.
- **Motto transition**: When did "Each for all and all for each" become "Non Nobis Solum"?

### Sources
- **McMorris thesis**: Now fully extracted (resolved in this session).
- **BAnQ newspapers**: Systematic search not yet possible (requires browser access).

---

## 6. The CLAUDE.md — Current Operating Instructions

The AI agent is governed by a `CLAUDE.md` file that defines:

1. **Execution model**: Autonomous loop — pick top priority, execute, save state, repeat. Stop only for human decisions, context limits, or empty queue.
2. **RALPH methodology**: Five-phase research cycle with formal/informal variants. Formal required for people, founding-era, and stub→draft advancement.
3. **Article pipeline**: stub → draft → R3-verified → E1-reviewed. No skipping stages. Each advancement requires specific task types (RESEARCH, VERIFY, WRITE, REVIEW).
4. **KB extraction rules**: Extract only stated claims. One source per fact. Flag uncertainty. Never silently overwrite conflicts.
5. **Article spawning thresholds**: Named persons, recurring events, physical structures, publications, structured programs.
6. **State management**: Save after every atomic unit. Log everything. Push to Drive every 5 units.

The full CLAUDE.md is ~300 lines and covers schemas, commands, and the priority queue system.

---

## 7. What I Need From You

The project has reached an inflection point. The autonomous online research loop is exhausted — every priority that can be completed without human intervention has been completed. The remaining work requires either:

- Physical/restricted source access
- Oral history collection
- Human downloads from proxy-blocked sites
- Strategic decisions about project direction

**Please advise on the following:**

### 7a. Protocol and Instruction Upgrades

The current CLAUDE.md was written for an initial research-heavy phase. Now that 27/28 articles are at E1-reviewed and the priority queue is empty of actionable items, the operating instructions need revision. Specifically:

1. **What should the agent do when the queue is empty of actionable items but blocked items exist?** Currently it stops and waits. Should it instead: audit existing articles for quality? Generate a reading-friendly export? Build cross-reference indices? Work on presentation/formatting?

2. **Should the article pipeline add stages beyond E1-reviewed?** For example: human-reviewed, published, or featured. Several articles are thin (600–750 words) and could benefit from deepening once new sources become available.

3. **Should the RALPH methodology be revised for a "maintenance and deepening" phase** where the agent re-examines existing articles with fresh eyes, looking for gaps, inconsistencies, or opportunities to merge/split articles?

4. **Is the article spawning threshold still correct?** 28 articles may be too many or too few. Some topics (like the 1994 centennial, the YMCA Quebec merger, post-2000 era, Indigenous reconciliation) have no articles despite being significant.

5. **Should the agent have instructions for handling user-provided oral history or downloaded sources?** Currently there is no formal "ingest user-provided content" workflow.

### 7b. Content Strategy

1. **Coverage gaps**: The wiki is heavily weighted toward pre-1950 history. The 1950–2000 period is almost undocumented. The post-2000 era has scattered facts. Should the agent prioritize filling these gaps, or is the historical focus intentional?

2. **Article depth vs. breadth**: Some articles are quite short (canoe-trips: 650 words, council-ring: 600 words, lake-wilson: 650 words). Should the agent try to deepen these, or is their brevity appropriate given limited source material?

3. **The "ralph-dawson" problem**: This is the only article at draft status with 0 words — content was lost during a context compaction. The agent has facts about Ralph Dawson in the KB but the article text needs to be rewritten. Should this be a priority?

4. **Potential new articles not yet created**:
   - The 1994 Centennial
   - YMCA Quebec / Kanawana governance history
   - The post-2000 era (year-round programming, rebranding)
   - Indigenous place names and reconciliation
   - The Camp Weredale relationship
   - Notable alumni beyond Stuart McLean
   - The physical plant / infrastructure evolution
   - Environmental and ecological history
   - Winter programming history

### 7c. Source Strategy

1. **The 36 unextracted sources**: Some are inaccessible (paywalled, audio, physical). Others are accessible but proxy-blocked. Should the human operator prioritize downloading the Internet Archive items? They are freely available and several cover the founding era.

2. **Oral history collection**: Three blocked priorities require oral history from the project owner. Should the CLAUDE.md include a structured interview protocol to make this collection efficient?

3. **The Concordia Archives**: The single richest untapped source. A physical visit could potentially resolve dozens of open questions. Should the agent prepare a "Concordia Archives visit checklist" of specific items to request?

### 7d. Output and Presentation

1. **Export format**: The wiki currently exists as markdown files in a git repo. Should the agent generate a reader-friendly export (single document, table of contents, index)?

2. **Cross-reference system**: Articles link to each other informally. Should there be a formal cross-reference index or graph?

3. **Timeline visualization**: The KB contains hundreds of dated facts. Should the agent generate a master chronology document?

---

## 8. Summary

| Dimension | Status |
|-----------|--------|
| Knowledge base | 724 facts, zero orphans, 1 conflict |
| Sources | 135 indexed, 99 extracted, 36 blocked |
| Articles | 28 total, 27 at highest quality tier |
| Word count | ~39,400 words |
| Priority queue | Empty of actionable items |
| Blockers | 16 items requiring human action |
| Open questions | ~185 across all articles, ~35 critical |

The foundation is solid. The question is: what comes next?
