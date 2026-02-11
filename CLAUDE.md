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
│   ├── articles.json         # Article status tracker
│   ├── context/ programs/ people/ places/ chronology/ documents/ meta/
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

### Article Status Schema

```json
{
  "article_id": "string",
  "title": "string",
  "wiki_folder": "context|programs|people|places|chronology|documents|meta",
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
