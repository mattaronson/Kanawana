# Next Session Prompt — Photo Integration

*Paste the block below into a fresh Claude Code session rooted at `D:\Kanawana`.*
*Created 2026-06-29. Task: autonomous photo integration from `D:\Kanawana\photodownloads\`.*

---

This is a continuing session for the Camp Kanawana research wiki. The master folder is **`D:\Kanawana`** (Windows). All state lives in committed files — nothing is needed from any prior chat.

**Before anything else:**
1. `git fetch origin` and confirm local HEAD == `origin/claude/camp-kanawana-research-zusW1`. If behind, fast-forward before doing any work. (A stale clone 207 commits behind cost a whole session on 2026-06-29 — don't trust local state until you've checked.)
2. Read in full: `project-docs/SESSION-HANDOFF.md` then `CLAUDE.md`. The handoff's **⚡ START HERE** block governs today.

**Today's task: photo integration, run autonomously end-to-end (oral history is deferred — do NOT run it).**

I've placed downloaded photo archives at **`D:\Kanawana\photodownloads\`** (3 ZIP files, ~100 MB, incl. `Kanawana Archives-3-001.zip`). Integrate them into the repo without checking in with me mid-task — just work the whole batch and report at the end:

1. Unzip to a scratch working area. **Do not commit the raw ZIPs or `photodownloads/`** — add them to `.gitignore` if needed.
2. Inventory every image. Cross-reference against `assets/images/credits.json` (provenance manifest) and `assets/images/PHOTO-ACQUISITION.md` (want-list). Match to existing `credits.json` entries where possible; create new entries for the rest.
3. File keepers into `assets/images/` using each entry's `target_filename`; set `status: "acquired"` and fill `filename`. Use your judgment on duplicates/low-quality/irrelevant images — skip them and note why.
4. Apply the **Canadian copyright rule**: pre-1949 photos are public domain in Canada (embed freely with a credit line). For 1950+ items, embed freely with the credit line **"Copyright All rights reserved by Kanawana"**.
5. Wire the images into the most relevant articles with proper credit lines, following the article template and encyclopedic tone in `CLAUDE.md`.
6. Update `credits.json`, log the work in `project-docs/research-log.md`, and **commit + push the feature branch in logical batches** as you go.

**Operating rules:**
- Develop on `claude/camp-kanawana-research-zusW1`; commit + push the feature branch freely, but **never push to `main` without my explicit go-ahead.**
- Keep going through the full archive without asking "what next?" Only stop for a genuine human-decision point per `CLAUDE.md` (a real rights/conflict question, or the queue being truly empty).
- When the batch is done, give me one consolidated report: images filed, articles illustrated, and anything skipped (with reasons).
