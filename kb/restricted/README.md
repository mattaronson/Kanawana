# The restricted register

**This directory holds a register of information deliberately WITHHELD from the
knowledge base and the wiki. It does not hold that information.**

## Why the distinction matters here

`github.com/mattaronson/Kanawana` is a **public** repository. Every commit is
published the moment it is pushed, and git history is permanent — deleting a
file later leaves it in the log. There is therefore no such thing as a
"confidential file" in this repo. Anything written here is on the open web.

So the register records that a piece of information exists, where it is, why it
is withheld, and when it may be reconsidered. The information itself stays in
the source document and is retrieved from there when the embargo lifts.

This is ordinary archival practice, not a workaround. A finding aid says a
personnel file exists and is restricted until a given year; it does not
reproduce the file's contents in the finding aid.

## What this protects against, and what it does not

The realistic harm is **indexing**, not existence. A negative assessment of a
nineteen-year-old counsellor, written in 1973 by their supervisor and now
sitting in a scanned report in an archive, is public but effectively unfindable:
nobody searching that person's name will reach it. The same sentence in a wiki
article, under their name, with a heading and a citation, is the first thing a
search returns for the rest of their life.

Keeping it out of `kb/facts.json` and `wiki/` is therefore the whole of the
protection, and it is worth having. It does not make the underlying document
private, and this register does not pretend otherwise.

## What must never be written into this directory

- The withheld text itself, quoted or paraphrased closely enough to reconstruct.
- The names of the people it concerns.
- Anything that would let a reader assemble the two.

A register entry that fails this is worse than no entry, because it publishes
the material under a heading announcing that it is sensitive.

## The embargo rule

Personal assessments of identifiable private individuals are held until the
**later** of:

- **record date + 75 years** — the common archival term for restricted
  personnel material; and
- **estimated year of birth + 100** — where an age can be inferred from the
  record (a "counsellor", typically 18-22, in a given season).

Release may come earlier on either of two grounds: the subject's own consent, or
confirmation of death. Release should never be automatic on the date alone —
`review_on` is a date to look again, not a date to publish.

## Fields

| field | meaning |
|---|---|
| `id` | `r_NNNN` |
| `source_id` | the source record the material sits in |
| `locator` | file and line range — enough to find it, nothing more |
| `category` | what kind of information (e.g. `personnel_assessment`) |
| `subjects` | how many people, never who |
| `reason` | why it is withheld |
| `withheld_by` / `withheld_at` | who made the call and when |
| `embargo_basis` | the rule applied |
| `review_on` | earliest date to reconsider |
| `release_conditions` | what would justify earlier release |

## Checking

`scripts/verify/restricted_guard.py` enforces the boundary. It reads the span
named in each `locator`, extracts the personal names in it **at runtime**, and
fails if any of them appear in `kb/facts.json` or `wiki/`. The names are never
written down — the guard derives them from the source each time it runs, which
is why this register can itself be public.
