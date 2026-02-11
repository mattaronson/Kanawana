# Kanawana Wiki Builder: Reference Manual

**Version**: 2.0.1
**Project**: LSM:kanawana-history
**Operating Instructions**: `1i8VVOC7uQbXeoToxsy4CTRBMsf-AZDJc` (loaded every session)
**Purpose**: Supplementary reference loaded on demand for templates, schemas, query guidance, and self-improvement review.

---

## Full Article Template

Use when advancing an article from stub to draft or beyond.

```markdown
# [Article Title]

<!-- status: stub|draft|R3-verified|E1-reviewed -->
<!-- confidence: low|medium|high -->
<!-- last_updated: YYYY-MM-DD -->
<!-- last_editor: [handoff_version] -->
<!-- ralph_loops: [contributing loop topics] -->

## Summary

[2-3 sentence overview]

## [Main Section 1]

[Content with inline citations using footnote format^1]

## [Main Section 2]

[Content]

## Timeline

| Date | Event | Source |
|------|-------|--------|
| YYYY | Event description | ^n |

## Open Questions

- [Critical] Question blocking article completion
- [Important] Question improving article
- [Nice-to-have] Question for future research

## Related Articles

- [[path/to/related-article|Display Text]]

## Sources

1. [Author/Title, Publication, Date. URL or Archive Reference]

## Research Notes

<!-- Internal notes for future sessions -->
```

**Stub template** (simpler): Title, status metadata, 2-3 sentence summary, known facts with citations, research questions. Full sections at draft stage.

---

## Wiki Folder Structure

Reflects actual Drive layout. Update as wiki grows.

```
kanawana-wiki/ (1N8952jWe8SLq0BJtdhzAbLRmhdUCKCQX)
+-- [articles at root level by topic]
|   +-- founding-1894.md, timeline.md, wartime-kanawana.md, etc.
|
+-- people/ (1FVgbwvxNLoJuB_GP_Ig9PQyN4Paf4GhG)
|   +-- [individual person articles]
|
+-- source-documents/ (1W5pLDQlkSZ7JsGk11Ixt0JytzYGFNWzX)
    +-- [cached source texts]
```

Create subfolders (programs/, places/) only when the first article in that category reaches draft status.

---

## Structured RALPH Loop Output

Use for formal RALPH loops (people stubs, founding-era articles, stub-to-draft advancement). Not required for informal loops.

```json
{
  "loop_topic": "descriptive topic name",
  "iteration": 1,
  "task_type": "RESEARCH|VERIFY|WRITE|REVIEW",
  "retrieve": {
    "cache_hits": ["slug1"],
    "queries_executed": ["query1"],
    "sources_found": [
      {"id": "src_NNN", "type": "web|archive|thesis", "title": "...", "url_or_ref": "..."}
    ]
  },
  "analyze": {
    "facts_extracted": [
      {"fact": "...", "source": "src_NNN", "confidence": "high|medium|low"}
    ],
    "contradictions": [],
    "gaps": ["..."]
  },
  "loop_decision": {
    "decision": "CONTINUE|ADVANCE|CONCLUDE",
    "rationale": "one sentence"
  },
  "process": {
    "articles_updated": ["path"],
    "kb_updated": true,
    "stubs_spawned": ["path"]
  },
  "hypothesize": {
    "next_queries": ["..."],
    "archive_leads": ["..."]
  }
}
```

---

## Query Templates

### Web Search

```
[person] YMCA Montreal camp [decade]
"[exact name]" Kanawana OR "Kamp Kanawana"
[topic] site:concordia.ca archives
[event] [year] Montreal Gazette OR Montreal Star
Camp Kanawana [activity] [year range]
"[person name]" obituary Montreal
YMCA Montreal annual report [year]
```

### Internet Archive

```
site:archive.org "kamp kanawana" OR "camp kanawana"
site:archive.org YMCA Montreal boys camp
site:archive.org collection:ymca-montreal-fonds [topic]
```

Prefer `djvu.txt` or plain text versions for extraction. After successful fetch, cache to Drive immediately.

### Cross-Reference Strategies

- Claim from web search: corroborate against cached source documents.
- Date from one source: verify against timeline article and at least one other source.
- Name spelling: check across all sources for variants (French/English differences common).
- Role attribution: verify against directors index and KB entries.

---

## Internet Archive Inventory

50 items identified in the YMCA Montreal fonds on archive.org (searched v47). Seven are cached. Highlights not yet cached:

- Green Triangle issues: 1932 (5), 1933 (3), 1935 (3), 1936 (2), 1938 (4), 1939 (3), 1940 (2)
- 1928/1929 "Come to Kanawana" brochures
- 1938/1941 radio broadcast scripts
- Director's Reports: 1973, 1975, 1977, 1978
- Annual Reports: 1965, 1969
- 1988 "Kanawana, A Place to Grow" report
- Ka-News: 1978-04, 1978-12, 1981-02
- The Lookout v1n3 (1993)
- Kamp Kanawana maps (1928 + undated)

---

## Source Reliability Guidance

Not all sources carry equal weight. Use judgment, not numerical scores.

**Strongest**: Original documents, firsthand accounts. Archive materials, camp reports, photographs, contemporaneous correspondence. The 1935 History, 1922 brochure, CFCF broadcast scripts.

**Strong**: Peer-reviewed and thesis-level research. McMorris thesis (2023).

**Reliable**: Official organizational sources. YMCA annual reports, CCA publications, institutional records, Kanawana Facts sheet.

**Useful but verify**: Contemporary news coverage. Montreal Gazette, Montreal Star. Good for dates and events, less reliable for interpretation.

**Supplementary**: Secondary books and articles that cite other sources. Follow their citations to the original.

**Use with caution**: Web sources without clear authorship. Can provide leads but claims need independent verification.

When two sources conflict, prefer the one closer in time to the event, with more direct access to the subject, and with more specific detail. Note significant conflicts in Research Notes.

---

## McMorris Thesis Reference

**Title**: "An Experience That Lasts a Lifetime: Building Modernity, Man, and Nation at the YMCA of Montreal's Kamp Kanawana, 1894-1967"
**Author**: Grace McMorris, MA thesis, Concordia University (August 2023)
**Supervisor**: Dr. Peter Gossage
**Drive ID**: 14ID3qU1s9B4AL_CxBgXyA32mAUE55x0M
**Spectrum URL**: https://spectrum.library.concordia.ca/id/eprint/992763/
**Status**: Chapters 1-3 + Conclusion fully extracted, 78 facts catalogued in KB

**Chapters**:
- Ch.1 (pp.22-52): "God's Laboratory" -- Christian character, Boys Work, health, gender
- Ch.2 (pp.53-79): "Playing Indian" -- Council rings, totem poles, Indian lore, colonialism
- Ch.3 (pp.80-106): "The National Vehicle" -- Canoe trips, voyageur myth, L&V Games, 1967 Centennial

**Archival sources cited**: P145/12B01 (season reports), P145/12B07 (program), P145/12B04 (communications), P145/02D (annual reports 1902-1964)

---

## Handoff JSON Schema

Practical minimum fields. Expand as needed.

```json
{
  "project": "kanawana-history",
  "version": 47,
  "timestamp": "ISO datetime",
  "kb_version": "3.2",
  "kb_file_id": "...",
  "instruction_version": "2.0.1",
  "instruction_file_id": "...",

  "source_cache": {
    "slug": {
      "drive_id": "...",
      "original_url": "...",
      "title": "...",
      "format": "txt",
      "date_cached": "YYYY-MM-DD",
      "size_chars": 0,
      "topics_relevant": ["..."]
    }
  },

  "article_status": {
    "E1-reviewed": ["article-path"],
    "R3-verified": ["..."],
    "draft": ["..."],
    "stub": ["..."]
  },

  "pending_stubs": [],
  "pending_writing": [],
  "pending_review": [],

  "next_session_priorities": [
    "P1: description",
    "P2: description"
  ],

  "self_improvement_notes": ["..."],

  "memory_entry": "LSM:kanawana-history|F:...|S:...|M:..."
}
```

---

## Self-Improvement Protocol

Run at session end, before generating handoff.

**Efficiency check**: Did any searches repeat a cached document? Did any loop run more than 3 iterations without concluding? Were priorities well-chosen?

**Instruction check**: Did anything in the operating instructions cause confusion or wasted effort? Did any terminology cause errors?

**Proposed changes**: Record in `self_improvement_notes`. Classify as:
- Minor (apply next session)
- Significant (test on one loop first)
- Structural (discuss with user)

Increment version number after applying changes. Note in Document Control.

---

## Design Rationale (v2.0)

The v1.2 instructions described an 8-subagent architecture that never operated as designed. The v2.0 split preserves the RALPH protocol in compact form while acknowledging reality: one Claude instance does sequential work.

The critical insight: features designed but never implemented should not be dismissed as failures. The source cache was specified in v1.2, never built, and the resulting redundant fetches wasted an estimated 30,000-60,000 tokens. The formal RALPH protocol, when tested in v47, caught a factual error that informal editing had missed across multiple sessions. Design that anticipates problems is vindicated when finally implemented.

---

## Document Control

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2026-02-06 | Created as companion to v2.0 Operating Instructions. Material moved from v1.2 monolith. |
| 2.0.1 | 2026-02-08 | Added Internet Archive inventory. Added McMorris thesis reference section. Added formal vs. informal RALPH guidance from v47 Protocol Test results. Updated handoff schema. Updated design rationale with v47 evidence. Updated ops file ID pointer. |
