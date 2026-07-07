# Session Handoff — Operational Lessons

*Read this first when resuming. These are working-method lessons from prior sessions that are
NOT captured in CLAUDE.md. Update this file when you learn something new about HOW to work
(not WHAT was found — that goes in the KB / research-log).*

*Last updated: 2026-07-02*

---

## Network access 403s — root cause found (2026-07-05)

The recurring HTTP 403 on `ymcaquebec.org`, `linkedin.com`, `facebook.com`, `concordia.ca`, `cbc.ca`,
`web.archive.org` (and, on testing, essentially every other non-package-registry domain —
`archive.org`, `spectrum.library.concordia.ca`, BAnQ, newspapers.com, instagram.com) was **not** a
proxy bug, a stale-session/propagation-timing issue, or the wrong environment being edited. Matt
confirmed (2026-07-05) he had typed the target domains into the environment's **Allowed Domains**
box but never switched the **Network Access level** dropdown itself to **Custom** — it was still on
Trusted (or None). The Allowed Domains list is inert unless the level is Custom; Trusted only
permits a fixed Anthropic allowlist (package registries, GitHub/GitLab/Bitbucket, cloud SDKs) that
none of this project's research domains are on. `curl -v` against the local agent proxy confirmed
the CONNECT tunnel reaches the upstream gateway fine and the gateway itself returns the 403 — the
local proxy and network path were never the problem.

**Fix**: in the environment settings (claude.ai/code → cloud icon → edit environment), explicitly
select **Custom** as the Network Access level (not just fill the domains box), save, then start a
**new** session — network policy is fixed at session boot, not hot-reloaded into a running session.
**If a future session still 403s on these hosts after Matt says he's fixed it**, re-verify the access
level is actually Custom (not just the domains list) before assuming it's a new/different problem.

## ⚡ START HERE (next session)

1. **See `project-docs/NEXT-SESSION-PROMPT.md` (2026-07-05 version) for the current handoff** —
   it supersedes the photo-integration prompt referenced lower in this section. Short version:
   the ~140 untapped plaque photos flagged in item 2 below got a full visual-mining pass on branch
   `claude/photo-image-metadata-mining-81iv0v` (PR #2, open/draft) — 159 new facts, a resolved
   director-timeline conflict (c_014, via oral history revealing a 1995 Executive/On-Site Director
   split), and a RALPH web-verification pass that's *partially* blocked on an egress-proxy 403
   Matt is trying to get lifted. Read the prompt file for the full state and the next concrete
   steps.
2. **Photo integration is DONE (2026-07-02).** 234 of the 244 delivered images are filed in
   `assets/images/{historical,maps,plaques,artifacts,art}/`, credited in `credits.json`, and a
   curated ~40-image selection is wired into 15 wiki articles. See research-log.md Campaign 22
   for the full account, including a rights-classification bug caught mid-integration (plaque and
   artifact photos were briefly misclassified as pre-1949 public domain based on the depicted
   subject's date rather than the photograph's own date — fixed before committing). The ~140
   dining-hall plaque photos flagged here as an untapped source are no longer untapped — see #1.
   8 want-list items from `PHOTO-ACQUISITION.md` are still `not_acquired` (flag-raising c.1910,
   camp truck c.1910, the 1898 Jubilee photo, Otoreke items, McCord postcard, Harold Cross
   portrait, centennial poster, Facebook album) — none were present in the 2026-06-29 delivery.
3. **NOT doing oral history right now** — Matt explicitly deferred it (2026-06-29), though he did
   volunteer a substantial piece of it unprompted on 2026-07-05 (the director-timeline
   restructuring in #1). The instrument at `project-docs/oral-history-instrument.md` is drafted
   and ready, but do not present/run it unless Matt asks.

## Resuming

- State lives entirely in committed files (`kb/facts.json`, `wiki/articles.json`,
  `queue/priorities.json`, `kb/conflicts.json`, `project-docs/research-log.md`) — not in chat.
  Nothing from a prior conversation is needed.
- **Trust the files over any remembered/label numbers.** File-verified state as of 2026-07-02
  (branch `claude/camp-kanawana-research-zusW1` @ commit `e202f20`, == `origin`):
  - `kb/facts.json`: **1,529 facts** (+4 from the photo-integration session: f_1564-f_1567, read
    directly off delivered plaque/artifact photos).
  - `sources/sources.json`: **544 sources** (+3 photo-batch sources). Note: the `source_count`
    field had drifted stale (read 492 against an actual array length of 541) before this session
    corrected it — don't trust that field blindly either; count the array if in doubt.
  - `kb/conflicts.json`: **13 conflicts**.
  - `wiki/articles.json`: **52 articles** (50 E1-reviewed, 2 R3-verified) — unchanged; the photo
    session added image galleries to 15 article *files* but did not touch `articles.json` or
    advance any status.
  - `assets/images/credits.json`: **246 entries**, 234 `acquired`.
- **Research provenance is fully preserved**: all 300 background agents have a committed report
  in `project-docs/research-provenance/reports/<id>.md` (292 completed = full final reports; 8
  spend-killed = their attempted searches + partial notes). `INDEX.md` is the lookup table. This
  was a one-time extraction from ephemeral transcripts on the old cloud sandbox — they're gone with
  that container, but the record survives in git.

## Housekeeping done 2026-06-29 (the stale-clone fix — read this, it cost a session)

- **What went wrong:** a session resumed in `C:\Users\Matt.ADESSKY\Kanawana`, a clone made
  2026-02-16 that had **never been re-fetched** and was **207 commits behind** `origin`. It showed
  KB v4.0 / 19 articles and looked like all the v4.8x work had been lost. It hadn't — the live
  GitHub remote (`github.com/mattaronson/Kanawana`) was current; the local clone was just stale.
  `git ls-remote` (queries the live remote) vs the stale local refs is what exposed it.
- **Lesson:** on resume, **always `git fetch` and compare local HEAD to `origin` before trusting
  local state.** A clone on disk is not proof of currency. If numbers look wildly wrong, suspect
  staleness before suspecting data loss.
- **What we did:** fast-forwarded the old C: clone to `origin`, then made a **fresh clone into
  `D:\Kanawana`** (the new master — C: had only ~5 GB free; D: has ~860 GB). Copied the only
  untracked local file (`.claude/settings.local.json`) across. New clone verified == `origin`,
  tree clean.

## Before searching/ingesting ANY source — avoid redundant work

- **Check the research-provenance archive FIRST.** `project-docs/research-provenance/INDEX.md`
  lists every prior research agent (topic, status, 1-line outcome); full reports are in
  `research-provenance/reports/<agent_id>.md`. Grep it before spawning an agent or running
  searches — null results are recorded there too, so you won't re-run dead-end searches. Agent IDs
  are reference labels only (NOT resumable cross-session — read the report, don't re-attach).
- **Check whether the source is already extracted.** Grep `sources/sources.json` for the source and
  look at `extracted` / `extraction_version`. Grep `kb/facts.json` for the topic. Many "blocked"
  priorities were actually already extracted (the McMorris thesis was re-queued as blocked
  multiple times despite being fully mined — the operator was rightly frustrated).
- A priority marked `blocked` is not proof of incompleteness. Re-read its `result`/`blocking_reason`
  before acting. Mark genuinely-finished items `completed` so they stop resurfacing.
- When an agent reports a finding, confirm it's in the KB **and** in the article prose. Facts often
  landed in `facts.json` but never got propagated into article text — that gap is real and worth a
  pass (see the c_009-c_013 / Otoreke-dates / Weskarini propagation fixes from an earlier session).

## Photos / images

- **The photo archive has been delivered.** Matt downloaded images via a browser session and placed
  the ZIPs at `D:\Kanawana\photodownloads\`. Integration process is in the START HERE block above;
  the rights/want-list live in `assets/images/credits.json` + `assets/images/PHOTO-ACQUISITION.md`.
- Two delivery paths exist generally: (a) operator drag-drop into chat, or (b) a Claude-for-Chrome
  session that downloads them. This batch came via a download → zip → `photodownloads/` drop.
- **Environment note:** the old cloud sandbox could not fetch images (all WebFetch → 403). This is
  now Matt's **local Windows machine** — do not assume the same limits; if you need to fetch
  something, test rather than assume it's blocked. Either way, prefer images Matt supplies.
- **Canadian copyright shortcut:** photographs made **before 1949 are public domain in Canada** —
  so the oldest archival images (1898, c.1910, 1915, 1944) are the safest to display. Flag
  1950+ items as "permission needed." **What matters is when the photograph itself was taken, not
  the date of the depicted subject.** A 2010-era photo of a 1933 plaque, or a 2026 scan of a 1920
  ribbon, is a modern photograph — copyright status follows the shoot date, not the artifact's era.
  This bug was caught mid-integration on 2026-07-02 (see research-log.md Campaign 22) after 28
  images were briefly misclassified; fixed before committing.
- **Parsing names off a plaque/board (dining-hall plaques, canoe boards, trip signs — the
  `assets/images/plaques/` album, ~140 of 151 not yet individually read):** a name paired with an
  explicit title ("Director," "Directors," "Head Counsellor," etc.) is staff; the untitled bulk of
  names is the group roster (CITs, section members, trip participants). Confirmed on the 1993 "CIT's
  of '93" board: Sophie Caisse and Simon Heller are labelled "directors" of the CIT program that
  year (distinct from Bruce Netherwood, the overall camp director 1988-1994 — see the directors
  table in `wiki/people/directors-index.md`), with 32 untitled names below them as the CIT roster
  (f_1568; Matt confirms he was one of the 32). Don't collapse a titled director's name into the
  same "staff" bucket as the roster below them — read the title text on the board, not just the
  layout. When names are hard to read (handwriting, lighting, low resolution), transcribe what's
  legible and flag the rest as illegible rather than guessing.
- Best image sources found: Concordia Records Management Flickr + the official Kanawana Flickr
  "University Concordia Archives" album; QAHN; CCA (Ross & Macdonald drawings). Concordia AtoM and
  CCA viewers sometimes block right-click download — capture the direct image URL as fallback.

## Background research agents (lessons from the old cloud sandbox)

*These are mostly sandbox-era lessons; on the local machine the working tree persists across
sessions, but background agents may still be ephemeral. Keep extracting anything important into
committed files.*

- **Agents can die mid-run on the org "monthly spend limit"** — 8 did in one prior session. Their
  final message is the error, not a report. Always read the **last real assistant text**, and treat
  a topic as covered only if a *sibling* agent or the KB confirms it.
- Prefer a **mechanical scan over re-running agents** when auditing for missed facts: a Python
  token-coverage check (distinctive entities/years/numbers vs `facts.json` + article text) is free,
  deterministic, and immune to spend limits. Pattern noted in research-log Campaign 21.
- An agent's `.output` file (sandbox) is a symlink to a JSONL transcript — parse the last assistant
  `text` block; don't read the raw JSONL as if it were the answer.
- **Agent transcripts were ephemeral** on the sandbox and NOT resumable cross-session — an agent ID
  is a reference label, not a handle you can `SendMessage` from a new session. **Extract what matters
  into the repo.** The `research-provenance/` archive is that extraction.

## The Background-tasks UI panel is misleading — do not trust it

- It shows orphaned cards from every agent ever spawned across the (repeatedly compacted) session.
  Their **timers tick up forever** (the UI computes `now − start`), so they appear to run for
  "hundreds of hours." **This is a display artifact, not real work.**
- Proof an agent is dead, not running: its **token/tool-use counts are frozen** (a live agent's
  would climb). Confirm reality with `TaskList` (→ "No tasks found"). Don't burn turns debating the
  panel; verify once and move on.

## Conflicts

- Follow the no-silent-overwrite rule: when sources disagree, add a `kb/conflicts.json` record and
  set `conflicts_with` on the facts. When resolving, prefer the **primary/official source**
  (e.g. RSVL/MELCCFP over a derived estimate) and note the reasoning in the conflict's `notes`.

## Git / environment

- This is now a **local Windows machine**, working in `D:\Kanawana`. Both **PowerShell** and a
  **bash** (Git for Windows) shell are available — each takes its own syntax.
- **`git push` works here** (credentials are cached; the fresh clone and fetches succeeded without
  prompting). This is different from the old sandbox where `gh` was absent and the GitHub MCP was
  often down. **Commit and push your work** — the stale-clone incident above is exactly why durable
  pushes matter.
- Develop on `claude/camp-kanawana-research-zusW1`; **never touch `main` without explicit go-ahead.**
  To merge with permission, fast-forward (`git push origin HEAD:main`) — the feature branch is a
  strict descendant of main.
- **On resume, `git fetch` first** and confirm local HEAD == `origin/<branch>` before trusting state.

## Session hygiene (token efficiency)

- **One session per phase** (research campaign / integration / photo pass / oral history); commit +
  push at each boundary, then start fresh. Drift is real — verify-the-UI tangents and re-derivation
  cost the most.
- Unrelated MCP tools (Canva, Shopify, QuickBooks, Uber, etc.) consume a large slice of the context
  window. Disconnecting unused MCP servers is a bigger, permanent saving than restarts.

## Highest-value remaining work (web research is near-exhausted)

1. **Photos (DO THIS FIRST)** — archive delivered to `D:\Kanawana\photodownloads\`; integrate into
   `assets/images/` + articles with credit lines per `credits.json` / `PHOTO-ACQUISITION.md`.
2. **Oral history** — the only path to the Chopsy legend, songs/cheers, Grand Portage/Longhouse.
   Instrument is drafted (`project-docs/oral-history-instrument.md`), present in one sitting —
   **but only when Matt asks** (he deferred it 2026-06-29).
3. Residual blocked items need **physical archives** (Concordia P0145), **paywalls**
   (Newspapers.com, Registre foncier), or books that are **print-disabled/borrow-only on IA**
   (Fong McConnell bio, Penton LCC history) — operator/physical access only.
