# Session Handoff — Operational Lessons

*Read this first when resuming. These are working-method lessons from prior sessions that are
NOT captured in CLAUDE.md. Update this file when you learn something new about HOW to work
(not WHAT was found — that goes in the KB / research-log).*

*Last updated: 2026-06-26*

---

## Resuming

- Run `continue`. State lives entirely in committed files (`kb/facts.json`, `wiki/articles.json`,
  `queue/priorities.json`, `kb/conflicts.json`, `project-docs/research-log.md`) — not in chat.
  Nothing from a prior conversation is needed.
- Current state: KB **v4.89** (1,525 facts, 541 sources, 13 conflicts). All 54 articles R3/E1.
  `main` == latest work (fully merged 2026-06-26).

## Before searching/ingesting ANY source — avoid redundant work

- **Check first whether it's already done.** Grep `sources/sources.json` for the source and look
  at `extracted` / `extraction_version`. Grep `kb/facts.json` for the topic. Many "blocked"
  priorities were actually already extracted (the McMorris thesis was re-queued as blocked
  multiple times despite being fully mined — the operator was rightly frustrated).
- A priority marked `blocked` is not proof of incompleteness. Re-read its `result`/`blocking_reason`
  before acting. Mark genuinely-finished items `completed` so they stop resurfacing.
- When an agent reports a finding, confirm it's in the KB **and** in the article prose. Facts often
  landed in `facts.json` but never got propagated into article text — that gap is real and worth a
  pass (see the c_009-c_013 / Otoreke-dates / Weskarini propagation fixes this session).

## Photos / images

- **The sandbox cannot fetch images** (all WebFetch → 403). Images arrive only via (a) operator
  drag-drop into chat, or (b) a Claude-for-Chrome session that downloads them.
- Infrastructure is ready: `assets/images/credits.json` (provenance manifest, one entry per
  identified image, created BEFORE the file lands) and `assets/images/PHOTO-ACQUISITION.md`
  (tiered checklist). A reusable Chrome prompt pattern: exact URLs + search terms + the exact
  `target_filename` + a per-item report format (direct URL, caption, date, rights).
- **Canadian copyright shortcut:** photographs made **before 1949 are public domain in Canada** —
  so the oldest archival images (1898, c.1910, 1915, 1944) are the safest to display. Flag
  1950+ items as "permission needed."
- Best image sources found: Concordia Records Management Flickr + the official Kanawana Flickr
  "University Concordia Archives" album; QAHN; CCA (Ross & Macdonald drawings). Concordia AtoM and
  CCA viewers sometimes block right-click download — capture the direct image URL as fallback.

## Background research agents

- **Agents can die mid-run on the org "monthly spend limit"** — 8 did this session. Their final
  message is the error, not a report. Always read the **last real assistant text**, and treat a
  topic as covered only if a *sibling* agent or the KB confirms it.
- Prefer a **mechanical scan over re-running agents** when auditing for missed facts: a Python
  token-coverage check (distinctive entities/years/numbers vs `facts.json` + article text) is free,
  deterministic, and immune to spend limits. Pattern saved conceptually in research-log Campaign 21.
- An agent's `.output` file is a symlink to a JSONL transcript — parse the last assistant `text`
  block; don't read the raw JSONL as if it were the answer.

## The Background-tasks UI panel is misleading — do not trust it

- It shows orphaned cards from every agent ever spawned across the (repeatedly compacted) session.
  Their **timers tick up forever** (the UI computes `now − start`), so they appear to run for
  "hundreds of hours." **This is a display artifact, not real work.**
- Proof an agent is dead, not running: its **token/tool-use counts are frozen** (a live agent's
  would climb). Confirm reality with `TaskList` (→ "No tasks found"), `uptime` (container is
  usually seconds/minutes old — ephemeral), and `ps aux | grep agent` (no subagent processes).
- Don't burn turns debating the panel; verify once and move on.

## Conflicts

- Follow the no-silent-overwrite rule: when sources disagree, add a `kb/conflicts.json` record and
  set `conflicts_with` on the facts. When resolving, prefer the **primary/official source**
  (e.g. RSVL/MELCCFP over a derived estimate) and note the reasoning in the conflict's `notes`.

## Git / merge

- `gh` is **not installed** and the **GitHub MCP server is often disconnected**, so PRs usually
  can't be opened from here. To merge with explicit operator permission, fast-forward:
  `git push origin HEAD:main` (the feature branch is a strict descendant of main, so it's clean).
- Develop on `claude/camp-kanawana-research-zusW1`; never touch `main` without explicit go-ahead.

## Session hygiene (token efficiency)

- **One session per phase** (research campaign / integration / photo pass / oral history); merge to
  `main` at each boundary, then start fresh. Drift is real — verify-the-UI tangents and
  re-derivation cost the most.
- MCP tools unrelated to this project (Canva, Shopify, QuickBooks, Uber, etc.) consume ~19% of the
  context window. Disconnecting unused MCP servers is a bigger, permanent saving than restarts.

## Highest-value remaining work (web research is near-exhausted)

1. **Oral history** — the only path to the Chopsy legend, songs/cheers, Grand Portage/Longhouse.
   Draft the full structured instrument once, present in one sitting (per CLAUDE.md pending item).
2. **Photos** — run the Chrome acquisition prompt; integrate into articles with credit lines.
3. Residual blocked items need **physical archives** (Concordia P0145), **paywalls**
   (Newspapers.com, Registre foncier), or books that are **print-disabled/borrow-only on IA**
   (Fong McConnell bio, Penton LCC history) — operator/physical access only.
