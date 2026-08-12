# Build State Review — 2026-08-12

*A point-in-time audit of the wiki, KB, and queue, done at the operator's request. This is a
review + roadmap document, not a research campaign — no new facts were extracted and no article
prose was changed. Three concrete gaps found during the audit were queued (p_218-p_221) but not
executed. Read this once, then resume the standing execution loop from the queue as normal.*

## 1. Headline numbers (verified by direct file inspection, not by trusting prior handoff docs)

| | Count |
|---|---|
| Wiki articles | 85 |
| — E1-reviewed | 50 |
| — draft | 28 |
| — R3-verified | 3 |
| — stub | 4 |
| KB facts | 1,947 |
| Sources | 645 |
| Conflicts logged | 20 (all resolved/resolved_editorially/likely_resolved, 1 partially_resolved) |
| Priority queue items | 221 (172 completed, 25 blocked, 16 pending, 3 done, 1 exhausted-web, +4 new from this review) |
| Cross-links (`[[...]]`) | 711, **0 broken** (verified by script — every target resolves to a real file) |

Current HEAD: `bbfe8aa` "Reorganize wiki as hub-and-spoke" (#4, merged to `main`), which itself
lands on top of `fbb41a4` "Merge Campaigns 40-73" (the `build-roadmap` branch). Both are on `main`
already — there is no unmerged work sitting on a stale branch.

## 2. What the last major push (Campaigns 40-73) actually did

Two back-to-back projects, both completed and merged:

1. **Workstream A/B/C plan** (Campaigns 40-70): standardized headers across 54 pre-existing
   articles, built two hub pages (`timeline-overview.md`, enhanced `quebec-camp-landscape.md`) and
   a tags schema, then spawned 24 new standalone articles — mostly splitting already-researched
   material out of `notable-alumni.md` and `directors-index.md`'s Two-Tier Era tables into their
   own pages (17 people, 1 place, 2 programs/documents, 4 chronology-era hub-fillers). Net: 54 → 78
   articles, **zero new research** — this was reorganization and synthesis of already-cited facts,
   not new fact-finding.
2. **Operator-authorized C5 privacy-policy revision** (Campaign 71): Matt (the operator, also this
   KB's oral-history source) asked in-session to add himself and brother Dan Aronson to the wiki,
   scoped narrowly (camp/public role only, no family/blog detail). 8 more articles spawned,
   including 6 formerly-privacy-listed director names with real documentation. 78 → 85 (excluding
   one article that was a stub-to-stub swap during folder reorg counting).
3. **Campaign 73**: three small VERIFY items closed out the queue's backlog of pre-network-fix
   blocked items.
4. **Hub-and-spoke reorg** (separate PR #4, most recent commit): re-filed 49 of 85 articles by
   *distance from Kanawana's own identity* rather than flat topic, per the pattern CLAUDE.md now
   documents. Rewrote all 415 affected cross-links. Verified independently in this review — link
   integrity holds.

## 3. Gaps found in this review (not previously tracked — now queued)

**a. 28 articles (33% of the wiki) are stalled at `draft`, one required task type short of
R3-verified.** All 28 were spawned in the Campaigns 65-71 synthesis push and never got a VERIFY
pass — the pipeline correctly held them at draft (no skipping stages), but nothing in the queue
was tracking the VERIFY debt. This is the single largest concrete lever available right now: none
of it requires new research, since every claim was already cited when the articles were split out
of `notable-alumni.md`/`directors-index.md`. **Queued as p_218.**

**b. 3 articles sitting at R3-verified never got their REVIEW pass**: `winter-programming.md`,
`indigenous-names-and-land.md`, `joanna-hoad.md`. **Queued as p_219.**

**c. 40 dangling `source_id` references** — facts in `kb/facts.json` cite source IDs that don't
exist in `sources/sources.json`. This exact problem was found and partially fixed in Campaigns 65,
66, 69, and 70 (each fixing a handful of typo'd/malformed IDs encountered incidentally while
working on unrelated articles), and pipeline.log explicitly flagged it twice as needing "a future
priorities.json entry" — that entry was never created. Re-counted directly against the current
files: 40 remain. **Queued as p_220.**

**d. Campaign 72's work is gone, not just unfinished.** Campaign 71's pipeline.log entry names 14
more plaque-only formerly-C5 names as "remaining, to be spawned as short honest stubs in a
following campaign," and a later log line references a "Campaign 72" batch as "still uncommitted,
left for the operator per their explicit instruction." No such commit exists on any branch, in
reflog, or in stash — the batch was never persisted and is unrecoverable (consistent with
`SESSION-HANDOFF.md`'s own warning that agent work is ephemeral until committed). **Queued as
p_221**, flagged to re-confirm scope with the operator first since the original C5 revision was
scoped case-by-case, not as a blanket list removal.

**e. Documentation has drifted out of sync with the actual state** — worth knowing before trusting
any file other than the primary state files (`kb/facts.json`, `wiki/articles.json`,
`queue/priorities.json`, `kb/conflicts.json`):
   - `project-docs/research-log.md` stops at Campaign 37 (2026-07-10) — Campaigns 38-73 exist
     only in `logs/pipeline.log`, never got the narrative write-up the earlier campaigns have.
     Not a blocker (pipeline.log has the facts), but if the narrative-log habit is worth keeping,
     future campaigns should write to both, or the convention should be formally retired in favor
     of pipeline.log alone.
   - `project-docs/SESSION-HANDOFF.md` and `project-docs/NEXT-SESSION-PROMPT.md` both describe
     state as of 2026-07-02/07-05 (1,529-1,704 facts, 52-78 articles) — 5+ weeks and 45+ campaigns
     stale. Their operational lessons (network-proxy fix, photo-rights bug, agent-ephemerality
     warning) are still valid and worth keeping; their numbers and "START HERE" pointers are not.
   - `project-docs/checkpoints/CURRENT_STATE.md` is a Session-3 (2026-02-16) RALPH checkpoint,
     effectively an artifact of an abandoned earlier tracking convention. Recommend archiving
     rather than updating, since `queue/priorities.json` has been the real source of truth for a
     long time.
   - None of this caused actual data loss or corruption — the underlying JSON state files are
     internally consistent and this review's spot-checks (link integrity, conflict-status audit,
     source-id audit) found no other silent divergence.

## 4. State of the genuinely-blocked queue (25 items)

Confirmed by reading each one: all 25 `blocked` items are honest dead ends per Phase 2's own
"exhausted" bar (8+ queries, 3+ surfaces, logged null results) — they need one of: a paid
Newspapers.com subscription, physical Concordia Archives access (P0145 fonds — several specific
box numbers now identified), oral history directly from Matt, or one Facebook/Issuu page that
needs a human with a JS-rendering browser. None of them should be re-attempted by further web
search; re-attempting would just re-confirm what's already logged. This matches CLAUDE.md Phase
2's own definition of a true dead-end requiring operator/physical access.

The `pending` items (16, now 20 with this review's additions) are actionable without operator
input except p_221 (needs a scope confirmation) and the oral-history-instrument items, which
CLAUDE.md's own pending directive says to hold until Matt asks.

## 5. Recommended next-steps order

1. **p_218 (VERIFY 28 drafts → R3-verified)** — highest value, zero new research needed, directly
   unblocks 33% of the wiki from its current pipeline stage. Batch in clusters of 4-6 as prior
   Workstream campaigns did.
2. **p_219 (REVIEW the 3 R3-verified articles → E1-reviewed)** — small, fast, closes out that
   status tier entirely (0 articles would remain at R3-verified).
3. **p_220 (fix 40 dangling source_ids)** — mechanical KB-integrity cleanup, same pattern as four
   prior campaigns already used successfully; low effort, prevents citation-marker verification
   from silently masking broken provenance.
4. **p_221 (14 plaque-only stub names)** — only after confirming scope with the operator per the
   note above.
5. Resume the standing pending-queue items (p_194-p_217) in existing rank order — most need either
   operator action or are already correctly parked.
6. Optional documentation hygiene: refresh `SESSION-HANDOFF.md`'s "START HERE" pointer to this
   review, and decide whether to keep maintaining `research-log.md`'s campaign narrative going
   forward or retire it in favor of `pipeline.log` alone (item 3e above).

No human-decision-point conflicts are open, and the queue is not empty — so per CLAUDE.md's
execution model, the standing instruction is to resume the loop at p_218 rather than wait for
further direction. This review stops here because it was itself the requested unit of work.
