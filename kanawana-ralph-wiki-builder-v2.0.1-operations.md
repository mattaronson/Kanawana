# Kanawana Wiki Builder: Operating Instructions

**Version**: 2.0.1
**Project**: LSM:kanawana-history
**Folder**: `1Q7YnhBY1gTpozuSBoZaPHxowCOhKrxNN`
**Reference Manual**: `1YZzUDD2lP4oFyl2V2SdfERRyqrD4h168` (load on demand, not every session)

---

## Quick Start

```
Continue Kanawana history.
Instructions: [THIS_FILE_ID]
Handoff: [INSERT_LATEST_HANDOFF_ID]
Folder: 1Q7YnhBY1gTpozuSBoZaPHxowCOhKrxNN
```

**Current handoff**: `16W0dktdS9EewoBsvfEOeD1LCCoYaTNdE` (v47, 2026-02-07)

Update this section with the new handoff ID at session end.

---

## Source Document Cache (CHECK BEFORE EVERY SEARCH)

Re-fetching previously retrieved documents is the single largest token waste in this project. The 1935 History alone was fetched 6-7 times before caching was implemented.

**Cache folder**: `source-documents/` (Drive ID: `1W5pLDQlkSZ7JsGk11Ixt0JytzYGFNWzX`)

**Cache index**: In the handoff under `source_cache`. Maps slugs to Drive file IDs, original URLs, and topic tags.

**Rules (no exceptions)**:

1. At session start, load `source_cache` from handoff into working memory.
2. Before ANY web_search or web_fetch for a document, check the cache by slug or topic tag.
3. If cached: download from Drive (1 API call). Do not search the web.
4. After ANY successful full-text extraction from Internet Archive, Concordia, or any web source: upload extracted text to the cache folder on Drive and register it in `source_cache`.
5. Include `topics_relevant` so loops on different subjects find cross-cutting sources.

**Cache entry format**:
```json
"slug": {
  "drive_id": "...",
  "original_url": "...",
  "title": "...",
  "format": "txt",
  "date_cached": "YYYY-MM-DD",
  "size_chars": 0,
  "topics_relevant": ["topic1", "topic2"]
}
```

---

## RALPH Loop Protocol

Every research cycle follows Retrieve, Analyze, Loop-decision, Process, Hypothesize.

**R: RETRIEVE** -- Check source cache first. Then execute web_search, web_fetch, drive_search, archive queries. Log sources checked and found.

**A: ANALYZE** -- Extract facts with source citations and confidence (high/medium/low). Flag contradictions. Check for entities that warrant new article stubs.

**L: LOOP DECISION** -- Three outcomes:
- CONTINUE: Not saturated, refine queries on same topic.
- ADVANCE: Good coverage, move to related subtopic.
- CONCLUDE: Sufficient material for current article stage.

Factors: saturation, critical gaps remaining, token budget.

**P: PROCESS** -- Add wiki-ready facts to article. Update KB. Flag items needing independent verification.

**H: HYPOTHESIZE** -- Propose follow-up queries, related threads, archive leads. Register new article stubs discovered during A phase.

### Mandatory RALPH Loop Before Writing or Review

No article advances to drafting or review without completing at least one full RALPH cycle. `pending_writing` and `pending_review` are queue positions, not authorizations. When picking up a queued item, run the appropriate loop first.

### When to Use Formal vs. Informal RALPH

The v47 Protocol Test established that formal RALPH loops (explicit phase labeling, structured output) catch errors that informal approaches miss. The test caught a significant factual conflation in ralph-dawson.md that had survived multiple informal editing sessions.

**Use formal RALPH** (explicit phase labels, structured output) for:
- People stubs and biographies (high conflation risk across similarly named documents)
- Founding-era articles (source density creates cross-contamination risk)
- Any article advancing from stub to draft

**Use informal RALPH** (mental model, no structured output) for:
- Adding facts to an existing draft from a cached source
- Minor updates and cross-reference additions
- E1 review passes on already-verified articles

---

## Four Task Types

A single Claude instance executes these sequentially. The labels clarify what mode you are operating in.

**RESEARCH**: Web search, archive lookup, Drive cache check. Produce facts with source citations.

**VERIFY**: Cross-reference claims against independent sources. For each factual claim: confirm cited source exists, search for one corroborating or contradicting source, check dates against timeline, check names against people index.

**WRITE**: Draft or revise article prose from verified facts. Encyclopedic tone, neutral voice, inline citations. Only after a RALPH loop has concluded with sufficient material.

**REVIEW**: Systematic fact-check of every claim in a completed article. Produce a correction list. Required before any article advances to R3-verified or E1-reviewed.

---

## Article Status Progression

| Status | Requirements |
|--------|-------------|
| stub | Title, 1+ fact, 1+ source, research questions listed |
| draft | Summary, 2+ sections, 3+ sources, structure complete |
| R3-verified | VERIFY pass complete, all claims cited, no critical gaps |
| E1-reviewed | REVIEW pass complete, cross-links verified, encyclopedic quality confirmed |

Advancement requires the corresponding task type to have been run.

---

## Article Spawning

During every ANALYZE and HYPOTHESIZE phase, check whether newly discovered entities already have wiki articles. If not, and the entity meets any of these thresholds, create a stub entry in the handoff's `pending_stubs`:

- Named person who held a camp role
- Recurring event or tradition
- Physical structure or location with its own history
- Publication or media
- Program or activity with structure and evolution

---

## Session Workflow

### 1. Bootstrap

1. Load this instruction document.
2. Load handoff (by ID from prompt, or find latest in folder).
3. Load KB from `kb_file_id` in handoff.
4. Load `source_cache` into working memory.
5. Display STATUS: article counts by status, active/pending queues, priorities.

### 2. Resume or Initialize

- If `pending_writing` or `pending_review`: pick highest priority, run prerequisite RALPH loop, then execute.
- Otherwise: work from `next_session_priorities`.

### 3. Execute

Run RALPH loops on assigned topics. After each loop concludes:
- Update article status if warranted.
- Register new sources in cache (upload text, add to index).
- Spawn stubs for discovered entities.
- Check token budget before starting next loop.

### 4. Session End

1. Complete or pause all active work.
2. Generate `next_session_priorities`.
3. Upload updated KB, handoff, and any new/revised wiki articles to Drive.
4. Update `source_cache` in handoff with any new cached documents.
5. Update this document's Quick Start with new handoff ID.
6. Upload updated instruction doc.
7. Update Claude Memory entry.

---

## Token Budget

| Remaining | Action |
|-----------|--------|
| >50% | Full execution, start new loops freely |
| 30-50% | Complete current loops, prioritize writing over new research |
| 20-30% | Complete active loop only, no new assignments |
| <20% | Immediate handoff. No new work. |

---

## Camp Terminology

Use consistently across all articles.

- **Chief**: Title for the camp Director through most of the 20th century. Same role, different era. Fell out of use by approximately 2020. In pre-2020 articles, use "Chief" with "(Director)" on first reference. Sourced to the 1935 History.
- **Section**: Age-based camper division (Senior, Junior, Juvenile, Bantam). Not a physical area.
- **Tuck / Tuck Shop**: Camp store.
- **Marois Day**: Major visiting/social event.
- **Council Ring**: Ceremonial gathering space, distinct from campfire area.
- **Voyageurs de la Verendrye**: Extended canoe tripping program introduced in the 1950s.
- **CIT**: Counsellor-in-Training program, introduced in the 1960s.
- **L&V Games**: Lumbermen vs. Voyageurs competition, inspired by Pinecrest Camp, started 1947.

Add new terms as discovered, sourced to earliest available documentation.

---

## Key File IDs

| Item | Drive ID |
|------|----------|
| Project folder | 1Q7YnhBY1gTpozuSBoZaPHxowCOhKrxNN |
| Wiki folder | 1N8952jWe8SLq0BJtdhzAbLRmhdUCKCQX |
| People folder | 1FVgbwvxNLoJuB_GP_Ig9PQyN4Paf4GhG |
| Source cache folder | 1W5pLDQlkSZ7JsGk11Ixt0JytzYGFNWzX |
| KB (v3.2) | 1-RTwDPujhRODKXHKBsIXXM1-0YnL-KtN |
| Reference Manual | 1YZzUDD2lP4oFyl2V2SdfERRyqrD4h168 |
| McMorris thesis PDF | 14ID3qU1s9B4AL_CxBgXyA32mAUE55x0M |

---

## When to Load the Reference Manual

Load `1YZzUDD2lP4oFyl2V2SdfERRyqrD4h168` when you need:
- Full article template (advancing stub to draft)
- Wiki folder structure reference
- Query templates for web search and archive research
- Sample RALPH loop walkthrough
- Handoff JSON schema details
- Self-improvement protocol steps
- Source reliability guidance
- Internet Archive inventory

Do not load every session.

---

## Document Control

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-24 | Initial creation |
| 1.1 | 2026-01-29 | Added explicit handoff ID to continuation prompt |
| 1.2 | 2026-02-05 | Source cache, article spawning, camp terminology, mandatory RALPH before writing |
| 2.0 | 2026-02-06 | Split into Operations + Reference Manual. 8 subagents replaced with 4 task types. Removed unused command reference, parallel execution diagrams, structured JSON outputs from per-session load. |
| 2.0.1 | 2026-02-08 | Incorporated v47 Protocol Test results: formal RALPH recommended for people/founding articles, informal for routine updates. Fixed Quick Start IDs. Added Key File IDs table. Expanded terminology (Voyageurs, CIT, L&V Games). Removed Protocol Test Directive (completed). |
