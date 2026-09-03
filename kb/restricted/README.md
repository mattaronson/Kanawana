# The restricted register

**The knowledge base holds restricted material. The published wiki must not.
This directory is the index of what is held back and why.**

## Where the line is, and why it is there

The operator's decision, 2026-09-03: the source archive is public already, and
the OCR corpus committed to this repository is fine where it is. What is
questionable is pushing named personal material into the **published wiki**.

So the boundary is the wiki, not the repository. Restricted material lives in
`kb/facts.json` like any other fact, carrying a `publication` block that marks
it restricted, names its register entry, and gives a review date. It is not
lost, which was the whole problem with the previous rule — "do not extract"
meant a later pass had no way to know something had been passed over, and would
read the same document to the same dead end.

## What this protects against, and what it does not

The realistic harm is **indexing**, not existence. A negative assessment of a
nineteen-year-old counsellor, written in 1973 by their supervisor and now
sitting in a scanned report in an archive, is public but effectively unfindable:
nobody searching that person's name will reach it. The same sentence in a wiki
article, under their name, with a heading and a citation, is the first thing a
search returns for the rest of their life.

Keeping it out of `wiki/` is therefore the whole of the protection. It does not
make the underlying document private, and nothing here pretends otherwise.

## What the register is for

The register is the human-readable index: what is held, in which document, what
kind, why, and when to look again. It points at fact ids and does not reproduce
their content — not because reproduction would be dangerous here, but because a
register that restates everything it indexes is no longer an index.

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
| `fact_ids` | the restricted facts in `kb/facts.json` this entry covers |
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

`scripts/verify/restricted_guard.py` is the publication gate. It checks that
every restricted fact is registered and carries a review date and a stated
basis, and that no personal name appearing **only** in restricted facts occurs
anywhere under `wiki/`. A name that also appears in an unrestricted fact is
ignored, because a person can be in the wiki for their job and restricted for
an assessment of it — Paul Mongraw directed Les Voyageurs in 1974, and that
belongs in the wiki.

Violations name the fact and the register entry, never the person.

**Wire this into the publication step before the wiki goes up.**
`scripts/build-content.ts` is still boilerplate; when it is pointed at `wiki/`,
this gate should run first and a non-zero exit should stop the build.

Two bugs found by its own regression test, both of which made it pass when it
should have failed, and both worth remembering: the name extractor originally
matched only title case, so names written in capitals for emphasis slid past it;
and a debugging session briefly put two of the protected surnames into the
stopword list, excusing them from every check. A guard that fails open is worse
than no guard, because it is trusted.
