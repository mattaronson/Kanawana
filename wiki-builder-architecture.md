# Ralph Loop Wiki Builder: Architecture Spec

*A research-to-wiki pipeline for building deep, source-grounded reference wikis from messy historical and archival material.*

## The Problem

Building a well-sourced wiki on a niche historical topic (Camp Kanawana, 1894-present) currently requires a human orchestrating an LLM across dozens of chat sessions, manually tracking article status, source caches, knowledge base versions, and cross-references. The workflow is effective but brutally manual. Each session burns context window on re-loading state, re-reading handoffs, and re-discovering what's already known.

The human contributes domain knowledge, editorial judgment, and access to physical/restricted sources. The LLM contributes research synthesis, source cross-referencing, fact extraction, drafting, and review. This spec codifies the LLM's role so it can run semi-autonomously, with the human intervening at decision points.

## Design Principles

**Source-grounded, not generative.** Every claim in every article must trace to a specific source. The system never invents facts. When sources conflict, it documents the conflict rather than resolving it silently.

**Incremental, not batch.** The wiki grows article by article, fact by fact. Each run should leave the project in a better state than it found it, even if interrupted.

**Human-in-the-loop at judgment points.** The system proposes; the human disposes. Article topics, editorial tone, conflict resolution, and "what to research next" are human decisions. Fact extraction, drafting, source discovery, and mechanical review are automated.

**Provenance everywhere.** Every fact in the KB records where it came from. Every article records which KB facts and sources it draws on. Audit trails are not optional.

**Instructions in execution order.** Within each section, constraints and rules appear before procedures. Within the document, components appear in the order a session encounters them: storage and state first, methodology second, operational components third.

---

## Part 1: Project Structure & Storage

*Claude reads this first because it needs to know where everything lives before doing anything.*

### Local filesystem

```
project/
├── config.yaml              # Project name, Drive folder IDs, model preferences
├── sources/
│   ├── sources.json          # Source index/manifest
│   └── cache/                # Raw cached source texts
│       ├── green-triangle/
│       ├── brochures/
│       └── web-pages/
├── kb/
│   ├── facts.json            # All facts with provenance
│   ├── conflicts.json        # Unresolved conflicts
│   └── versions/             # KB version snapshots
├── wiki/
│   ├── articles.json         # Article status tracker
│   ├── context/
│   ├── programs/
│   ├── people/
│   ├── places/
│   ├── chronology/
│   ├── documents/
│   └── meta/
├── queue/
│   └── priorities.json       # Research priority queue
└── logs/
    └── pipeline.log          # What ran, when, what changed
```

### Google Drive sync

Local filesystem is the working copy. Drive is a backup and sharing layer, not a workflow gate.

- `sync push` uploads changed files to Drive (runs periodically, not as a session boundary)
- `sync pull` downloads latest from Drive (only needed if project directory is lost or switching machines)
- Drive folder structure mirrors local structure

If the project directory is lost, `sync pull` from Drive recreates it. The only bootstrap requirement is the Drive folder ID (stored in Claude Memory).

### State recovery

The system can always reconstruct from Drive. `config.yaml` stores the Drive folder ID. All JSON state files and cached sources live in Drive. The project is never in a state where local-only data can't be recreated.

---

## Part 2: Execution Model

*Claude reads this second because it governs all behavior. The core principle: run autonomously until you hit a human decision point or a context limit. Never stop to ask permission for work the priority queue already authorizes.*

### Continuous execution loop

```
Bootstrap → Pick top priority → Execute → Save state → Pick next priority → Execute → ...
```

CC runs this loop indefinitely. It stops only for three reasons:

1. **Human decision required.** A conflict needs resolution, an article is ready for editorial review, or the priority queue is empty and needs human direction.
2. **Context limit approaching.** CC detects it's running low on context, finishes the current atomic unit of work (end of RALPH loop, end of task type), saves all state to disk, and prints: `Context limit reached. State saved. Run "continue" in a new session.`
3. **Human interrupts.** The human types something. CC finishes its current atomic unit, responds, and resumes.

CC never asks "what should I work on next?" unless `priorities.json` is empty or all remaining items require human input. If there's a clear next action, CC takes it.

### State saves: continuous, not session-end

State is saved to disk after every completed atomic unit of work. An atomic unit is:

- One completed RALPH loop (all five phases: R through H)
- One article status change (e.g., stub → draft)
- One source ingestion
- One KB extraction batch (one source fully extracted)

After each atomic unit, CC writes the affected JSON files (`articles.json`, `facts.json`, `sources.json`, `priorities.json`, `conflicts.json`) immediately. If CC dies mid-work, the project loses at most one incomplete RALPH loop or one partial extraction. Everything prior is on disk.

There is no "end of session" ritual. No handoff document. The project directory *is* the handoff.

### Bootstrap (first run only)

1. Create project directory structure per Part 1
2. Generate CLAUDE.md from this architecture spec (condensed, imperative, no rationale)
3. Migrate existing data (KB v3.2, cached sources, article inventory, source index) from Drive into the local structure
4. Populate `priorities.json` from v48 handoff priorities
5. Begin continuous execution loop

### Resume (subsequent sessions)

1. Read CLAUDE.md
2. Read `articles.json`, `facts.json`, `sources.json`, `priorities.json`
3. Print current state summary (article count by status, KB stats, top 3 priorities)
4. Begin continuous execution loop from top priority

No Drive sync needed on resume because CC's project directory persists between sessions. Drive sync (`sync push`) happens periodically as a backup, not as a workflow gate.

### Human decision points

CC pauses execution and asks the human only at these moments:

1. **Editorial review.** After REVIEW task completes on an article, present it and wait for accept/edit/reject. This is the primary quality gate.
2. **Conflict resolution.** When sources disagree and the conflict affects an article currently being worked on. Conflicts discovered during research that don't block current work get logged to `conflicts.json` and flagged in `priorities.json` for later resolution, without pausing.
3. **Empty queue.** When `priorities.json` has no actionable items (all remaining items need human input, or the queue is empty). Present coverage analysis and suggest next topics.

These are NOT pause points:

- Completing an article task type (just advance to the next one)
- Discovering a new source (ingest it, keep going)
- Finding a new entity that warrants a stub (add it to `priorities.json`, keep going)
- Finishing a RALPH loop (save state, start the next action)
- Encountering a non-blocking conflict (log it, keep going)

### Drive sync as backup

`sync push` runs after every 5 completed atomic units, or when CC pauses for a human decision, or when CC hits a context limit. It's a backup mechanism, not a workflow dependency. If CC crashes without a push, the local directory still has everything except the most recent Drive backup.

### Logging

Every atomic unit gets a timestamped entry in `pipeline.log`: what ran, what changed, duration. This replaces the handoff narrative. If the human wants to know what CC did in the last session, they read the log.

---

## Part 3: The RALPH Research Methodology

*Claude reads this third because the RALPH loop is the core intellectual method. It gets invoked by the article pipeline but is distinct from it. Understanding RALPH before the pipeline components prevents conflation.*

### What RALPH is

RALPH is a five-phase iterative research cycle: Retrieve, Analyze, Loop-decide, Process, Hypothesize. It structures how the system investigates any topic. Named after the Ralph Dawson protocol test (v47), which caught a factual conflation in a biographical stub that had survived multiple informal editing sessions.

RALPH is a **research methodology**, not the article pipeline. The article pipeline (Part 4) invokes RALPH loops as part of its RESEARCH and VERIFY task types. An article may go through multiple RALPH loops before advancing to the next pipeline stage.

### The five phases

**R: RETRIEVE.** Check source cache first (avoid redundant fetches). Then execute web searches, archive queries, Drive searches. Log every source checked and every source found, including dead ends. Output: list of sources consulted, new sources discovered, raw data stored to cache.

**A: ANALYZE.** Extract facts from retrieved material. Each fact gets a source citation and confidence level (high/medium/low). Flag contradictions against existing KB facts. Critically: check whether any newly discovered entities warrant new article stubs (people, places, programs, traditions, publications). Output: candidate facts, contradiction flags, stub candidates.

**L: LOOP DECISION.** This is the control mechanism that makes RALPH iterative rather than linear. Three possible outcomes:

- **CONTINUE**: Not saturated (still finding new information), refine queries on the same topic and loop back to R.
- **ADVANCE**: Good coverage on this subtopic, move to a related subtopic and loop back to R.
- **CONCLUDE**: Sufficient material for the current task. Exit the loop and proceed to P.

Factors informing the decision: saturation (are searches returning redundant results?), critical gaps (are there unanswered questions that sources might address?), token/time budget.

**P: PROCESS.** Add verified facts to KB via the KB Engine (Part 5). Update article draft if in a WRITE task. Flag items needing independent verification. Output: KB updated, article updated if applicable.

**H: HYPOTHESIZE.** Propose follow-up queries and research threads for future sessions. Identify archive leads worth pursuing. Register any new article stubs discovered during the A phase into the priority queue. Output: future research suggestions, new stub entries.

### When to use formal vs. informal RALPH

Formal RALPH (explicit phase labeling, structured output per phase) is mandatory for:

- People stubs and biographies (high conflation risk across similarly named documents)
- Founding-era articles (source density creates cross-contamination risk)
- Any article advancing from stub to draft status

Informal RALPH (mental model, no structured output) is acceptable for:

- Adding facts to an existing draft from a known cached source
- Minor updates and cross-reference additions
- E1 review passes on already-verified articles

The v47 protocol test established this distinction empirically. Formal RALPH caught errors that informal approaches missed.

### Mandatory RALPH before writing or review

No article advances to drafting or review without completing at least one full RALPH cycle on that topic. Queue positions (`pending_writing`, `pending_review`) are not authorizations. When picking up a queued item, run the appropriate RALPH loop first.

---

## Part 4: Article Pipeline

*Claude reads this after RALPH because the pipeline invokes RALPH loops. Understanding the methodology before the pipeline prevents treating RALPH as just another pipeline stage.*

### What the pipeline does

The article pipeline advances articles from initial stub through to reviewed, publishable state. It uses four task types executed sequentially, each of which may invoke one or more RALPH loops.

### Article status progression

| Status | What it means | Requirements to reach |
|--------|--------------|----------------------|
| **stub** | Topic identified, minimal content | Title, 1+ fact, 1+ source, research questions listed |
| **draft** | Substantive article exists | Summary, 2+ sections, 3+ sources, structure complete. Requires RESEARCH task + RALPH loop. |
| **R3-verified** | All claims independently checked | VERIFY task complete: every claim has cited source confirmed, dates checked against timeline, names checked against people index |
| **E1-reviewed** | Editorial quality confirmed | REVIEW task complete: cross-links verified, encyclopedic quality, no unsourced speculation, Open Questions are actionable |

Advancement requires the corresponding task type to have been run. No skipping stages.

### The four task types

These are operational modes, not pipeline stages. A single Claude instance executes them sequentially. The labels clarify what mode you're operating in.

**RESEARCH**: Discover and extract information. Web search, archive lookup, Drive cache check. Produce facts with source citations. Invokes one or more RALPH loops. Output: new KB facts, new sources cached, article stub or draft updated.

**VERIFY**: Cross-reference claims against independent sources. For each factual claim in the article: confirm the cited source actually says this, search for one corroborating or contradicting source, check dates against the project timeline, check names against the people index. Invokes formal RALPH when checking biographical claims. Output: correction list, confidence adjustments, conflict records.

**WRITE**: Draft or revise article prose from verified facts. Only runs after a RALPH loop has concluded with sufficient material. Encyclopedic tone, neutral voice, inline citations. Follows the article template (below). Output: article markdown file.

**REVIEW**: Systematic fact-check of a completed article. Every claim reviewed for source grounding, factual accuracy against KB, tone consistency, and absence of unsourced speculation. Check that Open Questions are specific and actionable. Check cross-links to other articles. Output: review notes, corrections applied, status advanced if passing.

### Article template

```markdown
# [Article Title]

*Status: [stub|draft|R3-verified|E1-reviewed] | Sources: [count]*
*Last Updated: [date]*

## Overview
[2-3 paragraph summary of the topic]

## [Chronological or thematic sections]
[Prose with inline source references]

## Open Questions
[Numbered list of specific, actionable research questions]

## Sources
[Full citation list with URLs where available]
```

### Article spawning

During every ANALYZE and HYPOTHESIZE phase of a RALPH loop, check whether newly discovered entities already have wiki articles. If not, and if the entity meets any threshold below, create a stub entry in `priorities.json`:

- Named person who held a camp role (director, staff, notable camper, researcher)
- Recurring event or tradition (L&V Games, Shawbridge Meet, Marois Day, Torch Ceremony)
- Physical structure or location with its own history (Chapel, Hospital, Council Ring)
- Publication or media (Green Triangle, Ka-News, NFB films)
- Program or activity with structure and evolution (canoe tripping, Woodcraft League, hebertism)

Stub entry includes: proposed article path, title, known facts with sources, initial research questions, cross-references to the article where the entity was discovered.

### Article status tracking schema

```json
{
  "article_id": "coeducation-gender",
  "title": "Coeducation and Gender at Kanawana",
  "wiki_folder": "context",
  "status": "draft",
  "status_history": [
    {"status": "stub", "at": "2026-02-10T09:00:00Z", "by": "auto", "task": "RESEARCH"},
    {"status": "draft", "at": "2026-02-10T09:35:00Z", "by": "auto", "task": "WRITE"}
  ],
  "ralph_loops_completed": 2,
  "kb_facts_used": ["f_0342", "f_0343", "f_0344", "f_0350"],
  "sources_cited": ["src_mcmorris_thesis", "src_ymca_website", "src_concordia_12A"],
  "open_questions": 7,
  "cross_links": ["section-names", "lv-games", "canoe-trips"],
  "file_id": "1KW2yhoZ-wr_71sTPbLJ3v81KW4ZEJ_p-",
  "word_count": 1850
}
```

### Commands

- `article new <topic>` - Create stub, run RESEARCH task with RALPH loop
- `article advance <article_id>` - Run next required task type for this article's status
- `article run-full <article_id>` - Run all remaining task types through E1-reviewed
- `article status` - Show all articles and their pipeline positions
- `article review <article_id>` - Present article for human review (after REVIEW task)

---

## Part 5: Source Discovery & KB Engine

*These two components are grouped because they form a natural pipeline: find sources, then extract facts from them. Both get invoked during RALPH loops.*

### Source Discovery & Ingestion

Finds, downloads, and caches primary and secondary sources. Produces structured source records with full-text content ready for fact extraction.

**Source types and handlers:**

| Source Type | Handler | Example |
|------------|---------|---------|
| Internet Archive items | `ia_handler` | Green Triangle newsletters 1932-1940 |
| Web pages | `web_handler` | YMCA Quebec history page, Concordia archives catalog |
| PDFs | `pdf_handler` | McMorris thesis, Director's Reports |
| User-provided text | `manual_handler` | Oral histories, physical document transcriptions |
| Archival catalog entries | `catalog_handler` | Concordia sub-series 12A listings (metadata only, no full text) |

**Source record schema:**

```json
{
  "source_id": "src_green_triangle_1932_v1n1",
  "type": "periodical",
  "title": "The Green Triangle, Vol. 1 No. 1",
  "date": "1932",
  "date_precision": "year",
  "origin": "internet_archive",
  "origin_url": "https://archive.org/details/...",
  "cache_path": "sources/cache/green-triangle/1932-v1n1.txt",
  "char_count": 4200,
  "ingested_at": "2026-02-10T09:00:00Z",
  "extracted": false,
  "extraction_version": null,
  "reliability": "primary",
  "notes": "Camper-authored newsletter. May contain errors in dates/names."
}
```

**Source index:** `sources.json` tracks all known sources, whether cached or not. Uncached sources (e.g., items known to exist at Concordia but not digitized) get records with `cache_path: null` and `type: "catalog_reference"`. This lets the system reason about what exists but can't yet access.

**Commands:**

- `discover <topic>` - Search Internet Archive, web, known archives for new sources on a topic
- `ingest <url>` - Download and cache a specific source
- `ingest-batch <source_list>` - Batch download (e.g., all Green Triangle issues)
- `catalog-scan` - Parse Concordia archives catalog pages and create catalog_reference records

### Knowledge Base Engine

Extracts discrete facts from cached sources, stores them with full provenance, detects conflicts, and serves as the single source of truth for article drafting.

**Extraction constraints (read these before running any extraction):**

- Extract only claims the source actually makes. No inference beyond what's stated.
- Preserve exact dates, names, and numbers from the source.
- Flag uncertainty in the source itself ("about 20 campers" vs "20 campers").
- Never combine information from multiple sources in a single fact. One fact, one source.
- When the source is ambiguous, the fact's confidence should reflect that ambiguity.

**Fact schema:**

```json
{
  "fact_id": "f_0342",
  "claim": "Camp Kanawana began admitting girls in 1968",
  "sources": ["src_ymca_website_history"],
  "confidence": "stated",
  "category": "coeducation",
  "entities": ["Camp Kanawana"],
  "date_ref": "1968",
  "conflicts_with": ["f_0343"],
  "added_version": "3.2",
  "added_by": "auto_extraction"
}
```

**Confidence levels:**

| Level | Meaning | Example |
|-------|---------|---------|
| `stated` | Source explicitly says this | "Camp opened in 1894" |
| `inferred` | Derived from source but not explicit | "Section system existed by 1922" (from brochure structure) |
| `user_knowledge` | Domain expert provided, not yet sourced | "Pathfinders is the senior girls section" |
| `disputed` | Multiple sources disagree | Coeducation date: 1968 vs 1969 |

**Conflict detection:** When a new fact contradicts an existing one (same entity + same attribute + different value), the system does NOT silently overwrite. It creates a conflict record linking both facts, flags the conflict for human review, and preserves both facts in the KB until resolved.

**Extraction pipeline:**

```
Source text → Chunking (by paragraph/section) → LLM extraction (applying constraints above) → 
  Candidate facts → Dedup against existing KB → Conflict check → 
  New facts added with provenance
```

**Commands:**

- `extract <source_id>` - Run fact extraction on a cached source
- `extract-all-new` - Extract from all sources not yet processed
- `kb-search <query>` - Semantic search across facts
- `kb-conflicts` - List all unresolved conflicts
- `kb-stats` - Counts by category, confidence, source coverage
- `kb-export` - Export full KB as markdown (for human review) or JSON

---

## Part 6: Wiki Manager

*The orchestration layer. Consulted during bootstrap and after each atomic unit to determine what to do next.*

### What it does

Tracks the overall wiki: which articles exist, their relationships, coverage gaps, and the global research priority queue.

### Coverage analysis

Compares KB facts against published articles to find:

- **Orphan facts**: KB facts not cited by any article
- **Thin articles**: Articles with fewer than N facts or sources
- **Coverage gaps**: KB categories with no corresponding article
- **Stale articles**: Articles whose cited sources have been updated since last edit

### Priority queue

A ranked list of potential next actions, stored in `priorities.json`:

- New articles suggested by orphan facts or Open Questions
- Sources worth ingesting (flagged during RALPH Retrieve phases)
- KB conflicts awaiting resolution
- Articles ready for the next task type

Priority computed from: number of available sources, number of related KB facts, cross-links from existing articles, and human-assigned weight.

### Cross-reference graph

Articles link to each other through their content. The wiki manager tracks these links and detects broken links (references to articles that don't exist yet), missing links (topics mentioned but not linked), and orphan articles (no incoming links from other articles).

### Commands

- `wiki status` - Dashboard: article count by status, KB stats, priority queue top 5
- `wiki gaps` - Coverage analysis
- `wiki graph` - Cross-reference visualization
- `wiki plan <n>` - Suggest next N actions with rationale
- `wiki export` - Export complete wiki as folder of markdown files

---

## Part 7: Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Orchestrator | Claude Code (CLI) | Already the working environment; agentic execution |
| LLM reasoning | Claude API (Sonnet for extraction/verification, Opus for drafting) | Cost-appropriate model selection per task |
| Web research | Web search tool / requests | Source discovery, RALPH Retrieve phase |
| Internet Archive | `internetarchive` Python package or direct API | Primary source repository |
| PDF extraction | `pdfplumber` or `pymupdf` | For thesis, reports |
| Storage | Local JSON + markdown files | Simple, inspectable, git-friendly |
| Drive sync | Google Drive API via `google-api-python-client` | Persistence, sharing |
| CLI interface | Python `click` or `typer` | Command structure |

---

## Part 8: Migration from Current Project

### Phase 1: Bootstrap from existing state

- Import current KB (v3.2 markdown) into `facts.json` format
- Import cached sources from Drive into local `sources/cache/`
- Create `articles.json` from handoff v48 article inventory
- Create `sources.json` from handoff v48 source listing
- Populate `priorities.json` from handoff v48 next priorities

### Phase 2: Validate on one article

- Pick one existing article at Draft status (e.g., `ralph-dawson`)
- Run RESEARCH task with formal RALPH loop
- Run VERIFY task
- Run WRITE task
- Run REVIEW task
- Compare automated output quality against manual session output
- Tune extraction and drafting prompts based on results

### Phase 3: Scale up

- Batch-ingest Green Triangle issues (P2 from current priority queue)
- Run extraction on all cached but unextracted sources
- Generate new article candidates from orphan facts and coverage gaps
- Human reviews priority queue and selects next articles

---

## Part 9: Proof of Concept Scope

For the Kanawana wiki specifically:

1. Migrate 48 sessions of work into the new structure
2. Complete the remaining ~15 articles identified in the wiki plan
3. Ingest all available Internet Archive sources (~40 items)
4. Build KB to ~500+ facts with full provenance
5. Produce a complete, interlinked wiki exportable as a static site

For the general-purpose wiki builder, Kanawana proves out: handling conflicting historical sources with date precision tracking, working with partial archival records (catalog references without full text), maintaining editorial quality across dozens of articles, scaling research across hundreds of sources, and human-AI collaboration on editorial judgment calls.

---

## Part 10: Open Design Questions

1. **Model routing**: Should extraction use Sonnet (cheaper, faster) while drafting uses Opus (higher quality)? Or is Sonnet sufficient for both?
2. **Batch vs interactive**: Should the pipeline prefer large batch runs (extract all sources, then draft all articles) or keep the current incremental approach?
3. **Version control**: Should the project directory be a git repo? Free versioning and diff capability, but adds complexity.
4. **Static site export**: Should the wiki be exportable as a browsable website (e.g., MkDocs)? Useful for sharing beyond the project team.
5. **MCP integration**: Should the pipeline expose itself as an MCP server for claude.ai conversations?
6. **Multi-project support**: Multiple wiki projects simultaneously, or single-project for POC?
7. **Ralph Loop ops manual integration**: The v2.0.1 Operations Manual (16ok4S59eS7C_KxEf2cLQQzENMqGgF8zW) and Reference Manual (1YZzUDD2lP4oFyl2V2SdfERRyqrD4h168) contain additional protocol details (camp terminology glossary, source reliability heuristics, etc.) that should be incorporated. How much goes into the codebase vs. stays as reference documentation?
