# Research Provenance Archive

Committed record of every background research agent spawned for this project, so future sessions
**do not redo searches that were already run** (including null/dead-end results, which are the
easiest work to accidentally repeat).

## Why this exists

Agent transcripts live under `/root/.claude/` — **container-local and ephemeral**. They vanish
when the container is reclaimed. This archive is the distilled, git-committed snapshot taken
2026-06-26 while the transcripts still existed.

## What's here

- **`INDEX.md`** — one row per agent: `agent_id | status | tool-uses | topic | 1-line outcome`.
  Statuses: `completed`, `spend-killed` (died on org monthly spend limit — value, if any, is in a
  sibling agent or the KB), `no-final`.
- **`reports/<agent_id>.md`** — the full final report for each *completed* agent.

## How to use it (do this BEFORE spawning a research agent or running web searches)

1. **Grep first.** `grep -i "<your topic>" project-docs/research-provenance/INDEX.md`
   and `grep -ril "<term>" project-docs/research-provenance/reports/`.
2. If a prior agent already covered it, **read its report** instead of re-searching. Null results
   count — if the report says "40 searches, no obituary found," don't re-run those 40 searches.
3. Only spawn a new agent for genuinely new angles, or to push past where a prior agent stopped
   (its report usually states what surfaces remain unchecked).

## Important caveat

**Agent IDs are reference labels, not resumable handles.** You cannot `SendMessage` a past agent in
a new session — its runtime is gone. Read the committed report; do not try to re-attach.

## Relationship to other records

- **Findings** are already integrated into `kb/facts.json` + `wiki/` (verified by the Campaign 21
  audit). This archive preserves the *process* (queries, surfaces, nulls), not new facts.
- **Campaign-level** narrative is in `project-docs/research-log.md`. This archive is the
  agent-level granularity beneath it.
